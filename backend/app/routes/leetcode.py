from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User, Student, LeetCodeProgress
from ..schemas import LeetCodeUpdate
from ..utils.auth import get_current_user
from datetime import datetime

router = APIRouter(prefix="/api/leetcode", tags=["LeetCode"])


def _get_student(user: User, db: Session) -> Student:
    s = db.query(Student).filter(Student.user_id == user.id).first()
    if not s:
        raise HTTPException(404, "Student profile not found")
    return s


@router.get("/progress")
def get_progress(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    student = _get_student(current_user, db)
    lc = db.query(LeetCodeProgress).filter(LeetCodeProgress.student_id == student.id).first()

    if not lc:
        return {
            "leetcode_username": None,
            "total_solved": 0,
            "easy_solved": 0,
            "medium_solved": 0,
            "hard_solved": 0,
            "acceptance_rate": 0,
            "contest_rating": 0,
            "global_ranking": None,
            "recent_activity": [],
            "is_demo_data": True,
            "last_synced_at": None,
            "note": "No LeetCode data yet. Please update your progress manually.",
        }

    return {
        "leetcode_username": lc.leetcode_username,
        "total_solved": lc.total_solved,
        "easy_solved": lc.easy_solved,
        "medium_solved": lc.medium_solved,
        "hard_solved": lc.hard_solved,
        "acceptance_rate": float(lc.acceptance_rate),
        "contest_rating": lc.contest_rating,
        "global_ranking": lc.global_ranking,
        "recent_activity": lc.recent_activity or [],
        "is_demo_data": lc.is_demo_data,
        "last_synced_at": lc.last_synced_at.isoformat() if lc.last_synced_at else None,
        "note": "Demo/manual data. Live LeetCode API integration can be added in production." if lc.is_demo_data else "Data synced from LeetCode.",
    }


@router.post("/update")
def update_progress(
    payload: LeetCodeUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    student = _get_student(current_user, db)
    lc = db.query(LeetCodeProgress).filter(LeetCodeProgress.student_id == student.id).first()

    if lc:
        lc.leetcode_username = payload.leetcode_username or lc.leetcode_username
        lc.total_solved = payload.total_solved
        lc.easy_solved = payload.easy_solved
        lc.medium_solved = payload.medium_solved
        lc.hard_solved = payload.hard_solved
        lc.acceptance_rate = payload.acceptance_rate
        lc.contest_rating = payload.contest_rating
        lc.global_ranking = payload.global_ranking
        lc.is_demo_data = True
        lc.last_synced_at = datetime.utcnow()
    else:
        lc = LeetCodeProgress(
            student_id=student.id,
            leetcode_username=payload.leetcode_username,
            total_solved=payload.total_solved,
            easy_solved=payload.easy_solved,
            medium_solved=payload.medium_solved,
            hard_solved=payload.hard_solved,
            acceptance_rate=payload.acceptance_rate,
            contest_rating=payload.contest_rating,
            global_ranking=payload.global_ranking,
            is_demo_data=True,
        )
        db.add(lc)

    db.commit()
    return {"message": "LeetCode progress updated", "total_solved": payload.total_solved}
