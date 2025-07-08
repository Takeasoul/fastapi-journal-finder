from pydantic import BaseModel
from datetime import date
from typing import Optional
from app.models.actual_specialty import SourceEnum

class ActualSpecialtyBase(BaseModel):
    pub_id: int
    specialty_id: int
    source: SourceEnum
    actual: bool
    start_date: Optional[date] = None
    end_date: Optional[date] = None

class ActualSpecialtyCreate(ActualSpecialtyBase):
    pass

class ActualSpecialtyUpdate(ActualSpecialtyBase):
    pass

class ActualSpecialtyOut(ActualSpecialtyBase):
    id: int

    class Config:
        from_attributes = True
