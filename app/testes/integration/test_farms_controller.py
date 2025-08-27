from models.tables import Farms
from controllers.producers_controller import ProducersController
from controllers.farms_controller import FarmsController
from seeds.data import (
    get_people_data,
    get_producers_data,
    get_farms_data,
    get_addresses_data,
)


def test_save_farm_controller_data_expected_Farms_object():
    data = get_producers_data()
    data["type"] = "PF"
    data["person"] = get_people_data()

    ctrl = ProducersController()
    producer = ctrl.save(data)

    data = get_farms_data()
    data["address"] = get_addresses_data()
    data["producer_id"] = producer.id

    ctrl = FarmsController()
    assert isinstance(ctrl.save(data), Farms)


def test_save_farm_controller_wrong_data_expected_Farms_None():
    data = get_farms_data()
    data["address"] = get_addresses_data()

    ctrl = FarmsController()
    assert ctrl.save(data) is None
