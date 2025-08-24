from models.model import Model
from models.tables import Companies
from sqlalchemy.orm import Session  # type: ignore
from log import logger
from helpers.exception import get_last_call


class CompaniesModel(Model):
    def __init__(self, session: Session = None):
        super().__init__(session)

    def _validate_cnpj(self: "CompaniesModel", cnpj: dict):
        pass

    def save(self: "CompaniesModel", data: dict) -> Companies | None:
        try:
            object = self.get_by_producer_id(Companies, data.get("producer_id"))
            if object is None:
                object = Companies(
                    producer_id=data.get("producer_id"),
                    cnpj=data.get("cnpj"),
                    fantasy_name=data.get("fantasy_name"),
                )
            else:
                object.cpf = data.get("cpf")
                object.fantasy_name = data.get("fantasy_name")

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
