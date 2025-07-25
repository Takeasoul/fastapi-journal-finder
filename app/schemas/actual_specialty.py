from pydantic import BaseModel
from datetime import date
from typing import Optional, List
from app.models.actual_specialty import SourceEnum
from app.schemas.publication import PublicationBase
from app.schemas.specialty import SpecialtyBase, SpecialtyResponse


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
    pub_id: Optional[int] = None
    specialty_id: Optional[int] = None
    source: Optional[SourceEnum] = None
    actual: Optional[bool] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None

class ActualSpecialtyOut(ActualSpecialtyBase):
    id: int
    specialty: Optional[SpecialtyResponse] = None

    class Config:
        from_attributes = True

class ActualSpecialtyResponse(ActualSpecialtyBase):
    id: int

    class Config:
        from_attributes = True


class ActualSpecialtyFilter(BaseModel):
    specialty_id: Optional[int] = None
    source: Optional[str] = None
    actual: Optional[bool] = None
    start_date_from: Optional[date] = None
    start_date_to: Optional[date] = None
    end_date_from: Optional[date] = None
    end_date_to: Optional[date] = None

class PaginatedActualSpecialtyResponse(BaseModel):
    items: List[ActualSpecialtyOut]
    total: int
    page: int
    per_page: int
    total_pages: int