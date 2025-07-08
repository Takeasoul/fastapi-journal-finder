from pydantic import BaseModel, field_validator
from typing import Optional, Set, List
from enum import Enum

from app.schemas.publication import LanguageEnum


class VakCategoryEnum(str, Enum):
    no = "нет"
    one = "1"
    two = "2"
    three = "3"

class PublicationBaseInfoBase(BaseModel):
    name: str
    issn: str
    directions: Optional[str] = None
    site: Optional[str] = None
    periodicity: Optional[int] = None
    languages: Optional[Set[LanguageEnum]] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    review_period: Optional[str] = None
    sections: Optional[str] = None
    vak_category: Optional[VakCategoryEnum] = None

class PaginatedBaseInfoResponse(BaseModel):
    items: List[PublicationBaseInfoBase]
    total: int
    page: int
    per_page: int
    total_pages: int

class PublicationBaseInfoOut(PublicationBaseInfoBase):
    class Config:
        from_attributes = True

class PublicationBaseInfoFilter(BaseModel):
    name: Optional[str] = None
    issn: Optional[str] = None
    directions: Optional[str] = None
    site: Optional[str] = None
    periodicity: Optional[int] = None
    languages: Optional[Set[LanguageEnum]] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    review_period: Optional[str] = None
    sections: Optional[str] = None
    vak_category: Optional[VakCategoryEnum] = None
