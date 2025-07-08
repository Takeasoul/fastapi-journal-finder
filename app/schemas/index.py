from pydantic import BaseModel, constr
from typing import Optional
from enum import Enum

class RincEnum(str, Enum):
    no = "1"
    yes = "2"
    partial = "3"

class SimpleYesNoEnum(str, Enum):
    no = "1"
    yes = "2"

class WosEnum(str, Enum):
    no = "1"
    yes = "2"
    translated = "3"

class WosQuartEnum(str, Enum):
    no = "1"
    q1 = "2"
    q2 = "3"
    q3 = "4"
    q4 = "5"

class ScopEnum(str, Enum):
    no = "1"
    yes = "2"
    translated = "3"

class ScopQuartEnum(str, Enum):
    no = "1"
    q1 = "2"
    q2 = "3"
    q3 = "4"
    q4 = "5"

class WhiteLevelEnum(str, Enum):
    no = "1"
    l1 = "2"
    l2 = "3"
    l3 = "4"

class VakCatEnum(str, Enum):
    no = "1"
    c1 = "2"
    c2 = "3"
    c3 = "4"

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
    white_level: WhiteLevelEnum
    vak: SimpleYesNoEnum
    vak_cat: VakCatEnum
    crossref: SimpleYesNoEnum
    doi: Optional[constr(max_length=45)] = None

class IndexCreate(IndexBase):
    pass

class IndexUpdate(IndexBase):
    pass

class IndexOut(IndexBase):
    class Config:
        from_attributes = True
