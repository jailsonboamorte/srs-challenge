from models.crops_model import CropsModel
from models.tables import Crops
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

    def sanitizer(self, farms: CropsModel) -> dict:
        if farms is None:
            return {}
