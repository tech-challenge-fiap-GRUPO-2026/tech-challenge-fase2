import random

from src.ga.genetic_algorithm import GeneticAlgorithmConfig
from src.models import City, Vehicle
from src.routing.tsp import TSPProblem, route_distance, solve_tsp


def test_route_distance_delegates_to_closed_tsp_fitness() -> None:
    route = [(0, 0), (0, 3), (4, 0)]

    assert route_distance(route) == 12


def test_route_distance_applies_distance_limit_penalty() -> None:
    route = [(0, 0), (0, 3), (4, 0)]

    assert route_distance(route, distance_limit=10) == 62


def test_solve_tsp_returns_solution_for_problem() -> None:
    depot = City(id="depot", location=(0, 0))
    problem = TSPProblem(depot=depot, cities=((1, 0), (1, 1), (0, 1)))
    config = GeneticAlgorithmConfig(population_size=6, generations=3, mutation_probability=0.1)

    solution = solve_tsp(problem, config, random.Random(4))

    assert solution.route[0] == depot
    assert set(solution.route[1:]) == set(problem.cities)
    assert solution.distance == solution.fitness_history[-1]
    assert len(solution.fitness_history) == config.generations


def test_solve_tsp_still_works_without_depot() -> None:
    problem = TSPProblem(cities=((0, 0), (1, 0), (1, 1), (0, 1)))
    config = GeneticAlgorithmConfig(population_size=6, generations=3, mutation_probability=0.1)

    solution = solve_tsp(problem, config, random.Random(4))

    assert set(solution.route) == set(problem.cities)
    assert solution.distance == solution.fitness_history[-1]
    assert len(solution.fitness_history) == config.generations


def test_solve_tsp_applies_vehicle_distance_limit() -> None:
    depot = City(id="depot", location=(0, 0))
    vehicle = Vehicle(id="truck-1", max_capacity=100, max_distance=10)
    problem = TSPProblem(depot=depot, cities=((3, 0), (3, 4)), vehicle=vehicle)
    config = GeneticAlgorithmConfig(population_size=6, generations=3, mutation_probability=0.1)

    solution = solve_tsp(problem, config, random.Random(4))

    assert solution.distance == 62
    assert solution.distance == solution.fitness_history[-1]
