"""
Pydantic schemas for request/response validation
"""
from __future__ import annotations
from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, EmailStr, Field, field_validator
import uuid


# ── Auth ──────────────────────────────────────────────────────────────────────

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)
    full_name: str = Field(min_length=2)
    role: str = "student"

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str
    email: str
    full_name: str
    role: str

class UserOut(BaseModel):
    id: str
    email: str
    full_name: str
    role: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


# ── Student Profile ───────────────────────────────────────────────────────────

class StudentProfileUpdate(BaseModel):
    phone: Optional[str] = None
    college: Optional[str] = None
    department: Optional[str] = None
    batch: Optional[str] = None
    year: Optional[int] = Field(None, ge=1, le=5)
    cgpa: Optional[float] = Field(None, ge=0, le=10)
    tenth_percent: Optional[float] = Field(None, ge=0, le=100)
    twelfth_percent: Optional[float] = Field(None, ge=0, le=100)
    semester_performance: Optional[List[Dict]] = None
    skill_programming: Optional[int] = Field(None, ge=0, le=100)
    skill_dsa: Optional[int] = Field(None, ge=0, le=100)
    skill_dbms: Optional[int] = Field(None, ge=0, le=100)
    skill_oop: Optional[int] = Field(None, ge=0, le=100)
    skill_web_dev: Optional[int] = Field(None, ge=0, le=100)
    skill_aiml: Optional[int] = Field(None, ge=0, le=100)
    skill_communication: Optional[int] = Field(None, ge=0, le=100)
    programming_languages: Optional[List[str]] = None
    target_role_id: Optional[str] = None

class StudentOut(BaseModel):
    id: str
    user_id: str
    full_name: str
    email: str
    phone: Optional[str]
    college: Optional[str]
    department: Optional[str]
    batch: Optional[str]
    year: Optional[int]
    cgpa: Optional[float]
    tenth_percent: Optional[float]
    twelfth_percent: Optional[float]
    semester_performance: Optional[List[Dict]]
    skill_programming: Optional[int]
    skill_dsa: Optional[int]
    skill_dbms: Optional[int]
    skill_oop: Optional[int]
    skill_web_dev: Optional[int]
    skill_aiml: Optional[int]
    skill_communication: Optional[int]
    programming_languages: Optional[List[str]]
    target_role_id: Optional[str]
    profile_completeness: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True


# ── Job Roles ─────────────────────────────────────────────────────────────────

class JobRoleOut(BaseModel):
    id: str
    name: str
    description: Optional[str]
    is_active: bool
    requirements: Optional[List[Dict]] = []

    class Config:
        from_attributes = True

class JobRoleCreate(BaseModel):
    name: str
    description: Optional[str] = None
    requirements: List[Dict[str, Any]] = []

class JobRoleUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
    requirements: Optional[List[Dict[str, Any]]] = None


# ── Assessment ────────────────────────────────────────────────────────────────

class QuestionOut(BaseModel):
    id: str
    assessment_type: str
    topic: Optional[str]
    question_text: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    difficulty: str

    class Config:
        from_attributes = True

class AnswerSubmit(BaseModel):
    question_id: str
    selected_option: str

class AssessmentSubmit(BaseModel):
    assessment_type: str
    answers: List[AnswerSubmit]
    time_taken_secs: Optional[int] = None

class AssessmentResultOut(BaseModel):
    assessment_id: str
    assessment_type: str
    total_questions: int
    correct_answers: int
    score: float
    time_taken_secs: Optional[int]
    completed_at: Optional[datetime]
    results: Optional[List[Dict]] = []

    class Config:
        from_attributes = True


# ── Coding ────────────────────────────────────────────────────────────────────

class CodingProblemOut(BaseModel):
    id: str
    title: str
    slug: str
    difficulty: str
    topic: Optional[str]
    description: str
    constraints: Optional[str]
    sample_input: Optional[str]
    sample_output: Optional[str]
    starter_code: Optional[Dict]
    hints: Optional[List[str]]

    class Config:
        from_attributes = True

class CodeSubmitRequest(BaseModel):
    problem_id: str
    language: str = "python"
    code: str

class CodeSubmitResponse(BaseModel):
    submission_id: str
    status: str
    test_cases_passed: int
    total_test_cases: int
    score: float
    feedback: str
    runtime_ms: Optional[int]


# ── LeetCode ──────────────────────────────────────────────────────────────────

class LeetCodeUpdate(BaseModel):
    leetcode_username: Optional[str] = None
    total_solved: int = 0
    easy_solved: int = 0
    medium_solved: int = 0
    hard_solved: int = 0
    acceptance_rate: float = 0
    contest_rating: int = 0
    global_ranking: Optional[int] = None

class LeetCodeOut(BaseModel):
    leetcode_username: Optional[str]
    total_solved: int
    easy_solved: int
    medium_solved: int
    hard_solved: int
    acceptance_rate: float
    contest_rating: int
    global_ranking: Optional[int]
    recent_activity: Optional[List[Dict]]
    is_demo_data: bool
    last_synced_at: Optional[datetime]

    class Config:
        from_attributes = True


# ── Resume ────────────────────────────────────────────────────────────────────

class ResumeAnalysisOut(BaseModel):
    id: str
    overall_score: int
    skills_score: int
    education_score: int
    projects_score: int
    experience_score: int
    completeness_score: int
    extracted_skills: List[str]
    certifications: List[str]
    keywords_found: List[str]
    missing_skills: List[str]
    missing_keywords: List[str]
    improvement_suggestions: List[Dict]
    analyzed_at: datetime

    class Config:
        from_attributes = True


# ── Interview ─────────────────────────────────────────────────────────────────

class InterviewStartRequest(BaseModel):
    job_role_id: str

class InterviewAnswerRequest(BaseModel):
    interview_id: str
    question_number: int
    question_text: str
    student_answer: str
    topic: Optional[str] = None

class InterviewFeedbackOut(BaseModel):
    question_number: int
    question_text: str
    student_answer: Optional[str]
    topic: Optional[str]
    technical_score: float
    relevance_score: float
    clarity_score: float
    communication_score: float
    completeness_score: float
    overall_score: float
    strengths: List[str]
    weaknesses: List[str]
    suggested_answer: Optional[str]
    improvement_tips: Optional[str]
    detailed_feedback: Optional[str]

    class Config:
        from_attributes = True

class InterviewQuestionResponse(BaseModel):
    interview_id: str
    question_number: int
    question_text: str
    topic: str
    total_questions: int


# ── Skill Profile ─────────────────────────────────────────────────────────────

class SkillProfileOut(BaseModel):
    dsa_score: float
    programming_score: float
    dbms_score: float
    oop_score: float
    aptitude_score: float
    coding_score: float
    technical_score: float
    interview_score: float
    resume_score: float
    leetcode_score: float
    communication_score: float
    web_dev_score: float
    aiml_score: float
    dsa_observations: int
    dbms_observations: int
    aptitude_observations: int
    coding_observations: int
    interview_observations: int
    resume_observations: int
    dsa_trend: str
    aptitude_trend: str
    coding_trend: str
    calculated_at: datetime

    class Config:
        from_attributes = True


# ── Readiness ─────────────────────────────────────────────────────────────────

class ReadinessRequest(BaseModel):
    job_role_id: str

class ReadinessOut(BaseModel):
    id: str
    job_role_id: str
    job_role_name: str
    readiness_category: str
    readiness_score: float
    confidence: float
    shap_values: Dict
    positive_factors: List[Dict]
    negative_factors: List[Dict]
    feature_snapshot: Dict
    model_version: str
    calculated_at: datetime
    is_demo: bool = True

    class Config:
        from_attributes = True

class SkillGapOut(BaseModel):
    skill_name: str
    student_score: float
    required_score: float
    gap: float
    priority: int
    confidence: str
    observations: int
    trend: str

    class Config:
        from_attributes = True


# ── Recommendations ───────────────────────────────────────────────────────────

class RecommendationOut(BaseModel):
    id: str
    summary: Optional[str]
    weekly_plan: List[Dict]
    skill_actions: List[Dict]
    resources: List[Dict]
    next_steps: List[str]
    is_demo: bool
    generated_by: str
    generated_at: datetime

    class Config:
        from_attributes = True


# ── Admin ─────────────────────────────────────────────────────────────────────

class AdminDashboardOut(BaseModel):
    total_students: int
    average_readiness: float
    students_ready: int
    students_moderately_ready: int
    students_needs_improvement: int
    most_common_weak_skill: str
    assessment_count: int
    departments: List[str]
    readiness_distribution: Dict
    skill_averages: Dict
    batch_readiness: List[Dict]
    department_comparison: List[Dict]
    skill_gap_heatmap: List[Dict]
    is_demo: bool = True

class AdminStudentSummary(BaseModel):
    id: str
    full_name: str
    email: str
    department: Optional[str]
    batch: Optional[str]
    readiness_category: Optional[str]
    readiness_score: Optional[float]
    target_role: Optional[str]
    strongest_skill: Optional[str]
    weakest_skill: Optional[str]
    last_assessment: Optional[datetime]
    profile_completeness: Optional[int]

class ModelEvaluationOut(BaseModel):
    accuracy: float
    precision: float
    recall: float
    f1_score: float
    confusion_matrix: List[List[int]]
    class_labels: List[str]
    training_samples: int
    is_demo_data: bool = True
    note: str
