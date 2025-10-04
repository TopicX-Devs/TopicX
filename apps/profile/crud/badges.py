from typing import List
from sqlalchemy.orm import Session
from apps.profile.models.profile import Badge

def create_badge(db: Session, badge_in):
    badge = Badge(name=badge_in.name.strip(), description=badge_in.description or "")
    db.add(badge)
    db.commit()
    db.refresh(badge)
    return badge

def list_badges(db: Session, skip: int = 0, limit: int = 100) -> List[Badge]:
    return db.query(Badge).offset(skip).limit(limit).all()

def get_badge(db: Session, badge_id: int):
    return db.query(Badge).filter(Badge.id == badge_id).first()

def delete_badge(db: Session, badge_id: int):
    badge = get_badge(db, badge_id)
    if not badge:
        return None
    db.delete(badge)
    db.commit()
    return badge
