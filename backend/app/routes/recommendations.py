from datetime import datetime
from ..models import LeetCodeProgress
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


@router.post("/dsa-plan")
def generate_dsa_plan(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    student = _get_student(current_user, db)

    progress = (
        db.query(LeetCodeProgress)
        .filter(LeetCodeProgress.student_id == student.id)
        .first()
    )

    if not progress or progress.sync_status != "SYNCED":
        raise HTTPException(
            status_code=400,
            detail="Connect and sync your LeetCode profile first."
        )

    easy = progress.easy_solved or 0
    medium = progress.medium_solved or 0
    hard = progress.hard_solved or 0

    if easy >= medium:
        focus = "Medium-level DSA practice"
    else:
        focus = "Strengthen Easy-level fundamentals"

    topics = [
        ("Arrays and Hashing", "Review arrays, hash maps, and frequency counting."),
        ("Two Pointers", "Practice pair problems and in-place array operations."),
        ("Sliding Window", "Practice fixed-size and variable-size windows."),
        ("Binary Search", "Practice sorted-array search and boundary conditions."),
        ("Linked Lists", "Review reversal, middle node, and cycle detection."),
        ("Stacks and Queues", "Practice valid parentheses and monotonic-stack basics."),
        ("Trees and Review", "Practice tree traversals and revise difficult problems."),
    ]

    weekly_plan = []
    for day, (topic, task) in enumerate(topics, start=1):
        weekly_plan.append({
            "day": day,
            "title": topic,
            "topic": topic,
            "task": task,
            "target_problems": 2 if day < 7 else 3,
            "difficulty": "Medium" if day in (2, 3, 4, 7) else "Easy",
            "focus": focus,
        })

    recommendation = Recommendation(
        student_id=student.id,
        summary=(
            f"Personalized 7-day DSA plan based on your synced profile: "
            f"{easy} Easy, {medium} Medium, and {hard} Hard problems solved. "
            f"Suggested focus: {focus}."
        ),
        weekly_plan=weekly_plan,
        skill_actions=[
            "Solve the daily problems before checking solutions.",
            "Record the approach and time complexity for each problem.",
            "Revisit problems you could not solve independently."
        ],
        resources=[
            {
                "title": "LeetCode Problem Set",
                "url": "https://leetcode.com/problemset/"
            }
        ],
        next_steps=[
            "Complete the seven-day plan.",
            "Sync your LeetCode profile again to review progress."
        ],
        is_demo=False,
        generated_by="placepilot_dsa_rules",
        generated_at=datetime.utcnow(),
    )

    db.add(recommendation)
    db.commit()
    db.refresh(recommendation)

    return {
        "message": "Personalized DSA plan generated successfully.",
        "recommendation_id": str(recommendation.id),
        "summary": recommendation.summary,
        "weekly_plan": recommendation.weekly_plan,
        "skill_actions": recommendation.skill_actions,
        "resources": recommendation.resources,
        "next_steps": recommendation.next_steps,
    }

