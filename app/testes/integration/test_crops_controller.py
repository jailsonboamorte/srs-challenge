from models.tables import Crops
from controllers.producers_controller import ProducersController
from controllers.farms_controller import FarmsController
from controllers.crops_controller import CropsController
from seeds.data import (
    get_addresses_data,
    get_crops_data,
    get_farms_data,
    get_people_data,
    get_producers_data,
)
from log import logger


def test_save_farm_controller_data_expected_Crops_object():
    data = get_producers_data()
    data["type"] = "PF"
    data["person"] = get_people_data()

    ctrl = ProducersController()
    producer = ctrl.save(data)

    data = get_farms_data()
    data["address"] = get_addresses_data()
    data["producer_id"] = producer.id
    ctrl = FarmsController()
    farm = ctrl.save(data)

    data = get_crops_data()
    data["farm_id"] = farm.id
    data["harvest_id"] = 1
    logger.warning(data)
    ctrl = CropsController()
    ctrl.save(data)

    assert isinstance(ctrl.save(data), Crops)


def test_save_farm_controller_wrong_data_expected_Crops_None():
    data = get_crops_data()

    ctrl = CropsController()
    assert ctrl.save(data) is None
