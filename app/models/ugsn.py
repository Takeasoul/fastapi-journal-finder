# app/models/ugsn.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.core.base import Base

class UGSN(Base):
    __tablename__ = "ugsn"

    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(8), nullable=False, unique=True)
    name = Column(String(90), nullable=False)
    specialties = relationship("Specialty", back_populates="ugsn_rel")