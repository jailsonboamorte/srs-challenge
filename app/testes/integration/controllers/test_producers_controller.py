from models.tables import Producers
from controllers.producers_controller import ProducersController
from seeds.data import get_people_data, get_producers_data, get_companies_data


def test_save_controller_PF_data_expected_Producers_object():
    data = get_producers_data()
    data["type"] = "PF"
    data["person"] = get_people_data()

    ctrl = ProducersController()
    assert isinstance(ctrl.save(data), Producers)


def test_save_controller_wrong_PF_data_expected_None():
    data = get_producers_data()
    data["type"] = "PF"
    data["person"] = get_people_data()
    data["person"]["cpf"] = 5299822472784

    ctrl = ProducersController()
    assert ctrl.save(data) is None


def test_save_controller_PJ_data_expected_Producers_object():
    data = get_producers_data()
    data["type"] = "PJ"
    data["company"] = get_companies_data()

    ctrl = ProducersController()
    assert isinstance(ctrl.save(data), Producers)


def test_save_controller_wrong_PJ_data_expected_None():
    data = get_producers_data()
    data["type"] = "PJ"
    data["person"] = get_companies_data()
    data["person"]["cpf"] = 5299822472784

    ctrl = ProducersController()
    assert ctrl.save(data) is None
