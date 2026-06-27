import random

import pytest

from src.ga.genetic_algorithm import GeneticAlgorithmConfig
from src.models import City, Delivery, Priority, Vehicle
from src.routing.vrp import VRPProblem, distribute_deliveries, generate_fleet_population, iterate_vrp, mutate_fleet, solve_vrp


def test_distribute_deliveries_assigns_every_delivery_once() -> None:
    deliveries = [
        Delivery(id="a", location=(1, 0), priority=Priority.HIGH, weight=4, due_time=10),
        Delivery(id="b", location=(2, 0), priority=Priority.MEDIUM, weight=3, due_time=20),
        Delivery(id="c", location=(3, 0), priority=Priority.LOW, weight=2, due_time=30),
    ]
    vehicles = [
        Vehicle(id="v1", max_capacity=5, max_distance=100),
        Vehicle(id="v2", max_capacity=5, max_distance=100),
    ]

    assignments = distribute_deliveries(deliveries, vehicles)
    assigned_deliveries = [delivery for route_deliveries in assignments.values() for delivery in route_deliveries]

    assert sorted(delivery.id for delivery in assigned_deliveries) == ["a", "b", "c"]
    assert len(assigned_deliveries) == len(set(assigned_deliveries))


def test_distribute_deliveries_requires_vehicle() -> None:
    deliveries = [Delivery(id="a", location=(1, 0), weight=1)]

    with pytest.raises(ValueError, match="At least one vehicle"):
        distribute_deliveries(deliveries, [])


def test_solve_vrp_returns_one_route_per_vehicle_and_total_fitness() -> None:
    depot = City(id="depot", location=(0, 0))
    deliveries = (
        Delivery(id="a", location=(3, 0), priority=Priority.HIGH, weight=4, due_time=10),
        Delivery(id="b", location=(0, 4), priority=Priority.MEDIUM, weight=4, due_time=10),
    )
    vehicles = (
        Vehicle(id="v1", max_capacity=5, max_distance=100),
        Vehicle(id="v2", max_capacity=5, max_distance=100),
    )
    config = GeneticAlgorithmConfig(population_size=4, generations=2, mutation_probability=0.0)

    solution = solve_vrp(VRPProblem(deliveries=deliveries, vehicles=vehicles, depot=depot), config, random.Random(1))

    assert len(solution.routes) == 2
    assert [route.vehicle.id for route in solution.routes] == ["v1", "v2"]
    assert sorted(delivery.id for route in solution.routes for delivery in route.deliveries) == ["a", "b"]
    assert solution.total_fitness == sum(route.fitness for route in solution.routes)
    assert solution.total_fitness == 14


def test_solve_vrp_applies_vehicle_capacity_per_route() -> None:
    depot = City(id="depot", location=(0, 0))
    deliveries = (
        Delivery(id="a", location=(3, 0), priority=Priority.LOW, weight=8),
        Delivery(id="b", location=(0, 4), priority=Priority.LOW, weight=8),
    )
    vehicles = (
        Vehicle(id="v1", max_capacity=5, max_distance=100),
        Vehicle(id="v2", max_capacity=5, max_distance=100),
    )
    config = GeneticAlgorithmConfig(population_size=4, generations=1, mutation_probability=0.0)

    solution = solve_vrp(VRPProblem(deliveries=deliveries, vehicles=vehicles, depot=depot), config, random.Random(1))

    assert solution.total_fitness == 14 + (3 * 25 * 2)


def test_iterate_vrp_yields_generation_states_with_aggregated_history() -> None:
    depot = City(id="depot", location=(0, 0))
    deliveries = (
        Delivery(id="a", location=(3, 0), priority=Priority.HIGH, weight=4, due_time=10),
        Delivery(id="b", location=(0, 4), priority=Priority.MEDIUM, weight=4, due_time=10),
    )
    vehicles = (
        Vehicle(id="v1", max_capacity=5, max_distance=100),
        Vehicle(id="v2", max_capacity=5, max_distance=100),
    )
    config = GeneticAlgorithmConfig(population_size=4, generations=2, mutation_probability=0.0)

    states = list(iterate_vrp(VRPProblem(deliveries=deliveries, vehicles=vehicles, depot=depot), config, random.Random(1)))

    assert [state.generation for state in states] == [1, 2]
    assert len(states[0].routes) == 2
    assert states[-1].fitness_history == [14, 14]
    assert states[-1].total_fitness == 14


def test_generate_fleet_population_preserves_each_delivery_once() -> None:
    deliveries = [Delivery(id=str(index), location=(index, 0), weight=1) for index in range(5)]
    vehicles = [
        Vehicle(id="v1", max_capacity=10, max_distance=100),
        Vehicle(id="v2", max_capacity=10, max_distance=100),
    ]

    population = generate_fleet_population(deliveries, vehicles, population_size=6, rng=random.Random(2))

    assert len(population) == 6
    for chromosome in population:
        assigned = [delivery for route in chromosome for delivery in route]
        assert sorted(delivery.id for delivery in assigned) == ["0", "1", "2", "3", "4"]
        assert len(assigned) == len(set(assigned))


def test_mutate_fleet_can_move_delivery_between_vehicle_routes() -> None:
    chromosome = [
        [Delivery(id="a", location=(1, 0), weight=1)],
        [Delivery(id="b", location=(2, 0), weight=1)],
    ]

    mutated = mutate_fleet(chromosome, mutation_probability=1.0, rng=random.Random(1))

    assigned = [delivery for route in mutated for delivery in route]

    assert sorted(delivery.id for delivery in assigned) == ["a", "b"]
    assert mutated != chromosome
