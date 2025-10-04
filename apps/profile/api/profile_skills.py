# apps/profile/api/profile_skills.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from core.db import get_db
from apps.profile.schemas.profile import AssignSkills, SkillOut
from apps.profile import crud as profile_crud
from apps.auth.deps import get_current_user, role_required

profile_skill_router = APIRouter(prefix="/profiles/{profile_id}/skills", tags=["profile-skills"])

@profile_skill_router.post("/", response_model=List[SkillOut])
def assign_skills(profile_id: int, payload: AssignSkills, db: Session = Depends(get_db),
                  current_user = Depends(get_current_user)):
    # authorize: owner or admin
    if current_user.role != "admin" and current_user.profile.id != profile_id:
        raise HTTPException(status.HTTP_403_FORBIDDEN)
    profile_crud.profile_skill.assign_skills_to_profile(db, profile_id, payload.skill_ids)
    return profile_crud.profile_skill.list_profile_skills(db, profile_id)

@profile_skill_router.get("/", response_model=List[SkillOut])
def list_skills(profile_id: int, db: Session = Depends(get_db)):
    return profile_crud.profile_skill.list_profile_skills(db, profile_id)

@profile_skill_router.delete("/{skill_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_skill(profile_id: int, skill_id: int, db: Session = Depends(get_db),
                 current_user = Depends(get_current_user)):
    if current_user.role != "admin" and current_user.profile.id != profile_id:
        raise HTTPException(status.HTTP_403_FORBIDDEN)
    ok = profile_crud.profile_skill.remove_skill_from_profile(db, profile_id, skill_id)
    if not ok:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Skill not found on profile")
    return None
