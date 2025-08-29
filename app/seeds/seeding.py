import random

from models.inserter import initialize_table
from seeds.data import (
    get_addresses_data,
    get_addresses_producers_data,
    get_companies_data,
    get_crops_data,
    get_farms_data,
    get_farms_producers_data,
    get_people_data,
    get_producers_data,
)


def get_initial_get_producers_data(qty: int = 10) -> list:
    data = []
    for id in range(1, qty + 1):
        row = get_producers_data()
        row["id"] = id
        data.append(row)
    return data


def get_initial_people_data(producers: list[dict]) -> list:
    data = []
    for producer in producers:
        row = get_people_data()
        row["producer_id"] = producer.get("id")
        data.append(row)
    return data


def get_initial_companies_data(producers: list[dict]) -> list:
    data = []
    for producer in producers:
        row = get_companies_data()
        row["producer_id"] = producer.get("id")
        data.append(row)
    return data


def get_initial_addresses_data(qty: int = 10) -> list:
    data = []
    for id in range(1, qty + 1):
        row = get_addresses_data()
        row["id"] = id
        data.append(row)
    return data


def get_initial_addresses_producers_data(producers: list[dict]) -> list:
    data = []
    for producer in producers:
        row = get_addresses_producers_data()
        row["address_id"] = row["producer_id"] = producer.get("id")
        data.append(row)
    return data


def get_initial_farms_data(addresses) -> list:
    data = []
    for address in addresses:
        row = get_farms_data()
        row["id"] = row["address_id"] = address.get("id")
        data.append(row)
    return data


def get_initial_farms_producers_data(farms: list[dict]) -> list:
    data = []
    for farm in farms:
        row = get_farms_producers_data()
        row["farm_id"] = row["producer_id"] = farm.get("id")
        data.append(row)
    return data


def get_initial_crops_data(farms: list[dict]) -> list:
    data = []

    harvest_ids = [1, 2, 3, 4, 5]
    for farm in farms:
        row = get_crops_data()
        row["farm_id"] = farm.get("id")
        row["harvest_id"] = random.choice(harvest_ids)
        data.append(row)
    return data


qty = 500
half = int(qty / 2) + 1

producers = get_initial_get_producers_data(qty)
people = get_initial_people_data(producers[:half])
companies = get_initial_companies_data(producers[half:])
addresses = get_initial_addresses_data(2 * qty)
addresses_producers = get_initial_addresses_producers_data(producers)
farms = get_initial_farms_data(addresses[:qty])
farms_producers = get_initial_farms_producers_data(farms)
crops = get_initial_crops_data(farms)


SEEDS_DATA = {
    "Addresses": addresses,
    "AddressesProducers": addresses_producers,
    "Companies": companies,
    "Farms": farms,
    "FarmsProducers": farms_producers,
    "People": people,
    "Producers": producers,
    "Crops": crops,
}

if __name__ == "__main__":
    initialize_table(SEEDS_DATA)
