from pydantic import BaseModel
from typing import Optional
from typing import Annotated, Optional, Union
from fastapi import FastAPI, Body


class PayloadPerson(BaseModel):
    name: str
    cpf: str


class PayloadCompany(BaseModel):
    fantasy_name: str
    cnpj: str


class PayloadAddress(BaseModel):
    state: str
    city: str
    zip_code: str


class PayloadHarvests(BaseModel):
    id: int
    name: str


class PayloadCrops(BaseModel):
    name: str
    harvest_id: int
    arable_area: int


class PayloadSaveProducer(BaseModel):
    code: str
    type: str

    person: Annotated[Optional[PayloadPerson], Body(embed=True)] = None
    company: Annotated[Optional[PayloadCompany], Body(embed=True)] = None

    def model_post_init(self, __context):
        if self.person is not None and self.company is not None:
            raise ValueError("Only one of 'person' or 'company' can be provided.")
        if self.person is None and self.company is None:
            raise ValueError("At least one of 'person' or 'company' must be provided.")


class PayloadUpdateProducer(BaseModel):
    code: str
    person: Annotated[Optional[PayloadPerson], Body(embed=True)] = None
    company: Annotated[Optional[PayloadCompany], Body(embed=True)] = None

    def model_post_init(self, __context):
        if self.person is not None and self.company is not None:
            raise ValueError("Only one of 'person' or 'company' can be provided.")
        if self.person is None and self.company is None:
            raise ValueError("At least one of 'person' or 'company' must be provided.")


class PayloadResponseProducer(BaseModel):
    id: int
    code: str
    status: str
    person: Annotated[Optional[PayloadPerson], Body(embed=True)] = None
    company: Annotated[Optional[PayloadCompany], Body(embed=True)] = None


class PayloadSaveFarms(BaseModel):
    name: str
    total_area: int
    arable_area: int
    vegetation_area: int
    address: PayloadAddress


class PayloadResponseFarms(BaseModel):
    id: int
    name: str
    total_area: int
    arable_area: int
    vegetation_area: int
    address: PayloadAddress


class PayloadResponseCrops(BaseModel):
    id: int
    farm_id: int
    arable_area: int
    address: PayloadAddress
    harvest: PayloadHarvests
