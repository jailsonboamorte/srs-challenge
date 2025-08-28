import copy
from seeds.data import get_producers_data, get_people_data, get_companies_data

payload_producers = get_producers_data()
payload_people = get_people_data()
payload_companies = get_companies_data()


save_person_producer_payload = copy.deepcopy(payload_producers)
save_person_producer_payload["person"] = copy.deepcopy(payload_people)
save_person_producer_payload["type"] = "PF"

save_company_producer_payload = copy.deepcopy(payload_producers)
save_company_producer_payload["company"] = copy.deepcopy(payload_companies)
save_person_producer_payload["type"] = "PJ"

save_producer_example = {
    "people_producer": {
        "value": save_person_producer_payload,
        "summary": "",
        "description": "",
    },
    "company_producer": {
        "value": save_company_producer_payload,
        "summary": "",
        "description": "",
    },
}

update_company_producer_payload = copy.deepcopy(save_company_producer_payload)
update_person_producer_payload = copy.deepcopy(save_person_producer_payload)
update_producer_example = {
    "people_producer": {
        "value": update_person_producer_payload,
        "summary": "",
        "description": "",
    },
    "company_producer": {
        "value": update_company_producer_payload,
        "summary": "",
        "description": "",
    },
}
