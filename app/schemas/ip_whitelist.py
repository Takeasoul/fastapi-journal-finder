from pydantic import constr
from typing import Optional
from pydantic import BaseModel

class IPWhitelistCreate(BaseModel):
    ip_network: str
    organization_name: Optional[str] = None

class IPWhitelistUpdate(BaseModel):
    id: Optional[int] = None
    ip_network: Optional[str] = None
    organization_name: Optional[str] = None

class IPWhitelistResponse(BaseModel):
    id: int
    ip_network: str
    organization_name: Optional[str]

    class Config:
        orm_mode = True