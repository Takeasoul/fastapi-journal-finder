from pydantic import BaseModel


class EduLevelBase(BaseModel):
    name: str


class EduLevelCreate(EduLevelBase):
    pass


class EduLevelUpdate(EduLevelBase):
    pass


class EduLevelOut(EduLevelBase):
    id: int

    class Config:
        from_attributes = True
