from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from datetime import datetime
from core.db import Base # assuming you have Base in core/db.py
from sqlalchemy import func
from sqlalchemy.orm import relationship

class Profile(Base):
    __tablename__ = "profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    full_name = Column(String, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    photo_url = Column(String, nullable=True)

    niversity = Column(String, nullable=True)
    faculty = Column(String, nullable=True)
    major = Column(String, nullable=True)

    points = Column(Integer, default=0)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="profile")  # linked to auth.models.User
    skills = relationship("ProfileSkill", back_populates="profile", cascade="all, delete-orphan")
    badges = relationship("ProfileBadge", back_populates="profile", cascade="all, delete-orphan")
