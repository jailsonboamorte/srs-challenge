from sqlalchemy.orm import Session  # type: ignore
from models.producers_model import ProducersModel
from models.companies_model import CompaniesModel
from models.people_model import PeopleModel
from models.tables import Producers, Companies, People
from log import logger
from helpers.exception import get_last_call


class ProducersController:
    def update(
        self: "ProducersController", id: int, data: dict
    ) -> ProducersModel | None:
        if id is None:
            return None

        producers_model = ProducersModel()
        try:
            data["id"] = id
            producer = producers_model.save(data)
            producers_model.session.commit()
            return producer

        except Exception as e:
            producers_model.session.rollback()
            logger.error(
                "Fail on {}.{}: ({})".format(
                    self.__class__.__name__, get_last_call(), e
                )
            )
        return None

    def _save_data(
        self: "ProducersController",
        data: dict,
        producer_id: int,
        session: Session = None,
    ) -> bool:
        type = data.get("type")
        if type == "PJ":
            company_model = CompaniesModel(session)
            data["company"]["producer_id"] = producer_id
            return isinstance(company_model.save(data["company"]), Companies)
        elif type == "PF":
            people_model = PeopleModel(session)
            data["person"]["producer_id"] = producer_id
            return isinstance(people_model.save(data["person"]), People)

        return False

    def save(self: "ProducersController", data: dict) -> Producers | None:
        producers_model = ProducersModel()
        session = producers_model.session
        try:
            producer = producers_model.save(data)
            if isinstance(producer, Producers):
                if self._save_data(data, producer.id, session):
                    producers_model.session.commit()
                    return producer
        except Exception as e:
            producers_model.session.rollback()
            logger.error(
                "Fail on {}.{}: ({})".format(
                    self.__class__.__name__, get_last_call(), e
                )
            )
        return None

    def sanitizer(self, producers: Producers) -> dict:
        if producers is None:
            return {}

        id = producers.__dict__.get("id")
        code = producers.__dict__.get("code")
        status = producers.__dict__.get("status")
        model = ProducersModel()
        people = model.get_by_producer_id(People, id)
        data = {"id": id, "code": code, "status": status.value}

        if people is not None:
            _data = people.__dict__
            data["person"] = {"name": _data.get("name"), "cpf": _data.get("cpf")}

        companies = model.get_by_producer_id(Companies, id)
        if companies is not None:
            _data = companies.__dict__
            data["company"] = {
                "fantasy_name": _data.get("fantasy_name"),
                "cnpj": _data.get("cnpj"),
            }

        return data

    def get(self, id: int) -> ProducersModel | None:
        try:
            model = ProducersModel()
            return self.sanitizer(model.get(Producers, id))
        except Exception as e:
            logger.error(
                "Fail on {}.{}: ({})".format(
                    self.__class__.__name__, get_last_call(), e
                )
            )
            return None

    def get_by_producer_id(self, producer_id: int) -> list[ProducersModel] | None:
        try:
            model = ProducersModel()

            records = model.get_by_producer_id(Producers, producer_id)
            return self.sanitizer(records)
        except Exception as e:
            logger.error(
                "Fail on {}.{}: ({})".format(
                    self.__class__.__name__, get_last_call(), e
                )
            )

    def delete(self, id: int) -> ProducersModel | None:
        try:
            model = ProducersModel()
            producers = model.delete(Producers, id)
            model.session.commit()
            return producers
        except Exception as e:
            logger.error(
                "Fail on {}.{}: ({})".format(
                    self.__class__.__name__, get_last_call(), e
                )
            )
            return False
