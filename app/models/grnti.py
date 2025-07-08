from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship

from app.core.base import Base

class Grnti(Base):
    __tablename__ = "grnti"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(8), nullable=False)
    name = Column(Text, nullable=False)

    actual_grnti_items = relationship("ActualGRNTI", back_populates="grnti")