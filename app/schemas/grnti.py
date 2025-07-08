from pydantic import BaseModel

class GrntiBase(BaseModel):
    code: str
    name: str

class GrntiCreate(GrntiBase):
    pass

class GrntiUpdate(GrntiBase):
    pass

class GrntiOut(GrntiBase):
    id: int

    class Config:
        from_attributes = True
