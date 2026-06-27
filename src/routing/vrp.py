from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Iterator, Sequence

from src.ga.genetic_algorithm import GeneticAlgorithmConfig, calculate_fitness, order_crossover, sort_population
from src.models import Vehicle

FleetChromosome = list[list[object]]


@dataclass(frozen=True)
class VRPProblem:
    deliveries: tuple[object, ...]
    vehicles: tuple[Vehicle, ...]
    depot: object | None = None


@dataclass(frozen=True)
class VRPRoute:
    vehicle: Vehicle
    deliveries: tuple[object, ...]
    route: list[object]
    fitness: float
    fitness_history: list[float]


@dataclass(frozen=True)
class VRPSolution:
    routes: list[VRPRoute]
    total_fitness: float


@dataclass(frozen=True)
class VRPGenerationState:
    generation: int
    routes: list[VRPRoute]
    total_fitness: float
    fitness_history: list[float]


def _priority_rank(delivery: object) -> int:
    priority = getattr(delivery, "priority", None)
    priority_value = getattr(priority, "value", priority)
    ranks = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
    return ranks.get(priority_value, 1)


def _delivery_sort_key(delivery: object) -> tuple[int, float, str]:
    due_time = getattr(delivery, "due_time", None)
    return (_priority_rank(delivery), float("inf") if due_time is None else float(due_time), str(getattr(delivery, "id", "")))


def distribute_deliveries(deliveries: Sequence[object], vehicles: Sequence[Vehicle]) -> dict[Vehicle, list[object]]:
    if not vehicles:
        raise ValueError("At least one vehicle is required to solve VRP.")

    assignments: dict[Vehicle, list[object]] = {vehicle: [] for vehicle in vehicles}
    loads: dict[Vehicle, float] = {vehicle: 0.0 for vehicle in vehicles}

    for delivery in sorted(deliveries, key=_delivery_sort_key):
        delivery_weight = float(getattr(delivery, "weight", 0.0))
        fitting_vehicles = [vehicle for vehicle in vehicles if loads[vehicle] + delivery_weight <= vehicle.max_capacity]
        candidates = fitting_vehicles or list(vehicles)
        selected_vehicle = min(candidates, key=lambda vehicle: (loads[vehicle], vehicle.max_capacity, vehicle.id))
        assignments[selected_vehicle].append(delivery)
        loads[selected_vehicle] += delivery_weight

    return assignments


def _random_source(rng: random.Random | None) -> random.Random:
    return rng if rng is not None else random


def _route_path(deliveries: Sequence[object], depot: object | None) -> list[object]:
    return [depot, *deliveries] if depot is not None else list(deliveries)


def _route_fitness(deliveries: Sequence[object], vehicle: Vehicle, depot: object | None) -> float:
    path = _route_path(deliveries, depot)
    if len(path) < 2:
        return 0.0

    return calculate_fitness(path, vehicle.max_capacity, vehicle.max_distance)


def _fleet_fitness(chromosome: FleetChromosome, vehicles: Sequence[Vehicle], depot: object | None) -> float:
    return sum(_route_fitness(route, vehicle, depot) for route, vehicle in zip(chromosome, vehicles))


def _build_vrp_routes(
    chromosome: FleetChromosome,
    vehicles: Sequence[Vehicle],
    depot: object | None,
    fitness_history: Sequence[float],
) -> list[VRPRoute]:
    routes: list[VRPRoute] = []
    for route_deliveries, vehicle in zip(chromosome, vehicles):
        fitness = _route_fitness(route_deliveries, vehicle, depot)
        routes.append(
            VRPRoute(
                vehicle=vehicle,
                deliveries=tuple(route_deliveries),
                route=_route_path(route_deliveries, depot),
                fitness=fitness,
                fitness_history=list(fitness_history),
            )
        )

    return routes


def _chromosome_from_assignments(assignments: dict[Vehicle, list[object]], vehicles: Sequence[Vehicle]) -> FleetChromosome:
    return [list(assignments[vehicle]) for vehicle in vehicles]


def _generate_random_chromosome(
    deliveries: Sequence[object],
    vehicles: Sequence[Vehicle],
    rng: random.Random,
) -> FleetChromosome:
    chromosome: FleetChromosome = [[] for _ in vehicles]
    shuffled_deliveries = rng.sample(list(deliveries), len(deliveries))
    for delivery in shuffled_deliveries:
        chromosome[rng.randrange(len(vehicles))].append(delivery)

    return chromosome


def generate_fleet_population(
    deliveries: Sequence[object],
    vehicles: Sequence[Vehicle],
    population_size: int,
    rng: random.Random | None = None,
) -> list[FleetChromosome]:
    if not vehicles:
        raise ValueError("At least one vehicle is required to solve VRP.")

    random_source = _random_source(rng)
    assignments = distribute_deliveries(deliveries, vehicles)
    population = [_chromosome_from_assignments(assignments, vehicles)]

    while len(population) < population_size:
        population.append(_generate_random_chromosome(deliveries, vehicles, random_source))

    return population


def _flatten_chromosome(chromosome: FleetChromosome) -> list[object]:
    return [delivery for route in chromosome for delivery in route]


def _route_sizes(chromosome: FleetChromosome) -> list[int]:
    return [len(route) for route in chromosome]


def _split_by_sizes(deliveries: Sequence[object], sizes: Sequence[int]) -> FleetChromosome:
    chromosome: FleetChromosome = []
    start = 0
    for size in sizes:
        end = start + size
        chromosome.append(list(deliveries[start:end]))
        start = end

    if start < len(deliveries) and chromosome:
        chromosome[-1].extend(deliveries[start:])

    return chromosome


def fleet_crossover(parent1: FleetChromosome, parent2: FleetChromosome, rng: random.Random | None = None) -> FleetChromosome:
    flat_parent1 = _flatten_chromosome(parent1)
    flat_parent2 = _flatten_chromosome(parent2)
    if len(flat_parent1) < 2:
        return [list(route) for route in parent1]

    child_sequence = order_crossover(flat_parent1, flat_parent2, rng)
    sizes = _route_sizes(parent1 if (_random_source(rng).random() < 0.5) else parent2)
    return _split_by_sizes(child_sequence, sizes)


def mutate_fleet(
    chromosome: FleetChromosome,
    mutation_probability: float,
    rng: random.Random | None = None,
) -> FleetChromosome:
    random_source = _random_source(rng)
    mutated = [list(route) for route in chromosome]
    if random_source.random() >= mutation_probability:
        return mutated

    non_empty_routes = [index for index, route in enumerate(mutated) if route]
    if not non_empty_routes:
        return mutated

    mutation_type = random_source.choice(["move", "swap", "reorder"])
    if mutation_type == "move" and len(mutated) > 1:
        origin = random_source.choice(non_empty_routes)
        destination = random_source.randrange(len(mutated))
        delivery = mutated[origin].pop(random_source.randrange(len(mutated[origin])))
        mutated[destination].insert(random_source.randrange(len(mutated[destination]) + 1), delivery)
    elif mutation_type == "swap" and len(non_empty_routes) >= 2:
        route_a, route_b = random_source.sample(non_empty_routes, 2)
        index_a = random_source.randrange(len(mutated[route_a]))
        index_b = random_source.randrange(len(mutated[route_b]))
        mutated[route_a][index_a], mutated[route_b][index_b] = mutated[route_b][index_b], mutated[route_a][index_a]
    else:
        route_index = random_source.choice(non_empty_routes)
        if len(mutated[route_index]) >= 2:
            index = random_source.randrange(len(mutated[route_index]) - 1)
            mutated[route_index][index], mutated[route_index][index + 1] = mutated[route_index][index + 1], mutated[route_index][index]

    return mutated


def solve_vrp(
    problem: VRPProblem,
    config: GeneticAlgorithmConfig | None = None,
    rng: random.Random | None = None,
) -> VRPSolution:
    final_state = None
    for state in iterate_vrp(problem, config, rng):
        final_state = state

    if final_state is None:
        return VRPSolution(routes=[], total_fitness=0.0)

    return VRPSolution(routes=final_state.routes, total_fitness=final_state.total_fitness)


def iterate_vrp(
    problem: VRPProblem,
    config: GeneticAlgorithmConfig | None = None,
    rng: random.Random | None = None,
) -> Iterator[VRPGenerationState]:
    config = config or GeneticAlgorithmConfig()
    random_source = _random_source(rng)
    population = generate_fleet_population(problem.deliveries, problem.vehicles, config.population_size, random_source)
    fitness_history: list[float] = []
    generations = config.generations if config.generations is not None else None

    generation = 1
    while generations is None or generation <= generations:
        population_fitness = [_fleet_fitness(chromosome, problem.vehicles, problem.depot) for chromosome in population]
        population, population_fitness = sort_population(population, population_fitness)
        best_chromosome = [list(route) for route in population[0]]
        total_fitness = population_fitness[0]
        fitness_history.append(total_fitness)

        yield VRPGenerationState(
            generation=generation,
            routes=_build_vrp_routes(best_chromosome, problem.vehicles, problem.depot, fitness_history),
            total_fitness=total_fitness,
            fitness_history=list(fitness_history),
        )

        new_population = [[list(route) for route in chromosome] for chromosome in population[: config.elite_size]]
        parent_pool = population[: max(2, min(config.parent_pool_size, len(population)))]
        while len(new_population) < config.population_size:
            parent1, parent2 = random_source.choices(parent_pool, k=2)
            child = fleet_crossover(parent1, parent2, random_source)
            child = mutate_fleet(child, config.mutation_probability, random_source)
            new_population.append(child)

        population = new_population
        generation += 1
