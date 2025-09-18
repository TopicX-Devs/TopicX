from sqlalchemy import Column , Intger , String
from core.db import Base
from sqlalchemy.orm import relationship

class Skill(Base):
    __tablename__ = "skills"


    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)

    # Relationships
    profiles = relationship("ProfileSkill", back_populates="skill", cascade="all, delete-orphan")