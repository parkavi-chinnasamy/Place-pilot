"""
SQLAlchemy ORM models for PlacePilot
"""
import uuid
from datetime import datetime
from sqlalchemy import (
    Column, String, Boolean, Integer, Numeric, Text, JSON,
    DateTime, ForeignKey, Enum as SAEnum, desc
)
from sqlalchemy import JSON as JSONB
from sqlalchemy.orm import relationship
from ..database import Base
import enum


# ── Enums ─────────────────────────────────────────────────────────────────────

class UserRole(str, enum.Enum):
    student = "student"
    admin = "admin"
    placement_officer = "placement_officer"


class ReadinessCategory(str, enum.Enum):
    ready = "Ready"
    moderately_ready = "Moderately Ready"
    needs_improvement = "Needs Improvement"


class AssessmentType(str, enum.Enum):
    coding = "coding"
    aptitude = "aptitude"
    technical = "technical"


class DifficultyLevel(str, enum.Enum):
    easy = "easy"
    medium = "medium"
    hard = "hard"


class SubmissionStatus(str, enum.Enum):
    pending = "pending"
    passed = "passed"
    failed = "failed"
    partial = "partial"


class EvidenceConfidence(str, enum.Enum):
    high = "High"
    medium = "Medium"
    low = "Low"


class TrendDirection(str, enum.Enum):
    improving = "improving"
    stable = "stable"
    declining = "declining"


# ── Models ────────────────────────────────────────────────────────────────────

class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    role = Column(SAEnum(UserRole), nullable=False, default=UserRole.student)
    is_active = Column(Boolean, default=True)
    is_demo = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    student = relationship("Student", back_populates="user", uselist=False)
    admin = relationship("Admin", back_populates="user", uselist=False)


class Student(Base):
    __tablename__ = "students"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    phone = Column(String(20))
    college = Column(String(255))
    department = Column(String(100))
    batch = Column(String(20))
    year = Column(Integer)
    profile_photo = Column(String(500))

    cgpa = Column(Numeric(4, 2))
    tenth_percent = Column(Numeric(5, 2))
    twelfth_percent = Column(Numeric(5, 2))
    semester_performance = Column(JSONB, default=list)

    skill_programming = Column(Integer, default=0)
    skill_dsa = Column(Integer, default=0)
    skill_dbms = Column(Integer, default=0)
    skill_oop = Column(Integer, default=0)
    skill_web_dev = Column(Integer, default=0)
    skill_aiml = Column(Integer, default=0)
    skill_communication = Column(Integer, default=0)

    programming_languages = Column(JSON, default=list)
    target_role_id = Column(String(36), ForeignKey("job_roles.id"), nullable=True)
    profile_completeness = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="student")
    target_role = relationship("JobRole")
    assessments = relationship("Assessment", back_populates="student")
    skill_profile = relationship("SkillProfile", back_populates="student", uselist=False)
    leetcode_progress = relationship("LeetCodeProgress", back_populates="student", uselist=False)
    leetcode_snapshots = relationship("LeetCodeSnapshot", back_populates="student", cascade="all, delete-orphan", order_by=lambda: desc(LeetCodeSnapshot.captured_at))
    readiness_results = relationship("ReadinessResult", back_populates="student")
    recommendations = relationship("Recommendation", back_populates="student")
    performance_history = relationship("PerformanceHistory", back_populates="student")
    resume_analyses = relationship("ResumeAnalysis", back_populates="student")
    interviews = relationship("Interview", back_populates="student")
    coding_submissions = relationship("CodingSubmission", back_populates="student")


class Admin(Base):
    __tablename__ = "admins"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    designation = Column(String(100), default="Placement Officer")
    college = Column(String(255))
    department = Column(String(100))
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    user = relationship("User", back_populates="admin")


class JobRole(Base):
    __tablename__ = "job_roles"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    requirements = relationship("RoleRequirement", back_populates="job_role", cascade="all, delete-orphan")


class RoleRequirement(Base):
    __tablename__ = "role_requirements"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    job_role_id = Column(String(36), ForeignKey("job_roles.id", ondelete="CASCADE"))
    skill_name = Column(String(100), nullable=False)
    required_score = Column(Integer, nullable=False)
    weight = Column(Numeric(4, 2), default=1.0)
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    job_role = relationship("JobRole", back_populates="requirements")


class AssessmentQuestion(Base):
    __tablename__ = "assessment_questions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    assessment_type = Column(SAEnum(AssessmentType), nullable=False)
    topic = Column(String(100))
    question_text = Column(Text, nullable=False)
    option_a = Column(Text, nullable=False)
    option_b = Column(Text, nullable=False)
    option_c = Column(Text, nullable=False)
    option_d = Column(Text, nullable=False)
    correct_option = Column(String(1), nullable=False)
    explanation = Column(Text)
    difficulty = Column(SAEnum(DifficultyLevel), default=DifficultyLevel.medium)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)


class Assessment(Base):
    __tablename__ = "assessments"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    student_id = Column(String(36), ForeignKey("students.id", ondelete="CASCADE"))
    assessment_type = Column(SAEnum(AssessmentType), nullable=False)
    total_questions = Column(Integer, nullable=False)
    correct_answers = Column(Integer, default=0)
    attempted_questions = Column(Integer, default=0)
    incorrect_answers = Column(Integer, default=0)
    unanswered_questions = Column(Integer, default=0)
    score = Column(Numeric(5, 2), default=0)
    status = Column(String(20), default="completed")  # "not_started", "in_progress", "completed"
    topic = Column(String(100), nullable=True)
    difficulty = Column(String(20), nullable=True)
    time_taken_secs = Column(Integer)
    completed_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    student = relationship("Student", back_populates="assessments")
    results = relationship("AssessmentResult", back_populates="assessment", cascade="all, delete-orphan")


class AssessmentResult(Base):
    __tablename__ = "assessment_results"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    assessment_id = Column(String(36), ForeignKey("assessments.id", ondelete="CASCADE"))
    question_id = Column(String(36), ForeignKey("assessment_questions.id"))
    selected_option = Column(String(1))
    is_correct = Column(Boolean)
    time_spent_secs = Column(Integer)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    assessment = relationship("Assessment", back_populates="results")
    question = relationship("AssessmentQuestion")


class CodingProblem(Base):
    __tablename__ = "coding_problems"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, nullable=False)
    difficulty = Column(SAEnum(DifficultyLevel), nullable=False)
    topic = Column(String(100))
    description = Column(Text, nullable=False)
    constraints = Column(Text)
    input_format = Column(Text)
    output_format = Column(Text)
    sample_input = Column(Text)
    sample_output = Column(Text)
    test_cases = Column(JSONB, default=list)
    starter_code = Column(JSONB, default=dict)
    solution = Column(Text)
    hints = Column(JSON, default=list)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    submissions = relationship("CodingSubmission", back_populates="problem")


class CodingSubmission(Base):
    __tablename__ = "coding_submissions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    student_id = Column(String(36), ForeignKey("students.id", ondelete="CASCADE"))
    problem_id = Column(String(36), ForeignKey("coding_problems.id"))
    language = Column(String(50), default="python")
    code = Column(Text, nullable=False)
    status = Column(SAEnum(SubmissionStatus), default=SubmissionStatus.pending)
    test_cases_passed = Column(Integer, default=0)
    total_test_cases = Column(Integer, default=0)
    runtime_ms = Column(Integer)
    memory_kb = Column(Integer)
    score = Column(Numeric(5, 2), default=0)
    feedback = Column(Text)
    submitted_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    student = relationship("Student", back_populates="coding_submissions")
    problem = relationship("CodingProblem", back_populates="submissions")


class LeetCodeProgress(Base):
    __tablename__ = "leetcode_progress"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    student_id = Column(String(36), ForeignKey("students.id", ondelete="CASCADE"), unique=True)
    leetcode_url = Column(String(255), nullable=True)
    leetcode_username = Column(String(100), nullable=True)
    total_solved = Column(Integer, default=0)
    easy_solved = Column(Integer, default=0)
    medium_solved = Column(Integer, default=0)
    hard_solved = Column(Integer, default=0)
    acceptance_rate = Column(Numeric(5, 2), default=0)
    contest_rating = Column(Integer, nullable=True)
    global_ranking = Column(Integer, nullable=True)
    contests_attended = Column(Integer, default=0)
    top_percentage = Column(Numeric(5, 2), nullable=True)
    streak = Column(Integer, default=0)
    total_active_days = Column(Integer, default=0)
    recent_activity = Column(JSONB, default=list)
    submission_calendar = Column(JSONB, default=dict)
    is_demo_data = Column(Boolean, default=False)
    sync_status = Column(String(50), default="NOT_CONNECTED")  # NOT_CONNECTED, SYNCED, SYNCING, FAILED
    last_sync_error = Column(Text, nullable=True)
    last_synced_at = Column(DateTime(timezone=True), nullable=True)
    delta_total = Column(Integer, default=0)
    delta_easy = Column(Integer, default=0)
    delta_medium = Column(Integer, default=0)
    delta_hard = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    student = relationship("Student", back_populates="leetcode_progress")


class LeetCodeSnapshot(Base):
    __tablename__ = "leetcode_snapshots"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    student_id = Column(String(36), ForeignKey("students.id", ondelete="CASCADE"), index=True)
    leetcode_username = Column(String(100))
    total_solved = Column(Integer, default=0)
    easy_solved = Column(Integer, default=0)
    medium_solved = Column(Integer, default=0)
    hard_solved = Column(Integer, default=0)
    acceptance_rate = Column(Numeric(5, 2), default=0)
    contest_rating = Column(Integer, nullable=True)
    global_ranking = Column(Integer, nullable=True)
    delta_solved = Column(Integer, default=0)
    captured_at = Column(DateTime(timezone=True), default=datetime.utcnow, index=True)

    student = relationship("Student", back_populates="leetcode_snapshots")


class ResumeAnalysis(Base):
    __tablename__ = "resume_analyses"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    student_id = Column(String(36), ForeignKey("students.id", ondelete="CASCADE"))
    job_role_id = Column(String(36), ForeignKey("job_roles.id"), nullable=True)
    file_path = Column(String(500))
    file_name = Column(String(255))
    extracted_skills = Column(JSON, default=list)
    extracted_education = Column(JSONB, default=list)
    extracted_projects = Column(JSONB, default=list)
    extracted_experience = Column(JSONB, default=list)
    certifications = Column(JSON, default=list)
    keywords_found = Column(JSON, default=list)
    overall_score = Column(Integer, default=0)
    skills_score = Column(Integer, default=0)
    education_score = Column(Integer, default=0)
    projects_score = Column(Integer, default=0)
    experience_score = Column(Integer, default=0)
    completeness_score = Column(Integer, default=0)
    missing_skills = Column(JSON, default=list)
    missing_keywords = Column(JSON, default=list)
    improvement_suggestions = Column(JSONB, default=list)
    analyzed_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    student = relationship("Student", back_populates="resume_analyses")
    job_role = relationship("JobRole")


class Interview(Base):
    __tablename__ = "interviews"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    student_id = Column(String(36), ForeignKey("students.id", ondelete="CASCADE"))
    job_role_id = Column(String(36), ForeignKey("job_roles.id"), nullable=True)
    total_questions = Column(Integer, default=0)
    average_score = Column(Numeric(5, 2), default=0)
    started_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    completed_at = Column(DateTime(timezone=True))

    student = relationship("Student", back_populates="interviews")
    job_role = relationship("JobRole")
    feedback = relationship("InterviewFeedback", back_populates="interview", cascade="all, delete-orphan")


class InterviewFeedback(Base):
    __tablename__ = "interview_feedback"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    interview_id = Column(String(36), ForeignKey("interviews.id", ondelete="CASCADE"))
    question_number = Column(Integer, nullable=False)
    question_text = Column(Text, nullable=False)
    student_answer = Column(Text)
    topic = Column(String(100))
    technical_score = Column(Numeric(4, 1), default=0)
    relevance_score = Column(Numeric(4, 1), default=0)
    clarity_score = Column(Numeric(4, 1), default=0)
    communication_score = Column(Numeric(4, 1), default=0)
    completeness_score = Column(Numeric(4, 1), default=0)
    overall_score = Column(Numeric(4, 1), default=0)
    strengths = Column(JSON, default=list)
    weaknesses = Column(JSON, default=list)
    suggested_answer = Column(Text)
    improvement_tips = Column(Text)
    detailed_feedback = Column(Text)
    answered_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    interview = relationship("Interview", back_populates="feedback")


class SkillProfile(Base):
    __tablename__ = "skill_profiles"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    student_id = Column(String(36), ForeignKey("students.id", ondelete="CASCADE"), unique=True)
    dsa_score = Column(Numeric(5, 2), default=0)
    programming_score = Column(Numeric(5, 2), default=0)
    dbms_score = Column(Numeric(5, 2), default=0)
    oop_score = Column(Numeric(5, 2), default=0)
    aptitude_score = Column(Numeric(5, 2), default=0)
    coding_score = Column(Numeric(5, 2), default=0)
    technical_score = Column(Numeric(5, 2), default=0)
    interview_score = Column(Numeric(5, 2), default=0)
    resume_score = Column(Numeric(5, 2), default=0)
    leetcode_score = Column(Numeric(5, 2), default=0)
    communication_score = Column(Numeric(5, 2), default=0)
    web_dev_score = Column(Numeric(5, 2), default=0)
    aiml_score = Column(Numeric(5, 2), default=0)
    dsa_observations = Column(Integer, default=0)
    dbms_observations = Column(Integer, default=0)
    aptitude_observations = Column(Integer, default=0)
    coding_observations = Column(Integer, default=0)
    interview_observations = Column(Integer, default=0)
    resume_observations = Column(Integer, default=0)
    dsa_trend = Column(SAEnum(TrendDirection), default=TrendDirection.stable)
    aptitude_trend = Column(SAEnum(TrendDirection), default=TrendDirection.stable)
    coding_trend = Column(SAEnum(TrendDirection), default=TrendDirection.stable)
    calculated_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    student = relationship("Student", back_populates="skill_profile")


class ReadinessResult(Base):
    __tablename__ = "readiness_results"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    student_id = Column(String(36), ForeignKey("students.id", ondelete="CASCADE"))
    job_role_id = Column(String(36), ForeignKey("job_roles.id"))
    readiness_category = Column(SAEnum(ReadinessCategory), default=ReadinessCategory.needs_improvement)
    readiness_score = Column(Numeric(5, 2), default=0)
    confidence = Column(Numeric(4, 2), default=0)
    shap_values = Column(JSONB, default=dict)
    positive_factors = Column(JSONB, default=list)
    negative_factors = Column(JSONB, default=list)
    feature_snapshot = Column(JSONB, default=dict)
    is_current = Column(Boolean, default=True)
    model_version = Column(String(50), default="v1.0-demo")
    calculated_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    student = relationship("Student", back_populates="readiness_results")
    job_role = relationship("JobRole")


class SkillGap(Base):
    __tablename__ = "skill_gaps"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    student_id = Column(String(36), ForeignKey("students.id", ondelete="CASCADE"))
    job_role_id = Column(String(36), ForeignKey("job_roles.id"))
    skill_name = Column(String(100), nullable=False)
    student_score = Column(Numeric(5, 2))
    required_score = Column(Numeric(5, 2))
    gap = Column(Numeric(5, 2))
    priority = Column(Integer)
    confidence = Column(SAEnum(EvidenceConfidence), default=EvidenceConfidence.medium)
    observations = Column(Integer, default=0)
    trend = Column(SAEnum(TrendDirection), default=TrendDirection.stable)
    calculated_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    student = relationship("Student")
    job_role = relationship("JobRole")


class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    student_id = Column(String(36), ForeignKey("students.id", ondelete="CASCADE"))
    job_role_id = Column(String(36), ForeignKey("job_roles.id"), nullable=True)
    readiness_id = Column(String(36), ForeignKey("readiness_results.id"), nullable=True)
    summary = Column(Text)
    weekly_plan = Column(JSONB, default=list)
    skill_actions = Column(JSONB, default=list)
    resources = Column(JSONB, default=list)
    next_steps = Column(JSON, default=list)
    is_demo = Column(Boolean, default=False)
    generated_by = Column(String(50), default="gemini")
    generated_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    student = relationship("Student", back_populates="recommendations")
    job_role = relationship("JobRole")


class PerformanceHistory(Base):
    __tablename__ = "performance_history"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    student_id = Column(String(36), ForeignKey("students.id", ondelete="CASCADE"))
    job_role_id = Column(String(36), ForeignKey("job_roles.id"), nullable=True)
    snapshot = Column(JSONB, nullable=False)
    readiness_category = Column(SAEnum(ReadinessCategory))
    readiness_score = Column(Numeric(5, 2))
    recorded_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    student = relationship("Student", back_populates="performance_history")
    job_role = relationship("JobRole")

