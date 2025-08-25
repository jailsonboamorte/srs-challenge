from models.model import Model
from models.tables import Crops
from sqlalchemy.orm import Session  # type: ignore
from log import logger
from helpers.exception import get_last_call


class CropsModel(Model):
    def __init__(self, session: Session = None):
        super().__init__(session)

    def save(self: "CropsModel", data: dict) -> Crops | None:
        try:
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
