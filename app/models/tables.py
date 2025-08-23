from sqlalchemy.orm import DeclarativeBase, mapped_column

from sqlalchemy import (
    Column,
    Enum,
    ForeignKey,
    Integer,
    String,
    text,
    TIMESTAMP,
    UniqueConstraint,
    func,
)
import enum


class Base(DeclarativeBase):
    id = mapped_column(Integer, primary_key=True, sort_order=-1)
    created_at = mapped_column(
        TIMESTAMP,
        server_default=func.now(),
        nullable=False,
        sort_order=100,
    )
    updated_at = mapped_column(
        TIMESTAMP,
        onupdate=func.now(),
        sort_order=101,
    )


class ModelStatusEnum(enum.Enum):
    canceled = "canceled"
    finished = "finished"
    started = "started"


class ModelCategoryEnum(enum.Enum):
    national = "national"
    international = "international"


class Producers(Base):
    __tablename__ = "producers"
    category = Column(Enum(ModelCategoryEnum))


class People(Base):
    __tablename__ = "people"
    __table_args__ = (UniqueConstraint("cpf", name="unique_cpf_idx"),)

    producer_id = Column(Integer, ForeignKey("producers.id"), nullable=False)
    name = Column(String(100), nullable=False)
    cpf = Column(String(20), nullable=False)


class Companies(Base):
    __tablename__ = "companies"
    __table_args__ = (UniqueConstraint("cnpj", name="unique_cnpj_idx"),)

    producer_id = Column(Integer, ForeignKey("producers.id"), nullable=False)
    fantasy_name = Column(String(100), nullable=False)
    cnpj = Column(String(20), nullable=False)
