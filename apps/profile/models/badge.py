from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from core.db import Base
from sqlalchemy import func


class Badge(Base):
    __tablename__ = "badges"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)
    icon_url = Column(String, nullable=True)

    # Relationships
    profiles = relationship("ProfileBadge", back_populates="badge", cascade="all, delete-orphan")
