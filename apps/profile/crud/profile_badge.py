# apps/profile/crud/profile_badge.py
from sqlalchemy.orm import Session
from apps.profile.models.profile import Profile, ProfileBadge, Badge

def assign_badges_to_profile(db: Session, profile_id: int, badge_ids: list):
    profile = db.query(Profile).filter(Profile.id == profile_id).first()
    if not profile:
        raise ValueError("Profile not found")
    for bid in set(badge_ids):
        exists = db.query(ProfileBadge).filter_by(profile_id=profile_id, badge_id=bid).first()
        if exists:
            continue
        pb = ProfileBadge(profile_id=profile_id, badge_id=bid)
        db.add(pb)
    db.commit()

def remove_badge_from_profile(db: Session, profile_id: int, badge_id: int):
    pb = db.query(ProfileBadge).filter_by(profile_id=profile_id, badge_id=badge_id).first()
    if not pb:
        return False
    db.delete(pb)
    db.commit()
    return True

def list_profile_badges(db: Session, profile_id: int):
    return (
        db.query(Badge)
        .join(ProfileBadge, Badge.id == ProfileBadge.badge_id)
        .filter(ProfileBadge.profile_id == profile_id)
        .all()
    )
