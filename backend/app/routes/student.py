from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User, Student, SkillProfile
from ..schemas import StudentProfileUpdate, StudentOut
from ..utils.auth import get_current_user

router = APIRouter(prefix="/api/student", tags=["Student"])


def _get_student(current_user: User, db: Session) -> Student:
    student = db.query(Student).filter(Student.user_id == current_user.id).first()
    if not student:
        raise HTTPException(404, "Student profile not found")
    return student


def _calc_completeness(student: Student) -> int:
    fields = [
        student.phone, student.college, student.department, student.batch,
        student.year, student.cgpa, student.tenth_percent, student.twelfth_percent,
        student.skill_programming, student.skill_dsa, student.skill_dbms,
        student.programming_languages,
    ]
    filled = sum(1 for f in fields if f is not None and f != 0 and f != [])
    return int((filled / len(fields)) * 100)


@router.get("/profile")
def get_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    student = _get_student(current_user, db)
    sp = db.query(SkillProfile).filter(SkillProfile.student_id == student.id).first()
    return {
        "id": str(student.id),
        "user_id": str(student.user_id),
        "full_name": current_user.full_name,
        "email": current_user.email,
        "phone": student.phone,
        "college": student.college,
        "department": student.department,
        "batch": student.batch,
        "year": student.year,
        "cgpa": float(student.cgpa) if student.cgpa else None,
        "tenth_percent": float(student.tenth_percent) if student.tenth_percent else None,
        "twelfth_percent": float(student.twelfth_percent) if student.twelfth_percent else None,
        "semester_performance": student.semester_performance or [],
        "skill_programming": student.skill_programming,
        "skill_dsa": student.skill_dsa,
        "skill_dbms": student.skill_dbms,
        "skill_oop": student.skill_oop,
        "skill_web_dev": student.skill_web_dev,
        "skill_aiml": student.skill_aiml,
        "skill_communication": student.skill_communication,
        "programming_languages": student.programming_languages or [],
        "target_role_id": str(student.target_role_id) if student.target_role_id else None,
        "profile_completeness": student.profile_completeness,
        "skill_profile": {
            "dsa_score": float(sp.dsa_score) if sp else 0,
            "programming_score": float(sp.programming_score) if sp else 0,
            "dbms_score": float(sp.dbms_score) if sp else 0,
            "oop_score": float(sp.oop_score) if sp else 0,
            "aptitude_score": float(sp.aptitude_score) if sp else 0,
            "coding_score": float(sp.coding_score) if sp else 0,
            "technical_score": float(sp.technical_score) if sp else 0,
            "interview_score": float(sp.interview_score) if sp else 0,
            "resume_score": float(sp.resume_score) if sp else 0,
            "leetcode_score": float(sp.leetcode_score) if sp else 0,
            "communication_score": float(sp.communication_score) if sp else 0,
        } if sp else None,
        "created_at": student.created_at.isoformat(),
    }


@router.put("/profile")
def update_profile(
    payload: StudentProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    student = _get_student(current_user, db)

    update_data = payload.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        if hasattr(student, key):
            setattr(student, key, value)

    student.profile_completeness = _calc_completeness(student)
    db.commit()
    db.refresh(student)
    return {"message": "Profile updated", "profile_completeness": student.profile_completeness}


@router.get("/dashboard-summary")
def dashboard_summary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    from ..models import ReadinessResult, Assessment, PerformanceHistory, JobRole
    student = _get_student(current_user, db)
    sp = db.query(SkillProfile).filter(SkillProfile.student_id == student.id).first()

    # Latest readiness
    readiness = (
        db.query(ReadinessResult)
        .filter(ReadinessResult.student_id == student.id, ReadinessResult.is_current == True)
        .order_by(ReadinessResult.calculated_at.desc())
        .first()
    )

    # Recent assessments
    recent_assessments = (
        db.query(Assessment)
        .filter(Assessment.student_id == student.id, Assessment.completed_at.isnot(None))
        .order_by(Assessment.completed_at.desc())
        .limit(5)
        .all()
    )

    # Performance history
    history = (
        db.query(PerformanceHistory)
        .filter(PerformanceHistory.student_id == student.id)
        .order_by(PerformanceHistory.recorded_at.desc())
        .limit(10)
        .all()
    )

    target_role_name = None
    if student.target_role_id:
        role = db.query(JobRole).filter(JobRole.id == student.target_role_id).first()
        target_role_name = role.name if role else None

    return {
        "student_name": current_user.full_name,
        "profile_completeness": student.profile_completeness,
        "target_role": target_role_name,
        "readiness": {
            "category": readiness.readiness_category if readiness else None,
            "score": float(readiness.readiness_score) if readiness else None,
            "job_role_id": str(readiness.job_role_id) if readiness else None,
            "calculated_at": readiness.calculated_at.isoformat() if readiness else None,
        } if readiness else None,
        "skill_profile": {
            "dsa": float(sp.dsa_score) if sp else 0,
            "programming": float(sp.programming_score) if sp else 0,
            "dbms": float(sp.dbms_score) if sp else 0,
            "oop": float(sp.oop_score) if sp else 0,
            "aptitude": float(sp.aptitude_score) if sp else 0,
            "coding": float(sp.coding_score) if sp else 0,
            "technical": float(sp.technical_score) if sp else 0,
            "interview": float(sp.interview_score) if sp else 0,
            "resume": float(sp.resume_score) if sp else 0,
            "leetcode": float(sp.leetcode_score) if sp else 0,
            "communication": float(sp.communication_score) if sp else 0,
        } if sp else {},
        "recent_assessments": [
            {
                "type": a.assessment_type.value,
                "score": float(a.score),
                "date": a.completed_at.isoformat(),
            }
            for a in recent_assessments
        ],
        "performance_history": [
            {
                "score": float(h.readiness_score) if h.readiness_score else 0,
                "category": h.readiness_category if h.readiness_category else None,
                "date": h.recorded_at.isoformat(),
            }
            for h in history
        ],
    }
