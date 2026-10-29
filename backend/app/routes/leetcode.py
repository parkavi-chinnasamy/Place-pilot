
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import User, Student, LeetCodeProgress, LeetCodeSnapshot
from ..schemas import LeetCodeUpdate
from ..utils.auth import get_current_user
from ..services.leetcode_service import (
    normalize_leetcode_url,
    sync_student_leetcode,
)
from ..services.readiness_service import calculate_readiness

router = APIRouter(prefix="/api/leetcode", tags=["LeetCode"])


def _get_student(user: User, db: Session) -> Student:
    student = db.query(Student).filter(Student.user_id == user.id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found")
    return student


def _get_progress(db: Session, student_id: str):
    return (
        db.query(LeetCodeProgress)
        .filter(LeetCodeProgress.student_id == student_id)
        .first()
    )


def _progress_dict(lc):
    if not lc:
        return {
            "leetcode_url": None,
            "leetcode_username": None,
            "total_solved": 0,
            "easy_solved": 0,
            "medium_solved": 0,
            "hard_solved": 0,
            "acceptance_rate": 0,
            "contest_rating": None,
            "global_ranking": None,
            "contests_attended": None,
            "top_percentage": None,
            "streak": None,
            "total_active_days": None,
            "submission_calendar": {},
            "sync_status": "NOT_CONNECTED",
            "last_sync_error": None,
            "last_synced_at": None,
            "delta_total": 0,
            "delta_easy": 0,
            "delta_medium": 0,
            "delta_hard": 0,
            "recent_activity": [],
            "is_demo_data": False,
            "note": "Connect your LeetCode profile to fetch your statistics.",
        }

    return {
        "leetcode_url": lc.leetcode_url,
        "leetcode_username": lc.leetcode_username,
        "total_solved": lc.total_solved or 0,
        "easy_solved": lc.easy_solved or 0,
        "medium_solved": lc.medium_solved or 0,
        "hard_solved": lc.hard_solved or 0,
        "acceptance_rate": float(lc.acceptance_rate or 0),
        "contest_rating": lc.contest_rating,
        "global_ranking": lc.global_ranking,
        "contests_attended": lc.contests_attended,
        "top_percentage": (
            float(lc.top_percentage)
            if lc.top_percentage is not None else None
        ),
        "streak": lc.streak,
        "total_active_days": lc.total_active_days,
        "submission_calendar": lc.submission_calendar or {},
        "sync_status": lc.sync_status or "NOT_CONNECTED",
        "last_sync_error": lc.last_sync_error,
        "last_synced_at": (
            lc.last_synced_at.isoformat() if lc.last_synced_at else None
        ),
        "delta_total": lc.delta_total or 0,
        "delta_easy": lc.delta_easy or 0,
        "delta_medium": lc.delta_medium or 0,
        "delta_hard": lc.delta_hard or 0,
        "recent_activity": lc.recent_activity or [],
        "is_demo_data": bool(lc.is_demo_data),
        "note": "Profile statistics retrieved.",
    }


@router.get("/progress")
def get_progress(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    student = _get_student(current_user, db)
    return _progress_dict(_get_progress(db, student.id))


@router.post("/connect")
def connect_leetcode(
    payload: LeetCodeUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    student = _get_student(current_user, db)

    normalized = normalize_leetcode_url(payload.leetcode_url or "")
    if not normalized:
        raise HTTPException(
            status_code=400,
            detail="Enter a valid public LeetCode profile URL.",
        )

    lc = _get_progress(db, student.id)

    if lc is None:
        lc = LeetCodeProgress(
            student_id=student.id,
            leetcode_url=normalized["canonical_url"],
            leetcode_username=normalized["username"],
            sync_status="NOT_CONNECTED",
            is_demo_data=False,
        )
        db.add(lc)
    else:
        lc.leetcode_url = normalized["canonical_url"]
        lc.leetcode_username = normalized["username"]
        lc.sync_status = "NOT_CONNECTED"
        lc.last_sync_error = None
        lc.is_demo_data = False

    db.commit()

    try:
        synced = sync_student_leetcode(db, str(student.id))
        return {
            "message": "LeetCode profile connected and synced.",
            "progress": _progress_dict(synced),
        }
    except Exception as exc:
        db.rollback()
        lc = _get_progress(db, student.id)
        detail = (
            lc.last_sync_error if lc and lc.last_sync_error
            else str(exc)
        )
        raise HTTPException(
            status_code=502,
            detail=f"Profile saved, but LeetCode sync failed: {detail}",
        )


@router.post("/sync")
def sync_leetcode(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    student = _get_student(current_user, db)

    try:
        synced = sync_student_leetcode(db, str(student.id), manual=True)
        return {
            "message": "LeetCode profile synced successfully.",
            "progress": _progress_dict(synced),
        }
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        db.rollback()
        lc = _get_progress(db, student.id)
        detail = (
            lc.last_sync_error if lc and lc.last_sync_error
            else str(exc)
        )
        raise HTTPException(
            status_code=502,
            detail=f"LeetCode sync failed: {detail}",
        )


@router.get("/snapshots")
def get_snapshots(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    student = _get_student(current_user, db)

    snapshots = (
        db.query(LeetCodeSnapshot)
        .filter(LeetCodeSnapshot.student_id == student.id)
        .order_by(LeetCodeSnapshot.captured_at.desc())
        .limit(100)
        .all()
    )

    return {
        "history": [
            {
                "username": item.leetcode_username,
                "total_solved": item.total_solved,
                "easy_solved": item.easy_solved,
                "medium_solved": item.medium_solved,
                "hard_solved": item.hard_solved,
                "contest_rating": item.contest_rating,
                "global_ranking": item.global_ranking,
                "delta_solved": item.delta_solved,
                "captured_at": (
                    item.captured_at.isoformat()
                    if item.captured_at else None
                ),
            }
            for item in snapshots
        ]
    }


# Update LeetCode stats manually or save profile details.
@router.post("/update")
def update_progress(
    payload: LeetCodeUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    student = _get_student(current_user, db)
    lc = _get_progress(db, student.id)

    if lc is None:
        lc = LeetCodeProgress(
            student_id=student.id,
            sync_status="SYNCED",
            is_demo_data=False,
        )
        db.add(lc)

    if payload.leetcode_username:
        lc.leetcode_username = payload.leetcode_username
        if not lc.leetcode_url:
            lc.leetcode_url = f"https://leetcode.com/u/{payload.leetcode_username}/"
    if payload.leetcode_url:
        lc.leetcode_url = payload.leetcode_url

    previous_total = int(lc.total_solved or 0)
    lc.total_solved = payload.total_solved
    lc.easy_solved = payload.easy_solved
    lc.medium_solved = payload.medium_solved
    lc.hard_solved = payload.hard_solved
    lc.acceptance_rate = payload.acceptance_rate
    lc.contest_rating = payload.contest_rating
    lc.global_ranking = payload.global_ranking
    lc.delta_total = int(lc.total_solved or 0) - previous_total
    lc.sync_status = "SYNCED"
    lc.last_synced_at = datetime.utcnow()
    lc.last_sync_error = None
    lc.is_demo_data = False

    snapshot = LeetCodeSnapshot(
        student_id=student.id,
        leetcode_username=lc.leetcode_username,
        total_solved=lc.total_solved,
        easy_solved=lc.easy_solved,
        medium_solved=lc.medium_solved,
        hard_solved=lc.hard_solved,
        acceptance_rate=lc.acceptance_rate or 0,
        contest_rating=lc.contest_rating,
        global_ranking=lc.global_ranking,
        delta_solved=lc.delta_total,
        captured_at=datetime.utcnow(),
    )
    db.add(snapshot)
    db.commit()
    db.refresh(lc)

    if student.target_role_id:
        try:
            calculate_readiness(db, student, str(student.target_role_id))
        except Exception:
            pass

    return {
        "message": "LeetCode progress updated successfully.",
        "progress": _progress_dict(lc),
    }
