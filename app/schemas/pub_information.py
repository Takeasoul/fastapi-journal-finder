from pydantic import BaseModel
from typing import Optional

class PubInformationBase(BaseModel):
    issn_print: Optional[str] = None
    issn_elect: Optional[str] = None
    issues_year: Optional[int] = None
    arts_issue: Optional[str] = None
    pages_issue: Optional[int] = None
    founding: Optional[str] = None
    release: Optional[str] = None
    el_archive: Optional[str] = None

class PubInformationCreate(PubInformationBase):
    pub_id: int

class PubInformationUpdate(PubInformationBase):
    issn_print: Optional[str] = None
    issn_elect: Optional[str] = None
    issues_year: Optional[int] = None
    arts_issue: Optional[str] = None
    pages_issue: Optional[int] = None
    founding: Optional[str] = None
    release: Optional[str] = None
    el_archive: Optional[str] = None

class PubInformationOut(PubInformationBase):
    pub_id: int

    class Config:
        from_attributes = True


class PubInformationResponse(BaseModel):
    issn_print: Optional[str] = None
    issn_elect: Optional[str] = None
    issues_year: Optional[int] = None
    arts_issue: Optional[str] = None
    pages_issue: Optional[int] = None
    founding: Optional[str] = None
    release: Optional[str] = None
    el_archive: Optional[str] = None

    class Config:
        from_attributes = True