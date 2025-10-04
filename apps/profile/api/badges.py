from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from core.db import get_db
from apps.profile.schemas.profile import BadgeCreate, BadgeOut
from apps.profile.crud import badges as badges_crud
from apps.auth.deps import role_required

badge_router = APIRouter(prefix="/badges", tags=["badges"])

@badge_router.post("/", response_model=BadgeOut, status_code=status.HTTP_201_CREATED, dependencies=[Depends(role_required("admin"))])
def create_badge(payload: BadgeCreate, db: Session = Depends(get_db)):
    try:
        return badges_crud.create_badge(db, payload)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@badge_router.get("/", response_model=List[BadgeOut])
def list_badges(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return badges_crud.list_badges(db, skip=skip, limit=limit)

@badge_router.delete("/{badge_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(role_required("admin"))])
def delete_badge(badge_id: int, db: Session = Depends(get_db)):
    deleted = badges_crud.delete_badge(db, badge_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Badge not found")
    return None