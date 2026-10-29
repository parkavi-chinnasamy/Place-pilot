"""
PlacePilot Database Migration: Clean Historical Resume Certifications
Re-analyzes existing resume records using the new universal certification
extraction engine to remove degrees, graduation years, percentages,
and declarations previously saved in placepilot.db.
"""

import os
import sys

sys.path.insert(0, ".")

from app.database import SessionLocal
from app.models.models import ResumeAnalysis
from app.services.resume_service import (
    extract_resume_text,
    parse_resume_sections,
    extract_certifications_flat,
    _is_disqualified,
    _clean_cert_line,
)


def migrate_saved_certifications():
    db = SessionLocal()
    try:
        rows = db.query(ResumeAnalysis).all()
        print(f"Checking {len(rows)} resume analysis records in database...")

        updated_count = 0
        for r in rows:
            old_certs = r.certifications or []
            new_certs = []

            # If original file is still present on disk, re-extract cleanly
            if r.file_path and os.path.exists(r.file_path):
                try:
                    with open(r.file_path, "rb") as f:
                        content = f.read()
                    text, _, _ = extract_resume_text(r.file_name, content)
                    sections = parse_resume_sections(text)
                    new_certs = extract_certifications_flat(sections, text)
                except Exception as err:
                    # Fallback to filtering the existing stored list
                    new_certs = [
                        _clean_cert_line(c)
                        for c in old_certs
                        if not _is_disqualified(_clean_cert_line(c))
                    ]
            else:
                new_certs = [
                    _clean_cert_line(c)
                    for c in old_certs
                    if not _is_disqualified(_clean_cert_line(c))
                ]

            if old_certs != new_certs:
                print(f"Record {r.id} ({r.file_name}):")
                print(f"  BEFORE: {old_certs}")
                print(f"  AFTER:  {new_certs}")
                r.certifications = new_certs
                updated_count += 1

        db.commit()
        print(f"\nMigration complete: Updated {updated_count} / {len(rows)} records successfully.")
    finally:
        db.close()


if __name__ == "__main__":
    migrate_saved_certifications()
