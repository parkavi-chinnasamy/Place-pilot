"""
Coding Practice API Routes
Provides LeetCode / OnlineGDB-style problem exploration, sandboxed execution,
genuine testcase judging, submission history, and placement readiness integration.
"""
from datetime import datetime
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import desc, func

from ..database import get_db, SessionLocal
from ..models import (
    User, Student, CodingProblem, CodingSubmission,
    DifficultyLevel, SubmissionStatus
)
from ..utils.auth import get_current_user, get_optional_current_user
from ..services.judge0_service import (
    run_single_execution, judge_problem_submission, outputs_match
)
from ..services.readiness_service import calculate_skill_profile
from ..data.coding_problem_bank import INITIAL_PROBLEMS

router = APIRouter(prefix="/api/coding", tags=["Coding Practice"])


# ── Pydantic Request / Response Schemas ────────────────────────────────────────

class RunCodeRequest(BaseModel):
    problem_id: Optional[str] = None
    language: str  # "python", "cpp", "java"
    code: str
    custom_input: Optional[str] = None


class SubmitCodeRequest(BaseModel):
    problem_id: str
    language: str
    code: str


# ── Database Seeder Helper ───────────────────────────────────────────────────

def ensure_coding_problems_seeded(db: Session):
    """Seeds or updates problem bank with latest starter templates and test cases."""
    for p_data in INITIAL_PROBLEMS:
        existing = db.query(CodingProblem).filter(CodingProblem.slug == p_data["slug"]).first()
        if existing:
            existing.title = p_data["title"]
            existing.difficulty = DifficultyLevel(p_data["difficulty"])
            existing.topic = p_data.get("topic", "DSA")
            existing.description = p_data["description"]
            existing.constraints = p_data.get("constraints")
            existing.input_format = p_data.get("input_format")
            existing.output_format = p_data.get("output_format")
            existing.sample_input = p_data.get("sample_input")
            existing.sample_output = p_data.get("sample_output")
            existing.hints = p_data.get("hints", [])
            existing.starter_code = p_data.get("starter_code", {})
            existing.test_cases = p_data.get("test_cases", [])
            existing.is_active = True
        else:
            prob = CodingProblem(
                title=p_data["title"],
                slug=p_data["slug"],
                difficulty=DifficultyLevel(p_data["difficulty"]),
                topic=p_data.get("topic", "DSA"),
                description=p_data["description"],
                constraints=p_data.get("constraints"),
                input_format=p_data.get("input_format"),
                output_format=p_data.get("output_format"),
                sample_input=p_data.get("sample_input"),
                sample_output=p_data.get("sample_output"),
                hints=p_data.get("hints", []),
                starter_code=p_data.get("starter_code", {}),
                test_cases=p_data.get("test_cases", []),
                is_active=True,
            )
            db.add(prob)
    db.commit()


# ── Endpoints ─────────────────────────────────────────────────────────────────

@router.get("/problems")
def list_problems(
    difficulty: Optional[str] = None,
    topic: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user),
):
    """
    List all active coding problems with optional filtering by difficulty, topic, and search.
    If authenticated student, includes solved status.
    """
    ensure_coding_problems_seeded(db)

    query = db.query(CodingProblem).filter(CodingProblem.is_active == True)

    if difficulty and difficulty != "all":
        try:
            query = query.filter(CodingProblem.difficulty == DifficultyLevel(difficulty.lower()))
        except ValueError:
            pass

    if topic and topic != "all":
        query = query.filter(CodingProblem.topic.ilike(f"%{topic}%"))

    if search:
        query = query.filter(
            CodingProblem.title.ilike(f"%{search}%") | CodingProblem.topic.ilike(f"%{search}%")
        )

    problems = query.order_by(CodingProblem.difficulty, CodingProblem.title).all()

    # Determine solved problems for current student
    solved_problem_ids = set()
    attempted_problem_ids = set()
    if current_user:
        student = db.query(Student).filter(Student.user_id == current_user.id).first()
        if student:
            passed_subs = db.query(CodingSubmission.problem_id).filter(
                CodingSubmission.student_id == student.id,
                CodingSubmission.status == SubmissionStatus.passed
            ).distinct().all()
            solved_problem_ids = {row[0] for row in passed_subs}

            all_subs = db.query(CodingSubmission.problem_id).filter(
                CodingSubmission.student_id == student.id
            ).distinct().all()
            attempted_problem_ids = {row[0] for row in all_subs}

    result = []
    for p in problems:
        # Exclude hidden test cases from problem list
        public_tests = [tc for tc in (p.test_cases or []) if not tc.get("is_hidden", False)]
        result.append({
            "id": str(p.id),
            "title": p.title,
            "slug": p.slug,
            "difficulty": p.difficulty.value if hasattr(p.difficulty, "value") else str(p.difficulty),
            "topic": p.topic,
            "description_preview": p.description[:120] + "..." if len(p.description) > 120 else p.description,
            "sample_test_count": len(public_tests),
            "is_solved": str(p.id) in solved_problem_ids,
            "is_attempted": str(p.id) in attempted_problem_ids,
        })

    return {
        "total": len(result),
        "problems": result,
    }


@router.get("/problems/{problem_id_or_slug}")
def get_problem_detail(
    problem_id_or_slug: str,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user),
):
    """
    Get full problem workspace details.
    Hidden test cases are NEVER returned.
    """
    ensure_coding_problems_seeded(db)

    problem = db.query(CodingProblem).filter(
        (CodingProblem.id == problem_id_or_slug) | (CodingProblem.slug == problem_id_or_slug)
    ).first()

    if not problem:
        raise HTTPException(404, "Coding problem not found")

    # Filter only public test cases
    public_test_cases = [
        {
            "test_number": i + 1,
            "input": tc.get("input", ""),
            "expected_output": tc.get("expected_output", ""),
            "explanation": tc.get("explanation", ""),
        }
        for i, tc in enumerate(problem.test_cases or [])
        if not tc.get("is_hidden", False)
    ]

    is_solved = False
    if current_user:
        student = db.query(Student).filter(Student.user_id == current_user.id).first()
        if student:
            is_solved = db.query(CodingSubmission).filter(
                CodingSubmission.student_id == student.id,
                CodingSubmission.problem_id == problem.id,
                CodingSubmission.status == SubmissionStatus.passed
            ).first() is not None

    return {
        "id": str(problem.id),
        "title": problem.title,
        "slug": problem.slug,
        "difficulty": problem.difficulty.value if hasattr(problem.difficulty, "value") else str(problem.difficulty),
        "topic": problem.topic,
        "description": problem.description,
        "constraints": problem.constraints,
        "input_format": problem.input_format,
        "output_format": problem.output_format,
        "sample_input": problem.sample_input,
        "sample_output": problem.sample_output,
        "hints": problem.hints or [],
        "starter_code": problem.starter_code or {},
        "sample_test_cases": public_test_cases,
        "is_solved": is_solved,
    }


@router.post("/run")
def run_code(
    payload: RunCodeRequest,
    db: Session = Depends(get_db),
):
    """
    Executes student code in sandbox.
    - If custom_input is provided: runs single execution with that input.
    - If no custom_input: runs code against public sample test cases of the problem.
    """
    code = payload.code.strip()
    if not code:
        raise HTTPException(400, "Source code cannot be empty")

    lang = payload.language.lower().strip()

    # Case 1: Custom input execution
    if payload.custom_input is not None:
        exec_res = run_single_execution(code, lang, stdin=payload.custom_input)
        return {
            "mode": "custom",
            "status": exec_res.get("status"),
            "status_description": exec_res.get("status_description"),
            "stdout": exec_res.get("stdout"),
            "stderr": exec_res.get("stderr"),
            "compile_output": exec_res.get("compile_output"),
            "runtime_ms": int(exec_res.get("time", 0) * 1000),
            "memory_kb": exec_res.get("memory", 0),
            "success": exec_res.get("success", False),
        }

    # Case 2: Run against public sample test cases
    if not payload.problem_id:
        raise HTTPException(400, "problem_id is required when custom_input is not provided")

    problem = db.query(CodingProblem).filter(CodingProblem.id == payload.problem_id).first()
    if not problem:
        raise HTTPException(404, "Problem not found")

    public_tests = [tc for tc in (problem.test_cases or []) if not tc.get("is_hidden", False)]
    if not public_tests:
        # Fallback to sample_input if defined
        if problem.sample_input:
            public_tests = [{
                "input": problem.sample_input,
                "expected_output": problem.sample_output or "",
                "explanation": "Sample Test Case",
            }]
        else:
            public_tests = [{"input": "", "expected_output": "", "explanation": "Default"}]

    sample_results = []
    all_passed = True

    for i, tc in enumerate(public_tests):
        inp = tc.get("input", "")
        exp = tc.get("expected_output", "")
        exec_res = run_single_execution(code, lang, stdin=inp)

        status = exec_res.get("status")
        if status == "Compilation Error":
            return {
                "mode": "samples",
                "status": "Compilation Error",
                "compile_output": exec_res.get("compile_output"),
                "all_passed": False,
                "test_results": [],
            }

        actual = exec_res.get("stdout", "")
        passed = (status == "Success") and outputs_match(actual, exp)
        if not passed:
            all_passed = False

        sample_results.append({
            "test_number": i + 1,
            "input": inp,
            "expected_output": exp,
            "actual_output": actual,
            "passed": passed,
            "status": "Passed" if passed else ("Wrong Answer" if status == "Success" else status),
            "stderr": exec_res.get("stderr"),
            "runtime_ms": int(exec_res.get("time", 0) * 1000),
            "memory_kb": exec_res.get("memory", 0),
        })

    return {
        "mode": "samples",
        "status": "All Sample Tests Passed" if all_passed else "Sample Tests Failed",
        "all_passed": all_passed,
        "test_results": sample_results,
    }


@router.post("/submit")
def submit_solution(
    payload: SubmitCodeRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Submits code for evaluation against all test cases (both public and hidden).
    Saves submission, computes score, and triggers placement readiness update.
    """
    code = payload.code.strip()
    if not code:
        raise HTTPException(400, "Source code cannot be empty")

    student = db.query(Student).filter(Student.user_id == current_user.id).first()
    if not student:
        raise HTTPException(404, "Student profile not found")

    problem = db.query(CodingProblem).filter(CodingProblem.id == payload.problem_id).first()
    if not problem:
        raise HTTPException(404, "Coding problem not found")

    all_test_cases = problem.test_cases or []
    if not all_test_cases:
        # Create at least one test case from sample input if empty
        all_test_cases = [{
            "input": problem.sample_input or "",
            "expected_output": problem.sample_output or "",
            "is_hidden": False,
        }]

    # Run genuine test case judging
    judge_result = judge_problem_submission(code, payload.language, all_test_cases)

    verdict = judge_result["verdict"]
    passed_count = judge_result["passed_count"]
    total_count = judge_result["total_count"]
    score = judge_result["score"]
    runtime_ms = judge_result["runtime_ms"]
    memory_kb = judge_result["memory_kb"]
    feedback = judge_result["feedback"]

    # Map verdict to DB submission_status enum
    if verdict == "Accepted":
        db_status = SubmissionStatus.passed
    elif passed_count > 0:
        db_status = SubmissionStatus.partial
    else:
        db_status = SubmissionStatus.failed

    # Persist submission
    submission = CodingSubmission(
        student_id=student.id,
        problem_id=problem.id,
        language=payload.language.lower(),
        code=code,
        status=db_status,
        test_cases_passed=passed_count,
        total_test_cases=total_count,
        runtime_ms=runtime_ms,
        memory_kb=memory_kb,
        score=score,
        feedback=f"[{verdict}] {feedback}",
        submitted_at=datetime.utcnow(),
    )
    db.add(submission)
    db.commit()
    db.refresh(submission)

    # Update placement readiness skill profile if solved or high score
    try:
        calculate_skill_profile(db, student)
    except Exception as e:
        print(f"Readiness update warning: {e}")

    return {
        "submission_id": str(submission.id),
        "verdict": verdict,
        "is_accepted": verdict == "Accepted",
        "passed_count": passed_count,
        "total_count": total_count,
        "score": score,
        "runtime_ms": runtime_ms,
        "memory_kb": memory_kb,
        "feedback": feedback,
        "compile_output": judge_result.get("compile_output"),
        "test_results": judge_result.get("test_results", []),
        "submitted_at": submission.submitted_at.isoformat(),
    }


@router.get("/submissions")
def get_submission_history(
    problem_id: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Get student submission history for a specific problem or across all problems.
    """
    student = db.query(Student).filter(Student.user_id == current_user.id).first()
    if not student:
        raise HTTPException(404, "Student profile not found")

    query = db.query(CodingSubmission).filter(CodingSubmission.student_id == student.id)
    if problem_id:
        query = query.filter(CodingSubmission.problem_id == problem_id)

    subs = query.order_by(desc(CodingSubmission.submitted_at)).limit(50).all()

    result = []
    for s in subs:
        # Extract verdict from feedback "[Verdict] ..."
        verdict = "Accepted" if s.status == SubmissionStatus.passed else "Failed"
        if s.feedback and s.feedback.startswith("[") and "]" in s.feedback:
            verdict = s.feedback[1:s.feedback.index("]")]

        prob_title = s.problem.title if s.problem else "Unknown Problem"
        result.append({
            "id": str(s.id),
            "problem_id": str(s.problem_id),
            "problem_title": prob_title,
            "language": s.language,
            "verdict": verdict,
            "status": s.status.value if hasattr(s.status, "value") else str(s.status),
            "passed_count": s.test_cases_passed,
            "total_count": s.total_test_cases,
            "score": float(s.score or 0),
            "runtime_ms": s.runtime_ms,
            "memory_kb": s.memory_kb,
            "submitted_at": s.submitted_at.isoformat(),
            "code_snippet": s.code[:200] if s.code else "",
        })

    return result


@router.get("/stats")
def get_coding_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Get student coding practice analytics:
    Total solved, difficulty breakdown, topic-wise success, and acceptance rate.
    """
    ensure_coding_problems_seeded(db)

    student = db.query(Student).filter(Student.user_id == current_user.id).first()
    if not student:
        raise HTTPException(404, "Student profile not found")

    all_problems = db.query(CodingProblem).filter(CodingProblem.is_active == True).all()
    total_problems = len(all_problems)
    total_easy = sum(1 for p in all_problems if p.difficulty == DifficultyLevel.easy)
    total_medium = sum(1 for p in all_problems if p.difficulty == DifficultyLevel.medium)
    total_hard = sum(1 for p in all_problems if p.difficulty == DifficultyLevel.hard)

    # Submissions
    submissions = db.query(CodingSubmission).filter(
        CodingSubmission.student_id == student.id
    ).all()

    total_submissions = len(submissions)
    passed_submissions = [s for s in submissions if s.status == SubmissionStatus.passed]
    acceptance_rate = round((len(passed_submissions) / total_submissions) * 100.0, 1) if total_submissions > 0 else 0.0

    # Solved problem IDs
    solved_problem_ids = {s.problem_id for s in passed_submissions}
    solved_problems = [p for p in all_problems if p.id in solved_problem_ids]

    solved_easy = sum(1 for p in solved_problems if p.difficulty == DifficultyLevel.easy)
    solved_medium = sum(1 for p in solved_problems if p.difficulty == DifficultyLevel.medium)
    solved_hard = sum(1 for p in solved_problems if p.difficulty == DifficultyLevel.hard)

    # Topic breakdown
    topics_map = {}
    for p in all_problems:
        t = p.topic or "General"
        if t not in topics_map:
            topics_map[t] = {"topic": t, "total": 0, "solved": 0}
        topics_map[t]["total"] += 1
        if p.id in solved_problem_ids:
            topics_map[t]["solved"] += 1

    return {
        "total_solved": len(solved_problem_ids),
        "total_problems": total_problems,
        "easy_solved": solved_easy,
        "total_easy": total_easy,
        "medium_solved": solved_medium,
        "total_medium": total_medium,
        "hard_solved": solved_hard,
        "total_hard": total_hard,
        "total_submissions": total_submissions,
        "acceptance_rate": acceptance_rate,
        "topic_stats": list(topics_map.values()),
    }
