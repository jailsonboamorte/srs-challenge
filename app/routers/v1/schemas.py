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
