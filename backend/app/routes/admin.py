from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db
from ..models import (
    User, Student, SkillProfile, ReadinessResult, Assessment,
    JobRole, SkillGap, UserRole
)
from ..utils.auth import get_current_admin
from ..ml.predictor import get_evaluation

router = APIRouter(prefix="/api/admin", tags=["Admin"])


@router.get("/dashboard")
def dashboard(
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    students = db.query(Student).join(User).filter(User.is_active == True, User.role == UserRole.student).all()
    total = len(students)

    # Readiness distribution
    ready = mod_ready = needs = 0
    for s in students:
        rr = (db.query(ReadinessResult)
              .filter(ReadinessResult.student_id == s.id, ReadinessResult.is_current == True)
              .order_by(ReadinessResult.calculated_at.desc()).first())
        if rr:
            cat = rr.readiness_category
            if cat == "Ready":
                ready += 1
            elif cat == "Moderately Ready":
                mod_ready += 1
            else:
                needs += 1

    # Skill averages
    profiles = db.query(SkillProfile).all()
    skill_avgs = {}
    if profiles:
        for skill in ["dsa", "programming", "dbms", "oop", "aptitude", "coding", "interview", "resume", "leetcode"]:
            vals = [float(getattr(p, f"{skill}_score") or 0) for p in profiles]
            skill_avgs[skill] = round(sum(vals) / len(vals), 1) if vals else 0

    # Most common weak skill
    gaps = db.query(SkillGap.skill_name, func.count(SkillGap.id).label("cnt")).group_by(SkillGap.skill_name).order_by(func.count(SkillGap.id).desc()).first()
    most_weak = gaps[0] if gaps else "DSA"

    # Assessment count
    assessment_count = db.query(Assessment).filter(Assessment.completed_at.isnot(None)).count()

    # Department comparison
    dept_map = {}
    for s in students:
        dept = s.department or "Unknown"
        if dept not in dept_map:
            dept_map[dept] = []
        rr = (db.query(ReadinessResult)
              .filter(ReadinessResult.student_id == s.id, ReadinessResult.is_current == True)
              .order_by(ReadinessResult.calculated_at.desc()).first())
        if rr:
            dept_map[dept].append(float(rr.readiness_score))

    dept_comparison = [
        {"department": d, "avg_readiness": round(sum(v)/len(v), 1), "count": len(v)}
        for d, v in dept_map.items() if v
    ]

    # Average readiness
    all_scores = []
    for s in students:
        rr = (db.query(ReadinessResult)
              .filter(ReadinessResult.student_id == s.id, ReadinessResult.is_current == True)
              .order_by(ReadinessResult.calculated_at.desc()).first())
        if rr:
            all_scores.append(float(rr.readiness_score))
    avg_readiness = round(sum(all_scores) / len(all_scores), 1) if all_scores else 0

    return {
        "total_students": total,
        "average_readiness": avg_readiness,
        "students_ready": ready,
        "students_moderately_ready": mod_ready,
        "students_needs_improvement": needs,
        "most_common_weak_skill": most_weak,
        "assessment_count": assessment_count,
        "skill_averages": skill_avgs,
        "readiness_distribution": {"Ready": ready, "Moderately Ready": mod_ready, "Needs Improvement": needs},
        "department_comparison": dept_comparison,
        "is_demo": True,
    }


@router.get("/students")
def list_students(
    department: str = None,
    batch: str = None,
    readiness_level: str = None,
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    q = db.query(Student).join(User).filter(User.role == UserRole.student, User.is_active == True)
    if department:
        q = q.filter(Student.department == department)
    if batch:
        q = q.filter(Student.batch == batch)

    students = q.all()
    result = []
    for s in students:
        user = db.query(User).filter(User.id == s.user_id).first()
        rr = (db.query(ReadinessResult)
              .filter(ReadinessResult.student_id == s.id, ReadinessResult.is_current == True)
              .order_by(ReadinessResult.calculated_at.desc()).first())
        sp = db.query(SkillProfile).filter(SkillProfile.student_id == s.id).first()

        if readiness_level and rr and rr.readiness_category != readiness_level:
            continue

        role = db.query(JobRole).filter(JobRole.id == s.target_role_id).first() if s.target_role_id else None

        strongest = weakest = None
        if sp:
            scores = {
                "DSA": float(sp.dsa_score or 0), "Programming": float(sp.programming_score or 0),
                "DBMS": float(sp.dbms_score or 0), "Aptitude": float(sp.aptitude_score or 0),
                "Coding": float(sp.coding_score or 0), "Interview": float(sp.interview_score or 0),
            }
            strongest = max(scores, key=scores.get)
            weakest = min(scores, key=scores.get)

        last_assessment = (db.query(Assessment)
                          .filter(Assessment.student_id == s.id, Assessment.completed_at.isnot(None))
                          .order_by(Assessment.completed_at.desc()).first())

        result.append({
            "id": str(s.id),
            "user_id": str(s.user_id),
            "full_name": user.full_name if user else "",
            "email": user.email if user else "",
            "department": s.department,
            "batch": s.batch,
            "cgpa": float(s.cgpa) if s.cgpa else None,
            "readiness_category": rr.readiness_category if rr else None,
            "readiness_score": float(rr.readiness_score) if rr else None,
            "target_role": role.name if role else None,
            "strongest_skill": strongest,
            "weakest_skill": weakest,
            "last_assessment": last_assessment.completed_at.isoformat() if last_assessment else None,
            "profile_completeness": s.profile_completeness,
        })

    return result


@router.get("/students/{student_id}")
def get_student_detail(
    student_id: str,
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(404, "Student not found")

    user = db.query(User).filter(User.id == student.user_id).first()
    sp = db.query(SkillProfile).filter(SkillProfile.student_id == student.id).first()
    readiness_list = (db.query(ReadinessResult)
                     .filter(ReadinessResult.student_id == student.id, ReadinessResult.is_current == True)
                     .all())
    assessments = (db.query(Assessment)
                  .filter(Assessment.student_id == student.id, Assessment.completed_at.isnot(None))
                  .order_by(Assessment.completed_at.desc()).limit(10).all())

    return {
        "student": {
            "id": str(student.id),
            "full_name": user.full_name if user else "",
            "email": user.email if user else "",
            "department": student.department,
            "batch": student.batch,
            "year": student.year,
            "cgpa": float(student.cgpa) if student.cgpa else None,
            "tenth_percent": float(student.tenth_percent) if student.tenth_percent else None,
            "twelfth_percent": float(student.twelfth_percent) if student.twelfth_percent else None,
            "programming_languages": student.programming_languages,
            "profile_completeness": student.profile_completeness,
        },
        "skill_profile": {
            "dsa": float(sp.dsa_score or 0),
            "programming": float(sp.programming_score or 0),
            "dbms": float(sp.dbms_score or 0),
            "oop": float(sp.oop_score or 0),
            "aptitude": float(sp.aptitude_score or 0),
            "coding": float(sp.coding_score or 0),
            "interview": float(sp.interview_score or 0),
            "resume": float(sp.resume_score or 0),
            "leetcode": float(sp.leetcode_score or 0),
        } if sp else {},
        "readiness": [
            {
                "job_role_id": str(r.job_role_id),
                "category": r.readiness_category,
                "score": float(r.readiness_score),
                "calculated_at": r.calculated_at.isoformat(),
            }
            for r in readiness_list
        ],
        "recent_assessments": [
            {
                "type": a.assessment_type.value,
                "score": float(a.score),
                "correct": a.correct_answers,
                "total": a.total_questions,
                "date": a.completed_at.isoformat(),
            }
            for a in assessments
        ],
    }


@router.get("/skill-gaps")
def skill_gap_heatmap(
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    students = db.query(Student).join(User).filter(User.role == UserRole.student).limit(30).all()
    skills = ["dsa", "programming", "dbms", "oop", "aptitude", "coding", "interview", "resume", "leetcode"]

    heatmap = []
    for s in students:
        user = db.query(User).filter(User.id == s.user_id).first()
        sp = db.query(SkillProfile).filter(SkillProfile.student_id == s.id).first()
        row = {"student_name": user.full_name if user else str(s.id), "department": s.department}
        for skill in skills:
            row[skill] = float(getattr(sp, f"{skill}_score") or 0) if sp else 0
        heatmap.append(row)

    # Skill averages and weakness counts
    skill_stats = {}
    for skill in skills:
        vals = [row[skill] for row in heatmap]
        avg = round(sum(vals) / len(vals), 1) if vals else 0
        affected = sum(1 for v in vals if v < 60)
        skill_stats[skill] = {"average": avg, "below_60_count": affected}

    return {"heatmap": heatmap, "skill_stats": skill_stats}


@router.get("/analytics")
def analytics(
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    from ..models import PerformanceHistory
    from datetime import datetime, timedelta

    # Readiness trend over last 30 days
    cutoff = datetime.utcnow() - timedelta(days=30)
    history = (db.query(PerformanceHistory)
               .filter(PerformanceHistory.recorded_at >= cutoff)
               .order_by(PerformanceHistory.recorded_at).all())

    trend_by_date = {}
    for h in history:
        d = h.recorded_at.strftime("%Y-%m-%d")
        if d not in trend_by_date:
            trend_by_date[d] = []
        if h.readiness_score:
            trend_by_date[d].append(float(h.readiness_score))

    readiness_trend = [
        {"date": d, "avg_readiness": round(sum(v)/len(v), 1)}
        for d, v in sorted(trend_by_date.items()) if v
    ]

    return {
        "readiness_trend": readiness_trend,
        "is_demo": True,
    }


@router.get("/model-evaluation")
def model_evaluation(admin: User = Depends(get_current_admin)):
    return get_evaluation()
