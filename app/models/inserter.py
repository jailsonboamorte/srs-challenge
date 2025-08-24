from models.addresses_model import AddressesModel
from models.addresses_producers import AddressesProducersModel
from models.companies_model import CompaniesModel
from models.crops_model import CropsModel
from models.farms_model import FarmsModel
from models.farms_producers_model import FarmsProducersModel
from models.harvests_model import HarvestsModel
from models.people_model import PeopleModel
from models.producers_model import ProducersModel


table_maps = {
    "Addresses": AddressesModel(),
    "AddressesProducers": AddressesProducersModel(),
    "Companies": CompaniesModel(),
    "Crops": CropsModel(),
    "Farms": FarmsModel(),
    "FarmsProducers": FarmsProducersModel(),
    "Harvests": HarvestsModel(),
    "People": PeopleModel(),
    "Producers": ProducersModel(),
}


def initialize_table(tables):
    for model_name in tables:
        if len(tables[model_name]) > 0:
            model = table_maps[model_name]
            for row in tables[model_name]:
                model.save(row)
                model.session.commit()
