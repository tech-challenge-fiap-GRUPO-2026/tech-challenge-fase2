from __future__ import annotations

import math
import random
from dataclasses import dataclass
from typing import Sequence

Point = tuple[float, float]
Route = list[object]
Population = list[Route]
HIGH_PRIORITY_DELAY_PENALTY = 100.0
MEDIUM_PRIORITY_DELAY_PENALTY = 30.0
LOW_PRIORITY_DELAY_PENALTY = 10.0
CAPACITY_EXCESS_PENALTY = 25.0
DISTANCE_EXCESS_PENALTY = 25.0

_PENALTY_MAP: dict[str, float] = {
    "HIGH": HIGH_PRIORITY_DELAY_PENALTY,
    "MEDIUM": MEDIUM_PRIORITY_DELAY_PENALTY,
    "LOW": LOW_PRIORITY_DELAY_PENALTY,
}

default_problems: dict[int, list[Point]] = {
    5: [(733, 251), (706, 87), (546, 97), (562, 49), (576, 253)],
    10: [
        (470, 169),
        (602, 202),
        (754, 239),
        (476, 233),
        (468, 301),
        (522, 29),
        (597, 171),
        (487, 325),
        (746, 232),
        (558, 136),
    ],
    12: [
        (728, 67),
        (560, 160),
        (602, 312),
        (712, 148),
        (535, 340),
        (720, 354),
        (568, 300),
        (629, 260),
        (539, 46),
        (634, 343),
        (491, 135),
        (768, 161),
    ],
    15: [
        (512, 317),
        (741, 72),
        (552, 50),
        (772, 346),
        (637, 12),
        (589, 131),
        (732, 165),
        (605, 15),
        (730, 38),
        (576, 216),
        (589, 381),
        (711, 387),
        (563, 228),
        (494, 22),
        (787, 288),
    ],
    20: [
        (514, 306),
        (741, 72),
        (552, 50),
        (772, 346),
        (637, 12),
        (589, 131),
        (732, 165),
        (605, 15),
        (730, 38),
        (576, 216),
        (589, 381),
        (711, 387),
        (563, 228),
        (494, 22),
        (787, 288),
        (664, 178),
        (509, 41),
        (450, 250),
        (790, 112),
        (620, 336),
    ],
    25: [
        (514, 306),
        (741, 72),
        (552, 50),
        (772, 346),
        (637, 12),
        (589, 131),
        (732, 165),
        (605, 15),
        (730, 38),
        (576, 216),
        (589, 381),
        (711, 387),
        (563, 228),
        (494, 22),
        (787, 288),
        (664, 178),
        (509, 41),
        (450, 250),
        (790, 112),
        (620, 336),
        (681, 59),
        (530, 162),
        (770, 241),
        (487, 188),
        (610, 290),
    ],
    30: [
        (514, 306),
        (741, 72),
        (552, 50),
        (772, 346),
        (637, 12),
        (589, 131),
        (732, 165),
        (605, 15),
        (730, 38),
        (576, 216),
        (589, 381),
        (711, 387),
        (563, 228),
        (494, 22),
        (787, 288),
        (664, 178),
        (509, 41),
        (450, 250),
        (790, 112),
        (620, 336),
        (681, 59),
        (530, 162),
        (770, 241),
        (487, 188),
        (610, 290),
        (720, 120),
        (545, 332),
        (467, 98),
        (756, 196),
        (642, 255),
    ],
}


@dataclass(frozen=True)
class GeneticAlgorithmConfig:
    population_size: int = 100
    generations: int | None = 100
    mutation_probability: float = 0.3
    elite_size: int = 1
    parent_pool_size: int = 10


@dataclass(frozen=True)
class GeneticAlgorithmResult:
    best_route: Route
    best_fitness: float
    best_fitness_history: list[float]
    best_route_history: list[Route]


def _random_source(rng: random.Random | None) -> random.Random:
    return rng if rng is not None else random


def generate_random_population(
    cities_location: Sequence[object],
    population_size: int,
    rng: random.Random | None = None,
    fixed_start: object | None = None,
) -> Population:
    random_source = _random_source(rng)
    population: Population = []

    for _ in range(population_size):
        route = random_source.sample(list(cities_location), len(cities_location))
        if fixed_start is not None:
            route = [fixed_start, *route]
        population.append(route)

    return population


def _get_location(gene: object) -> Point:
    location = getattr(gene, "location", gene)
    return location  # type: ignore[return-value]


def _compute_late_delivery_penalty(gene: object, arrival_time: float) -> float:
    priority = getattr(gene, "priority", None)
    due_time = getattr(gene, "due_time", None)

    if due_time is None:
        return 0.0

    priority_value = getattr(priority, "value", priority)
    penalty_factor = _PENALTY_MAP.get(priority_value)
    if penalty_factor is None:
        return 0.0

    delay = arrival_time - due_time
    return delay * penalty_factor if delay > 0 else 0.0


def _compute_capacity_penalty(path: Sequence[object], capacity_limit: float | None) -> float:
    if capacity_limit is None:
        return 0.0

    total_weight = 0.0
    for gene in path:
        total_weight += float(getattr(gene, "weight", 0.0))

    excess_weight = total_weight - capacity_limit
    return excess_weight * CAPACITY_EXCESS_PENALTY if excess_weight > 0 else 0.0


def _compute_distance_penalty(distance: float, distance_limit: float | None) -> float:
    if distance_limit is None:
        return 0.0

    excess_distance = distance - distance_limit
    return excess_distance * DISTANCE_EXCESS_PENALTY if excess_distance > 0 else 0.0


def calculate_distance(point1: object, point2: object) -> float:
    point1 = _get_location(point1)
    point2 = _get_location(point2)
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


def calculate_fitness(
    path: Sequence[object],
    capacity_limit: float | None = None,
    distance_limit: float | None = None,
) -> float:
    distance = 0.0
    penalty = 0.0
    arrival_time = 0.0
    path_size = len(path)

    for index in range(path_size):
        if index > 0:
            arrival_time += calculate_distance(path[index - 1], path[index])
            penalty += _compute_late_delivery_penalty(path[index], arrival_time)

        distance += calculate_distance(path[index], path[(index + 1) % path_size])

    penalty += _compute_capacity_penalty(path, capacity_limit)
    penalty += _compute_distance_penalty(distance, distance_limit)
    return distance + penalty


def order_crossover(
    parent1: Sequence[object],
    parent2: Sequence[object],
    rng: random.Random | None = None,
    fixed_start: object | None = None,
) -> Route:
    random_source = _random_source(rng)
    if fixed_start is not None:
        parent1 = parent1[1:]
        parent2 = parent2[1:]

    length = len(parent1)

    start_index = random_source.randint(0, length - 1)
    end_index = random_source.randint(start_index + 1, length)

    child = list(parent1[start_index:end_index])
    remaining_positions = [index for index in range(length) if index < start_index or index >= end_index]
    remaining_genes = [gene for gene in parent2 if gene not in child]

    for position, gene in zip(remaining_positions, remaining_genes):
        child.insert(position, gene)

    if fixed_start is not None:
        child.insert(0, fixed_start)

    return child


def mutate(
    solution: Sequence[object],
    mutation_probability: float,
    rng: random.Random | None = None,
    fixed_start: object | None = None,
) -> Sequence[object]:
    random_source = _random_source(rng)
    mutated_solution = list(solution)
    start_index = 1 if fixed_start is not None else 0

    if random_source.random() < mutation_probability:
        if len(solution) - start_index < 2:
            return solution

        index = random_source.randint(start_index, len(solution) - 2)
        mutated_solution[index], mutated_solution[index + 1] = solution[index + 1], solution[index]

    return mutated_solution


def sort_population(population: Sequence[Route], fitness: Sequence[float]) -> tuple[tuple[Route, ...], tuple[float, ...]]:
    sorted_pairs = sorted(zip(population, fitness), key=lambda pair: pair[1])
    sorted_population = tuple(individual for individual, _ in sorted_pairs)
    sorted_fitness = tuple(fitness_value for _, fitness_value in sorted_pairs)

    return sorted_population, sorted_fitness


def run_genetic_algorithm(
    cities_location: Sequence[object],
    config: GeneticAlgorithmConfig | None = None,
    rng: random.Random | None = None,
    fixed_start: object | None = None,
    capacity_limit: float | None = None,
    distance_limit: float | None = None,
) -> GeneticAlgorithmResult:
    config = config or GeneticAlgorithmConfig()
    random_source = _random_source(rng)
    population = generate_random_population(cities_location, config.population_size, random_source, fixed_start)
    best_fitness_history: list[float] = []
    best_route_history: list[Route] = []
    generations = config.generations if config.generations is not None else 100

    for _ in range(generations):
        population_fitness = [calculate_fitness(individual, capacity_limit, distance_limit) for individual in population]
        population, population_fitness = sort_population(population, population_fitness)

        best_route = population[0]
        best_fitness = population_fitness[0]
        best_fitness_history.append(best_fitness)
        best_route_history.append(list(best_route))

        new_population = [list(individual) for individual in population[: config.elite_size]]
        parent_pool = population[: config.parent_pool_size]

        while len(new_population) < config.population_size:
            parent1, parent2 = random_source.choices(parent_pool, k=2)
            child = order_crossover(parent1, parent2, random_source, fixed_start)
            child = list(mutate(child, config.mutation_probability, random_source, fixed_start))
            new_population.append(child)

        population = new_population

    return GeneticAlgorithmResult(
        best_route=best_route_history[-1],
        best_fitness=best_fitness_history[-1],
        best_fitness_history=best_fitness_history,
        best_route_history=best_route_history,
    )
