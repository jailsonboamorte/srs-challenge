from models.inserter import initialize_table
from seeds.data import get_producers_data


def get_initial_get_producers_data(qty: int = 10) -> list:
    data = []
    for id in range(1, qty + 1):
        row = get_producers_data()
        row["id"] = id
        data.append(row)
    return data


producers = get_initial_get_producers_data()


SEEDS_DATA = {"Producers": producers}

if __name__ == "__main__":
    initialize_table(SEEDS_DATA)
