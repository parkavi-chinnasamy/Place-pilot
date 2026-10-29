"""
Populate assessment questions into the persistent SQLite database.
Idempotent: skips questions that already exist (matching question_text).
"""
import sys
import os

# Add parent directory to path so imports work
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.abspath(os.path.join(current_dir, "..", ".."))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from app.database import SessionLocal
from app.models.models import AssessmentQuestion, AssessmentType, DifficultyLevel
from app.data.question_bank import QUESTIONS_DATA

def populate():
    db = SessionLocal()
    try:
        added_count = 0
        existing_texts = {q.question_text.strip().lower() for q in db.query(AssessmentQuestion).all()}

        for q in QUESTIONS_DATA:
            text = q["question_text"].strip()
            if text.lower() in existing_texts:
                continue

            new_q = AssessmentQuestion(
                assessment_type=AssessmentType(q["assessment_type"]),
                topic=q["topic"],
                difficulty=DifficultyLevel(q["difficulty"]),
                question_text=text,
                option_a=q["option_a"],
                option_b=q["option_b"],
                option_c=q["option_c"],
                option_d=q["option_d"],
                correct_option=q["correct_option"].strip().upper(),
                explanation=q.get("explanation", ""),
                is_active=True
            )
            db.add(new_q)
            existing_texts.add(text.lower())
            added_count += 1

        db.commit()
        total_now = db.query(AssessmentQuestion).count()
        print(f"Added {added_count} new questions. Total active questions in DB: {total_now}")
        return total_now
    finally:
        db.close()

if __name__ == "__main__":
    populate()
