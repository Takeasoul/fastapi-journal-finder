from enum import Enum

from sqlalchemy import Column, Integer, Text, Enum as SqlEnum, Date
from sqlalchemy.dialects.mysql import SET
from sqlalchemy.orm import relationship
from app.core.base import Base

class SerialTypeEnum11(str, Enum):
    PERIODIC = "периодическое издание"

class SerialElemEnum(str, Enum):
    ISSUE = "выпуск журнала"
    ARTICLE_COLLECTION = "сборник статей"

class PurposeEnum(str, Enum):
    SCIENTIFIC = "научное"

class DistributionEnum(str, Enum):
    PRINT_ONLY = "только в печатном виде"
    ELECTRONIC_ONLY = "только в электронном виде"
    PRINT_AND_ELECTRONIC = "в печатном и электронном виде"

class AccessEnum(str, Enum):
    ALL_OPEN = "все выпуски в открытом доступе"
    ALL_PAID = "все выпуски в платном доступе"
    CURRENT_PAID_ARCHIVE_OPEN = "текущие выпуски в платном доступе, архивные выпуски - в открытом"
    OPEN_SOME_ARTICLES = "в открытом доступе отдельные статьи"

class MainFinanceEnum(str, Enum):
    SUBSCRIPTION = "подписка"
    FOUNDER = "учредитель"
    AUTHORS_PAYMENTS = "платежи авторов"
    SPONSOR = "спонсор"
    ADVERTISING = "реклама"
    BUDGET = "госбюджет"
    GRANTS = "гранты"

class MultidiscEnum(str, Enum):
    NOT_MULTIDISC = "не является мультидисциплинарным"
    ALL_SCIENCES = "мультидисциплинарный по всем научным направлениям"
    SOC_HUM = "мультидисциплинарный в области общественных и гуманитарных наук"
    NAT_TECH = "мультидисциплинарный в области естественных и технических наук"
    
class LanguageEnum(str, Enum):
    russian = "русский"
    english = "английский"
    german = "немецкий"
    french = "французский"
    spanish = "испанский"
    japanese = "японский"
    chinese = "китайский"
    ukrainian = "украинский"
    azerbaijani = "азербайджанский"
    bulgarian = "болгарский"
    belarusian = "белорусский"
    tajik = "таджикский"
    kazakh = "казахский"
    italian = "итальянский"
    macedonian = "македонский"
    polish = "польский"
class Publication(Base):
    __tablename__ = "publication"

    id = Column(Integer, primary_key=True)
    el_id = Column(Integer, nullable=False)
    vak_id = Column(Integer, nullable=True)
    name = Column(Text, nullable=False)

    serial_type = Column(SqlEnum(SerialTypeEnum11, native_enum=False, create_type=False, values_callable=lambda obj: [e.value for e in obj]), nullable=False)
    serial_elem = Column(SqlEnum(SerialElemEnum, native_enum=False, create_type=False, values_callable=lambda obj: [e.value for e in obj]), nullable=True)
    purpose = Column(SqlEnum(PurposeEnum, native_enum=False, create_type=False, values_callable=lambda obj: [e.value for e in obj]), nullable=True)
    distribution = Column(SqlEnum(DistributionEnum, native_enum=False, create_type=False, values_callable=lambda obj: [e.value for e in obj]), nullable=True)
    access = Column(SqlEnum(AccessEnum, native_enum=False, create_type=False, values_callable=lambda obj: [e.value for e in obj]), nullable=True)
    main_finance = Column(SqlEnum(MainFinanceEnum, native_enum=False, create_type=False, values_callable=lambda obj: [e.value for e in obj]), nullable=True)
    multidisc = Column(SqlEnum(MultidiscEnum, native_enum=False, create_type=False, values_callable=lambda obj: [e.value for e in obj]), nullable=False)

    language = Column(SET(LanguageEnum), nullable=True)

    el_updated_at = Column(Date, nullable=True)

    # связи
    actual_oecd_items = relationship("ActualOECD", back_populates="publication")
    actual_grnti_items = relationship("ActualGRNTI", back_populates="publication")
    actual_specialties = relationship("ActualSpecialty", back_populates="publication")
    main_sections = relationship("MainSection", back_populates="publication")
    contact = relationship("Contact", back_populates="publication", uselist=False)
    pub_information = relationship("PubInformation", back_populates="publication", uselist=False)
    index = relationship("Index", uselist=False, back_populates="publication")
    review = relationship("Review", uselist=False, back_populates="publication")
    journals = relationship("Journal", back_populates="publication", cascade="all, delete-orphan")
