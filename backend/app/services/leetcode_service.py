
import json
import re
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from sqlalchemy.orm import Session
from ..models import LeetCodeProgress, LeetCodeSnapshot


def normalize_leetcode_url(url: str) -> Optional[Dict[str, str]]:
    """Validate and normalize a public LeetCode profile URL."""
    if not url or not url.strip():
        return None

    candidate = url.strip()
    if "://" not in candidate:
        candidate = "https://" + candidate

    try:
        parsed = urllib.parse.urlparse(candidate)
        if parsed.scheme not in ("http", "https"):
            return None
        if parsed.hostname not in ("leetcode.com", "www.leetcode.com"):
            return None

        parts = [p for p in parsed.path.split("/") if p]
        if parts and parts[0] == "u":
            parts = parts[1:]

        if len(parts) != 1:
            return None

        username = parts[0]
        if not re.fullmatch(r"[A-Za-z0-9_-]+", username):
            return None

        return {
            "username": username,
            "canonical_url": f"https://leetcode.com/u/{username}/",
        }
    except (ValueError, AttributeError):
        return None


def fetch_leetcode_stats(username: str) -> Dict[str, Any]:
    """Fetch public profile statistics through LeetCode GraphQL."""
    query = """
    query getUserProfile($username: String!) {
      matchedUser(username: $username) {
        username
        profile { ranking }
        submitStatsGlobal {
          acSubmissionNum { difficulty count submissions }
          totalSubmissionNum { difficulty count submissions }
        }
        userCalendar { streak totalActiveDays submissionCalendar }
      }
      userContestRanking(username: $username) {
        attendedContestsCount rating topPercentage
      }
    }
    """

    payload = json.dumps({
        "query": query,
        "variables": {"username": username},
    }).encode("utf-8")

    request = urllib.request.Request(
        "https://leetcode.com/graphql",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 PlacePilot/1.0",
            "Referer": f"https://leetcode.com/u/{username}/",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            result = json.loads(response.read().decode("utf-8"))
    except Exception as exc:
        raise RuntimeError(f"Unable to contact LeetCode: {exc}") from exc

    if result.get("errors"):
        raise RuntimeError("LeetCode returned a GraphQL error.")

    data = result.get("data") or {}
    matched = data.get("matchedUser")
    if not matched:
        raise ValueError("LeetCode profile not found or not publicly available.")

    solved = {"All": 0, "Easy": 0, "Medium": 0, "Hard": 0}
    ac_submissions = 0
    entries = (
        (matched.get("submitStatsGlobal") or {}).get("acSubmissionNum") or []
    )
    for entry in entries:
        difficulty = entry.get("difficulty")
        if difficulty in solved:
            solved[difficulty] = int(entry.get("count") or 0)
        if difficulty == "All":
            ac_submissions = int(entry.get("submissions") or 0)

    total_submissions = 0
    total_entries = (
        (matched.get("submitStatsGlobal") or {}).get("totalSubmissionNum") or []
    )
    for entry in total_entries:
        if entry.get("difficulty") == "All":
            total_submissions = int(entry.get("submissions") or 0)

    acceptance_rate = (
        round((ac_submissions / total_submissions) * 100, 2)
        if total_submissions > 0
        else None
    )

    calendar = matched.get("userCalendar") or {}
    raw_calendar = calendar.get("submissionCalendar") or "{}"
    try:
        submission_calendar = (
            json.loads(raw_calendar)
            if isinstance(raw_calendar, str)
            else raw_calendar
        )
    except (TypeError, ValueError):
        submission_calendar = {}

    contest = data.get("userContestRanking") or {}

    return {
        "leetcode_username": matched.get("username") or username,
        "total_solved": solved["All"],
        "easy_solved": solved["Easy"],
        "medium_solved": solved["Medium"],
        "hard_solved": solved["Hard"],
        "acceptance_rate": acceptance_rate,
        "contest_rating": contest.get("rating"),
        "global_ranking": (matched.get("profile") or {}).get("ranking"),
        "contests_attended": contest.get("attendedContestsCount"),
        "top_percentage": contest.get("topPercentage"),
        "streak": calendar.get("streak"),
        "total_active_days": calendar.get("totalActiveDays"),
        "submission_calendar": submission_calendar,
    }


def sync_student_leetcode(
    db: Session,
    student_id: str,
    manual: bool = False,
) -> LeetCodeProgress:
    """Fetch stats and save progress plus a snapshot.

    A failed fetch preserves the last successfully saved statistics.
    """
    progress = (
        db.query(LeetCodeProgress)
        .filter(LeetCodeProgress.student_id == student_id)
        .first()
    )

    if not progress or not progress.leetcode_url:
        raise ValueError("Connect a LeetCode profile URL first.")

    profile = normalize_leetcode_url(progress.leetcode_url)
    if not profile:
        progress.sync_status = "FAILED"
        progress.last_sync_error = "Invalid LeetCode profile URL."
        db.commit()
        raise ValueError("Invalid LeetCode profile URL.")

    progress.sync_status = "SYNCING"
    progress.last_sync_error = None
    db.commit()

    try:
        stats = fetch_leetcode_stats(profile["username"])
        previous_total = int(progress.total_solved or 0)

        progress.leetcode_url = profile["canonical_url"]
        progress.leetcode_username = stats["leetcode_username"]

        for field in (
            "total_solved",
            "easy_solved",
            "medium_solved",
            "hard_solved",
            "acceptance_rate",
            "contest_rating",
            "global_ranking",
            "contests_attended",
            "top_percentage",
            "streak",
            "total_active_days",
            "submission_calendar",
        ):
            value = stats.get(field)
            # Missing optional values should not erase valid stored data.
            if value is not None:
                setattr(progress, field, value)

        progress.delta_total = int(progress.total_solved or 0) - previous_total
        progress.delta_easy = int(progress.easy_solved or 0) - int(
            getattr(progress, "easy_solved", 0) or 0
        )
        progress.delta_medium = 0
        progress.delta_hard = 0

        progress.is_demo_data = False
        progress.sync_status = "SYNCED"
        progress.last_sync_error = None
        progress.last_synced_at = datetime.now(timezone.utc)

        snapshot = LeetCodeSnapshot(
            student_id=student_id,
            leetcode_username=progress.leetcode_username,
            total_solved=progress.total_solved or 0,
            easy_solved=progress.easy_solved or 0,
            medium_solved=progress.medium_solved or 0,
            hard_solved=progress.hard_solved or 0,
            acceptance_rate=progress.acceptance_rate or 0,
            contest_rating=progress.contest_rating,
            global_ranking=progress.global_ranking,
            delta_solved=progress.delta_total or 0,
            captured_at=datetime.now(timezone.utc),
        )
        db.add(snapshot)
        db.commit()
        db.refresh(progress)
        return progress

    except Exception as exc:
        db.rollback()
        progress = (
            db.query(LeetCodeProgress)
            .filter(LeetCodeProgress.student_id == student_id)
            .first()
        )
        if progress:
            progress.sync_status = "FAILED"
            progress.last_sync_error = str(exc)[:500]
            db.commit()
        raise
def ensure_leetcode_progress_columns():
    """Add missing LeetCode columns to an existing SQLite database."""
    from sqlalchemy import inspect, text
    from ..database import engine

    inspector = inspect(engine)

    if "leetcode_progress" not in inspector.get_table_names():
        return

    existing_columns = {
        column["name"]
        for column in inspector.get_columns("leetcode_progress")
    }

    columns_to_add = {
        "leetcode_url": "VARCHAR(255)",
        "contests_attended": "INTEGER DEFAULT 0",
        "top_percentage": "NUMERIC(5, 2)",
        "streak": "INTEGER DEFAULT 0",
        "total_active_days": "INTEGER DEFAULT 0",
        "submission_calendar": "JSON",
        "sync_status": "VARCHAR(50) DEFAULT 'NOT_CONNECTED'",
        "last_sync_error": "TEXT",
        "delta_total": "INTEGER DEFAULT 0",
        "delta_easy": "INTEGER DEFAULT 0",
        "delta_medium": "INTEGER DEFAULT 0",
        "delta_hard": "INTEGER DEFAULT 0",
    }

    with engine.begin() as connection:
        for column_name, column_type in columns_to_add.items():
            if column_name not in existing_columns:
                connection.execute(
                    text(
                        f"ALTER TABLE leetcode_progress "
                        f"ADD COLUMN {column_name} {column_type}"
                    )
                )