from pydantic import BaseModel, constr
from typing import Optional
from enum import Enum

class ViewEnum(str, Enum):
    double_blind = "двойное слепое рецензирование"  # двойное слепое рецензирование
    single_blind = "одностороннее слепое рецензирование"  # одностороннее слепое рецензирование
    open_review = "открытое рецензирование"  # открытое рецензирование
    reviews_published = "рецензии открыто публикуются"  # рецензии открыто публикуются

class ReviewByEnum(str, Enum):
    editorial_board_or_experts = "членами редколлегии или внешними экспертами"  # членами редколлегии или внешними экспертами
    editorial_board = "членами редакционной коллегии"  # членами редакционной коллегии
    external_experts = "внешними экспертами, отобранными редакцией"  # внешними экспертами, отобранными редакцией
    authors = "рецензии предоставляются авторами"  # рецензии предоставляются авторами
    editor_in_chief = "главным редактором"  # главным редактором

class ReviewBase(BaseModel):
    pub_id: int
    view: Optional[ViewEnum] = None
    review_count: Optional[int] = None
    rejected: Optional[int] = None
    period_pub: Optional[constr(max_length=15)] = None
    review_by: Optional[ReviewByEnum] = None

class ReviewCreate(ReviewBase):
    pass

class ReviewUpdate(ReviewBase):
    pass

class ReviewOut(ReviewBase):
    class Config:
        from_attributes = True
