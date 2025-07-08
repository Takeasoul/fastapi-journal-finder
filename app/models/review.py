from sqlalchemy import Column, Integer, Enum, String, SmallInteger, ForeignKey
from sqlalchemy.orm import relationship

from app.core.base import Base
import enum

class ViewEnum(str, enum.Enum):
    double_blind = "1"   # двойное слепое рецензирование
    single_blind = "2"   # одностороннее слепое рецензирование
    open_review = "3"    # открытое рецензирование
    reviews_published = "4"  # рецензии открыто публикуются

class ReviewByEnum(str, enum.Enum):
    editorial_board_or_experts = "1"  # членами редколлегии или внешними экспертами
    editorial_board = "2"              # членами редакционной коллегии
    external_experts = "3"             # внешними экспертами, отобранными редакцией
    authors = "4"                     # рецензии предоставляются авторами
    editor_in_chief = "5"             # главным редактором

class Review(Base):
    __tablename__ = "review"

    pub_id = Column(Integer, ForeignKey("publication.id", onupdate="CASCADE", ondelete="CASCADE"), primary_key=True)
    view = Column(Enum(ViewEnum), nullable=True)
    review_count = Column(SmallInteger, nullable=True)
    rejected = Column(SmallInteger, nullable=True)
    period_pub = Column(String(15), nullable=True)
    review_by = Column(Enum(ReviewByEnum), nullable=True)

    publication = relationship("Publication", back_populates="review")
