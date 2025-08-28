from faker import Faker
from pytest_schema import exact_schema
from seeds.data import (
    get_producers_data,
    get_people_data,
    get_addresses_data,
    get_farms_data,
)
from log import logger

fake = Faker("pt_BR")


def test_save_farm_expected_code_200(client_headers):
    payload = get_producers_data()
    payload["person"] = get_people_data()
    payload["type"] = "PF"

    response = client_headers.post("/v1/producers/", json=payload)

    payload = get_farms_data()
    payload["address"] = get_addresses_data()
    producer_id = response.json()["id"]
    response = client_headers.post(f"/v1/farms/{producer_id}", json=payload)

    assert response.status_code == 200


def test_save_farm_expected_code_404(client_headers):
    payload = get_producers_data()
    payload["person"] = get_people_data()
    payload["type"] = "PF"

    response = client_headers.post("/v1/producers/", json=payload)

    payload = get_farms_data()
    payload["total_area"] = 1
    payload["address"] = get_addresses_data()
    producer_id = response.json()["id"]
    response = client_headers.post(f"/v1/farms/{producer_id}", json=payload)
    logger.warning(response.text)

    assert response.status_code == 404
