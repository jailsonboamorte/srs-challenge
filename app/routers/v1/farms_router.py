from typing import Annotated

from fastapi import Body, APIRouter, HTTPException


from controllers.farms_controller import FarmsController
from routers.v1.payload_examples import save_farm_example
from routers.v1.schemas import PayloadResponseFarms, PayloadSaveFarms


router = APIRouter()
farms_ctrl = FarmsController()

router = APIRouter(
    prefix="/farms",
    tags=["farms"],
    # dependencies=[Depends(validate_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.get("/{id}")
async def get(id: str) -> PayloadResponseFarms:
    user = farms_ctrl.get(id)
    if user is None:
        raise HTTPException(status_code=404, detail="Farms not found")
    return user


@router.post("/{producer_id}")
async def save(
    producer_id: int,
    body: Annotated[
        PayloadSaveFarms,
        Body(openapi_examples=save_farm_example),
    ],
) -> PayloadResponseFarms:
    data = body.model_dump()
    data["producer_id"] = producer_id
    user = farms_ctrl.save(data)

    if user is None:
        raise HTTPException(status_code=404, detail="Farm not save")
    farm = farms_ctrl.get(user.id)
    return farm


# @router.put("/{id}")
# async def update(
#    id: str,
#    body: Annotated[PayloadSaveFarms, Body(openapi_examples=save_farm_example)],
# ):
#    data = body.model_dump()
#    user = farms_ctrl.update(id, data)
#
#    if user is None:
#        raise HTTPException(status_code=400, detail="Farm not updated")
