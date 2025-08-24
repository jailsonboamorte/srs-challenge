from models.model import Model
from models.tables import FarmsProducers
from sqlalchemy.orm import Session  # type: ignore
from log import logger
from helpers.exception import get_last_call


class FarmsProducersModel(Model):
    def __init__(self, session: Session = None):
        super().__init__(session)

    def save(self: "FarmsProducersModel", data: dict) -> FarmsProducers | None:
        try:
            object = self.get_by_producer_id(FarmsProducers, data.get("producer_id"))
            if object is None:
                object = FarmsProducers(
                    farm_id=data.get("farm_id"),
                    producer_id=data.get("producer_id"),
                )
            else:
                object.farm_id = data.get("farm_id")
                object.producer_id = data.get("producer_id")

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
