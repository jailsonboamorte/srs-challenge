from models.model import Model
from models.tables import Producers
from sqlalchemy.orm import Session  # type: ignore
from log import logger
from helpers.exception import get_last_call


class ProducersModel(Model):
    def __init__(self, session: Session = None):
        super().__init__(session)

    def save(self: "ProducersModel", data: dict) -> Producers | None:
        try:
            object = self.get(Producers, data.get("id"))
            if object is None:
                object = Producers(status=data.get("status"), code=data.get("code"))

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
