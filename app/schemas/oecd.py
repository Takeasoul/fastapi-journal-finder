from pydantic import BaseModel

class OECDBase(BaseModel):
    code: str
    name: str

class OECDCreate(OECDBase):
    pass

class OECDUpdate(OECDBase):
    code: str
    name: str

class OECDOut(OECDBase):
    id: int

    class Config:
        from_attributes = True
