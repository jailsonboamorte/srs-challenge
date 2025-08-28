from typing import Annotated

from fastapi import Body, APIRouter, HTTPException


from controllers.crops_controller import CropsController
from routers.v1.payload_examples import save_crop_example
from routers.v1.schemas import PayloadResponseCrops, PayloadSaveCrops
from log import logger


router = APIRouter()
crops_ctrl = CropsController()

router = APIRouter(
    prefix="/crops",
    tags=["crops"],
    # dependencies=[Depends(validate_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.get("/{id}")
async def get(id: str) -> PayloadResponseCrops:
    user = crops_ctrl.get(id)
    if user is None:
        raise HTTPException(status_code=404, detail="Crops not found")
    return user


@router.post("/{farm_id}")
async def save(
    farm_id: int,
    body: Annotated[
        PayloadSaveCrops,
        Body(openapi_examples=save_crop_example),
    ],
) -> PayloadResponseCrops:
    data = body.model_dump()
    data["farm_id"] = farm_id
    user = crops_ctrl.save(data)

    if user is None:
        raise HTTPException(status_code=404, detail="Crop not save")
    crop = crops_ctrl.get(user.id)
    logger.warning(crop)
    return crop


# @router.put("/{id}")
# async def update(
#    id: str,
#    body: Annotated[PayloadSaveCrops, Body(openapi_examples=save_crop_example)],
# ):
#    data = body.model_dump()
#    user = crops_ctrl.update(id, data)
#
#    if user is None:
#        raise HTTPException(status_code=400, detail="Crop not updated")
