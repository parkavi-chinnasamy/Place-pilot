from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User, Student, Interview, InterviewFeedback, JobRole
from ..schemas import InterviewStartRequest, InterviewAnswerRequest
from ..utils.auth import get_current_user
from ..services.interview_service import get_interview_questions, evaluate_answer

router = APIRouter(prefix="/api/interview", tags=["Interview"])


def _get_student(user: User, db: Session) -> Student:
    s = db.query(Student).filter(Student.user_id == user.id).first()
    if not s:
        raise HTTPException(404, "Student profile not found")
    return s


@router.post("/start")
def start_interview(
    payload: InterviewStartRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    student = _get_student(current_user, db)
    role = db.query(JobRole).filter(JobRole.id == payload.job_role_id).first()
    if not role:
        raise HTTPException(404, "Job role not found")

    interview = Interview(
        student_id=student.id,
        job_role_id=payload.job_role_id,
        started_at=datetime.utcnow(),
    )
    db.add(interview)
    db.commit()
    db.refresh(interview)

    questions = get_interview_questions(role.name, count=5)
    return {
        "interview_id": str(interview.id),
        "job_role": role.name,
        "total_questions": len(questions),
        "questions": [
            {"number": i + 1, "text": q["q"], "topic": q["topic"]}
            for i, q in enumerate(questions)
        ],
    }


@router.post("/evaluate")
def evaluate(
    payload: InterviewAnswerRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    student = _get_student(current_user, db)
    interview = db.query(Interview).filter(
        Interview.id == payload.interview_id,
        Interview.student_id == student.id,
    ).first()
    if not interview:
        raise HTTPException(404, "Interview not found")

    role = db.query(JobRole).filter(JobRole.id == interview.job_role_id).first()
    role_name = role.name if role else "Software Developer"

    feedback = evaluate_answer(
        question=payload.question_text,
        answer=payload.student_answer,
        topic=payload.topic or "General",
        job_role_name=role_name,
    )

    fb = InterviewFeedback(
        interview_id=interview.id,
        question_number=payload.question_number,
        question_text=payload.question_text,
        student_answer=payload.student_answer,
        topic=payload.topic,
        technical_score=feedback.get("technical_score", 0),
        relevance_score=feedback.get("relevance_score", 0),
        clarity_score=feedback.get("clarity_score", 0),
        communication_score=feedback.get("communication_score", 0),
        completeness_score=feedback.get("completeness_score", 0),
        overall_score=feedback.get("overall_score", 0),
        strengths=feedback.get("strengths", []),
        weaknesses=feedback.get("weaknesses", []),
        suggested_answer=feedback.get("suggested_answer"),
        improvement_tips=feedback.get("improvement_tips"),
        detailed_feedback=feedback.get("detailed_feedback"),
    )
    db.add(fb)
    db.commit()
    db.refresh(fb)

    return {
        "question_number": fb.question_number,
        "question_text": fb.question_text,
        "student_answer": fb.student_answer,
        "topic": fb.topic,
        "scores": {
            "technical": float(fb.technical_score),
            "relevance": float(fb.relevance_score),
            "clarity": float(fb.clarity_score),
            "communication": float(fb.communication_score),
            "completeness": float(fb.completeness_score),
            "overall": float(fb.overall_score),
        },
        "strengths": fb.strengths,
        "weaknesses": fb.weaknesses,
        "suggested_answer": fb.suggested_answer,
        "improvement_tips": fb.improvement_tips,
        "detailed_feedback": fb.detailed_feedback,
    }


@router.post("/complete/{interview_id}")
def complete_interview(
    interview_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    student = _get_student(current_user, db)
    interview = db.query(Interview).filter(
        Interview.id == interview_id,
        Interview.student_id == student.id,
    ).first()
    if not interview:
        raise HTTPException(404, "Interview not found")

    feedbacks = db.query(InterviewFeedback).filter(
        InterviewFeedback.interview_id == interview.id
    ).all()

    if feedbacks:
        avg = sum(float(f.overall_score) for f in feedbacks) / len(feedbacks)
        interview.average_score = round(avg, 2)
        interview.total_questions = len(feedbacks)

    interview.completed_at = datetime.utcnow()
    db.commit()

    return {
        "interview_id": str(interview.id),
        "total_questions": interview.total_questions,
        "average_score": float(interview.average_score),
        "completed_at": interview.completed_at.isoformat(),
    }


@router.get("/history")
def get_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    student = _get_student(current_user, db)
    interviews = (
        db.query(Interview)
        .filter(Interview.student_id == student.id, Interview.completed_at.isnot(None))
        .order_by(Interview.completed_at.desc())
        .limit(10)
        .all()
    )
    result = []
    for iv in interviews:
        role = db.query(JobRole).filter(JobRole.id == iv.job_role_id).first()
        result.append({
            "id": str(iv.id),
            "job_role": role.name if role else "Unknown",
            "total_questions": iv.total_questions,
            "average_score": float(iv.average_score),
            "completed_at": iv.completed_at.isoformat(),
        })
    return result
