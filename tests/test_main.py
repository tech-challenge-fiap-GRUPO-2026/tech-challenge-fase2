from src.main import parse_args, select_vehicle
from src.models import Vehicle


def test_select_vehicle_returns_vehicle_matching_id() -> None:
    vehicles = [
        Vehicle(id="1", max_capacity=50, max_distance=120),
        Vehicle(id="2", max_capacity=75, max_distance=180),
    ]

    selected = select_vehicle(vehicles, "2")

    assert selected == vehicles[1]


def test_select_vehicle_uses_first_vehicle_when_id_is_missing() -> None:
    vehicles = [Vehicle(id="1", max_capacity=50, max_distance=120)]

    selected = select_vehicle(vehicles, None)

    assert selected == vehicles[0]


def test_parse_args_uses_defaults_when_no_options_are_passed() -> None:
    args = parse_args([])

    assert args.vehicle_id is None
    assert args.population_size == 100
    assert args.mutation_probability == 0.5
    assert str(args.deliveries_file).endswith("data/deliveries_sample.csv")
    assert str(args.vehicles_file).endswith("data/vehicles_sample.csv")


def test_parse_args_reads_custom_options() -> None:
    args = parse_args([
        "--vehicle-id",
        "3",
        "--population-size",
        "42",
        "--mutation-probability",
        "0.25",
        "--deliveries-file",
        "data/custom_deliveries.csv",
        "--vehicles-file",
        "data/custom_vehicles.csv",
    ])

    assert args.vehicle_id == "3"
    assert args.population_size == 42
    assert args.mutation_probability == 0.25
    assert str(args.deliveries_file) == "data/custom_deliveries.csv"
    assert str(args.vehicles_file) == "data/custom_vehicles.csv"
