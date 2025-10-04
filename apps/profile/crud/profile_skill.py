# apps/profile/crud/profile_skill.py
from sqlalchemy.orm import Session
from apps.profile.models.profile import Profile, ProfileSkill, Skill

def assign_skills_to_profile(db: Session, profile_id: int, skill_ids: list):
    profile = db.query(Profile).filter(Profile.id == profile_id).first()
    if not profile:
        raise ValueError("Profile not found")
    added = []
    for sid in set(skill_ids):
        exists = db.query(ProfileSkill).filter_by(profile_id=profile_id, skill_id=sid).first()
        if exists:
            continue
        ps = ProfileSkill(profile_id=profile_id, skill_id=sid)
        db.add(ps)
        added.append(sid)
    db.commit()
    return added

def remove_skill_from_profile(db: Session, profile_id: int, skill_id: int):
    ps = db.query(ProfileSkill).filter_by(profile_id=profile_id, skill_id=skill_id).first()
    if not ps:
        return False
    db.delete(ps)
    db.commit()
    return True

def list_profile_skills(db: Session, profile_id: int):
    return db.query(Skill).join(ProfileSkill, Skill.id == ProfileSkill.skill_id).filter(ProfileSkill.profile_id == profile_id).all()
