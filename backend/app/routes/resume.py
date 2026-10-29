import os
import re
from datetime import datetime
from typing import Optional

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    UploadFile,
    File,
    Form,
)
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import User, Student, ResumeAnalysis, RoleRequirement, JobRole
from ..utils.auth import get_current_user
from ..config import get_settings
from ..services.resume_service import (
    extract_resume_text,
    parse_resume_sections,
    extract_certifications,
    extract_certifications_flat,
    extract_skills_with_evidence,
    evaluate_experience_and_profile,
    analyze_role_skills,
    calculate_ats_score,
)

router = APIRouter(prefix="/api/resume", tags=["Resume"])
settings = get_settings()


def _get_student(user: User, db: Session) -> Student:
    student = db.query(Student).filter(
        Student.user_id == user.id
    ).first()

    if not student:
        raise HTTPException(404, "Student profile not found")

    return student


@router.post("/analyze")
async def analyze_resume(
    file: UploadFile = File(...),
    job_role_id: Optional[str] = Form(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    student = _get_student(current_user, db)

    filename = file.filename or ""
    extension = os.path.splitext(filename)[1].lower()

    if extension not in (".pdf", ".docx", ".doc"):
        raise HTTPException(
            400, "Only PDF and DOCX resumes are supported."
        )

    content = await file.read()

    if not content:
        raise HTTPException(400, "The uploaded file is empty.")

    if len(content) > settings.max_upload_size_mb * 1024 * 1024:
        raise HTTPException(
            400,
            f"File too large (max {settings.max_upload_size_mb}MB)",
        )

    try:
        text, parsing_warnings, ocr_used = extract_resume_text(filename, content)
    except ValueError as err:
        err_msg = str(err)
        if "Unreadable or scanned" in err_msg:
            raise HTTPException(422, err_msg)
        raise HTTPException(400, err_msg)

    # 1. Section Boundary Parsing
    sections = parse_resume_sections(text)

    # 2. Extract certifications with evidence-based confidence scoring
    confirmed_certs, uncertain_certs, cert_warnings = extract_certifications(sections, text)
    # Flat list of confirmed certification titles (for ATS scoring and DB storage)
    certifications_flat = [c["title"] for c in confirmed_certs]

    # 3. Context-aware skill extraction with category & evidence
    skills_data = extract_skills_with_evidence(text, sections)
    extracted_skills = skills_data["skills_list"]

    # 4. Experience & Fresher Profile evaluation (fair scoring for students)
    profile_info = evaluate_experience_and_profile(text, sections)

    # 5. Role-Specific Analysis
    role_name = None
    req_list = []
    if job_role_id:
        target_role = db.query(JobRole).filter(JobRole.id == job_role_id).first()
        if target_role:
            role_name = target_role.name
        reqs = (
            db.query(RoleRequirement)
            .filter(RoleRequirement.job_role_id == job_role_id)
            .all()
        )
        req_list = [{"skill_name": req.skill_name} for req in reqs]

    role_analysis = analyze_role_skills(
        detected_skills=extracted_skills,
        role_name_or_id=role_name or job_role_id,
        db_requirements=req_list,
    )

    # 6. ATS Scoring Calculation
    ats_score_data = calculate_ats_score(
        text=text,
        sections=sections,
        detected_skills=extracted_skills,
        role_analysis=role_analysis,
        profile_info=profile_info,
        certifications=certifications_flat,
    )

    # Merge cert_warnings into parsing_warnings
    all_warnings = parsing_warnings + cert_warnings

    # 7. Persist to storage & database
    os.makedirs(settings.upload_dir, exist_ok=True)
    safe_filename = re.sub(r"[^A-Za-z0-9._-]", "_", filename)
    fname = (
        f"{student.id}_"
        f"{datetime.utcnow().strftime('%Y%m%d%H%M%S%f')}_"
        f"{safe_filename}"
    )
    fpath = os.path.join(settings.upload_dir, fname)

    with open(fpath, "wb") as output_file:
        output_file.write(content)

    try:
        ra = ResumeAnalysis(
            student_id=student.id,
            job_role_id=job_role_id if job_role_id else None,
            file_path=fpath,
            file_name=filename,
            extracted_skills=extracted_skills,
            extracted_education=[{"raw": line} for line in sections.get("education", [])],
            extracted_projects=[{"raw": line} for line in sections.get("projects", [])],
            extracted_experience=[{"raw": line} for line in sections.get("experience", []) + sections.get("internship", [])],
            certifications=certifications_flat,
            keywords_found=extracted_skills,
            overall_score=ats_score_data["overall_score"],
            skills_score=ats_score_data["skills_score"],
            education_score=ats_score_data["education_score"],
            projects_score=ats_score_data["projects_score"],
            experience_score=ats_score_data["experience_score"],
            completeness_score=ats_score_data["completeness_score"],
            missing_skills=role_analysis["missing_required"],
            missing_keywords=role_analysis["missing_preferred"],
            improvement_suggestions=ats_score_data["improvement_suggestions"],
        )

        db.add(ra)
        db.commit()
        db.refresh(ra)

    except Exception:
        db.rollback()
        if os.path.exists(fpath):
            os.remove(fpath)
        raise HTTPException(500, "Could not save the resume analysis.")

    return {
        "id": str(ra.id),
        "file_name": ra.file_name,
        "overall_score": ra.overall_score,
        "skills_score": ra.skills_score,
        "education_score": ra.education_score,
        "projects_score": ra.projects_score,
        "experience_score": ra.experience_score,
        "completeness_score": ra.completeness_score,
        "extracted_skills": ra.extracted_skills,
        "keywords_found": ra.keywords_found,
        # Backward-compatible flat list of confirmed cert titles
        "certifications": certifications_flat,
        # Structured certification data with confidence
        "certifications_confirmed": confirmed_certs,
        "certifications_uncertain": uncertain_certs,
        "cert_warnings": cert_warnings,
        "missing_skills": ra.missing_skills,
        "missing_keywords": ra.missing_keywords,
        "improvement_suggestions": ra.improvement_suggestions,
        "internship_found": profile_info["has_internship"],
        "internship_status": (
            "Internship verified"
            if profile_info["has_internship"]
            else "No internship detected"
        ),
        "analyzed_at": ra.analyzed_at.isoformat(),
        "score_note": ats_score_data["formula_explanation"],
        # Enhanced fields for rich UI & transparent inspection
        "candidate_type": profile_info["candidate_type"],
        "is_fresher": profile_info["is_fresher"],
        "ocr_used": ocr_used,
        "parsing_warnings": all_warnings,
        "skills_by_category": skills_data["skills_by_category"],
        "skills_with_evidence": skills_data["skills_details"],
        "role_analysis": {
            "role_title": role_analysis["role_title"],
            "matched_skills": role_analysis["matched_skills"],
            "missing_required": role_analysis["missing_required"],
            "missing_preferred": role_analysis["missing_preferred"],
            "uncertain_skills": role_analysis["uncertain_skills"],
            "match_ratio": role_analysis["match_ratio"],
        },
        "score_breakdown_details": ats_score_data["breakdown_details"],
    }


@router.get("/history")
def get_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    student = _get_student(current_user, db)

    analyses = (
        db.query(ResumeAnalysis)
        .filter(ResumeAnalysis.student_id == student.id)
        .order_by(ResumeAnalysis.analyzed_at.desc())
        .limit(10)
        .all()
    )

    result = []
    for item in analyses:
        role_name = None
        if item.job_role_id:
            role = db.query(JobRole).filter(JobRole.id == item.job_role_id).first()
            if role:
                role_name = role.name

        result.append({
            "id": str(item.id),
            "file_name": item.file_name,
            "overall_score": item.overall_score,
            "skills_score": item.skills_score,
            "education_score": item.education_score,
            "projects_score": item.projects_score,
            "experience_score": item.experience_score,
            "completeness_score": item.completeness_score,
            "job_role_name": role_name or "General Analysis",
            "analyzed_at": item.analyzed_at.isoformat(),
        })

    return result


@router.get("/history/{analysis_id}")
def get_history_detail(
    analysis_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    student = _get_student(current_user, db)

    item = (
        db.query(ResumeAnalysis)
        .filter(ResumeAnalysis.id == analysis_id, ResumeAnalysis.student_id == student.id)
        .first()
    )
    if not item:
        raise HTTPException(404, "Analysis record not found.")

    role_name = None
    if item.job_role_id:
        role = db.query(JobRole).filter(JobRole.id == item.job_role_id).first()
        if role:
            role_name = role.name

    return {
        "id": str(item.id),
        "file_name": item.file_name,
        "overall_score": item.overall_score,
        "skills_score": item.skills_score,
        "education_score": item.education_score,
        "projects_score": item.projects_score,
        "experience_score": item.experience_score,
        "completeness_score": item.completeness_score,
        "extracted_skills": item.extracted_skills or [],
        "keywords_found": item.keywords_found or [],
        "certifications": item.certifications or [],
        "missing_skills": item.missing_skills or [],
        "missing_keywords": item.missing_keywords or [],
        "improvement_suggestions": item.improvement_suggestions or [],
        "job_role_name": role_name or "General Analysis",
        "analyzed_at": item.analyzed_at.isoformat(),
    }
