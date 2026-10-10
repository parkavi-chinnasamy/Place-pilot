from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User, JobRole, RoleRequirement
from ..schemas import JobRoleCreate, JobRoleUpdate
from ..utils.auth import get_current_user, get_current_admin

router = APIRouter(prefix="/api/job-roles", tags=["Job Roles"])


@router.get("")
def list_roles(db: Session = Depends(get_db)):
    roles = db.query(JobRole).filter(JobRole.is_active == True).all()
    result = []
    for r in roles:
        reqs = db.query(RoleRequirement).filter(RoleRequirement.job_role_id == r.id).all()
        result.append({
            "id": str(r.id),
            "name": r.name,
            "description": r.description,
            "is_active": r.is_active,
            "requirements": [
                {"skill_name": req.skill_name, "required_score": req.required_score, "weight": float(req.weight)}
                for req in reqs
            ],
        })
    return result


@router.get("/{role_id}")
def get_role(role_id: str, db: Session = Depends(get_db)):
    role = db.query(JobRole).filter(JobRole.id == role_id).first()
    if not role:
        raise HTTPException(404, "Job role not found")
    reqs = db.query(RoleRequirement).filter(RoleRequirement.job_role_id == role.id).all()
    return {
        "id": str(role.id),
        "name": role.name,
        "description": role.description,
        "is_active": role.is_active,
        "requirements": [
            {"skill_name": r.skill_name, "required_score": r.required_score, "weight": float(r.weight)}
            for r in reqs
        ],
    }


@router.post("")
def create_role(
    payload: JobRoleCreate,
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    if db.query(JobRole).filter(JobRole.name == payload.name).first():
        raise HTTPException(400, "Role name already exists")

    role = JobRole(name=payload.name, description=payload.description)
    db.add(role)
    db.flush()

    for req in payload.requirements:
        r = RoleRequirement(
            job_role_id=role.id,
            skill_name=req["skill_name"],
            required_score=req["required_score"],
            weight=req.get("weight", 1.0),
        )
        db.add(r)

    db.commit()
    db.refresh(role)
    return {"id": str(role.id), "name": role.name, "message": "Job role created"}


@router.put("/{role_id}")
def update_role(
    role_id: str,
    payload: JobRoleUpdate,
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    role = db.query(JobRole).filter(JobRole.id == role_id).first()
    if not role:
        raise HTTPException(404, "Job role not found")

    if payload.name:
        role.name = payload.name
    if payload.description is not None:
        role.description = payload.description
    if payload.is_active is not None:
        role.is_active = payload.is_active

    if payload.requirements is not None:
        db.query(RoleRequirement).filter(RoleRequirement.job_role_id == role.id).delete()
        for req in payload.requirements:
            r = RoleRequirement(
                job_role_id=role.id,
                skill_name=req["skill_name"],
                required_score=req["required_score"],
                weight=req.get("weight", 1.0),
            )
            db.add(r)

    db.commit()
    return {"message": "Job role updated"}
