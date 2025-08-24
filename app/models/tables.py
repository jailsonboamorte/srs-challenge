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


class ModelStateEnum(enum.Enum):
    AC = "Acre"
    AL = "Alagoas"
    AP = "Amapá"
    AM = "Amazonas"
    BA = "Bahia"
    CE = "Ceará"
    DF = "Distrito Federal"
    ES = "Espírito Santo"
    GO = "Goiás"
    MA = "Maranhão"
    MT = "Mato Grosso"
    MS = "Mato Grosso do Sul"
    MG = "Minas Gerais"
    PA = "Pará"
    PB = "Paraíba"
    PR = "Paraná"
    PE = "Pernambuco"
    PI = "Piauí"
    RJ = "Rio de Janeiro"
    RN = "Rio Grande do Norte"
    RS = "Rio Grande do Sul"
    RO = "Rondônia"
    RR = "Roraima"
    SC = "Santa Catarina"
    SP = "São Paulo"
    SE = "Sergipe"
    TO = "Tocantins"


class ModelCityEnum(enum.Enum):
    RIO_BRANCO = "Rio Branco"  # AC
    MACEIO = "Maceió"  # AL
    MACAPA = "Macapá"  # AP
    MANAUS = "Manaus"  # AM
    SALVADOR = "Salvador"  # BA
    FORTALEZA = "Fortaleza"  # CE
    BRASILIA = "Brasília"  # DF
    VITORIA = "Vitória"  # ES
    GOIANIA = "Goiânia"  # GO
    SAO_LUIS = "São Luís"  # MA
    CUIABA = "Cuiabá"  # MT
    CAMPO_GRANDE = "Campo Grande"  # MS
    BELO_HORIZONTE = "Belo Horizonte"  # MG
    BELEM = "Belém"  # PA
    JOAO_PESSOA = "João Pessoa"  # PB
    CURITIBA = "Curitiba"  # PR
    RECIFE = "Recife"  # PE
    TERESINA = "Teresina"  # PI
    RIO_DE_JANEIRO = "Rio de Janeiro"  # RJ
    NATAL = "Natal"  # RN
    PORTO_ALEGRE = "Porto Alegre"  # RS
    PORTO_VELHO = "Porto Velho"  # RO
    BOA_VISTA = "Boa Vista"  # RR
    FLORIANOPOLIS = "Florianópolis"  # SC
    SAO_PAULO = "São Paulo"  # SP
    ARACAJU = "Aracaju"  # SE
    PALMAS = "Palmas"  # TO


class Producers(Base):
    __tablename__ = "producers"
    category = Column(
        Enum(ModelCategoryEnum), nullable=False, server_default="national"
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

    state = Column(Enum(ModelStateEnum), nullable=False)
    city = Column(Enum(ModelCityEnum), nullable=False)
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
    arabel_area = Column(Integer, nullable=False, comment="Área agricultável")
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
    __table_args__ = (
        UniqueConstraint("farm_id", "harvest_id", name="unique_farm_id_harvest_id_idx"),
    )

    farm_id = Column(Integer, ForeignKey("farms.id"), nullable=False)
    harvest_id = Column(Integer, ForeignKey("harvests.id"), nullable=False)
    arabel_area = Column(Integer, nullable=False, comment="Área agricultável")
    status = Column(Enum(ModelStatusEnum), nullable=False)


# op.execute('DROP TYPE IF EXISTS modelcategoryenum;')
