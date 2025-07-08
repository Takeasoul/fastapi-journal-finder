from sqlalchemy import Column, Integer, Date, Numeric, Text, SmallInteger, ForeignKey
from sqlalchemy.orm import relationship
from app.core.base import Base

class Journal(Base):
    __tablename__ = "journal"

    id = Column(Integer, primary_key=True, index=True)
    pub_id = Column(Integer, ForeignKey("publication.id", ondelete="CASCADE"), nullable=False)
    last_send_date = Column(Date, nullable=True)
    price = Column(Numeric(10, 2), nullable=True)
    copyright_fee = Column(Numeric(10, 2), nullable=True)
    expert = Column(SmallInteger, nullable=True)
    review = Column(SmallInteger, nullable=True)
    url = Column(Text, nullable=True)

    publication = relationship("Publication", back_populates="journals")
