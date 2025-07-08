from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship

from app.core.base import Base

class OECD(Base):
    __tablename__ = "oecd"

    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(8), nullable=False)
    name = Column(Text, nullable=False)

    actual_oecd_items = relationship("ActualOECD", back_populates="oecd")