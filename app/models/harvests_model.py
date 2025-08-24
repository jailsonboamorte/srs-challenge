from models.model import Model
from models.tables import Harvests
from sqlalchemy.orm import Session  # type: ignore
from log import logger
from helpers.exception import get_last_call


class HarvestsModel(Model):
    def __init__(self, session: Session = None):
        super().__init__(session)

    def save(self: "HarvestsModel", data: dict) -> Harvests | None:
        try:
            object = self.get(Harvests, data.get("id"))
            if object is None:
                object = Harvests(name=data.get("name"))

            object.name = data.get("name")

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
