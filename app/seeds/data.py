import random

from faker import Faker  # type: ignore

fake = Faker("pt_BR")


def get_producers_data() -> dict:
    return {"status": "active", "code": str(fake.uuid4())}


def get_people_data() -> dict:
    return {
        "producer_id": None,
        "name": fake.name(),
        "cpf": fake.ssn(),
    }


def get_companies_data() -> dict:
    return {
        "producer_id": None,
        "fantasy_name": fake.name(),
        "cnpj": fake.company_id(),
    }


def get_crops_data() -> dict:
    _plant_name = {"café", "milho", "feijão", "arroz", "ervilha", "grão de bico"}
    plant_name = random.choice(list(_plant_name))

    _status = {"canceled", "finished", "started"}
    status = random.choice(list(_status))

    _arable_area = {100, 200, 500, 750, 1000}
    arable_area = random.choice(list(_arable_area))

    return {
        "farm_id": None,
        "harvest_id": None,
        "plant_name": plant_name,
        "arable_area": arable_area,
        "status": status,
    }


def get_farms_data() -> dict:
    _arable_area = {1000, 2000, 5000, 7500, 10000}
    arable_area = random.choice(list(_arable_area))

    _vegetation_area = {100, 200, 500, 750, 1000}
    vegetation_area = random.choice(list(_vegetation_area))

    return {
        "adddress_id": None,
        "name": fake.name(),
        "total_area": vegetation_area + arable_area,
        "vegetation_area": vegetation_area,
        "arable_area": arable_area,
    }


def get_addresses_data() -> dict:
    return {
        "city": fake.city(),
        "state": fake.estado_nome(),
        "zip_code": fake.postcode(),
    }


def get_addresses_producers_data() -> dict:
    return {"adddress_id": None, "producer_id": None}


def get_farms_producers_data() -> dict:
    return {"adddress_id": None, "farm_id": None}
