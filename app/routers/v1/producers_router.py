from typing import Annotated

from fastapi import Body, APIRouter, HTTPException


from controllers.producers_controller import ProducersController
from routers.v1.payload_examples import save_producer_example, update_producer_example
from routers.v1.schemas import (
    PayloadResponseProducer,
    PayloadSaveProducer,
    PayloadUpdateProducer,
)
from log import logger


router = APIRouter()
producer_ctrl = ProducersController()

router = APIRouter(
    prefix="/producers",
    tags=["producers"],
    # dependencies=[Depends(validate_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.get("/{id}")
async def get(id: str) -> PayloadResponseProducer:
    user = producer_ctrl.get(id)
    if user is None:
        raise HTTPException(status_code=404, detail="Producers not found")
    return user


@router.delete("/{id}")
async def delete(id: str):
    user = producer_ctrl.delete(id)
    if user is False:
        raise HTTPException(status_code=404, detail="Producers not found")
    return {}


@router.post("/")
async def save(
    body: Annotated[
        PayloadSaveProducer,
        Body(openapi_examples=save_producer_example),
    ],
) -> PayloadResponseProducer:
    data = body.model_dump()
    user = producer_ctrl.save(data)

    if user is None:
        raise HTTPException(status_code=404, detail="Producer not save")
    producer = producer_ctrl.get(user.id)
    return producer


@router.put("/{id}")
async def password(
    id: str,
    body: Annotated[
        PayloadUpdateProducer, Body(openapi_examples=update_producer_example)
    ],
):
    data = body.model_dump()
    user = producer_ctrl.update(id, data)

    if user is None:
        raise HTTPException(status_code=400, detail="Producer not updated")
