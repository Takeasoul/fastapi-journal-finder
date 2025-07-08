from pydantic import BaseModel

class UGSNBase(BaseModel):
    code: str
    name: str

class UGSNCreate(UGSNBase):
    pass

class UGSNUpdate(UGSNBase):
    pass

class UGSNOut(UGSNBase):
    id: int

    class Config:
        from_attributes = True