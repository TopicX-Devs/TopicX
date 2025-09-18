from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from core.db import Base


class ProfileSkill(Base):
    __tablename__ = "profile_skills"

    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("profiles.id", ondelete="CASCADE"))
    skill_id = Column(Integer, ForeignKey("skills.id", ondelete="CASCADE"))

    # Relationships
    profile = relationship("Profile", back_populates="skills")
    skill = relationship("Skill", back_populates="profiles")
