from models.inserter import initialize_table
from datetime import datetime


def get_harvests_data() -> dict:
    current_year = datetime.now().year
    start_year = current_year - 5

    yearly_data = []
    for year in range(start_year, current_year + 1):
        yearly_data.append({"name": year, "description": year})
    return yearly_data


harvests = get_harvests_data()
BASICS_DATA = {"Harvests": harvests}


def insert_basics() -> None:
    initialize_table(BASICS_DATA)


if __name__ == "__main__":
    insert_basics()
