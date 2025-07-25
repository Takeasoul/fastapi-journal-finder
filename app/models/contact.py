from sqlalchemy import Column, Integer, Text, String, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.core.base import Base
from enum import Enum

class CountryEnum(str, Enum):
    russia = "Россия"
    usa = "USA"
    russia_alt = "Russia"
    uk = "UK"

class Contact(Base):
    __tablename__ = "contact"

    pub_id = Column(Integer, ForeignKey("publication.id", onupdate="CASCADE", ondelete="CASCADE"), primary_key=True)
    country = Column(SQLEnum(CountryEnum, values_callable=lambda x: [e.value for e in x]), nullable=False)
    city_id = Column(Integer, ForeignKey("city.id", onupdate="CASCADE", ondelete="RESTRICT"), nullable=True)
    addr = Column(Text, nullable=True)
    email = Column(String(45), nullable=True)
    phone = Column(String(20), nullable=True)
    site = Column(Text, nullable=True)

    publication = relationship("Publication", back_populates="contact")
    city = relationship("City", back_populates="contacts")