from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.base import Base

class Specialty(Base):
    __tablename__ = "specialty"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(8), nullable=False)
    name = Column(String(160), nullable=False)
    ugsn = Column(Integer, ForeignKey("ugsn.id", onupdate="CASCADE", ondelete="RESTRICT"), nullable=True)
    level_id = Column(Integer, ForeignKey("edu_level.id", onupdate="CASCADE", ondelete="RESTRICT"), nullable=True)

    ugsn_rel = relationship("UGSN", back_populates="specialties")
    level = relationship("EduLevel", back_populates="specialties")
    actual_specialties = relationship("ActualSpecialty", back_populates="specialty")