from pydantic import BaseModel, EmailStr, HttpUrl
from typing import Optional
from enum import Enum

class CountryEnum(str, Enum):
    russia = "Россия"
    usa = "USA"
    russia_alt = "Russia"
    uk = "UK"

class ContactBase(BaseModel):
    pub_id: int
    country: CountryEnum
    city_id: Optional[int] = None
    addr: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    site: Optional[str] = None

class ContactCreate(ContactBase):
    pass

class ContactUpdate(ContactBase):
    pass

class ContactOut(ContactBase):
    class Config:
        from_attributes = True
