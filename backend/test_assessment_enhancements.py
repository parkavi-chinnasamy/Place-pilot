"""
Verification script for PlacePilot assessment enhancements:
1. Topic, difficulty, and question count filtering
2. Zero answer submission score = 0% marks
3. Detailed counting (attempted, correct, incorrect, unanswered)
4. Assessment session lifecycle (Not Started -> In Progress -> Completed)
5. Readiness engine integration
"""
import sys, os
sys.path.insert(0, '.')

from app.database import SessionLocal
from app.models.models import (
    User, Student, Assessment, AssessmentQuestion,
    AssessmentType, DifficultyLevel, SkillProfile, ReadinessResult
)
from app.routes.assessment import start_assessment, submit_assessment, get_assessment_status, get_questions
from app.schemas.schemas import AssessmentStart, AssessmentSubmit, AnswerSubmit

def run_tests():
    db = SessionLocal()
    try:
        print("=" * 60)
        print("RUNNING PLACEPILOT ASSESSMENT ENHANCEMENTS TEST SUITE")
        print("=" * 60)

        # 1. Verify question bank
        total_q = db.query(AssessmentQuestion).count()
        print(f"[TEST 1] Total questions in database: {total_q}")
        assert total_q >= 90, f"Expected at least 90 questions, got {total_q}"

        # Check by difficulty
        easy_q = db.query(AssessmentQuestion).filter(AssessmentQuestion.difficulty == DifficultyLevel.easy).count()
        med_q = db.query(AssessmentQuestion).filter(AssessmentQuestion.difficulty == DifficultyLevel.medium).count()
        hard_q = db.query(AssessmentQuestion).filter(AssessmentQuestion.difficulty == DifficultyLevel.hard).count()
        print(f"         Easy: {easy_q}, Medium: {med_q}, Hard: {hard_q}")
        assert easy_q > 0 and med_q > 0 and hard_q > 0, "All difficulty tiers must have questions"

        # 2. Pick a test student
        student = db.query(Student).first()
        user = db.query(User).filter(User.id == student.user_id).first()
        print(f"[TEST 2] Using student: {user.full_name} ({user.email})")

        # 3. Test question selection with filters
        filtered_qs = get_questions(
            assessment_type="technical",
            count=5,
            topic="DBMS",
            difficulty="medium",
            current_user=user,
            db=db
        )
        print(f"[TEST 3] Selected {len(filtered_qs)} DBMS Medium Technical questions:")
        for q in filtered_qs:
            print(f"         - [{q['difficulty']}] {q['topic']}: {q['question_text'][:40]}...")
        assert len(filtered_qs) > 0, "Filter should return questions"

        # 4. Test starting a test (In Progress status)
        start_payload = AssessmentStart(
            assessment_type="aptitude",
            topic="Quantitative",
            difficulty="easy",
            count=5
        )
        started = start_assessment(start_payload, current_user=user, db=db)
        asm_id = started["assessment_id"]
        print(f"[TEST 4] Started assessment session ID: {asm_id}")
        assert started["status"] == "in_progress", f"Expected in_progress, got {started['status']}"
        assert len(started["questions"]) == 5, f"Expected 5 questions, got {len(started['questions'])}"

        # Verify status endpoint reflects In Progress
        status_res = get_assessment_status(current_user=user, db=db)
        print(f"         Aptitude status after start: {status_res['aptitude']['status']}")
        assert status_res["aptitude"]["status"] == "In Progress", "Status should be 'In Progress'"

        # 5. TEST CRITICAL REQUIREMENT: SUBMITTING ZERO ANSWERS MUST GIVE 0 MARKS!
        zero_payload = AssessmentSubmit(
            assessment_id=asm_id,
            assessment_type="aptitude",
            answers=[AnswerSubmit(question_id=q["id"], selected_option=None) for q in started["questions"]],
            time_taken_secs=45
        )
        res_zero = submit_assessment(zero_payload, current_user=user, db=db)
        print(f"[TEST 5] Submitting ZERO answers result:")
        print(f"         Score: {res_zero['score']}%")
        print(f"         Attempted: {res_zero['attempted_questions']}")
        print(f"         Correct: {res_zero['correct_answers']}")
        print(f"         Incorrect: {res_zero['incorrect_answers']}")
        print(f"         Unanswered: {res_zero['unanswered_questions']}")
        print(f"         Status: {res_zero['status']}")

        assert res_zero["score"] == 0.0, f"Expected 0.0 score, got {res_zero['score']}"
        assert res_zero["attempted_questions"] == 0, f"Expected 0 attempted, got {res_zero['attempted_questions']}"
        assert res_zero["correct_answers"] == 0, f"Expected 0 correct, got {res_zero['correct_answers']}"
        assert res_zero["unanswered_questions"] == 5, f"Expected 5 unanswered, got {res_zero['unanswered_questions']}"
        assert res_zero["status"] == "completed", "Status should be completed"

        # 6. Test submitting partial answers with correct & incorrect calculations
        # Start a new technical test
        tech_started = start_assessment(
            AssessmentStart(assessment_type="technical", count=4),
            current_user=user,
            db=db
        )
        t_qs = tech_started["questions"]
        q0 = db.query(AssessmentQuestion).filter(AssessmentQuestion.id == t_qs[0]["id"]).first()
        q1 = db.query(AssessmentQuestion).filter(AssessmentQuestion.id == t_qs[1]["id"]).first()

        # Let's answer q0 correctly, q1 incorrectly, and leave q2 and q3 unanswered
        wrong_opt = "B" if q1.correct_option != "B" else "C"
        partial_answers = [
            AnswerSubmit(question_id=str(q0.id), selected_option=q0.correct_option), # correct
            AnswerSubmit(question_id=str(q1.id), selected_option=wrong_opt),           # incorrect
            AnswerSubmit(question_id=t_qs[2]["id"], selected_option=None),              # unanswered
            AnswerSubmit(question_id=t_qs[3]["id"], selected_option=""),                # unanswered
        ]

        partial_sub = AssessmentSubmit(
            assessment_id=tech_started["assessment_id"],
            assessment_type="technical",
            answers=partial_answers,
            time_taken_secs=60
        )
        res_part = submit_assessment(partial_sub, current_user=user, db=db)
        print(f"[TEST 6] Submitting Partial answers (1 correct, 1 wrong, 2 unans out of 4):")
        print(f"         Score: {res_part['score']}%")
        print(f"         Attempted: {res_part['attempted_questions']}")
        print(f"         Correct: {res_part['correct_answers']}")
        print(f"         Incorrect: {res_part['incorrect_answers']}")
        print(f"         Unanswered: {res_part['unanswered_questions']}")

        assert res_part["score"] == 25.0, f"Expected 25.0% (1/4), got {res_part['score']}"
        assert res_part["attempted_questions"] == 2, f"Expected 2 attempted, got {res_part['attempted_questions']}"
        assert res_part["correct_answers"] == 1, f"Expected 1 correct, got {res_part['correct_answers']}"
        assert res_part["incorrect_answers"] == 1, f"Expected 1 incorrect, got {res_part['incorrect_answers']}"
        assert res_part["unanswered_questions"] == 2, f"Expected 2 unanswered, got {res_part['unanswered_questions']}"

        # 7. Verify status persistence after submission
        status_after = get_assessment_status(current_user=user, db=db)
        print(f"[TEST 7] Status after submission:")
        print(f"         Aptitude status: {status_after['aptitude']['status']}, Last score: {status_after['aptitude']['last_score']}%")
        print(f"         Technical status: {status_after['technical']['status']}, Last score: {status_after['technical']['last_score']}%")
        assert status_after["aptitude"]["status"] == "Completed"
        assert status_after["technical"]["status"] == "Completed"

        # 8. Verify readiness engine integration
        sp = db.query(SkillProfile).filter(SkillProfile.student_id == student.id).first()
        print(f"[TEST 8] Student SkillProfile updated:")
        print(f"         Technical Score: {sp.technical_score}, Observations: {sp.dbms_observations}")
        print(f"         Aptitude Score: {sp.aptitude_score}, Observations: {sp.aptitude_observations}")
        assert sp.technical_score is not None and sp.aptitude_score is not None

        print("=" * 60)
        print("ALL TESTS PASSED SUCCESSFULLY! 100% VERIFIED!")
        print("=" * 60)
    finally:
        db.close()

if __name__ == "__main__":
    run_tests()
