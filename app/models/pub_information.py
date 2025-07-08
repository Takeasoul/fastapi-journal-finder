from sqlalchemy import Column, Integer, String, SmallInteger, ForeignKey
from sqlalchemy.orm import relationship

from app.core.base import Base

class PubInformation(Base):
    __tablename__ = "pub_information"

    pub_id = Column(Integer, ForeignKey("publication.id", onupdate="CASCADE", ondelete="CASCADE"), primary_key=True)
    issn_print = Column(String(9), nullable=True)
    issn_elect = Column(String(9), nullable=True)
    issues_year = Column(SmallInteger, nullable=True)
    arts_issue = Column(Integer, nullable=True)
    pages_issue = Column(Integer, nullable=True)
    founding = Column(String(4), nullable=True)
    release = Column(String(9), nullable=True)
    el_archive = Column(String(20), nullable=True)
    publication = relationship("Publication", back_populates="pub_information", uselist=False)
