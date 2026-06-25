from src.data_loader import load_vehicles_csv
from src.data_loader import load_deliveries_csv


def test_load_vehicles_csv_reads_capacity_and_distance() -> None:
    vehicles = load_vehicles_csv("data/vehicles_sample.csv")

    assert len(vehicles) >= 5
    assert vehicles[0].max_capacity == 50
    assert vehicles[1].max_distance == 180


def test_load_deliveries_csv_reads_brazil_capitals_map() -> None:
    deliveries = load_deliveries_csv("data/brazil_capitals_sample.csv")

    assert len(deliveries) == 27
    assert deliveries[0].id == "Rio Branco"
    assert deliveries[-1].id == "Porto Alegre"
