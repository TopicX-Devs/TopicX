# apps/profile/api/profile_badges.py
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from core.db import get_db
from apps.profile.schemas.profile import AssignBadges, BadgeOut
from apps.profile.crud import profile_badge as profile_badge_crud
from apps.auth.deps import get_current_user

profile_badge_router = APIRouter()

@profile_badge_router.post("/", response_model=List[BadgeOut])
def assign_badges(profile_id: int, payload: AssignBadges, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    if current_user.role != "admin" and getattr(current_user, "profile", None) and current_user.profile.id != profile_id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Not authorized")
    profile_badge_crud.assign_badges_to_profile(db, profile_id, payload.badge_ids)
    return profile_badge_crud.list_profile_badges(db, profile_id)

@profile_badge_router.get("/", response_model=List[BadgeOut])
def list_profile_badges(profile_id: int, db: Session = Depends(get_db)):
    return profile_badge_crud.list_profile_badges(db, profile_id)

@profile_badge_router.delete("/{badge_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_badge(profile_id: int, badge_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    if current_user.role != "admin" and getattr(current_user, "profile", None) and current_user.profile.id != profile_id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Not authorized")
    ok = profile_badge_crud.remove_badge_from_profile(db, profile_id, badge_id)
    if not ok:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Badge not assigned")
    return None
