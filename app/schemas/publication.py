from enum import Enum

from fastapi import Query
from pydantic import BaseModel
from typing import Optional, Set, List
from datetime import date

from app.schemas.actual_grnti import ActualGRNTIBase, ActualGRNTIResponse
from app.schemas.actual_oecd import ActualOECDBase, ActualOECDResponse
from app.schemas.index import IndexResponse
from app.schemas.main_section import MainSectionBase, MainSectionResponse
from app.schemas.pub_information import PubInformationResponse


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

class PublicationBase(BaseModel):
    el_id: int
    vak_id: Optional[int] = None
    name: str
    serial_type: SerialTypeEnum11
    serial_elem: Optional[SerialElemEnum] = None
    purpose: Optional[PurposeEnum] = None
    distribution: Optional[DistributionEnum] = None
    access: Optional[AccessEnum] = None
    main_finance: Optional[MainFinanceEnum] = None
    multidisc: MultidiscEnum
    language: Optional[Set[LanguageEnum]] = None
    el_updated_at: Optional[date] = None

class PublicationCreate(PublicationBase):
    pass

class PublicationUpdate(PublicationBase):
    el_id: int = None
    vak_id: Optional[int] = None
    name: str = None
    serial_type: SerialTypeEnum11 = None
    serial_elem: Optional[SerialElemEnum] = None
    purpose: Optional[PurposeEnum] = None
    distribution: Optional[DistributionEnum] = None
    access: Optional[AccessEnum] = None
    main_finance: Optional[MainFinanceEnum] = None
    multidisc: MultidiscEnum = None
    language: Optional[Set[LanguageEnum]] = None
    el_updated_at: Optional[date] = None

class PublicationOut(BaseModel):
    id: int
    el_id: Optional[int] = None
    vak_id: Optional[int] = None
    name: Optional[str] = None
    serial_type: Optional[str]
    serial_elem: Optional[str] = None
    purpose: Optional[str] = None
    distribution: Optional[str] = None
    access: Optional[str] = None
    main_finance: Optional[str] = None
    multidisc: Optional[str] = None
    language: Optional[List[str]] = None
    el_updated_at: Optional[date] = None
    actual_oecd_items: Optional[List[ActualOECDResponse]] = None
    actual_grnti_items: Optional[List[ActualGRNTIResponse]] = None
    main_sections: Optional[List[MainSectionResponse]] = None
    class Config:
        from_attributes = True

class PublicationResponse(BaseModel):
    id: int  # Обязательное поле
    el_id: Optional[int] = None  # Может быть None
    vak_id: Optional[int] = None  # Может быть None
    name: Optional[str] = None  # Может быть None
    serial_type: Optional[str] = None  # Может быть None
    serial_elem: Optional[str] = None  # Может быть None
    purpose: Optional[str] = None  # Может быть None
    distribution: Optional[str] = None  # Может быть None
    access: Optional[str] = None  # Может быть None
    main_finance: Optional[str] = None  # Может быть None
    multidisc: Optional[str] = None  # Может быть None
    language: Optional[List[str]] = None  # Может быть None
    el_updated_at: Optional[date] = None  # Может быть None
    class Config:
        from_attributes = True

class PublicationResponseWith(BaseModel):
    id: int
    el_id: Optional[int] = None
    vak_id: Optional[int] = None
    name: Optional[str] = None
    serial_type: Optional[str] = None
    serial_elem: Optional[str] = None
    purpose: Optional[str] = None
    distribution: Optional[str] = None
    access: Optional[str] = None
    main_finance: Optional[str] = None
    multidisc: Optional[str] = None
    language: Optional[List[str]] = None
    el_updated_at: Optional[date] = None

    actual_oecd_items: List[ActualOECDResponse] = []
    actual_grnti_items: List[ActualGRNTIResponse] = []
    main_sections: List[MainSectionResponse] = []

    pub_information: Optional[PubInformationResponse] = None
    index: Optional[IndexResponse] = None

    class Config:
        from_attributes = True

class PaginatedResponse(BaseModel):
    items: List[PublicationResponse]
    total: int
    page: int
    per_page: int
    total_pages: int

class PaginatedResponseWith(BaseModel):
    items: List[PublicationResponseWith]
    total: int
    page: int
    per_page: int
    total_pages: int

class PublicationFilter(BaseModel):
    el_id: Optional[int] = None
    vak_id: Optional[int] = None
    name: Optional[str] = None
    serial_type: Optional[SerialTypeEnum11] = None
    serial_elem: Optional[SerialElemEnum] = None
    purpose: Optional[PurposeEnum] = None
    distribution: Optional[DistributionEnum] = None
    access: Optional[AccessEnum] = None
    main_finance: Optional[MainFinanceEnum] = None
    multidisc: Optional[MultidiscEnum] = None
    languages: Optional[Set[LanguageEnum]] = None
    el_updated_at_from: Optional[date] = None
    el_updated_at_to: Optional[date] = None

class PublicationFilterWithSpec(BaseModel):
    el_id: Optional[int] = None
    vak_id: Optional[int] = None
    name: Optional[str] = None
    serial_type: Optional[SerialTypeEnum11] = None
    serial_elem: Optional[SerialElemEnum] = None
    purpose: Optional[PurposeEnum] = None
    distribution: Optional[DistributionEnum] = None
    access: Optional[AccessEnum] = None
    main_finance: Optional[MainFinanceEnum] = None
    multidisc: Optional[MultidiscEnum] = None
    languages: Optional[Set[LanguageEnum]] = None
    el_updated_at_from: Optional[date] = None
    el_updated_at_to: Optional[date] = None
    actual_specialty: Optional[List[int]] = Query(None, alias="actual_specialty")
