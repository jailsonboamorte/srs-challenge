from models.model import Model
from models.tables import People
from sqlalchemy.orm import Session  # type: ignore
from log import logger
from helpers.exception import get_last_call
from helpers.validation import validate_cpf


class PeopleModel(Model):
    def __init__(self, session: Session = None):
        super().__init__(session)

    def save(self: "PeopleModel", data: dict) -> People | None:
        try:
            object = self.get_by_producer_id(People, data.get("producer_id"))
            if validate_cpf(data.get("cpf")) is False:
                return None

            if object is None:
                object = People(
                    producer_id=data.get("producer_id"),
                    cpf=data.get("cpf"),
                    name=data.get("name"),
                )
            else:
                object.cpf = data.get("cpf")
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
