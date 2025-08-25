from models.model import Model
from models.tables import Addresses
from sqlalchemy.orm import Session  # type: ignore
from log import logger
from helpers.exception import get_last_call


class AddressesModel(Model):
    def __init__(self, session: Session = None):
        super().__init__(session)

    def save(self: "AddressesModel", data: dict) -> Addresses | None:
        try:
            object = self.get(Addresses, data.get("id"))
            if object is None:
                object = Addresses(
                    state=data.get("state"),
                    city=data.get("city"),
                    zip_code=data.get("zip_code"),
                )
            else:
                object.state = data.get("state")
                object.city = data.get("city")
                object.zip_code = data.get("zip_code")

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
