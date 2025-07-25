from typing import Optional

from pydantic import BaseModel

from app.schemas.oecd import OECDBase, OECDOut


class ActualOECDBase(BaseModel):
    pub_id: int
    oecd_id: int
    actual: bool

class ActualOECDCreate(ActualOECDBase):
    pass

class ActualOECDUpdate(ActualOECDBase):
    pub_id: Optional[int] = None
    oecd_id: Optional[int] = None
    actual: Optional[bool] = None

class ActualOECDOut(ActualOECDBase):
    id: int
    oecd: Optional[OECDOut] = None

    class Config:
        from_attributes = True

class ActualOECDResponse(ActualOECDBase):
    id: int

    class Config:
        from_attributes = True
