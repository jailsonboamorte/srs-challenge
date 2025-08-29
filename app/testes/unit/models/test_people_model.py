from models.companies_model import CompaniesModel
from models.people_model import PeopleModel
from models.producers_model import ProducersModel
from models.tables import People, Companies
from seeds.data import get_people_data, get_producers_data, get_companies_data
from log import logger


def test_save_invalid_cpf_expected_None():
    producers_data = get_producers_data()

    producer_model = ProducersModel()
    session = producer_model.session

    producer = producer_model.save(producers_data)

    people_model = PeopleModel(session)

    people_data = get_people_data()
    people_data["producer_id"] = producer.id
    people_data["cpf"] = 12345678900

    assert people_model.save(people_data) is None

    # clear data
    producer_model.session.rollback()


def test_save_valid_cpf_expected_People_object():
    producers_data = get_producers_data()

    producer_model = ProducersModel()
    session = producer_model.session

    producer = producer_model.save(producers_data)

    people_model = PeopleModel(session)

    people_data = get_people_data()
    people_data["producer_id"] = producer.id
    people_data["cpf"] = 52998224725

    assert isinstance(people_model.save(people_data), People)

    # clear data
    producer_model.session.rollback()


def test_save_invalid_cnpj_expected_None():
    producers_data = get_producers_data()

    producer_model = ProducersModel()
    session = producer_model.session

    producer = producer_model.save(producers_data)

    companies_model = CompaniesModel(session)

    company_data = get_companies_data()
    company_data["producer_id"] = producer.id
    company_data["cnpj"] = "11.444.777/0001-62"

    assert companies_model.save(company_data) is None

    # clear data
    producer_model.session.rollback()


def test_save_valid_cnpj_expected_Companies_object():
    producers_data = get_producers_data()

    producer_model = ProducersModel()
    session = producer_model.session

    producer = producer_model.save(producers_data)

    companies_model = CompaniesModel(session)

    company_data = get_companies_data()
    company_data["producer_id"] = producer.id
    company_data["cnpj"] = "11.444.777/0001-61"

    assert isinstance(companies_model.save(company_data), Companies)

    # clear data
    producer_model.session.rollback()
