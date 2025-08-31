import enum

from pydantic import BaseModel, constr
from typing import Optional
from enum import Enum

class ViewEnum(str, enum.Enum):
    double_blind = "двойное слепое рецензирование"
    single_blind = "одностороннее слепое рецензирование"
    open_review = "открытое рецензирование"
    reviews_published = "рецензии открыто публикуются"

class ReviewByEnum(str, enum.Enum):
    editorial_board_or_experts = "членами редколлегии или внешними экспертами"
    editorial_board = "членами редакционной коллегии"
    external_experts = "внешними экспертами, отобранными редакцией"
    authors = "рецензии предоставляются авторами"
    editor_in_chief = "главным редактором"

class ReviewBase(BaseModel):
    pub_id: int
    view: Optional[ViewEnum] = None
    review_count: Optional[str] = None
    rejected: Optional[int] = None
    period_pub: Optional[constr(max_length=15)] = None
    review_by: Optional[ReviewByEnum] = None

class ReviewCreate(ReviewBase):
    pass

class ReviewUpdate(ReviewBase):
    pub_id: Optional[int] = None
    view: Optional[ViewEnum] = None
    review_count: Optional[str] = None
    rejected: Optional[int] = None
    period_pub: Optional[constr(max_length=15)] = None
    review_by: Optional[ReviewByEnum] = None

class ReviewOut(ReviewBase):
    class Config:
        from_attributes = True
