# apps/profile/schemas/profile.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class SkillBase(BaseModel):
    name: str

class SkillCreate(SkillBase):
    pass

class SkillOut(SkillBase):
    id: int
    class Config:
        orm_mode = True

class BadgeBase(BaseModel):
    name: str
    description: Optional[str] = None
    icon_url: Optional[str] = None

class BadgeCreate(BadgeBase):
    pass

class BadgeOut(BadgeBase):
    id: int
    class Config:
        orm_mode = True

class ProfileBase(BaseModel):
    full_name: str
    username: str
    photo_url: Optional[str] = None
    university: Optional[str] = None
    faculty: Optional[str] = None
    major: Optional[str] = None

class ProfileCreate(ProfileBase):
    pass

class ProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    username: Optional[str] = None
    photo_url: Optional[str] = None
    university: Optional[str] = None
    faculty: Optional[str] = None
    major: Optional[str] = None

class ProfileOut(ProfileBase):
    id: int
    points: int
    created_at: datetime
    updated_at: datetime
    skills: List[SkillOut] = []
    badges: List[BadgeOut] = []
    class Config:
        orm_mode = True

class AssignSkills(BaseModel):
    skill_ids: List[int]

class AssignBadges(BaseModel):
    badge_ids: List[int]
