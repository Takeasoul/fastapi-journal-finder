from sqlalchemy import Column, Integer, String, Text, Enum
from sqlalchemy.dialects.mysql import SET, TINYTEXT, VARCHAR
from app.core.base import Base
from app.models.publication import LanguageEnum


class PublicationBaseInfo(Base):
    __tablename__ = "publication_base_info"  # имя в базе (VIEW)

    name = Column("Наименование", VARCHAR(255), primary_key=True)  # ключа в VIEW нет, возьмём name как pk
    issn = Column("ISSN (печ/эл)", VARCHAR(19), nullable=False)
    directions = Column("Направления", Text, nullable=True)
    site = Column("Сайт", VARCHAR(255), nullable=True)
    periodicity = Column("Периодичность", Integer, nullable=True)  # tinyint -> Integer
    languages = Column("Языки", SET(LanguageEnum), nullable=False)
    email = Column("Почта", VARCHAR(45), nullable=True)
    phone = Column("Телефон", VARCHAR(20), nullable=True)
    review_period = Column("Срок рецензирования", VARCHAR(15), nullable=True)
    sections = Column("Разделы", Text, nullable=True)
    vak_category = Column("Категория ВАК", Enum("нет","1","2","3"), nullable=True)