from sqlalchemy import Column, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.core.base import Base

class ActualOECD(Base):
    __tablename__ = "actual_oecd"

    id = Column(Integer, primary_key=True, autoincrement=True)
    pub_id = Column(Integer, ForeignKey("publication.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    oecd_id = Column(Integer, ForeignKey("oecd.id", onupdate="CASCADE", ondelete="NO ACTION"), nullable=False)
    actual = Column(Boolean, nullable=False)

    publication = relationship("Publication", back_populates="actual_oecd_items")
    oecd = relationship("OECD", back_populates="actual_oecd_items")
