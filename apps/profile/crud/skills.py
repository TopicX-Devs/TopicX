# apps/profile/crud/skills.py
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List
from apps.profile.models.profile import Skill, ProfileSkill, Profile
from apps.profile.schemas.profile import SkillCreate

def create_skill(db: Session, skill_in: SkillCreate) -> Skill:
    skill = Skill(name=skill_in.name.strip())
    db.add(skill)
    try:
        db.commit()
        db.refresh(skill)
    except IntegrityError:
        db.rollback()
        raise
    return skill

def get_skill_by_id(db: Session, skill_id: int) -> Skill:
    return db.query(Skill).filter(Skill.id == skill_id).first()

def get_skill_by_name(db: Session, name: str) -> Skill:
    return db.query(Skill).filter(Skill.name == name).first()

def list_skills(db: Session, skip: int = 0, limit: int = 100) -> List[Skill]:
    return db.query(Skill).offset(skip).limit(limit).all()

def delete_skill(db: Session, skill_id: int) -> None:
    skill = get_skill_by_id(db, skill_id)
    if not skill:
        return None
    db.delete(skill)
    db.commit()
    return skill
