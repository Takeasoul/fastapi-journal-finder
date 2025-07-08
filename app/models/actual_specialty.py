from sqlalchemy import Column, Integer, Boolean, ForeignKey, Date, Enum as SqlEnum
from enum import Enum

from sqlalchemy.orm import relationship

from app.core.base import Base

class SourceEnum(str, Enum):
    elib = "elib"
    vak = "вак"

class ActualSpecialty(Base):
    __tablename__ = "actual_specialty"

    id = Column(Integer, primary_key=True, autoincrement=True)
    pub_id = Column(Integer, ForeignKey("publication.id"), nullable=False)
    specialty_id = Column(Integer, ForeignKey("specialty.id"), nullable=False)
    source = Column(SqlEnum(SourceEnum, native_enum=False, create_type=False, values_callable=lambda obj: [e.value for e in obj]), nullable=False)
    actual = Column(Boolean, nullable=False)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)

    publication = relationship("Publication", back_populates="actual_specialties")
    specialty = relationship("Specialty", back_populates="actual_specialties")