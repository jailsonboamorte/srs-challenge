from models.farms_producers_model import FarmsProducersModel
from models.farms_model import FarmsModel
from models.addresses_model import AddressesModel
from models.tables import Farms, Addresses, FarmsProducers
from log import logger
from helpers.exception import get_last_call


class FarmsController:
    def save(self: "FarmsController", data: dict) -> Farms | None:
        address_model = AddressesModel()
        session = address_model.session
        farms_model = FarmsModel(session)
        farm_producer_model = FarmsProducersModel(session)
        try:
            address = address_model.save(data["address"])
            if isinstance(address, Addresses):
                data["address_id"] = address.id
                farm = farms_model.save(data)
                if isinstance(farm, Farms):
                    data["farm_id"] = farm.id
                    if isinstance(farm_producer_model.save(data), FarmsProducers):
                        farms_model.session.commit()
                        return farm

        except Exception as e:
            farms_model.session.rollback()
            logger.error(
                "Fail on {}.{}: ({})".format(
                    self.__class__.__name__, get_last_call(), e
                )
            )
        return None

    def sanitizer(self, farms: Farms) -> dict:
        if farms is None:
            return {}

        model = FarmsModel()
        address = model.get(Addresses, farms.__dict__.get("address_id"))

        data = {
            "id": farms.__dict__.get("id"),
            "name": farms.__dict__.get("name"),
            "total_area": farms.__dict__.get("total_area"),
            "arable_area": farms.__dict__.get("arable_area"),
            "vegetation_area": farms.__dict__.get("vegetation_area"),
            "address": {
                "state": address.__dict__.get("state"),
                "city": address.__dict__.get("city"),
                "zip_code": address.__dict__.get("zip_code"),
            },
        }
        return data

    def get(self, id: int) -> FarmsModel | None:
        try:
            model = FarmsModel()
            return self.sanitizer(model.get(Farms, id))
        except Exception as e:
            logger.error(
                "Fail on {}.{}: ({})".format(
                    self.__class__.__name__, get_last_call(), e
                )
            )
            return None
