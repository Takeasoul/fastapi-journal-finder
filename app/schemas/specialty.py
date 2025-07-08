from pydantic import BaseModel
from typing import Optional
from app.schemas.edu_level import EduLevelBase

class SpecialtyBase(BaseModel):
    code: str
    name: str
    ugsn: int
    level_id: Optional[int]

class SpecialtyCreate(SpecialtyBase):
    pass

class SpecialtyUpdate(SpecialtyBase):
    pass

class SpecialtyOut(SpecialtyBase):
    id: int
    level: Optional[EduLevelBase]

    class Config:
        from_attributes = True