from pathlib import Path

from src.main import parse_args, route_slice_for_generation, select_depot_location, select_vehicle, select_vehicles, uses_brazil_map_background
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


def test_select_vehicles_uses_all_vehicles_when_ids_are_missing() -> None:
    vehicles = [
        Vehicle(id="1", max_capacity=50, max_distance=120),
        Vehicle(id="2", max_capacity=75, max_distance=180),
    ]

    selected = select_vehicles(vehicles, None)

    assert selected == vehicles


def test_select_vehicles_returns_requested_vehicles() -> None:
    vehicles = [
        Vehicle(id="1", max_capacity=50, max_distance=120),
        Vehicle(id="2", max_capacity=75, max_distance=180),
        Vehicle(id="3", max_capacity=90, max_distance=220),
    ]

    selected = select_vehicles(vehicles, ["1", "3"])

    assert selected == [vehicles[0], vehicles[2]]


def test_parse_args_uses_defaults_when_no_options_are_passed() -> None:
    args = parse_args([])

    assert args.vehicle_id is None
    assert args.vehicle_ids is None
    assert args.mode == "tsp"
    assert args.population_size == 100
    assert args.mutation_probability == 0.5
    assert args.elite_size == 1
    assert args.fps == 30
    assert str(args.deliveries_file).endswith("data/deliveries_sample.csv")
    assert str(args.vehicles_file).endswith("data/vehicles_sample.csv")


def test_parse_args_reads_custom_options() -> None:
    args = parse_args([
        "--mode",
        "vrp",
        "--vehicle-id",
        "3",
        "--vehicle-ids",
        "1",
        "2",
        "--population-size",
        "42",
        "--mutation-probability",
        "0.25",
        "--elite-size",
        "4",
        "--fps",
        "12",
        "--deliveries-file",
        "data/custom_deliveries.csv",
        "--vehicles-file",
        "data/custom_vehicles.csv",
    ])

    assert args.vehicle_id == "3"
    assert args.vehicle_ids == ["1", "2"]
    assert args.mode == "vrp"
    assert args.population_size == 42
    assert args.mutation_probability == 0.25
    assert args.elite_size == 4
    assert args.fps == 12
    assert str(args.deliveries_file) == "data/custom_deliveries.csv"
    assert str(args.vehicles_file) == "data/custom_vehicles.csv"


def test_select_depot_location_uses_brazil_capitals_map_depot() -> None:
    depot = select_depot_location(Path("data/brazil_capitals_sample.csv"))

    assert depot == (50, 28)


def test_select_depot_location_uses_default_depot_for_other_files() -> None:
    depot = select_depot_location(Path("data/deliveries_sample.csv"))

    assert depot == (-1.4615, -48.4968)


def test_uses_brazil_map_background_only_for_capitals_dataset() -> None:
    assert uses_brazil_map_background(Path("data/brazil_capitals_sample.csv")) is True
    assert uses_brazil_map_background(Path("data/deliveries_sample.csv")) is False


def test_route_slice_for_generation_reveals_route_progressively() -> None:
    route = ["depot", "a", "b", "c"]

    partial_route, closed = route_slice_for_generation(route, generation=1)
    full_route, full_closed = route_slice_for_generation(route, generation=4)
    later_route, later_closed = route_slice_for_generation(route, generation=10)

    assert partial_route == ["depot", "a"]
    assert closed is False
    assert full_route == route
    assert full_closed is True
    assert later_route == route
    assert later_closed is True
