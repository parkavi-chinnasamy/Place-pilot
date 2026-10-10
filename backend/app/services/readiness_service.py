"""
Adaptive Explainable Placement Readiness Engine
Core service that orchestrates:
  1. Skill profile calculation
  2. Role-requirement comparison
  3. Random Forest prediction
  4. SHAP explanation
  5. Skill gap prioritization
"""
from datetime import datetime
from typing import Dict, List, Optional
from sqlalchemy.orm import Session
from ..models import (
    Student, SkillProfile, ReadinessResult, SkillGap,
    JobRole, RoleRequirement, PerformanceHistory,
    Assessment, AssessmentType, LeetCodeProgress, ResumeAnalysis,
    Interview, TrendDirection, EvidenceConfidence
)
from ..ml.predictor import predict_readiness
import uuid


SKILL_TO_FEATURE = {
    "dsa":           "dsa_score",
    "programming":   "programming_score",
    "dbms":          "dbms_score",
    "oop":           "oop_score",
    "aptitude":      "aptitude_score",
    "coding":        "coding_score",
    "technical":     "technical_score",
    "interview":     "interview_score",
    "resume":        "resume_score",
    "leetcode":      "leetcode_score",
    "communication": "communication_score",
    "web_dev":       "web_dev_score",
    "aiml":          "aiml_score",
}


def calculate_skill_profile(db: Session, student: Student) -> SkillProfile:
    """
    Build a unified skill profile from all data sources:
    - Academic performance (CGPA, subject skills)
    - Assessment scores (aptitude, coding, technical)
    - LeetCode progress
    - Resume analysis
    - Interview performance
    """
    # Gather assessment scores
    assessments = db.query(Assessment).filter(
        Assessment.student_id == student.id,
        Assessment.completed_at.isnot(None)
    ).all()

    coding_scores = [a.score for a in assessments if a.assessment_type == AssessmentType.coding]
    aptitude_scores = [a.score for a in assessments if a.assessment_type == AssessmentType.aptitude]
    technical_scores = [a.score for a in assessments if a.assessment_type == AssessmentType.technical]

    # LeetCode
    lc = db.query(LeetCodeProgress).filter(LeetCodeProgress.student_id == student.id).first()
    leetcode_score = 0.0
    if lc and lc.total_solved > 0:
        # Score based on solved count and difficulty mix
        raw = (lc.easy_solved * 1 + lc.medium_solved * 2 + lc.hard_solved * 3)
        leetcode_score = min(100.0, raw * 0.15 + lc.acceptance_rate * 0.3)

    # Resume
    resumes = db.query(ResumeAnalysis).filter(
        ResumeAnalysis.student_id == student.id
    ).order_by(ResumeAnalysis.analyzed_at.desc()).all()
    resume_score = float(resumes[0].overall_score) if resumes else 0.0

    # Interviews
    interviews = db.query(Interview).filter(
        Interview.student_id == student.id,
        Interview.completed_at.isnot(None)
    ).all()
    interview_scores = [float(i.average_score) for i in interviews if i.average_score]

    # Academic → 0-100 score
    cgpa_score = float(student.cgpa) * 10 if student.cgpa else 60.0

    # Blend self-assessed skills with assessment data
    def blend(self_assessed: int, measured_scores: list) -> float:
        if not measured_scores:
            return float(self_assessed) * 0.6 + 40.0 * 0.4  # weight self-assessment lower
        measured_avg = sum(measured_scores) / len(measured_scores)
        return self_assessed * 0.3 + measured_avg * 0.7

    sp = db.query(SkillProfile).filter(SkillProfile.student_id == student.id).first()
    if not sp:
        sp = SkillProfile(student_id=student.id)
        db.add(sp)

    sp.dsa_score         = round(blend(student.skill_dsa or 0, coding_scores), 2)
    sp.programming_score = round(blend(student.skill_programming or 0, coding_scores), 2)
    sp.dbms_score        = round(blend(student.skill_dbms or 0, technical_scores), 2)
    sp.oop_score         = round(blend(student.skill_oop or 0, technical_scores), 2)
    sp.aptitude_score    = round(float(sum(aptitude_scores) / len(aptitude_scores)) if aptitude_scores else blend(70, []), 2)
    sp.coding_score      = round(float(sum(coding_scores) / len(coding_scores)) if coding_scores else blend(student.skill_programming or 0, []), 2)
    sp.technical_score   = round(float(sum(technical_scores) / len(technical_scores)) if technical_scores else blend(student.skill_dbms or 0, []), 2)
    sp.interview_score   = round(float(sum(interview_scores) / len(interview_scores)) if interview_scores else float(student.skill_communication or 0) * 0.7, 2)
    sp.resume_score      = round(resume_score if resume_score > 0 else float(student.skill_communication or 0) * 0.8, 2)
    sp.leetcode_score    = round(leetcode_score if leetcode_score > 0 else float(student.skill_dsa or 0) * 0.6, 2)
    sp.communication_score = round(float(student.skill_communication or 0), 2)
    sp.web_dev_score     = round(float(student.skill_web_dev or 0), 2)
    sp.aiml_score        = round(float(student.skill_aiml or 0), 2)

    # Evidence tracking
    sp.dsa_observations      = len(coding_scores)
    sp.dbms_observations     = len(technical_scores)
    sp.aptitude_observations = len(aptitude_scores)
    sp.coding_observations   = len(coding_scores)
    sp.interview_observations = len(interview_scores)
    sp.resume_observations   = len(resumes)
    sp.calculated_at = datetime.utcnow()

    db.commit()
    db.refresh(sp)
    return sp


def calculate_readiness(
    db: Session,
    student: Student,
    job_role_id: str
) -> Dict:
    """
    Full readiness calculation pipeline:
    1. Update skill profile
    2. Get role requirements
    3. Predict with Random Forest
    4. Explain with SHAP
    5. Identify & prioritize skill gaps
    6. Store results
    """
    # Step 1: Update skill profile
    sp = calculate_skill_profile(db, student)

    # Step 2: Get role
    role = db.query(JobRole).filter(JobRole.id == job_role_id).first()
    if not role:
        raise ValueError(f"Job role {job_role_id} not found")

    requirements = db.query(RoleRequirement).filter(
        RoleRequirement.job_role_id == job_role_id
    ).all()

    # Step 3: Build feature dict for ML model
    # Use float() everywhere to avoid Decimal type issues with SQLite/numpy
    def f(val): return float(val) if val is not None else 0.0

    cgpa_score = f(student.cgpa) * 10 if student.cgpa else 60.0
    features = {
        "academic_score":    round(cgpa_score, 2),
        "dsa_score":         round(f(sp.dsa_score), 2),
        "programming_score": round(f(sp.programming_score), 2),
        "dbms_score":        round(f(sp.dbms_score), 2),
        "oop_score":         round(f(sp.oop_score), 2),
        "aptitude_score":    round(f(sp.aptitude_score), 2),
        "coding_score":      round(f(sp.coding_score), 2),
        "technical_score":   round(f(sp.technical_score), 2),
        "interview_score":   round(f(sp.interview_score), 2),
        "resume_score":      round(f(sp.resume_score), 2),
        "leetcode_score":    round(f(sp.leetcode_score), 2),
        "communication_score": round(f(sp.communication_score), 2),
    }

    # Step 4: Random Forest prediction + SHAP
    prediction = predict_readiness(features)

    # Step 5: Calculate skill gaps
    skill_gaps = []
    for req in requirements:
        student_score = getattr(sp, f"{req.skill_name}_score", None)
        if student_score is None:
            student_score = features.get(f"{req.skill_name}_score", 50.0)

        student_score = float(student_score)
        required = float(req.required_score)
        gap = max(0.0, required - student_score)

        obs = getattr(sp, f"{req.skill_name}_observations", 0) or 0
        confidence = (
            EvidenceConfidence.high if obs >= 3
            else EvidenceConfidence.medium if obs >= 1
            else EvidenceConfidence.low
        )

        skill_gaps.append({
            "skill_name": req.skill_name,
            "student_score": round(student_score, 1),
            "required_score": required,
            "gap": round(gap, 1),
            "weight": float(req.weight),
            "confidence": confidence.value,
            "observations": obs,
        })

    # Sort by gap × weight (priority)
    skill_gaps.sort(key=lambda x: float(x["gap"]) * float(x["weight"]), reverse=True)
    for i, g in enumerate(skill_gaps):
        g["priority"] = i + 1

    # Step 6: Mark old results as not current
    db.query(ReadinessResult).filter(
        ReadinessResult.student_id == student.id,
        ReadinessResult.job_role_id == job_role_id,
        ReadinessResult.is_current == True,
    ).update({"is_current": False})

    # Step 7: Store new readiness result
    result = ReadinessResult(
        student_id=student.id,
        job_role_id=job_role_id,
        readiness_category=prediction["readiness_category"],
        readiness_score=prediction["readiness_score"],
        confidence=prediction["confidence"],
        shap_values=prediction["shap_values"],
        positive_factors=prediction["positive_factors"],
        negative_factors=prediction["negative_factors"],
        feature_snapshot=features,
        is_current=True,
        model_version="v1.0-demo",
    )
    db.add(result)

    # Step 8: Update skill gaps table
    db.query(SkillGap).filter(
        SkillGap.student_id == student.id,
        SkillGap.job_role_id == job_role_id
    ).delete()

    for g in skill_gaps:
        sg = SkillGap(
            student_id=student.id,
            job_role_id=job_role_id,
            skill_name=g["skill_name"],
            student_score=g["student_score"],
            required_score=g["required_score"],
            gap=g["gap"],
            priority=g["priority"],
            confidence=g["confidence"],
            observations=g["observations"],
        )
        db.add(sg)

    # Step 9: Store performance history
    history = PerformanceHistory(
        student_id=student.id,
        job_role_id=job_role_id,
        snapshot=features,
        readiness_category=prediction["readiness_category"],
        readiness_score=prediction["readiness_score"],
    )
    db.add(history)

    db.commit()
    db.refresh(result)

    return {
        "readiness_result": result,
        "skill_gaps": skill_gaps,
        "skill_profile": sp,
        "job_role": role,
        "features": features,
    }
