from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.core.base import Base

class City(Base):
    __tablename__ = "city"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(45), nullable=False)

    contacts = relationship("Contact", back_populates="city")