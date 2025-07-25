from pydantic import BaseModel
from typing import Optional
from app.schemas.edu_level import EduLevelBase, EduLevelOut
from app.schemas.ugsn import UGSNOut, UGSNBase


class SpecialtyBase(BaseModel):
    code: str
    name: str
    ugsn: Optional[int]
    level_id: Optional[int]

class SpecialtyCreate(SpecialtyBase):
    pass

class SpecialtyUpdate(SpecialtyBase):
    code: Optional[str] = None
    name: Optional[str] = None
    ugsn: Optional[int] = None
    level_id: Optional[int] = None

class SpecialtyOut(BaseModel):
    id: int
    code: str
    name: str
    ugsn: Optional[UGSNOut] = None
    level: Optional[EduLevelOut] = None

    class Config:
        from_attributes = True

class SpecialtyResponse(BaseModel):
    id: int
    code: str
    name: str
    ugsn: Optional[int]
    level_id: Optional[int]  # обязательно должно быть

    class Config:
        from_attributes = True