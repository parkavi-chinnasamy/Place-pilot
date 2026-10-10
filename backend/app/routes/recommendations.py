from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User, Student, Recommendation, JobRole
from ..utils.auth import get_current_user

router = APIRouter(prefix="/api/recommendations", tags=["Recommendations"])


def _get_student(user: User, db: Session) -> Student:
    s = db.query(Student).filter(Student.user_id == user.id).first()
    if not s:
        raise HTTPException(404, "Student profile not found")
    return s


@router.get("")
def get_recommendations(
    job_role_id: str = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    student = _get_student(current_user, db)
    q = db.query(Recommendation).filter(Recommendation.student_id == student.id)
    if job_role_id:
        q = q.filter(Recommendation.job_role_id == job_role_id)
    recs = q.order_by(Recommendation.generated_at.desc()).limit(5).all()

    result = []
    for r in recs:
        role = db.query(JobRole).filter(JobRole.id == r.job_role_id).first() if r.job_role_id else None
        result.append({
            "id": str(r.id),
            "job_role_name": role.name if role else "General",
            "summary": r.summary,
            "weekly_plan": r.weekly_plan or [],
            "skill_actions": r.skill_actions or [],
            "resources": r.resources or [],
            "next_steps": r.next_steps or [],
            "is_demo": r.is_demo,
            "generated_by": r.generated_by,
            "generated_at": r.generated_at.isoformat(),
        })
    return result
