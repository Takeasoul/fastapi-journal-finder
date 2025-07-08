from sqlalchemy import Column, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.core.base import Base

class ActualGRNTI(Base):
    __tablename__ = "actual_grnti"

    id = Column(Integer, primary_key=True, autoincrement=True)
    pub_id = Column(Integer, ForeignKey("publication.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    grnti_id = Column(Integer, ForeignKey("grnti.id", onupdate="CASCADE", ondelete="NO ACTION"), nullable=False)
    actual = Column(Boolean, nullable=False)

    publication = relationship("Publication", back_populates="actual_grnti_items")
    grnti = relationship("Grnti", back_populates="actual_grnti_items")