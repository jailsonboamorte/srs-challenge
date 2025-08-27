from models.model import Model
from models.tables import Crops, Farms
from sqlalchemy.orm import Session  # type: ignore
from log import logger
from helpers.exception import get_last_call
from sqlalchemy import and_, func


class CropsModel(Model):
    def __init__(self, session: Session = None):
        super().__init__(session)

    def _get_area_occuped(self: "CropsModel", farm_id):
        conditions = and_(Crops.farm_id == farm_id, Crops.status == "started")
        area_occuped = (
            self.session.query(func.sum(getattr(Crops, "arable_area")))
            .filter(conditions)
            .scalar()
        )
        return area_occuped if area_occuped else 0

    def has_available_area(self: "CropsModel", farm_id: int, desired_area: int) -> bool:
        area_occuped = self._get_area_occuped(farm_id)
        farm = self.session.get(Farms, farm_id)
        logger.warning(
            "farm.total_area: %s vegetation_area: %s  area_occuped: %s desired_area: %s",
            farm.total_area,
            farm.vegetation_area,
            area_occuped,
            desired_area,
        )
        return (farm.total_area - farm.vegetation_area) >= (area_occuped + desired_area)

    def save(self: "CropsModel", data: dict) -> Crops | None:
        try:
            if not self.has_available_area(
                data.get("farm_id"), data.get("arable_area")
            ):
                logger.warning("No area available")
                return None

            object = self.get(Crops, data.get("id"))
            if object is None:
                object = Crops(
                    farm_id=data.get("farm_id"),
                    harvest_id=data.get("harvest_id"),
                    arable_area=data.get("arable_area"),
                    status=data.get("status"),
                )
            else:
                object.farm_id = data.get("farm_id")
                object.harvest_id = data.get("harvest_id")
                object.arable_area = data.get("arable_area")
                object.status = data.get("status")

            self.session.add(object)
            self.session.flush()

            return object

        except Exception as e:
            self.session.rollback()
            logger.error(
                "Fail on {}.{}: ({})".format(
                    self.__class__.__name__, get_last_call(), e
                )
            )
            return None
