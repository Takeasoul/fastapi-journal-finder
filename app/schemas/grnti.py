from typing import Optional

from pydantic import BaseModel

class GrntiBase(BaseModel):
    code: str
    name: str

class GrntiCreate(GrntiBase):
    pass

class GrntiUpdate(GrntiBase):
    code: Optional[str] = None
    name: Optional[str] = None

class GrntiOut(GrntiBase):
    id: int

    class Config:
        from_attributes = True
