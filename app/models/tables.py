from sqlalchemy.orm import DeclarativeBase, mapped_column

from sqlalchemy import (
    Column,
    Enum,
    ForeignKey,
    Integer,
    String,
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


class ModelCropsStatusEnum(enum.Enum):
    canceled = "canceled"
    finished = "finished"
    started = "started"


class ModelProducersStatusEnum(enum.Enum):
    active = "active"
    inactive = "inactive"


class Producers(Base):
    __tablename__ = "producers"
    __table_args__ = (UniqueConstraint("code", name="unique_code_idx"),)

    code = Column(String(100), nullable=False)
    status = Column(
        Enum(ModelProducersStatusEnum), nullable=False, server_default="active"
    )


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


class Addresses(Base):
    __tablename__ = "addresses"

    state = Column(String(20), nullable=False)
    city = Column(String(20), nullable=False)
    zip_code = Column(String(15), nullable=False)


class Harvests(Base):
    __tablename__ = "harvests"
    __table_args__ = (UniqueConstraint("name", name="unique_harvest_name_idx"),)

    name = Column(String(30), nullable=False)
    description = Column(String(150), nullable=False)


class AddressesProducers(Base):
    __tablename__ = "addresses_producers"
    __table_args__ = (
        UniqueConstraint(
            "address_id", "producer_id", name="unique_address_id_producer_id"
        ),
    )

    address_id = Column(Integer, ForeignKey("addresses.id"), nullable=False)
    producer_id = Column(Integer, ForeignKey("producers.id"), nullable=False)


class Farms(Base):
    __tablename__ = "farms"

    address_id = Column(Integer, ForeignKey("addresses.id"), nullable=False)
    name = Column(String(150), nullable=False)
    total_area = Column(Integer, nullable=False, comment="Área total da fazenda")
    arable_area = Column(Integer, nullable=False, comment="Área agricultável")
    vegetation_area = Column(Integer, nullable=False, comment="Área de vegetação")


class FarmsProducers(Base):
    __tablename__ = "farms_producers"
    __table_args__ = (
        UniqueConstraint(
            "farm_id", "producer_id", name="unique_farm_id_producer_id_idx"
        ),
    )

    farm_id = Column(Integer, ForeignKey("farms.id"), nullable=False)
    producer_id = Column(Integer, ForeignKey("producers.id"), nullable=False)


class Crops(Base):
    __tablename__ = "crops"

    farm_id = Column(Integer, ForeignKey("farms.id"), nullable=False)
    harvest_id = Column(Integer, ForeignKey("harvests.id"), nullable=False)
    arable_area = Column(Integer, nullable=False, comment="Área agricultável")
    status = Column(Enum(ModelCropsStatusEnum), nullable=False, default="started")


# op.execute('DROP TYPE IF EXISTS modelcategoryenum;')
