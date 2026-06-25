from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Iterator, Sequence

from src.ga.genetic_algorithm import (
    GeneticAlgorithmConfig,
    GeneticAlgorithmResult,
    calculate_fitness,
    generate_random_population,
    mutate,
    order_crossover,
    sort_population,
    run_genetic_algorithm,
)
from src.models import Vehicle


@dataclass(frozen=True)
class TSPProblem:
    cities: tuple[object, ...]
    depot: object | None = None
    vehicle: Vehicle | None = None


@dataclass(frozen=True)
class TSPSolution:
    route: list[object]
    distance: float
    fitness_history: list[float]


@dataclass(frozen=True)
class TSPGenerationState:
    generation: int
    population: list[list[object]]
    best_route: list[object]
    best_fitness: float
    fitness_history: list[float]


def route_distance(
    route: Sequence[object],
    capacity_limit: float | None = None,
    distance_limit: float | None = None,
) -> float:
    return calculate_fitness(route, capacity_limit, distance_limit)


def iterate_tsp(
    problem: TSPProblem,
    config: GeneticAlgorithmConfig | None = None,
    rng: random.Random | None = None,
) -> Iterator[TSPGenerationState]:
    config = config or GeneticAlgorithmConfig()
    random_source = rng if rng is not None else random
    capacity_limit = problem.vehicle.max_capacity if problem.vehicle is not None else None
    distance_limit = problem.vehicle.max_distance if problem.vehicle is not None else None
    population = generate_random_population(problem.cities, config.population_size, random_source, problem.depot)
    fitness_history: list[float] = []

    generation = 1
    while config.generations is None or generation <= config.generations:
        population_fitness = [calculate_fitness(individual, capacity_limit, distance_limit) for individual in population]
        population, population_fitness = sort_population(population, population_fitness)

        best_route = list(population[0])
        best_fitness = population_fitness[0]
        fitness_history.append(best_fitness)

        yield TSPGenerationState(
            generation=generation,
            population=[list(individual) for individual in population],
            best_route=best_route,
            best_fitness=best_fitness,
            fitness_history=list(fitness_history),
        )

        new_population = [list(best_route)]
        parent_pool = population[: max(2, min(config.parent_pool_size, len(population)))]

        while len(new_population) < config.population_size:
            parent1, parent2 = random_source.choices(parent_pool, k=2)
            child = order_crossover(parent1, parent2, random_source, problem.depot)
            child = list(mutate(child, config.mutation_probability, random_source, problem.depot))
            new_population.append(child)

        population = new_population
        generation += 1


def solve_tsp(
    problem: TSPProblem,
    config: GeneticAlgorithmConfig | None = None,
    rng: random.Random | None = None,
) -> TSPSolution:
    capacity_limit = problem.vehicle.max_capacity if problem.vehicle is not None else None
    distance_limit = problem.vehicle.max_distance if problem.vehicle is not None else None
    result: GeneticAlgorithmResult = run_genetic_algorithm(
        problem.cities,
        config,
        rng,
        problem.depot,
        capacity_limit,
        distance_limit,
    )
    return TSPSolution(
        route=result.best_route,
        distance=result.best_fitness,
        fitness_history=result.best_fitness_history,
    )
