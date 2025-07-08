from pydantic import BaseModel

class RoleCreateRequest(BaseModel):
    name: str
    parent_id: int | None = None

class RoleResponse(BaseModel):
    id: int
    name: str
    parent_id: int | None = None

    class Config:
        from_attributes = True
