from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from datetime import datetime
from core.db import Base # assuming you have Base in core/db.py
from sqlalchemy import func
from sqlalchemy.orm import relationship

class Profile(Base):
    __tablename__ = "profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id") , nullable=False , unique=True)

    full_name = Column(String, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    photo_url = Column(String, nullable=True)

    university = Column(String, nullable=True)
    faculty = Column(String, nullable=True)
    major = Column(String, nullable=True)

    points = Column(Integer, default=0)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="profile")  # linked to auth.models.User
    skills = relationship("ProfileSkill", back_populates="profile", cascade="all, delete-orphan")
    badges = relationship("ProfileBadge", back_populates="profile", cascade="all, delete-orphan")


class Skill(Base):
    __tablename__ = "skills"


    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)

    # Relationships
    profiles = relationship("ProfileSkill", back_populates="skill", cascade="all, delete-orphan")


class ProfileSkill(Base):
    __tablename__ = "profile_skills"

    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("profiles.id", ondelete="CASCADE"))
    skill_id = Column(Integer, ForeignKey("skills.id", ondelete="CASCADE"))

    # Relationships
    profile = relationship("Profile", back_populates="skills")
    skill = relationship("Skill", back_populates="profiles")


class ProfileBadge(Base):
    __tablename__ = "profile_badges"

    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("profiles.id", ondelete="CASCADE"))
    badge_id = Column(Integer, ForeignKey("badges.id", ondelete="CASCADE"))

    awarded_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    profile = relationship("Profile", back_populates="badges")
    badge = relationship("Badge", back_populates="profiles")



class Badge(Base):
    __tablename__ = "badges"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)
    icon_url = Column(String, nullable=True)

    # Relationships
    profiles = relationship("ProfileBadge", back_populates="badge", cascade="all, delete-orphan")
