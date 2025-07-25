from typing import Optional

from pydantic import BaseModel

class UGSNBase(BaseModel):
    code: str
    name: str

class UGSNCreate(UGSNBase):
    pass

class UGSNUpdate(UGSNBase):
    code: Optional[str] = None
    name: Optional[str] = None
class UGSNOut(UGSNBase):
    id: int

    class Config:
        from_attributes = True