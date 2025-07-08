from pydantic import BaseModel
from typing import Optional

class MainSectionBase(BaseModel):
    pub_id: int
    section_id: int
    actual: bool

class MainSectionCreate(MainSectionBase):
    pass

class MainSectionUpdate(MainSectionBase):
    pass

class MainSectionOut(MainSectionBase):
    id: int

    class Config:
        from_attributes = True
