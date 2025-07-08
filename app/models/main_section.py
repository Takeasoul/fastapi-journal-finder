from sqlalchemy import Column, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.core.base import Base

class MainSection(Base):
    __tablename__ = "main_sections"

    id = Column(Integer, primary_key=True, autoincrement=True)
    pub_id = Column(Integer, ForeignKey("publication.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    section_id = Column(Integer, ForeignKey("section.id", onupdate="CASCADE", ondelete="NO ACTION"), nullable=False)
    actual = Column(Boolean, nullable=False)

    publication = relationship("Publication", back_populates="main_sections")
    section = relationship("Section", back_populates="main_sections")
