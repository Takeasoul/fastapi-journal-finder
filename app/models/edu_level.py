from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.core.base import Base

class EduLevel(Base):
    __tablename__ = "edu_level"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    specialties = relationship("Specialty", back_populates="level")