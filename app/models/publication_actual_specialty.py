import enum

from sqlalchemy import Column, Integer, Boolean, ForeignKey, Date, Enum as SqlEnum, SmallInteger, VARCHAR, String

from app.core.base import Base


class SourceEnum(enum.Enum):
    elib = "elib"
    vak = "вак"

class PublicationActualSpecialty(Base):
    __tablename__ = "publication_actual_specialty"  # имя VIEW в БД

    name = Column("Наименование", String(255), primary_key=True)  # pk нет, выбираем name
    issn = Column("ISSN (печ/эл)", VARCHAR(19), nullable=False)
    specialty_name = Column("Наименование специальности", VARCHAR(170), nullable=True)
    source = Column("Источник",SqlEnum(SourceEnum, native_enum=False, create_type=False, values_callable=lambda obj: [e.value for e in obj]), nullable=False)
    actual_flag = Column("Признак актуальности", SmallInteger, nullable=False)
    inclusion_date = Column("Дата включения в перечень", String(10), nullable=True)
    exclusion_date = Column("Дата исключения из перечня", String(10), nullable=True)
