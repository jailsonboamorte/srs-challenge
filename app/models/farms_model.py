from models.model import Model
from models.tables import Farms
from sqlalchemy.orm import Session  # type: ignore
from log import logger
from helpers.exception import get_last_call


class FarmsModel(Model):
    def __init__(self, session: Session = None):
        super().__init__(session)

    def save(self: "FarmsModel", data: dict) -> Farms | None:
        try:
            object = self.id(Farms, data.get("id"))
            if object is None:
                object = Farms(
                    address_id=data.get("address_id"),
                    total_area=data.get("total_area"),
                    arable_area=data.get("arable_area"),
                    vegetation_area=data.get("vegetation_area"),
                )
            else:
                object.address_id = data.get("address_id")
                object.total_area = data.get("total_area")
                object.arable_area = data.get("arable_area")
                object.vegetation_area = data.get("vegetation_area")

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
