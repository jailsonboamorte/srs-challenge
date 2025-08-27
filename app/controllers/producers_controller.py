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

            if (
                self.save_store_content(
                    self.bucket_name,
                    self.path_name,
                    producer.id,
                    data.get("producer"),
                )
            ) is True:
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

    def sanitizer(self, producers: ProducersModel) -> dict:
        if producers is None:
            return {}

        id = producers.__dict__.get("id")
        code = producers.__dict__.get("code")
        status = producers.__dict__.get("status")

        people = producers.get_by_producer_id(People, id)
        if people is not None:
            data = people.__dict__
            person = {"name": data.get("name"), "cpf": data.get("cpf")}

        company = producers.get_by_producer_id(Companies, id)
        if company is not None:
            data = company.__dict__
            person = {
                "fantasy_name": data.get("fantasy_name"),
                "cnpj": data.get("cnpj"),
            }

        data = {
            "id": id,
            "code": code,
            "status": status,
            "company": company,
            "person": person,
        }

        return data

    def get(self, id: int) -> ProducersModel | None:
        try:
            model = ProducersModel()
            producers = self.sanitizer(model.get(Producers, id))
            if producers:
                return producers
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
