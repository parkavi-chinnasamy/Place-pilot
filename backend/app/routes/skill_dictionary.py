"""
Admin-only endpoints for viewing and updating the extendable Skill Dictionary.
Follows the existing authentication pattern (get_current_admin).
"""
import json
from pathlib import Path
from typing import Any, Dict, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from ..utils.auth import get_current_admin
from ..models import User
from ..services.resume_service import reload_skill_taxonomy, SKILL_TAXONOMY, _DICT_PATH

router = APIRouter(prefix="/api/admin/skill-dictionary", tags=["Admin - Skill Dictionary"])


# ──────────────────────────────────────────────────────────────────────────────
# Pydantic schemas
# ──────────────────────────────────────────────────────────────────────────────

class SkillEntry(BaseModel):
    category: str
    aliases: list[str]
    regex: str


class AddSkillRequest(BaseModel):
    skill_name: str
    category: str
    aliases: list[str]
    regex: str


class UpdateSkillRequest(BaseModel):
    category: Optional[str] = None
    aliases: Optional[list[str]] = None
    regex: Optional[str] = None


# ──────────────────────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────────────────────

def _read_dict_file() -> Dict[str, Any]:
    """Read the JSON dict file, returning an empty structure if missing."""
    if _DICT_PATH.is_file():
        with open(_DICT_PATH, "r", encoding="utf-8") as fh:
            return json.load(fh)
    return {"_version": "1.0.0", "skills": {}}


def _write_dict_file(data: Dict[str, Any]) -> None:
    """Write (overwrite) the JSON dict file atomically."""
    _DICT_PATH.parent.mkdir(parents=True, exist_ok=True)
    tmp = _DICT_PATH.with_suffix(".tmp")
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)
    tmp.replace(_DICT_PATH)


# ──────────────────────────────────────────────────────────────────────────────
# Endpoints
# ──────────────────────────────────────────────────────────────────────────────

@router.get("")
def list_skills(admin: User = Depends(get_current_admin)):
    """Return the full in-memory skill taxonomy (merged built-in + JSON)."""
    return {
        "total": len(SKILL_TAXONOMY),
        "source_file": str(_DICT_PATH),
        "file_exists": _DICT_PATH.is_file(),
        "skills": {
            name: {
                "category": spec.get("category", ""),
                "aliases": spec.get("aliases", []),
                "regex": spec.get("regex", ""),
            }
            for name, spec in SKILL_TAXONOMY.items()
        },
    }


@router.post("")
def add_skill(body: AddSkillRequest, admin: User = Depends(get_current_admin)):
    """Add a new skill entry to the skill dictionary JSON and reload."""
    data = _read_dict_file()
    if body.skill_name in data.get("skills", {}):
        raise HTTPException(400, f"Skill '{body.skill_name}' already exists. Use PUT to update.")
    data.setdefault("skills", {})[body.skill_name] = {
        "category": body.category,
        "aliases": body.aliases,
        "regex": body.regex,
    }
    _write_dict_file(data)
    reload_skill_taxonomy()
    return {"message": f"Skill '{body.skill_name}' added successfully.", "total_skills": len(SKILL_TAXONOMY)}


@router.put("/{skill_name}")
def update_skill(skill_name: str, body: UpdateSkillRequest, admin: User = Depends(get_current_admin)):
    """Update an existing skill entry in the dictionary JSON and reload."""
    data = _read_dict_file()
    existing = data.get("skills", {}).get(skill_name)
    if not existing:
        raise HTTPException(404, f"Skill '{skill_name}' not found in skill_dictionary.json.")
    if body.category is not None:
        existing["category"] = body.category
    if body.aliases is not None:
        existing["aliases"] = body.aliases
    if body.regex is not None:
        existing["regex"] = body.regex
    data["skills"][skill_name] = existing
    _write_dict_file(data)
    reload_skill_taxonomy()
    return {"message": f"Skill '{skill_name}' updated successfully.", "updated": existing}


@router.delete("/{skill_name}")
def delete_skill(skill_name: str, admin: User = Depends(get_current_admin)):
    """Remove a skill from the dictionary JSON and reload."""
    data = _read_dict_file()
    if skill_name not in data.get("skills", {}):
        raise HTTPException(404, f"Skill '{skill_name}' not found in skill_dictionary.json.")
    del data["skills"][skill_name]
    _write_dict_file(data)
    reload_skill_taxonomy()
    return {"message": f"Skill '{skill_name}' deleted.", "remaining_skills": len(data["skills"])}


@router.post("/reload")
def force_reload(admin: User = Depends(get_current_admin)):
    """Force a reload of the skill taxonomy from disk (useful after manual file edits)."""
    updated = reload_skill_taxonomy()
    return {"message": "Skill taxonomy reloaded from disk.", "total_skills": len(updated)}
