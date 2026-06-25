import random

from src.ga.genetic_algorithm import (
    GeneticAlgorithmConfig,
    calculate_distance,
    calculate_fitness,
    generate_random_population,
    mutate,
    order_crossover,
    run_genetic_algorithm,
    sort_population,
)


def test_calculate_distance_uses_euclidean_distance() -> None:
    assert calculate_distance((0, 0), (3, 4)) == 5


def test_calculate_fitness_closes_route() -> None:
    route = [(0, 0), (3, 0), (3, 4)]

    assert calculate_fitness(route) == 12


def test_generate_random_population_creates_valid_permutations() -> None:
    cities = [(0, 0), (1, 1), (2, 2)]
    population = generate_random_population(cities, 5, random.Random(1))

    assert len(population) == 5
    assert all(len(individual) == len(cities) for individual in population)
    assert all(set(individual) == set(cities) for individual in population)


def test_sort_population_orders_by_lowest_fitness() -> None:
    population = [[(0, 0)], [(1, 1)], [(2, 2)]]
    fitness = [3.0, 1.0, 2.0]

    sorted_population, sorted_fitness = sort_population(population, fitness)

    assert sorted_population == ([(1, 1)], [(2, 2)], [(0, 0)])
    assert sorted_fitness == (1.0, 2.0, 3.0)


def test_order_crossover_preserves_permutation() -> None:
    parent1 = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]
    parent2 = [(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)]

    child = order_crossover(parent1, parent2, random.Random(2))

    assert len(child) == len(parent1)
    assert set(child) == set(parent1)
    assert len(set(child)) == len(parent1)


def test_mutate_swaps_adjacent_genes_when_probability_matches() -> None:
    solution = [(0, 0), (1, 1), (2, 2)]

    mutated = mutate(solution, mutation_probability=1.0, rng=random.Random(1))

    assert mutated == [(1, 1), (0, 0), (2, 2)]
    assert solution == [(0, 0), (1, 1), (2, 2)]


def test_mutate_keeps_solution_when_probability_does_not_match() -> None:
    solution = [(0, 0), (1, 1), (2, 2)]

    mutated = mutate(solution, mutation_probability=0.0, rng=random.Random(1))

    assert mutated == solution


def test_run_genetic_algorithm_returns_best_solution_history() -> None:
    cities = [(0, 0), (1, 0), (1, 1), (0, 1)]
    config = GeneticAlgorithmConfig(population_size=8, generations=5, mutation_probability=0.2)

    result = run_genetic_algorithm(cities, config, random.Random(3))

    assert len(result.best_route) == len(cities)
    assert set(result.best_route) == set(cities)
    assert len(result.best_fitness_history) == config.generations
    assert len(result.best_route_history) == config.generations
    assert result.best_fitness == result.best_fitness_history[-1]


def test_run_genetic_algorithm_applies_distance_limit() -> None:
    cities = [(0, 0), (3, 0)]
    config = GeneticAlgorithmConfig(population_size=4, generations=2, mutation_probability=0.2)

    result = run_genetic_algorithm(cities, config, random.Random(3), distance_limit=5)

    assert result.best_fitness == 31
    assert result.best_fitness_history[-1] == 31
