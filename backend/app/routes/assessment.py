from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from ..models import (
    User, Student, Assessment, AssessmentResult,
    AssessmentQuestion, AssessmentType
)
from ..schemas import AssessmentSubmit, AssessmentResultOut
from ..utils.auth import get_current_user
import random

router = APIRouter(prefix="/api/assessments", tags=["Assessments"])


def _get_student(user: User, db: Session) -> Student:
    s = db.query(Student).filter(Student.user_id == user.id).first()
    if not s:
        raise HTTPException(404, "Student profile not found")
    return s


@router.get("/questions/{assessment_type}")
def get_questions(
    assessment_type: str,
    count: int = 15,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        atype = AssessmentType(assessment_type)
    except ValueError:
        raise HTTPException(400, f"Invalid assessment type: {assessment_type}")

    questions = (
        db.query(AssessmentQuestion)
        .filter(AssessmentQuestion.assessment_type == atype, AssessmentQuestion.is_active == True)
        .all()
    )
    if not questions:
        raise HTTPException(404, "No questions available for this assessment type")

    selected = random.sample(questions, min(count, len(questions)))
    return [
        {
            "id": str(q.id),
            "assessment_type": q.assessment_type.value,
            "topic": q.topic,
            "question_text": q.question_text,
            "option_a": q.option_a,
            "option_b": q.option_b,
            "option_c": q.option_c,
            "option_d": q.option_d,
            "difficulty": q.difficulty.value,
        }
        for q in selected
    ]


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

    correct = 0
    results_data = []
    for ans in payload.answers:
        q = db.query(AssessmentQuestion).filter(
            AssessmentQuestion.id == ans.question_id
        ).first()
        if not q:
            continue
        is_correct = q.correct_option.upper() == ans.selected_option.upper()
        if is_correct:
            correct += 1
        results_data.append((q, ans.selected_option, is_correct))

    total = len(results_data)
    score = round((correct / total) * 100, 2) if total > 0 else 0

    assessment = Assessment(
        student_id=student.id,
        assessment_type=atype,
        total_questions=total,
        correct_answers=correct,
        score=score,
        time_taken_secs=payload.time_taken_secs,
        completed_at=datetime.utcnow(),
    )
    db.add(assessment)
    db.flush()

    for q, selected, is_correct in results_data:
        ar = AssessmentResult(
            assessment_id=assessment.id,
            question_id=q.id,
            selected_option=selected.upper(),
            is_correct=is_correct,
        )
        db.add(ar)

    db.commit()
    db.refresh(assessment)

    # Return results with correct answers
    detail = []
    for q, selected, is_correct in results_data:
        detail.append({
            "question_id": str(q.id),
            "question_text": q.question_text,
            "selected_option": selected.upper(),
            "correct_option": q.correct_option,
            "is_correct": is_correct,
            "explanation": q.explanation,
            "topic": q.topic,
        })

    return {
        "assessment_id": str(assessment.id),
        "assessment_type": atype.value,
        "total_questions": total,
        "correct_answers": correct,
        "score": score,
        "time_taken_secs": payload.time_taken_secs,
        "completed_at": assessment.completed_at.isoformat(),
        "results": detail,
    }


@router.get("/history")
def get_history(
    assessment_type: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    student = _get_student(current_user, db)
    q = db.query(Assessment).filter(
        Assessment.student_id == student.id,
        Assessment.completed_at.isnot(None),
    )
    if assessment_type:
        try:
            atype = AssessmentType(assessment_type)
            q = q.filter(Assessment.assessment_type == atype)
        except ValueError:
            pass

    assessments = q.order_by(Assessment.completed_at.desc()).limit(20).all()
    return [
        {
            "id": str(a.id),
            "type": a.assessment_type.value,
            "total_questions": a.total_questions,
            "correct_answers": a.correct_answers,
            "score": float(a.score),
            "time_taken_secs": a.time_taken_secs,
            "completed_at": a.completed_at.isoformat(),
        }
        for a in assessments
    ]
