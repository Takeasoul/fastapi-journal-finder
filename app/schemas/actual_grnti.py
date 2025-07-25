from typing import Optional

from pydantic import BaseModel

from app.schemas.grnti import GrntiBase, GrntiOut


class ActualGRNTIBase(BaseModel):
    pub_id: int
    grnti_id: int
    actual: bool

class ActualGRNTICreate(ActualGRNTIBase):
    pass

class ActualGRNTIUpdate(ActualGRNTIBase):
    pub_id: Optional[int] = None
    grnti_id: Optional[int] = None
    actual: Optional[bool] = None

class ActualGRNTIOut(ActualGRNTIBase):
    id: int
    grnti: Optional[GrntiOut] = None

    class Config:
        from_attributes = True

class ActualGRNTIResponse(ActualGRNTIBase):
    id: int

    class Config:
        from_attributes = True
