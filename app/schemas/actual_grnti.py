from pydantic import BaseModel

class ActualGRNTIBase(BaseModel):
    pub_id: int
    grnti_id: int
    actual: bool

class ActualGRNTICreate(ActualGRNTIBase):
    pass

class ActualGRNTIUpdate(ActualGRNTIBase):
    pass

class ActualGRNTIOut(ActualGRNTIBase):
    id: int

    class Config:
        from_attributes = True
