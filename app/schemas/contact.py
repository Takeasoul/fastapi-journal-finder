import enum

from pydantic import BaseModel, EmailStr, HttpUrl
from typing import Optional

from app.schemas.city import CityBase, CityOut
from app.schemas.publication import PublicationBase


class CountryEnum(str, enum.Enum):
    russia = "Россия"
    usa = "USA"
    russia_alt = "Russia"
    uk = "UK"
    cyprus = "Cyprus"
    austria = "Austria"
    thailand = "Thailand"
    taghikistan = "Таджикистан"
    belarussia = "Беларусь"

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
    pub_id: Optional[int] = None
    country: Optional[CountryEnum] = None
    city_id: Optional[int] = None
    addr: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    site: Optional[str] = None

class ContactOut(ContactBase):
    city: Optional[CityOut] = None
    class Config:
        from_attributes = True

class ContactResponse(ContactBase):
    class Config:
        from_attributes = True
