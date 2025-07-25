from pydantic import BaseModel
from typing import Optional, List
from enum import Enum

from app.models import PublicationActualSpecialty


class SourceEnum(str, Enum):
    elib = "elib"
    vak = "вак"

class PublicationActualSpecialtyBase(BaseModel):
    name: str = None
    issn: str = None
    specialty_name: Optional[str] = None
    source: Optional[SourceEnum]
    actual_flag: int = None
    inclusion_date: Optional[str] = None  # Можно потом переделать на date, если надо
    exclusion_date: Optional[str] = None

class PublicationActualSpecialtyOut(PublicationActualSpecialtyBase):
    class Config:
        from_attributes = True

class PublicationActualSpecialtyFilter(BaseModel):
    name: Optional[str] = None
    issn: Optional[str] = None
    specialty_name: Optional[str] = None
    source: Optional[SourceEnum] = None
    actual_flag: Optional[int] = None
    inclusion_date: Optional[str] = None
    exclusion_date: Optional[str] = None

class PublicationActualSpecialtyResponse(BaseModel):
    items: List[PublicationActualSpecialtyOut]  # Use Pydantic model here
    total: int
    page: int
    per_page: int
    total_pages: int