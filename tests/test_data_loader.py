from src.data_loader import load_vehicles_csv


def test_load_vehicles_csv_reads_capacity_and_distance() -> None:
    vehicles = load_vehicles_csv("data/vehicles_sample.csv")

    assert len(vehicles) >= 5
    assert vehicles[0].max_capacity == 50
    assert vehicles[1].max_distance == 180
