from models.addresses_model import AddressesModel
from models.farms_model import FarmsModel
from models.crops_model import CropsModel
from models.tables import Crops
from seeds.data import get_addresses_data, get_farms_data, get_crops_data


def test_save_available_arable_area_expected_Crops_object():
    addresses_data = get_addresses_data()
    farms_data = get_farms_data()
    crops_data = get_crops_data()

    address_model = AddressesModel()
    session = address_model.session

    address = address_model.save(addresses_data)

    farms_model = FarmsModel(session)

    farms_data = get_farms_data()
    farms_data["address_id"] = address.id

    farm = farms_model.save(farms_data)

    crops_model = CropsModel(session)

    crops_data = get_crops_data()
    crops_data["farm_id"] = farm.id
    crops_data["harvest_id"] = 1
    crops_data["arable_area"] = farm.total_area - farm.vegetation_area

    assert isinstance(crops_model.save(crops_data), Crops)

    # clear data
    address_model.session.rollback()


def test_save_no_available_arable_area_expected_None():
    addresses_data = get_addresses_data()
    farms_data = get_farms_data()
    crops_data = get_crops_data()

    address_model = AddressesModel()
    session = address_model.session

    address = address_model.save(addresses_data)

    farms_model = FarmsModel(session)

    farms_data = get_farms_data()
    farms_data["address_id"] = address.id

    farm = farms_model.save(farms_data)

    crops_model = CropsModel(session)

    splited_area = int(farm.total_area - farm.vegetation_area / 3)

    crops_data = get_crops_data()
    crops_data["farm_id"] = farm.id
    crops_data["status"] = "started"

    crops_data["harvest_id"] = 1
    crops_data["arable_area"] = splited_area
    crops_model.save(crops_data)

    crops_data["harvest_id"] = 2
    crops_data["arable_area"] = splited_area
    crops_model.save(crops_data)

    crops_data["harvest_id"] = 3
    crops_data["arable_area"] = splited_area
    crops_model.save(crops_data)

    crops_data["harvest_id"] = 4
    crops_data["arable_area"] = splited_area

    assert crops_model.save(crops_data) is None

    # clear data
    address_model.session.rollback()
