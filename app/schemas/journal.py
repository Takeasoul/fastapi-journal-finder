from datetime import date
from typing import Optional, List
from pydantic import BaseModel, HttpUrl, condecimal

from app.schemas.publication import PublicationBase, PublicationResponse


class JournalBase(BaseModel):
    pub_id: int
    last_send_date: Optional[date] = None
    price: Optional[condecimal(max_digits=10, decimal_places=2)] = None
    copyright_fee: Optional[condecimal(max_digits=10, decimal_places=2)] = None
    expert: Optional[int] = None
    review: Optional[int] = None
    url: Optional[HttpUrl] = None

class JournalCreate(JournalBase):
    pass

class JournalUpdate(BaseModel):
    pub_id: Optional[int] = None
    last_send_date: Optional[date] = None
    price: Optional[condecimal(max_digits=10, decimal_places=2)] = None
    copyright_fee: Optional[condecimal(max_digits=10, decimal_places=2)] = None
    expert: Optional[int] = None
    review: Optional[int] = None
    url: Optional[HttpUrl] = None

class JournalFilter(BaseModel):
    pub_id: Optional[int] = None
    last_send_date: Optional[date] = None
    last_send_date_from: Optional[date] = None
    last_send_date_to: Optional[date] = None
    price: Optional[condecimal(max_digits=10, decimal_places=2)] = None
    price_from: Optional[condecimal(max_digits=10, decimal_places=2)] = None
    price_to: Optional[condecimal(max_digits=10, decimal_places=2)] = None
    copyright_fee: Optional[condecimal(max_digits=10, decimal_places=2)] = None
    copyright_fee_from: Optional[condecimal(max_digits=10, decimal_places=2)] = None
    copyright_fee_to: Optional[condecimal(max_digits=10, decimal_places=2)] = None
    expert: Optional[int] = None
    review: Optional[int] = None
    url: Optional[str] = None

class PaginatedJournalResponse(BaseModel):
    items: List["JournalOut"]
    total: int
    page: int
    per_page: int
    total_pages: int

class JournalOut(JournalBase):
    id: int
    publication: Optional[PublicationResponse] = None

    class Config:
        from_attributes = True

class JournalResponse(JournalBase):
    id: int

    class Config:
        from_attributes = True

