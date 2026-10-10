-- ============================================================
-- PlacePilot Database Schema
-- PostgreSQL 15+
-- ============================================================

-- Extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- ============================================================
-- ENUM TYPES
-- ============================================================

CREATE TYPE user_role AS ENUM ('student', 'admin', 'placement_officer');
CREATE TYPE readiness_category AS ENUM ('Ready', 'Moderately Ready', 'Needs Improvement');
CREATE TYPE assessment_type AS ENUM ('coding', 'aptitude', 'technical');
CREATE TYPE difficulty_level AS ENUM ('easy', 'medium', 'hard');
CREATE TYPE submission_status AS ENUM ('pending', 'passed', 'failed', 'partial');
CREATE TYPE evidence_confidence AS ENUM ('High', 'Medium', 'Low');
CREATE TYPE trend_direction AS ENUM ('improving', 'stable', 'declining');

-- ============================================================
-- USERS
-- ============================================================

CREATE TABLE users (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email           VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name       VARCHAR(255) NOT NULL,
    role            user_role NOT NULL DEFAULT 'student',
    is_active       BOOLEAN NOT NULL DEFAULT TRUE,
    is_demo         BOOLEAN NOT NULL DEFAULT FALSE,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role  ON users(role);

-- ============================================================
-- STUDENTS
-- ============================================================

CREATE TABLE students (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id         UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,

    -- Personal
    phone           VARCHAR(20),
    college         VARCHAR(255),
    department      VARCHAR(100),
    batch           VARCHAR(20),
    year            INTEGER CHECK (year BETWEEN 1 AND 5),
    profile_photo   VARCHAR(500),

    -- Academic
    cgpa            NUMERIC(4,2) CHECK (cgpa BETWEEN 0 AND 10),
    tenth_percent   NUMERIC(5,2) CHECK (tenth_percent BETWEEN 0 AND 100),
    twelfth_percent NUMERIC(5,2) CHECK (twelfth_percent BETWEEN 0 AND 100),

    -- Semester performance (JSON array of {sem, gpa})
    semester_performance JSONB DEFAULT '[]'::JSONB,

    -- Skills (self-assessed, 0-100)
    skill_programming   INTEGER DEFAULT 0 CHECK (skill_programming BETWEEN 0 AND 100),
    skill_dsa           INTEGER DEFAULT 0 CHECK (skill_dsa BETWEEN 0 AND 100),
    skill_dbms          INTEGER DEFAULT 0 CHECK (skill_dbms BETWEEN 0 AND 100),
    skill_oop           INTEGER DEFAULT 0 CHECK (skill_oop BETWEEN 0 AND 100),
    skill_web_dev       INTEGER DEFAULT 0 CHECK (skill_web_dev BETWEEN 0 AND 100),
    skill_aiml          INTEGER DEFAULT 0 CHECK (skill_aiml BETWEEN 0 AND 100),
    skill_communication INTEGER DEFAULT 0 CHECK (skill_communication BETWEEN 0 AND 100),

    -- Languages known
    programming_languages TEXT[] DEFAULT '{}',

    -- Target role
    target_role_id  UUID,

    -- Profile completeness (0-100, calculated)
    profile_completeness INTEGER DEFAULT 0,

    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT uq_students_user UNIQUE (user_id)
);

CREATE INDEX idx_students_user_id    ON students(user_id);
CREATE INDEX idx_students_department ON students(department);
CREATE INDEX idx_students_batch      ON students(batch);

-- ============================================================
-- ADMINS / PLACEMENT OFFICERS
-- ============================================================

CREATE TABLE admins (
    id          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id     UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    designation VARCHAR(100) DEFAULT 'Placement Officer',
    college     VARCHAR(255),
    department  VARCHAR(100),
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_admins_user UNIQUE (user_id)
);

-- ============================================================
-- JOB ROLES
-- ============================================================

CREATE TABLE job_roles (
    id          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name        VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    is_active   BOOLEAN DEFAULT TRUE,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ============================================================
-- ROLE REQUIREMENTS (skill targets per role)
-- ============================================================

CREATE TABLE role_requirements (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    job_role_id     UUID NOT NULL REFERENCES job_roles(id) ON DELETE CASCADE,
    skill_name      VARCHAR(100) NOT NULL,
    required_score  INTEGER NOT NULL CHECK (required_score BETWEEN 0 AND 100),
    weight          NUMERIC(4,2) DEFAULT 1.0,
    description     TEXT,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_role_skill UNIQUE (job_role_id, skill_name)
);

CREATE INDEX idx_role_req_role ON role_requirements(job_role_id);

-- ============================================================
-- ASSESSMENT QUESTIONS
-- ============================================================

CREATE TABLE assessment_questions (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    assessment_type assessment_type NOT NULL,
    topic           VARCHAR(100),
    question_text   TEXT NOT NULL,
    option_a        TEXT NOT NULL,
    option_b        TEXT NOT NULL,
    option_c        TEXT NOT NULL,
    option_d        TEXT NOT NULL,
    correct_option  CHAR(1) NOT NULL CHECK (correct_option IN ('A','B','C','D')),
    explanation     TEXT,
    difficulty      difficulty_level DEFAULT 'medium',
    is_active       BOOLEAN DEFAULT TRUE,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_aq_type ON assessment_questions(assessment_type);
CREATE INDEX idx_aq_topic ON assessment_questions(topic);

-- ============================================================
-- ASSESSMENTS (test sessions)
-- ============================================================

CREATE TABLE assessments (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_id      UUID NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    assessment_type assessment_type NOT NULL,
    total_questions INTEGER NOT NULL,
    correct_answers INTEGER DEFAULT 0,
    score           NUMERIC(5,2) DEFAULT 0,
    time_taken_secs INTEGER,
    completed_at    TIMESTAMPTZ,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_assessments_student ON assessments(student_id);
CREATE INDEX idx_assessments_type    ON assessments(assessment_type);

-- ============================================================
-- ASSESSMENT RESULTS (per-question answers)
-- ============================================================

CREATE TABLE assessment_results (
    id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    assessment_id       UUID NOT NULL REFERENCES assessments(id) ON DELETE CASCADE,
    question_id         UUID NOT NULL REFERENCES assessment_questions(id),
    selected_option     CHAR(1) CHECK (selected_option IN ('A','B','C','D')),
    is_correct          BOOLEAN,
    time_spent_secs     INTEGER,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_ar_assessment ON assessment_results(assessment_id);

-- ============================================================
-- CODING PROBLEMS
-- ============================================================

CREATE TABLE coding_problems (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title           VARCHAR(255) NOT NULL,
    slug            VARCHAR(255) UNIQUE NOT NULL,
    difficulty      difficulty_level NOT NULL,
    topic           VARCHAR(100),
    description     TEXT NOT NULL,
    constraints     TEXT,
    input_format    TEXT,
    output_format   TEXT,
    sample_input    TEXT,
    sample_output   TEXT,
    test_cases      JSONB DEFAULT '[]'::JSONB,
    starter_code    JSONB DEFAULT '{}'::JSONB,
    solution        TEXT,
    hints           TEXT[],
    is_active       BOOLEAN DEFAULT TRUE,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_cp_difficulty ON coding_problems(difficulty);
CREATE INDEX idx_cp_topic      ON coding_problems(topic);

-- ============================================================
-- CODING SUBMISSIONS
-- ============================================================

CREATE TABLE coding_submissions (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_id      UUID NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    problem_id      UUID NOT NULL REFERENCES coding_problems(id),
    language        VARCHAR(50) NOT NULL DEFAULT 'python',
    code            TEXT NOT NULL,
    status          submission_status NOT NULL DEFAULT 'pending',
    test_cases_passed INTEGER DEFAULT 0,
    total_test_cases  INTEGER DEFAULT 0,
    runtime_ms      INTEGER,
    memory_kb       INTEGER,
    score           NUMERIC(5,2) DEFAULT 0,
    feedback        TEXT,
    submitted_at    TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_cs_student  ON coding_submissions(student_id);
CREATE INDEX idx_cs_problem  ON coding_submissions(problem_id);
CREATE INDEX idx_cs_status   ON coding_submissions(status);

-- ============================================================
-- LEETCODE PROGRESS
-- ============================================================

CREATE TABLE leetcode_progress (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_id      UUID NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    leetcode_username VARCHAR(100),
    total_solved    INTEGER DEFAULT 0,
    easy_solved     INTEGER DEFAULT 0,
    medium_solved   INTEGER DEFAULT 0,
    hard_solved     INTEGER DEFAULT 0,
    acceptance_rate NUMERIC(5,2) DEFAULT 0,
    contest_rating  INTEGER DEFAULT 0,
    global_ranking  INTEGER,
    recent_activity JSONB DEFAULT '[]'::JSONB,
    is_demo_data    BOOLEAN DEFAULT TRUE,
    last_synced_at  TIMESTAMPTZ DEFAULT NOW(),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_lc_student UNIQUE (student_id)
);

-- ============================================================
-- RESUME ANALYSIS
-- ============================================================

CREATE TABLE resume_analyses (
    id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_id          UUID NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    job_role_id         UUID REFERENCES job_roles(id),
    file_path           VARCHAR(500),
    file_name           VARCHAR(255),

    -- Extracted data
    extracted_skills    TEXT[] DEFAULT '{}',
    extracted_education JSONB DEFAULT '[]'::JSONB,
    extracted_projects  JSONB DEFAULT '[]'::JSONB,
    extracted_experience JSONB DEFAULT '[]'::JSONB,
    certifications      TEXT[] DEFAULT '{}',
    keywords_found      TEXT[] DEFAULT '{}',

    -- Scores
    overall_score       INTEGER DEFAULT 0 CHECK (overall_score BETWEEN 0 AND 100),
    skills_score        INTEGER DEFAULT 0,
    education_score     INTEGER DEFAULT 0,
    projects_score      INTEGER DEFAULT 0,
    experience_score    INTEGER DEFAULT 0,
    completeness_score  INTEGER DEFAULT 0,

    -- Analysis
    missing_skills      TEXT[] DEFAULT '{}',
    missing_keywords    TEXT[] DEFAULT '{}',
    improvement_suggestions JSONB DEFAULT '[]'::JSONB,

    analyzed_at         TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_ra_student ON resume_analyses(student_id);

-- ============================================================
-- INTERVIEWS
-- ============================================================

CREATE TABLE interviews (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_id      UUID NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    job_role_id     UUID REFERENCES job_roles(id),
    total_questions INTEGER DEFAULT 0,
    average_score   NUMERIC(5,2) DEFAULT 0,
    started_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    completed_at    TIMESTAMPTZ
);

CREATE INDEX idx_interviews_student ON interviews(student_id);

-- ============================================================
-- INTERVIEW FEEDBACK (per question)
-- ============================================================

CREATE TABLE interview_feedback (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    interview_id    UUID NOT NULL REFERENCES interviews(id) ON DELETE CASCADE,
    question_number INTEGER NOT NULL,
    question_text   TEXT NOT NULL,
    student_answer  TEXT,
    topic           VARCHAR(100),

    -- Scores (0-10 each)
    technical_score     NUMERIC(4,1) DEFAULT 0,
    relevance_score     NUMERIC(4,1) DEFAULT 0,
    clarity_score       NUMERIC(4,1) DEFAULT 0,
    communication_score NUMERIC(4,1) DEFAULT 0,
    completeness_score  NUMERIC(4,1) DEFAULT 0,
    overall_score       NUMERIC(4,1) DEFAULT 0,

    -- AI Feedback
    strengths           TEXT[] DEFAULT '{}',
    weaknesses          TEXT[] DEFAULT '{}',
    suggested_answer    TEXT,
    improvement_tips    TEXT,
    detailed_feedback   TEXT,

    answered_at         TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_if_interview ON interview_feedback(interview_id);

-- ============================================================
-- SKILL PROFILES (unified, calculated)
-- ============================================================

CREATE TABLE skill_profiles (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_id      UUID NOT NULL REFERENCES students(id) ON DELETE CASCADE,

    -- Core scores (0-100, calculated from all data sources)
    dsa_score           NUMERIC(5,2) DEFAULT 0,
    programming_score   NUMERIC(5,2) DEFAULT 0,
    dbms_score          NUMERIC(5,2) DEFAULT 0,
    oop_score           NUMERIC(5,2) DEFAULT 0,
    aptitude_score      NUMERIC(5,2) DEFAULT 0,
    coding_score        NUMERIC(5,2) DEFAULT 0,
    technical_score     NUMERIC(5,2) DEFAULT 0,
    interview_score     NUMERIC(5,2) DEFAULT 0,
    resume_score        NUMERIC(5,2) DEFAULT 0,
    leetcode_score      NUMERIC(5,2) DEFAULT 0,
    communication_score NUMERIC(5,2) DEFAULT 0,
    web_dev_score       NUMERIC(5,2) DEFAULT 0,
    aiml_score          NUMERIC(5,2) DEFAULT 0,

    -- Evidence tracking
    dsa_observations        INTEGER DEFAULT 0,
    dbms_observations       INTEGER DEFAULT 0,
    aptitude_observations   INTEGER DEFAULT 0,
    coding_observations     INTEGER DEFAULT 0,
    interview_observations  INTEGER DEFAULT 0,
    resume_observations     INTEGER DEFAULT 0,

    -- Trends
    dsa_trend           trend_direction DEFAULT 'stable',
    aptitude_trend      trend_direction DEFAULT 'stable',
    coding_trend        trend_direction DEFAULT 'stable',

    calculated_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_sp_student UNIQUE (student_id)
);

-- ============================================================
-- READINESS RESULTS
-- ============================================================

CREATE TABLE readiness_results (
    id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_id          UUID NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    job_role_id         UUID NOT NULL REFERENCES job_roles(id),

    -- Prediction
    readiness_category  readiness_category NOT NULL DEFAULT 'Needs Improvement',
    readiness_score     NUMERIC(5,2) DEFAULT 0,   -- 0-100 prototype score
    confidence          NUMERIC(4,2) DEFAULT 0,   -- model confidence

    -- SHAP explanation
    shap_values         JSONB DEFAULT '{}'::JSONB,
    positive_factors    JSONB DEFAULT '[]'::JSONB,
    negative_factors    JSONB DEFAULT '[]'::JSONB,

    -- Feature snapshot used for prediction
    feature_snapshot    JSONB DEFAULT '{}'::JSONB,

    is_current          BOOLEAN DEFAULT TRUE,
    model_version       VARCHAR(50) DEFAULT 'v1.0-demo',
    calculated_at       TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_rr_student  ON readiness_results(student_id);
CREATE INDEX idx_rr_role     ON readiness_results(job_role_id);
CREATE INDEX idx_rr_current  ON readiness_results(student_id, is_current);

-- ============================================================
-- SKILL GAPS
-- ============================================================

CREATE TABLE skill_gaps (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_id      UUID NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    job_role_id     UUID NOT NULL REFERENCES job_roles(id),
    skill_name      VARCHAR(100) NOT NULL,
    student_score   NUMERIC(5,2),
    required_score  NUMERIC(5,2),
    gap             NUMERIC(5,2),
    priority        INTEGER,
    confidence      evidence_confidence DEFAULT 'Medium',
    observations    INTEGER DEFAULT 0,
    trend           trend_direction DEFAULT 'stable',
    calculated_at   TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_sg_student ON skill_gaps(student_id, job_role_id);

-- ============================================================
-- RECOMMENDATIONS
-- ============================================================

CREATE TABLE recommendations (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_id      UUID NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    job_role_id     UUID REFERENCES job_roles(id),
    readiness_id    UUID REFERENCES readiness_results(id),

    -- Content
    summary         TEXT,
    weekly_plan     JSONB DEFAULT '[]'::JSONB,
    skill_actions   JSONB DEFAULT '[]'::JSONB,
    resources       JSONB DEFAULT '[]'::JSONB,
    next_steps      TEXT[] DEFAULT '{}',

    is_demo         BOOLEAN DEFAULT FALSE,
    generated_by    VARCHAR(50) DEFAULT 'gemini',
    generated_at    TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_rec_student ON recommendations(student_id);

-- ============================================================
-- PERFORMANCE HISTORY (snapshot per recalculation)
-- ============================================================

CREATE TABLE performance_history (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_id      UUID NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    job_role_id     UUID REFERENCES job_roles(id),
    snapshot        JSONB NOT NULL,  -- full skill profile snapshot
    readiness_category readiness_category,
    readiness_score NUMERIC(5,2),
    recorded_at     TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_ph_student     ON performance_history(student_id);
CREATE INDEX idx_ph_recorded_at ON performance_history(recorded_at);

-- ============================================================
-- TRIGGERS – updated_at auto-update
-- ============================================================

CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER trg_students_updated_at
    BEFORE UPDATE ON students
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER trg_job_roles_updated_at
    BEFORE UPDATE ON job_roles
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER trg_lc_updated_at
    BEFORE UPDATE ON leetcode_progress
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();
