from typing import Optional

from pydantic import BaseModel

class RoleRequest(BaseModel):
    name: str
    parent_id: int | None = None

class RoleResponse(BaseModel):
    id: int
    name: Optional[str]
    parent_id: Optional[int] | None = None

    class Config:
        from_attributes = True
