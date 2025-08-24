from models.model import Model
from models.tables import AddressesProducers
from sqlalchemy.orm import Session  # type: ignore
from log import logger
from helpers.exception import get_last_call


class AddressesProducersModel(Model):
    def __init__(self, session: Session = None):
        super().__init__(session)

    def save(self: "AddressesProducersModel", data: dict) -> AddressesProducers | None:
        try:
            object = self.get_by_producer_id(
                AddressesProducers, data.get("producer_id")
            )
            if object is None:
                object = AddressesProducers(
                    address_id=data.get("address_id"),
                    producer_id=data.get("producer_id"),
                )
            else:
                object.address_id = data.get("address_id")
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
