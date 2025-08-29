from alembic.config import Config
from alembic import command
from log import logger
from models.basics import insert_basics


def run_migrations():
    alembic_cfg = Config("alembic.ini")
    logger.info("Starting up...")
    logger.info("run alembic upgrade head...")
    command.upgrade(alembic_cfg, "head")
    logger.warning("Shutting down...")


def init_db() -> None:
    run_migrations()
    insert_basics()
