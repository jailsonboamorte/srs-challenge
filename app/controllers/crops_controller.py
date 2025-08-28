from models.crops_model import CropsModel
from models.tables import Crops, Harvests
from log import logger
from helpers.exception import get_last_call


class CropsController:
    def save(self: "CropsController", data: dict) -> Crops | None:
        crops_model = CropsModel()
        logger.warning(data)
        try:
            crop = crops_model.save(data)
            if isinstance(crop, Crops):
                crops_model.session.commit()
                return crop

        except Exception as e:
            crops_model.session.rollback()
            logger.error(
                "Fail on {}.{}: ({})".format(
                    self.__class__.__name__, get_last_call(), e
                )
            )
        return None

    def sanitizer(self, crops: Crops) -> dict:
        if crops is None:
            return {}
        model = CropsModel()
        harvests = model.get(Harvests, crops.__dict__.get("harvest_id"))

        data = {
            "id": crops.__dict__.get("id"),
            "farm_id": crops.__dict__.get("farm_id"),
            "arable_area": crops.__dict__.get("arable_area"),
            "status": crops.__dict__.get("status"),
            "harvest": {
                "id": harvests.__dict__.get("id"),
                "name": harvests.__dict__.get("name"),
            },
        }
        return data

    def get(self, id: int) -> CropsModel | None:
        try:
            model = CropsModel()
            return self.sanitizer(model.get(Crops, id))
        except Exception as e:
            logger.error(
                "Fail on {}.{}: ({})".format(
                    self.__class__.__name__, get_last_call(), e
                )
            )
            return None
