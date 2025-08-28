from faker import Faker
from pytest_schema import exact_schema
from seeds.data import get_producers_data, get_people_data, get_companies_data
from log import logger

fake = Faker("pt_BR")

path = "users"


payload_companies = get_companies_data()


def test_save_people_producer_expected_code_200(client_headers):
    payload = get_producers_data()
    payload["person"] = get_people_data()
    payload["type"] = "PF"

    response = client_headers.post("/v1/producers/", json=payload)

    assert response.status_code == 200


def test_save_people_producer_expected_code_404(client_headers):
    payload = get_producers_data()
    payload["person"] = get_people_data()
    payload["type"] = "PF"
    payload["person"]["cpf"] = "14524"

    response = client_headers.post("/v1/producers/", json=payload)

    assert response.status_code == 404


def test_save_company_producer_expected_code_200(client_headers):
    payload = get_producers_data()
    payload["company"] = get_companies_data()
    payload["type"] = "PJ"

    response = client_headers.post("/v1/producers/", json=payload)

    assert response.status_code == 200


def test_save_company_producer_expected_code_404(client_headers):
    payload = get_producers_data()
    payload["company"] = get_companies_data()
    payload["type"] = "PJ"
    payload["company"]["cnpj"] = "14524"

    response = client_headers.post("/v1/producers/", json=payload)

    assert response.status_code == 404


def test_update_people_producer_expected_code_200(client_headers):
    payload = get_producers_data()
    payload["person"] = get_people_data()
    payload["type"] = "PF"

    response = client_headers.post("/v1/producers/", json=payload)
    id = response.json()["id"]

    payload["person"] = get_people_data()
    response = client_headers.put(f"/v1/producers/{id}", json=payload)
    assert response.status_code == 200


def test_delete_people_producer_expected_code_200(client_headers):
    payload = get_producers_data()
    payload["person"] = get_people_data()
    payload["type"] = "PF"

    response = client_headers.post("/v1/producers/", json=payload)
    id = response.json()["id"]

    payload["person"] = get_people_data()
    response = client_headers.delete(f"/v1/producers/{id}")

    response = client_headers.get(f"/v1/producers/{id}")
    status = response.json()["status"]
    assert status == "inactive"


def test_get_people_producer_expected_code_200(client_headers):
    payload = get_producers_data()
    payload["person"] = get_people_data()
    payload["type"] = "PF"

    response = client_headers.post("/v1/producers/", json=payload)
    id = response.json()["id"]

    response = client_headers.get(f"/v1/producers/{id}")
    cpf = response.json()["person"]["cpf"]
    assert cpf == payload["person"]["cpf"]
