from models.people_model import PeopleModel
from models.producers_model import ProducersModel
from models.tables import People
from seeds.data import get_people_data, get_producers_data
from log import logger


def test_save_invalid_cpf_expected_None():
    producers_data = get_producers_data()

    producer_model = ProducersModel()
    session = producer_model.session

    producer = producer_model.save(producers_data)

    logger.warning(producer.id)

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

    logger.warning(producer.id)

    people_model = PeopleModel(session)

    people_data = get_people_data()
    people_data["producer_id"] = producer.id
    people_data["cpf"] = 52998224725

    assert isinstance(people_model.save(people_data), People)

    # clear data
    producer_model.session.rollback()
