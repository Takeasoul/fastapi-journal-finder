from pydantic import BaseModel, constr
from typing import Optional
from enum import Enum

class RincEnum(str, Enum):
    no = "нет"
    yes = "да"
    partial = "учитываются отдельные статьи"

class SimpleYesNoEnum(str, Enum):
    no = "нет"
    yes = "да"

class WosEnum(str, Enum):
    no = "нет"
    yes = "да"
    translated = "переводная версия"

class WosQuartEnum(str, Enum):
    no = "нет"
    q1 = "1"
    q2 = "2"
    q3 = "3"
    q4 = "4"

class ScopEnum(str, Enum):
    no = "нет"
    yes = "да"
    translated = "переводная версия"

class ScopQuartEnum(str, Enum):
    no = "нет"
    q1 = "1"
    q2 = "2"
    q3 = "3"
    q4 = "4"

class WiteLevelEnum(str, Enum):
    no = "нет"
    l1 = "1"
    l2 = "2"
    l3 = "3"
    l4 = "4"

class VakCatEnum(str, Enum):
    no = "нет"
    c1 = "1"
    c2 = "2"
    c3 = "3"

class IndexBase(BaseModel):
    pub_id: int
    rinc: RincEnum
    rinc_core: SimpleYesNoEnum
    rsci: SimpleYesNoEnum
    doaj: SimpleYesNoEnum
    wos: WosEnum
    wos_quart: WosQuartEnum
    scop: ScopEnum
    scop_quart: ScopQuartEnum
    white: SimpleYesNoEnum
    wite_level: WiteLevelEnum
    vak: SimpleYesNoEnum
    vak_cat: VakCatEnum
    crossref: SimpleYesNoEnum
    doi: Optional[constr(max_length=45)] = None

class IndexCreate(IndexBase):
    pass

class IndexUpdate(IndexBase):
    pub_id: Optional[int] = None
    rinc: Optional[RincEnum] = None
    rinc_core: Optional[SimpleYesNoEnum] = None
    rsci: Optional[SimpleYesNoEnum] = None
    doaj: Optional[SimpleYesNoEnum] = None
    wos: Optional[WosEnum] = None
    wos_quart: Optional[WosQuartEnum] = None
    scop: Optional[ScopEnum] = None
    scop_quart: Optional[ScopQuartEnum] = None
    white: Optional[SimpleYesNoEnum] = None
    wite_level: Optional[WiteLevelEnum] = None
    vak: Optional[SimpleYesNoEnum] = None
    vak_cat: Optional[VakCatEnum] = None
    crossref: Optional[SimpleYesNoEnum] = None
    doi: Optional[constr(max_length=45)] = None

class IndexOut(IndexBase):
    class Config:
        from_attributes = True


class IndexResponse(BaseModel):
    rinc: Optional[str] = None
    rinc_core: Optional[str] = None
    rsci: Optional[str] = None
    doaj: Optional[str] = None
    wos: Optional[str] = None
    wos_quart: Optional[str] = None
    scop: Optional[str] = None
    scop_quart: Optional[str] = None
    white: Optional[str] = None
    wite_level: Optional[str] = None
    vak: Optional[str] = None
    vak_cat: Optional[str] = None
    crossref: Optional[str] = None
    doi: Optional[str] = None