import enum

from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.core.base import Base
from sqlalchemy.dialects.postgresql import ENUM as SqlEnum

class RincEnum(str, enum.Enum):
    no = "нет"
    yes = "да"
    partial = "учитываются отдельные статьи"

class SimpleYesNoEnum(str, enum.Enum):
    no = "нет"
    yes = "да"

class WosEnum(str, enum.Enum):
    no = "нет"
    yes = "да"
    translated = "переводная версия"

class WosQuartEnum(str, enum.Enum):
    no = "нет"
    q1 = "1"
    q2 = "2"
    q3 = "3"
    q4 = "4"

class ScopEnum(str, enum.Enum):
    no = "нет"
    yes = "да"
    translated = "переводная версия"

class ScopQuartEnum(str, enum.Enum):
    no = "нет"
    q1 = "1"
    q2 = "2"
    q3 = "3"
    q4 = "4"

class WiteLevelEnum(str, enum.Enum):
    no = "нет"
    l1 = "1"
    l2 = "2"
    l3 = "3"
    l4 = "4"

class VakCatEnum(str, enum.Enum):
    no = "нет"
    c1 = "1"
    c2 = "2"
    c3 = "3"

class Index(Base):
    __tablename__ = "index"

    pub_id = Column(Integer, ForeignKey("publication.id", onupdate="CASCADE", ondelete="CASCADE"), primary_key=True)
    rinc = Column(SqlEnum(RincEnum, native_enum=False, create_type=False, values_callable=lambda obj: [e.value for e in obj]), nullable=False)
    rinc_core = Column(SqlEnum(SimpleYesNoEnum, native_enum=False, create_type=False, values_callable=lambda obj: [e.value for e in obj]), nullable=False)
    rsci = Column(SqlEnum(SimpleYesNoEnum, native_enum=False, create_type=False, values_callable=lambda obj: [e.value for e in obj]), nullable=False)
    doaj = Column(SqlEnum(SimpleYesNoEnum, native_enum=False, create_type=False, values_callable=lambda obj: [e.value for e in obj]), nullable=False)
    wos = Column(SqlEnum(WosEnum, native_enum=False, create_type=False, values_callable=lambda obj: [e.value for e in obj]), nullable=False)
    wos_quart = Column(SqlEnum(WosQuartEnum, native_enum=False, create_type=False, values_callable=lambda obj: [e.value for e in obj]), nullable=False)
    scop = Column(SqlEnum(ScopEnum, native_enum=False, create_type=False, values_callable=lambda obj: [e.value for e in obj]), nullable=False)
    scop_quart = Column(SqlEnum(ScopQuartEnum, native_enum=False, create_type=False, values_callable=lambda obj: [e.value for e in obj]), nullable=False)
    white = Column(SqlEnum(SimpleYesNoEnum, native_enum=False, create_type=False, values_callable=lambda obj: [e.value for e in obj]), nullable=False)
    wite_level = Column(SqlEnum(WiteLevelEnum, native_enum=False, create_type=False, values_callable=lambda obj: [e.value for e in obj]), nullable=False)
    vak = Column(SqlEnum(SimpleYesNoEnum, native_enum=False, create_type=False, values_callable=lambda obj: [e.value for e in obj]), nullable=False)
    vak_cat = Column(SqlEnum(VakCatEnum, native_enum=False, create_type=False, values_callable=lambda obj: [e.value for e in obj]), nullable=False)
    crossref = Column(SqlEnum(SimpleYesNoEnum, native_enum=False, create_type=False, values_callable=lambda obj: [e.value for e in obj]), nullable=False)
    doi = Column(String(45), nullable=True)

    publication = relationship("Publication", back_populates="index")