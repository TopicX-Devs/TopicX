# apps/profile/api/skills.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from core.db import get_db
from apps.profile import crud as profile_crud  # adjust imports to your module layout
from apps.profile.schemas.profile import SkillCreate, SkillOut
from apps.auth.deps import get_current_user, role_required

skill_router = APIRouter(prefix="/skills", tags=["skills"])


@skill_router.post("/", response_model=SkillOut, status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(role_required("admin"))])
def create_skill(skill_in: SkillCreate, db: Session = Depends(get_db)):
    try:
        return profile_crud.skills.create_skill(db, skill_in)
    except Exception as e:
        # If IntegrityError, convert to 409
        from sqlalchemy.exc import IntegrityError
        if isinstance(e, IntegrityError):
            raise HTTPException(status_code=409, detail="Skill already exists")
        raise

@skill_router.get("/", response_model=List[SkillOut])
def list_skills(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return profile_crud.skills.list_skills(db, skip=skip, limit=limit)

@skill_router.delete("/{skill_id}", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(role_required("admin"))])
def delete_skill(skill_id: int, db: Session = Depends(get_db)):
    deleted = profile_crud.skills.delete_skill(db, skill_id)
    if not deleted:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Skill not found")
    return None
