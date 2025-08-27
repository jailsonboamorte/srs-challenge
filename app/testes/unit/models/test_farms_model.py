from models.addresses_model import AddressesModel
from models.farms_model import FarmsModel
from models.tables import Farms
from seeds.data import get_addresses_data, get_farms_data
from log import logger


def test_save_correct_vegetable_area_expected_Farms_object():
    addresses_data = get_addresses_data()
    farms_data = get_farms_data()

    address_model = AddressesModel()
    session = address_model.session

    address = address_model.save(addresses_data)

    farms_model = FarmsModel(session)

    farms_data = get_farms_data()
    farms_data["address_id"] = address.id

    assert isinstance(farms_model.save(farms_data), Farms)

    # clear data
    address_model.session.rollback()


def test_save_wrong_vegetable_area_expected_Farms_None():
    addresses_data = get_addresses_data()
    farms_data = get_farms_data()

    address_model = AddressesModel()
    session = address_model.session

    address = address_model.save(addresses_data)

    farms_model = FarmsModel(session)

    farms_data = get_farms_data()
    farms_data["address_id"] = address.id
    farms_data["vegetation_area"] = farms_data.get("total_area") + 1

    assert farms_model.save(farms_data) is None

    # clear data
    address_model.session.rollback()
