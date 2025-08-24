from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from constants import DATABASE_URL
from log import logger


class DB:
    session = None
    __instance = None
    engine = None

    def __init__(self) -> None:
        self.engine = create_engine(DATABASE_URL, echo=True)

    def get_session(self) -> Session:
        if self.session is None:
            self.create_session()

        return self.session

    def create_session(self) -> None:
        logger.warning("Session Created")
        self.session = Session(self.engine)

    def __del__(self):
        logger.warning("Session Closed")
        self.session.close()

    @staticmethod
    def create():
        if DB.__instance is None:
            DB.__instance = DB()

        return DB.__instance
