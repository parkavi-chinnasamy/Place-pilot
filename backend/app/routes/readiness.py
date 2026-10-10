from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User, Student, ReadinessResult, SkillGap, PerformanceHistory, JobRole, Recommendation
from ..schemas import ReadinessRequest
from ..utils.auth import get_current_user
from ..services.readiness_service import calculate_readiness
from ..services.recommendation_service import generate_recommendations

router = APIRouter(prefix="/api/readiness", tags=["Readiness"])


def _get_student(user: User, db: Session) -> Student:
    s = db.query(Student).filter(Student.user_id == user.id).first()
    if not s:
        raise HTTPException(404, "Student profile not found")
    return s


@router.post("/calculate")
def calculate(
    payload: ReadinessRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    student = _get_student(current_user, db)
    try:
        result = calculate_readiness(db, student, payload.job_role_id)
    except ValueError as e:
        raise HTTPException(404, str(e))

    rr = result["readiness_result"]
    role = result["job_role"]
    gaps = result["skill_gaps"]
    sp = result["skill_profile"]

    # Build skill profile dict for recommendation engine
    profile_dict = {
        "dsa_score": float(sp.dsa_score or 0),
        "programming_score": float(sp.programming_score or 0),
        "dbms_score": float(sp.dbms_score or 0),
        "aptitude_score": float(sp.aptitude_score or 0),
        "coding_score": float(sp.coding_score or 0),
        "interview_score": float(sp.interview_score or 0),
        "resume_score": float(sp.resume_score or 0),
        "leetcode_score": float(sp.leetcode_score or 0),
    }

    # Generate recommendations
    rec_data = generate_recommendations(
        student_name=current_user.full_name,
        skill_profile=profile_dict,
        skill_gaps=gaps,
        readiness_category=rr.readiness_category,
        job_role_name=role.name,
        positive_factors=rr.positive_factors or [],
        negative_factors=rr.negative_factors or [],
    )

    # Store recommendation
    existing_rec = db.query(Recommendation).filter(
        Recommendation.student_id == student.id,
        Recommendation.job_role_id == payload.job_role_id,
    ).first()

    if existing_rec:
        existing_rec.summary = rec_data.get("summary")
        existing_rec.weekly_plan = rec_data.get("weekly_plan", [])
        existing_rec.skill_actions = rec_data.get("skill_actions", [])
        existing_rec.resources = rec_data.get("resources", [])
        existing_rec.next_steps = rec_data.get("next_steps", [])
        existing_rec.is_demo = rec_data.get("is_demo", True)
        existing_rec.generated_by = rec_data.get("generated_by", "demo")
    else:
        rec = Recommendation(
            student_id=student.id,
            job_role_id=payload.job_role_id,
            readiness_id=rr.id,
            summary=rec_data.get("summary"),
            weekly_plan=rec_data.get("weekly_plan", []),
            skill_actions=rec_data.get("skill_actions", []),
            resources=rec_data.get("resources", []),
            next_steps=rec_data.get("next_steps", []),
            is_demo=rec_data.get("is_demo", True),
            generated_by=rec_data.get("generated_by", "demo"),
        )
        db.add(rec)

    db.commit()

    return {
        "readiness": {
            "id": str(rr.id),
            "job_role_id": str(rr.job_role_id),
            "job_role_name": role.name,
            "readiness_category": rr.readiness_category,
            "readiness_score": float(rr.readiness_score),
            "confidence": float(rr.confidence),
            "positive_factors": rr.positive_factors,
            "negative_factors": rr.negative_factors,
            "shap_values": rr.shap_values,
            "feature_snapshot": rr.feature_snapshot,
            "model_version": rr.model_version,
            "calculated_at": rr.calculated_at.isoformat(),
            "is_demo": True,
            "disclaimer": "This readiness score is a prototype model output based on synthetic training data. It is NOT a guarantee of placement success.",
        },
        "skill_gaps": gaps,
        "recommendations": rec_data,
    }


@router.get("/current")
def get_current_readiness(
    job_role_id: str = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    student = _get_student(current_user, db)
    q = db.query(ReadinessResult).filter(
        ReadinessResult.student_id == student.id,
        ReadinessResult.is_current == True,
    )
    if job_role_id:
        q = q.filter(ReadinessResult.job_role_id == job_role_id)

    results = q.order_by(ReadinessResult.calculated_at.desc()).all()
    output = []
    for r in results:
        role = db.query(JobRole).filter(JobRole.id == r.job_role_id).first()
        output.append({
            "id": str(r.id),
            "job_role_id": str(r.job_role_id),
            "job_role_name": role.name if role else "Unknown",
            "readiness_category": r.readiness_category,
            "readiness_score": float(r.readiness_score),
            "confidence": float(r.confidence),
            "positive_factors": r.positive_factors,
            "negative_factors": r.negative_factors,
            "calculated_at": r.calculated_at.isoformat(),
            "is_demo": True,
        })
    return output


@router.get("/history")
def get_readiness_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    student = _get_student(current_user, db)
    history = (
        db.query(PerformanceHistory)
        .filter(PerformanceHistory.student_id == student.id)
        .order_by(PerformanceHistory.recorded_at.desc())
        .limit(30)
        .all()
    )
    return [
        {
            "id": str(h.id),
            "readiness_category": h.readiness_category,
            "readiness_score": float(h.readiness_score) if h.readiness_score else 0,
            "snapshot": h.snapshot,
            "recorded_at": h.recorded_at.isoformat(),
        }
        for h in history
    ]


@router.get("/skill-gaps")
def get_skill_gaps(
    job_role_id: str = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    student = _get_student(current_user, db)
    q = db.query(SkillGap).filter(SkillGap.student_id == student.id)
    if job_role_id:
        q = q.filter(SkillGap.job_role_id == job_role_id)
    gaps = q.order_by(SkillGap.priority).all()
    return [
        {
            "skill_name": g.skill_name,
            "student_score": float(g.student_score) if g.student_score else 0,
            "required_score": float(g.required_score) if g.required_score else 0,
            "gap": float(g.gap) if g.gap else 0,
            "priority": g.priority,
            "confidence": g.confidence,
            "observations": g.observations,
            "trend": g.trend,
        }
        for g in gaps
    ]
