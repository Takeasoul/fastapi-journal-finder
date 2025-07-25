from sqlalchemy import Column, Integer, Enum, String, SmallInteger, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ENUM as SqlEnum  # Используем SqlEnum для настройки Enum

from app.core.base import Base
import enum


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

class Review(Base):
    __tablename__ = "review"

    pub_id = Column(Integer, ForeignKey("publication.id", onupdate="CASCADE", ondelete="CASCADE"), primary_key=True)
    view = Column(
        SqlEnum(ViewEnum, native_enum=False, create_type=False, values_callable=lambda obj: [e.value for e in obj]),
        nullable=True
    )
    review_count = Column(SmallInteger, nullable=True)
    rejected = Column(SmallInteger, nullable=True)
    period_pub = Column(String(15), nullable=True)
    review_by = Column(
        SqlEnum(ReviewByEnum, native_enum=False, create_type=False, values_callable=lambda obj: [e.value for e in obj]),
        nullable=True
    )

    publication = relationship("Publication", back_populates="review")
