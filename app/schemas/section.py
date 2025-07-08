from pydantic import BaseModel

class SectionBase(BaseModel):
    name: str

class SectionCreate(SectionBase):
    pass

class SectionUpdate(SectionBase):
    pass

class SectionOut(SectionBase):
    id: int

    class Config:
        from_attributes = True
