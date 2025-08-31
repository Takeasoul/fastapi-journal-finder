from pydantic import BaseModel


class EduLevelBase(BaseModel):
    name: str


class EduLevelCreate(EduLevelBase):
    pass


class EduLevelUpdate(EduLevelBase):
    pass


class EduLevelOut(BaseModel):
    id: int
    name: str = None

    class Config:
        from_attributes = True
