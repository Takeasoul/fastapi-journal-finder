from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.core.base import Base

class Section(Base):
    __tablename__ = "section"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(45), nullable=False)

    main_sections = relationship("MainSection", back_populates="section")
