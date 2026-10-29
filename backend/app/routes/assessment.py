from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
import random

from ..database import get_db
from ..models import (
    User, Student, Assessment, AssessmentResult,
    AssessmentQuestion, AssessmentType, DifficultyLevel
)
from ..schemas import AssessmentSubmit, AssessmentStart
from ..utils.auth import get_current_user
from ..services.readiness_service import calculate_skill_profile, calculate_readiness

router = APIRouter(prefix="/api/assessments", tags=["Assessments"])


def _get_student(user: User, db: Session) -> Student:
    s = db.query(Student).filter(Student.user_id == user.id).first()
    if not s:
        raise HTTPException(404, "Student profile not found")
    return s


@router.get("/meta/{assessment_type}")
def get_assessment_meta(
    assessment_type: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Get available topics, difficulty counts, and total questions for a given assessment type.
    """
    try:
        atype = AssessmentType(assessment_type)
    except ValueError:
        raise HTTPException(400, f"Invalid assessment type: {assessment_type}")

    questions = db.query(AssessmentQuestion).filter(
        AssessmentQuestion.assessment_type == atype,
        AssessmentQuestion.is_active == True
    ).all()

    # Normalize topics by stripping whitespace and using case‑insensitive set
    topics = sorted(list({(q.topic or "").strip() for q in questions if q.topic and q.topic.strip()}))
    diff_counts = {"easy": 0, "medium": 0, "hard": 0}
    for q in questions:
        diff_val = q.difficulty.value if hasattr(q.difficulty, "value") else str(q.difficulty)
        if diff_val in diff_counts:
            diff_counts[diff_val] += 1

    return {
        "assessment_type": atype.value,
        "total_available": len(questions),
        "topics": topics,
        "difficulty_counts": diff_counts,
    }


@router.get("/questions/{assessment_type}")
def get_questions(
    assessment_type: str,
    count: int = Query(15, ge=1, le=50),
    topic: Optional[str] = Query(None),
    difficulty: Optional[str] = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        atype = AssessmentType(assessment_type)
    except ValueError:
        raise HTTPException(400, f"Invalid assessment type: {assessment_type}")

    q = db.query(AssessmentQuestion).filter(
        AssessmentQuestion.assessment_type == atype,
        AssessmentQuestion.is_active == True
    )

    if topic and topic.strip() and topic.lower() != "all":
        # Exact case‑insensitive match for the requested topic
        q = q.filter(AssessmentQuestion.topic.ilike(topic.strip()))

    if difficulty and difficulty.strip() and difficulty.lower() != "all":
        try:
            diff_enum = DifficultyLevel(difficulty.strip().lower())
            q = q.filter(AssessmentQuestion.difficulty == diff_enum)
        except ValueError:
            pass

    questions = q.all()
    if not questions:
        # No matching questions for the selected filters.
        raise HTTPException(404, "No questions available for the selected topic and difficulty.")

    # Ensure we return the requested count, supplementing if needed
    count_requested = count
    if len(questions) < count_requested:
        additional_q = (
            db.query(AssessmentQuestion)
            .filter(
                AssessmentQuestion.assessment_type == atype,
                AssessmentQuestion.is_active == True,
                ~AssessmentQuestion.id.in_([q_item.id for q_item in questions])
            )
            .all()
        )
        questions = (questions + additional_q)[:count_requested]
    selected = random.sample(questions, min(count_requested, len(questions)))
    return [
        {
            "id": str(item.id),
            "assessment_type": item.assessment_type.value,
            "topic": item.topic,
            "question_text": item.question_text,
            "option_a": item.option_a,
            "option_b": item.option_b,
            "option_c": item.option_c,
            "option_d": item.option_d,
            "difficulty": item.difficulty.value if hasattr(item.difficulty, "value") else str(item.difficulty),
        }
        for item in selected
    ]


@router.post("/start")
def start_assessment(
    payload: AssessmentStart,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Start an assessment session, record in_progress state in persistent database,
    and return the question list and assessment_id.
    """
    student = _get_student(current_user, db)

    try:
        atype = AssessmentType(payload.assessment_type)
    except ValueError:
        raise HTTPException(400, f"Invalid assessment type: {payload.assessment_type}")

    # Build question query
    q = db.query(AssessmentQuestion).filter(
        AssessmentQuestion.assessment_type == atype,
        AssessmentQuestion.is_active == True
    )

    if payload.topic and payload.topic.strip() and payload.topic.lower() != "all":
        # Exact case‑insensitive match for the requested topic
        q = q.filter(AssessmentQuestion.topic.ilike(payload.topic.strip()))

    if payload.difficulty and payload.difficulty.strip() and payload.difficulty.lower() != "all":
        try:
            diff_enum = DifficultyLevel(payload.difficulty.strip().lower())
            q = q.filter(AssessmentQuestion.difficulty == diff_enum)
        except ValueError:
            pass

    questions = q.all()
    if not questions:
        # No matching questions for the requested filters.
        # Previously we fell back to the full pool, which caused mixing of topics.
        raise HTTPException(404, "No questions available for the selected topic and difficulty.")

    # Determine requested count and supplement if pool is smaller
    count_requested = payload.count or 15
    if len(questions) < count_requested:
        # Supplement with more questions that still match the original filters (topic/difficulty)
        supplement_query = db.query(AssessmentQuestion).filter(
            AssessmentQuestion.assessment_type == atype,
            AssessmentQuestion.is_active == True,
            ~AssessmentQuestion.id.in_([q_item.id for q_item in questions])
        )
        if payload.topic and payload.topic.strip() and payload.topic.lower() != "all":
            supplement_query = supplement_query.filter(AssessmentQuestion.topic.ilike(payload.topic.strip()))
        if payload.difficulty and payload.difficulty.strip() and payload.difficulty.lower() != "all":
            try:
                diff_enum = DifficultyLevel(payload.difficulty.strip().lower())
                supplement_query = supplement_query.filter(AssessmentQuestion.difficulty == diff_enum)
            except ValueError:
                pass
        additional_q = supplement_query.all()
        questions = (questions + additional_q)[:count_requested]
    selected = random.sample(questions, min(count_requested, len(questions)))

    # Mark older in_progress assessments older than 2 hours as abandoned
    two_hours_ago = datetime.utcnow() - timedelta(hours=2)
    db.query(Assessment).filter(
        Assessment.student_id == student.id,
        Assessment.assessment_type == atype,
        Assessment.status == "in_progress",
        Assessment.created_at < two_hours_ago
    ).update({"status": "abandoned"})

    # Create new in_progress assessment session
    assessment = Assessment(
        student_id=student.id,
        assessment_type=atype,
        total_questions=len(selected),
        correct_answers=0,
        attempted_questions=0,
        incorrect_answers=0,
        unanswered_questions=len(selected),
        score=0.0,
        status="in_progress",
        topic=payload.topic if payload.topic and payload.topic.lower() != "all" else "Mixed Topics",
        difficulty=payload.difficulty if payload.difficulty and payload.difficulty.lower() != "all" else "Mixed",
        created_at=datetime.utcnow(),
    )
    db.add(assessment)
    db.commit()
    db.refresh(assessment)

    return {
        "assessment_id": str(assessment.id),
        "assessment_type": atype.value,
        "total_questions": len(selected),
        "status": "in_progress",
        "topic": assessment.topic,
        "difficulty": assessment.difficulty,
        "questions": [
            {
                "id": str(item.id),
                "assessment_type": item.assessment_type.value,
                "topic": item.topic,
                "question_text": item.question_text,
                "option_a": item.option_a,
                "option_b": item.option_b,
                "option_c": item.option_c,
                "option_d": item.option_d,
                "difficulty": item.difficulty.value if hasattr(item.difficulty, "value") else str(item.difficulty),
            }
            for item in selected
        ]
    }


@router.post("/submit")
def submit_assessment(
    payload: AssessmentSubmit,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    student = _get_student(current_user, db)

    try:
        atype = AssessmentType(payload.assessment_type)
    except ValueError:
        raise HTTPException(400, "Invalid assessment type")

    attempted = 0
    correct = 0
    results_data = []

    for ans in payload.answers:
        q = db.query(AssessmentQuestion).filter(
            AssessmentQuestion.id == ans.question_id
        ).first()
        if not q:
            continue

        selected = (ans.selected_option or "").strip().upper() if ans.selected_option else ""
        is_attempted = selected in ["A", "B", "C", "D"]

        if is_attempted:
            attempted += 1
            is_correct = (selected == q.correct_option.strip().upper())
            final_selected = selected
        else:
            is_correct = False
            final_selected = None  # None indicates unanswered

        if is_correct:
            correct += 1

        results_data.append((q, final_selected, is_correct, is_attempted))

    total = len(results_data)
    unanswered = total - attempted
    incorrect = attempted - correct

    # CRITICAL SCORING FIX: Submitting with zero answers gives 0.0 marks!
    if total == 0 or attempted == 0 or correct == 0:
        score = 0.0
    else:
        score = round((correct / total) * 100, 2)

    # Check for existing assessment to update
    assessment = None
    if payload.assessment_id:
        assessment = db.query(Assessment).filter(
            Assessment.id == payload.assessment_id,
            Assessment.student_id == student.id
        ).first()

    now = datetime.utcnow()
    if assessment:
        assessment.total_questions = total
        assessment.correct_answers = correct
        assessment.attempted_questions = attempted
        assessment.incorrect_answers = incorrect
        assessment.unanswered_questions = unanswered
        assessment.score = score
        assessment.status = "completed"
        assessment.time_taken_secs = payload.time_taken_secs or 0
        assessment.completed_at = now
    else:
        assessment = Assessment(
            student_id=student.id,
            assessment_type=atype,
            total_questions=total,
            correct_answers=correct,
            attempted_questions=attempted,
            incorrect_answers=incorrect,
            unanswered_questions=unanswered,
            score=score,
            status="completed",
            time_taken_secs=payload.time_taken_secs or 0,
            completed_at=now,
            created_at=now,
        )
        db.add(assessment)
        db.flush()

    # Clear previous results if updating an assessment
    db.query(AssessmentResult).filter(AssessmentResult.assessment_id == assessment.id).delete()

    # Insert individual question results
    for q, selected, is_correct, is_att in results_data:
        ar = AssessmentResult(
            assessment_id=assessment.id,
            question_id=q.id,
            selected_option=selected,
            is_correct=is_correct,
            created_at=now,
        )
        db.add(ar)

    db.commit()
    db.refresh(assessment)

    # Seamlessly trigger placement readiness recalculation
    try:
        calculate_skill_profile(db, student)
        if student.target_role_id:
            calculate_readiness(db, student, str(student.target_role_id))
    except Exception as e:
        print("Notice: Auto-update readiness engine after assessment:", e)

    detail = []
    for q, selected, is_correct, is_att in results_data:
        detail.append({
            "question_id": str(q.id),
            "question_text": q.question_text,
            "selected_option": selected,
            "correct_option": q.correct_option,
            "is_correct": is_correct,
            "is_attempted": is_att,
            "explanation": q.explanation,
            "topic": q.topic,
            "difficulty": q.difficulty.value if hasattr(q.difficulty, "value") else str(q.difficulty),
        })

    return {
        "assessment_id": str(assessment.id),
        "assessment_type": atype.value,
        "total_questions": total,
        "attempted_questions": attempted,
        "correct_answers": correct,
        "incorrect_answers": incorrect,
        "unanswered_questions": unanswered,
        "score": score,
        "status": "completed",
        "time_taken_secs": payload.time_taken_secs or 0,
        "completed_at": assessment.completed_at.isoformat() if assessment.completed_at else now.isoformat(),
        "results": detail,
    }


@router.get("/status")
def get_assessment_status(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Returns consistent completion status (Not Started, In Progress, Completed)
    across all 3 assessment types for the authenticated student.
    """
    student = _get_student(current_user, db)

    statuses = {}
    for atype in [AssessmentType.aptitude, AssessmentType.coding, AssessmentType.technical]:
        # Check active in_progress (created in last 2 hours)
        two_hours_ago = datetime.utcnow() - timedelta(hours=2)
        active = (
            db.query(Assessment)
            .filter(
                Assessment.student_id == student.id,
                Assessment.assessment_type == atype,
                Assessment.status == "in_progress",
                Assessment.created_at >= two_hours_ago
            )
            .order_by(Assessment.created_at.desc())
            .first()
        )

        # Check latest completed
        latest_completed = (
            db.query(Assessment)
            .filter(
                Assessment.student_id == student.id,
                Assessment.assessment_type == atype,
                Assessment.status == "completed"
            )
            .order_by(Assessment.completed_at.desc())
            .first()
        )

        attempts_count = (
            db.query(Assessment)
            .filter(
                Assessment.student_id == student.id,
                Assessment.assessment_type == atype,
                Assessment.status == "completed"
            )
            .count()
        )

        best_score_rec = (
            db.query(func.max(Assessment.score))
            .filter(
                Assessment.student_id == student.id,
                Assessment.assessment_type == atype,
                Assessment.status == "completed"
            )
            .scalar()
        )

        if active:
            status_text = "In Progress"
        elif latest_completed:
            status_text = "Completed"
        else:
            status_text = "Not Started"

        statuses[atype.value] = {
            "type": atype.value,
            "status": status_text,
            "attempts_count": attempts_count,
            "active_assessment_id": str(active.id) if active else None,
            "last_score": float(latest_completed.score) if latest_completed and latest_completed.score is not None else None,
            "last_completed_at": latest_completed.completed_at.isoformat() if latest_completed and latest_completed.completed_at else None,
            "best_score": float(best_score_rec) if best_score_rec is not None else None,
            "total_questions": latest_completed.total_questions if latest_completed else (active.total_questions if active else None),
            "correct_answers": latest_completed.correct_answers if latest_completed else None,
        }

    return statuses


@router.get("/history")
def get_history(
    assessment_type: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    student = _get_student(current_user, db)
    q = db.query(Assessment).filter(
        Assessment.student_id == student.id,
        Assessment.status == "completed"
    )
    if assessment_type:
        try:
            atype = AssessmentType(assessment_type)
            q = q.filter(Assessment.assessment_type == atype)
        except ValueError:
            pass

    assessments = q.order_by(Assessment.completed_at.desc()).limit(50).all()
    return [
        {
            "id": str(a.id),
            "type": a.assessment_type.value,
            "status": a.status or "completed",
            "topic": a.topic or "Mixed",
            "difficulty": a.difficulty or "Mixed",
            "total_questions": a.total_questions,
            "attempted_questions": a.attempted_questions or a.total_questions,
            "correct_answers": a.correct_answers,
            "incorrect_answers": a.incorrect_answers or 0,
            "unanswered_questions": a.unanswered_questions or 0,
            "score": float(a.score),
            "time_taken_secs": a.time_taken_secs,
            "completed_at": a.completed_at.isoformat() if a.completed_at else a.created_at.isoformat(),
        }
        for a in assessments
    ]
