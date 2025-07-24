from pydantic import constr
from typing import Optional
from pydantic import BaseModel

class IPWhitelistCreate(BaseModel):
    ip_network: str
    organization_name: Optional[str] = None

class IPWhitelistUpdate(BaseModel):
    organization_name: str

class IPWhitelistResponse(BaseModel):
    id: int
    ip_network: str
    organization_name: Optional[str]

    class Config:
        orm_mode = True