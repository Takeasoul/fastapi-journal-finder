from pydantic import BaseModel

class ActualOECDBase(BaseModel):
    pub_id: int
    oecd_id: int
    actual: bool

class ActualOECDCreate(ActualOECDBase):
    pass

class ActualOECDUpdate(ActualOECDBase):
    pass

class ActualOECDOut(ActualOECDBase):
    id: int

    class Config:
        from_attributes = True
