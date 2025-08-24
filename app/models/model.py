from sqlalchemy.orm import Session

from helpers.exception import get_last_call
from log import logger
from models.db import DB
from models.tables import Base

db = DB.create()


class Model:
    session = None

    def __init__(self, session: Session = None) -> None:
        if session:
            self.session = session
        else:
            self.session = db.get_session()

    def get(self, table: Base, id: int) -> Base | None:
        try:
            if id is None:
                return None
            object = self.session.get(table, id)
            return object

        except Exception as e:
            logger.error(
                "Fail on {}.{}: ({})".format(
                    self.__class__.__name__, get_last_call(), e
                )
            )
            return None

    def get_by_producer_id(self, table: Base, producer_id: int) -> Base | None:
        try:
            if id is None:
                return None
            object = (
                self.session.query(table).filter(table.producer_id == producer_id).one()
            )

            return object

        except Exception as e:
            logger.error(
                "Fail on {}.{}: ({})".format(
                    self.__class__.__name__, get_last_call(), e
                )
            )
            return None

    def delete(self, table: Base, id: int, status="inactive") -> Base | None:
        try:
            object = self.session.get(table, id)
            if object:
                object.status = status
                self.session.flush()
                return object
            return None
        except Exception as e:
            logger.error(
                "Fail on {}.{}: ({})".format(
                    self.__class__.__name__, get_last_call(), e
                )
            )
            return None
