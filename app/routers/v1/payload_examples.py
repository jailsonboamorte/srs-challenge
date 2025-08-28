import copy
from seeds.data import (
    get_producers_data,
    get_people_data,
    get_companies_data,
    get_addresses_data,
    get_farms_data,
    get_crops_data,
)

payload_producers = get_producers_data()
payload_people = get_people_data()
payload_companies = get_companies_data()
payload_addresses = get_addresses_data()
payload_farms = get_farms_data()
payload_crops = get_crops_data()


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


save_farm_payload = copy.deepcopy(payload_farms)
save_farm_payload["address"] = copy.deepcopy(payload_addresses)

save_farm_example = {
    "farm": {
        "value": save_farm_payload,
        "summary": "",
        "description": "",
    }
}

save_crop_payload = copy.deepcopy(payload_crops)
save_crop_payload["harvest_id"] = 1

save_crop_example = {
    "crop": {
        "value": save_crop_payload,
        "summary": "",
        "description": "",
    }
}
