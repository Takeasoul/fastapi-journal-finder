from pydantic import BaseModel
from typing import Optional

from app.schemas.section import SectionBase, SectionOut


class MainSectionBase(BaseModel):
    pub_id: int
    section_id: int
    actual: bool

class MainSectionCreate(MainSectionBase):
    pass

class MainSectionUpdate(MainSectionBase):
    pub_id: Optional[int] = None
    section_id: Optional[int] = None
    actual: Optional[bool] = None

class MainSectionOut(MainSectionBase):
    id: int
    section: Optional[SectionOut] = None

    class Config:
        from_attributes = True

class MainSectionResponse(MainSectionBase):
    id: int

    class Config:
        from_attributes = True
