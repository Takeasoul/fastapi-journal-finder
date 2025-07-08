from sqlalchemy import Column, Integer, Enum, String, ForeignKey
from sqlalchemy.orm import relationship

from app.core.base import Base
import enum

class RincEnum(str, enum.Enum):
    no = "1"
    yes = "2"
    partial = "3"  # учитываются отдельные статьи

class SimpleYesNoEnum(str, enum.Enum):
    no = "1"
    yes = "2"

class WosEnum(str, enum.Enum):
    no = "1"
    yes = "2"
    translated = "3"

class WosQuartEnum(str, enum.Enum):
    no = "1"
    q1 = "2"
    q2 = "3"
    q3 = "4"
    q4 = "5"

class ScopEnum(str, enum.Enum):
    no = "1"
    yes = "2"
    translated = "3"

class ScopQuartEnum(str, enum.Enum):
    no = "1"
    q1 = "2"
    q2 = "3"
    q3 = "4"
    q4 = "5"

class WhiteLevelEnum(str, enum.Enum):
    no = "1"
    l1 = "2"
    l2 = "3"
    l3 = "4"

class VakCatEnum(str, enum.Enum):
    no = "1"
    c1 = "2"
    c2 = "3"
    c3 = "4"

class Index(Base):
    __tablename__ = "index"

    pub_id = Column(Integer, ForeignKey("publication.id", onupdate="CASCADE", ondelete="CASCADE"), primary_key=True)
    rinc = Column(Enum(RincEnum), nullable=False)
    rinc_core = Column(Enum(SimpleYesNoEnum), nullable=False)
    rsci = Column(Enum(SimpleYesNoEnum), nullable=False)
    doaj = Column(Enum(SimpleYesNoEnum), nullable=False)
    wos = Column(Enum(WosEnum), nullable=False)
    wos_quart = Column(Enum(WosQuartEnum), nullable=False)
    scop = Column(Enum(ScopEnum), nullable=False)
    scop_quart = Column(Enum(ScopQuartEnum), nullable=False)
    white = Column(Enum(SimpleYesNoEnum), nullable=False)
    white_level = Column(Enum(WhiteLevelEnum), nullable=False)
    vak = Column(Enum(SimpleYesNoEnum), nullable=False)
    vak_cat = Column(Enum(VakCatEnum), nullable=False)
    crossref = Column(Enum(SimpleYesNoEnum), nullable=False)
    doi = Column(String(45), nullable=True)

    publication = relationship("Publication", back_populates="index")