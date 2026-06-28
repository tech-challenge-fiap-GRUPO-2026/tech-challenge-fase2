from __future__ import annotations

import random
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from src.data_loader import load_deliveries_csv, load_vehicles_csv
from src.ga.genetic_algorithm import GeneticAlgorithmConfig
from src.routing.tsp import TSPProblem, iterate_tsp
from src.routing.vrp import VRPProblem, iterate_vrp


DEFAULT_EXPERIMENT_CONFIGS = (
    "pop50.yaml",
    "pop100.yaml",
    "pop100_no_elitism.yaml",
    "pop500.yaml",
    "pop500_no_elitism.yaml",
)

DEFAULT_DEPOT_LOCATION = (-1.4615, -48.4968)
BRAZIL_CAPITALS_DEPOT_LOCATION = (50, 28)


@dataclass(frozen=True)
class ExperimentCase:
    name: str
    config_path: Path
    config: GeneticAlgorithmConfig
    crossover_rate: float
    population_size: int
    mutation_rate: float
    elitism_size: int
    parent_pool_size: int
    max_generations: int


@dataclass(frozen=True)
class ExperimentResult:
    name: str
    config_path: str
    population_size: int
    mutation_rate: float
    crossover_rate: float
    elitism_size: int
    parent_pool_size: int
    max_generations: int
    initial_fitness: float
    best_fitness: float
    improvement: float
    improvement_percent: float
    best_generation: int
    final_generation: int
    duration_seconds: float
    route_count: int
    fitness_history: list[float]


def _parse_scalar(value: str) -> int | float | str | bool:
    lowered = value.lower()
    if lowered in {"true", "false"}:
        return lowered == "true"

    try:
        return int(value)
    except ValueError:
        try:
            return float(value)
        except ValueError:
            return value.strip("'\"")


def load_simple_yaml(path: str | Path) -> dict[str, int | float | str | bool]:
    data: dict[str, int | float | str | bool] = {}
    for raw_line in Path(path).read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue

        key, value = line.split(":", 1)
        data[key.strip()] = _parse_scalar(value.strip())

    return data


def load_experiment_cases(config_dir: str | Path, config_names: Iterable[str] = DEFAULT_EXPERIMENT_CONFIGS) -> list[ExperimentCase]:
    base_dir = Path(config_dir)
    cases: list[ExperimentCase] = []

    for config_name in config_names:
        config_path = base_dir / config_name
        raw = load_simple_yaml(config_path)
        population_size = int(raw.get("population_size", 100))
        mutation_rate = float(raw.get("mutation_rate", 0.3))
        crossover_rate = float(raw.get("crossover_rate", 0.8))
        elitism_size = int(raw.get("elitism_size", 1))
        parent_pool_size = int(raw.get("parent_pool_size", 10))
        max_generations = int(raw.get("max_generations", 100))
        cases.append(
            ExperimentCase(
                name=config_path.stem,
                config_path=config_path,
                config=GeneticAlgorithmConfig(
                    population_size=population_size,
                    generations=max_generations,
                    mutation_probability=mutation_rate,
                    elite_size=elitism_size,
                    parent_pool_size=parent_pool_size,
                ),
                crossover_rate=crossover_rate,
                population_size=population_size,
                mutation_rate=mutation_rate,
                elitism_size=elitism_size,
                parent_pool_size=parent_pool_size,
                max_generations=max_generations,
            )
        )

    return cases


def _select_vehicle(vehicles: list[object], vehicle_id: str | None) -> object | None:
    if vehicle_id is None:
        return vehicles[0] if vehicles else None

    for vehicle in vehicles:
        if getattr(vehicle, "id", None) == vehicle_id:
            return vehicle

    available = ", ".join(str(getattr(vehicle, "id", "?")) for vehicle in vehicles)
    raise SystemExit(f'Veiculo "{vehicle_id}" nao encontrado. Disponiveis: {available or "nenhum"}.')


def _select_vehicles(vehicles: list[object], vehicle_ids: list[str] | None) -> list[object]:
    if vehicle_ids is None:
        return vehicles

    selected = []
    for vehicle_id in vehicle_ids:
        selected.append(_select_vehicle(vehicles, vehicle_id))

    return [vehicle for vehicle in selected if vehicle is not None]


def _select_depot_location(deliveries_file: str | Path | None) -> tuple[float, float]:
    if deliveries_file is None:
        return DEFAULT_DEPOT_LOCATION

    if Path(deliveries_file).resolve() == (Path(__file__).resolve().parents[2] / "data" / "brazil_capitals_sample.csv").resolve():
        return BRAZIL_CAPITALS_DEPOT_LOCATION

    return DEFAULT_DEPOT_LOCATION


def _calculate_improvement(initial_fitness: float, final_fitness: float) -> tuple[float, float]:
    improvement = initial_fitness - final_fitness
    if initial_fitness == 0:
        return improvement, 0.0

    return improvement, (improvement / initial_fitness) * 100


def run_single_experiment(
    case: ExperimentCase,
    deliveries: list[object],
    vehicles: list[object],
    *,
    mode: str = "tsp",
    vehicle_id: str | None = None,
    vehicle_ids: list[str] | None = None,
    seed: int | None = None,
    deliveries_file: str | Path | None = None,
) -> ExperimentResult:
    rng = random.Random(seed)
    start = time.perf_counter()

    if mode == "vrp":
        selected_vehicles = _select_vehicles(vehicles, vehicle_ids)
        if not selected_vehicles:
            raise SystemExit("Modo VRP requer ao menos um veiculo.")

        problem = VRPProblem(deliveries=tuple(deliveries), vehicles=tuple(selected_vehicles), depot=_select_depot_location(deliveries_file))
        final_state = None
        for state in iterate_vrp(problem, case.config, rng):
            final_state = state

        if final_state is None:
            raise RuntimeError("Nao foi possivel executar o experimento VRP.")

        history = list(final_state.fitness_history)
        initial_fitness = history[0]
        best_fitness = min(history)
        convergence_generation = history.index(best_fitness) + 1
        best_generation = convergence_generation
        final_generation = final_state.generation
        route_count = len(final_state.routes)
    else:
        vehicle = _select_vehicle(vehicles, vehicle_id)
        problem = TSPProblem(cities=tuple(deliveries), depot=_select_depot_location(deliveries_file), vehicle=vehicle)
        final_state = None
        for state in iterate_tsp(problem, case.config, rng):
            final_state = state

        if final_state is None:
            raise RuntimeError("Nao foi possivel executar o experimento TSP.")

        history = list(final_state.fitness_history)
        initial_fitness = history[0]
        best_fitness = min(history)
        convergence_generation = history.index(best_fitness) + 1
        best_generation = convergence_generation
        final_generation = final_state.generation
        route_count = 1

    duration_seconds = time.perf_counter() - start
    improvement, improvement_percent = _calculate_improvement(initial_fitness, best_fitness)

    return ExperimentResult(
        name=case.name,
        config_path=str(case.config_path),
        population_size=case.population_size,
        mutation_rate=case.mutation_rate,
        crossover_rate=case.crossover_rate,
        elitism_size=case.elitism_size,
        parent_pool_size=case.parent_pool_size,
        max_generations=case.max_generations,
        initial_fitness=initial_fitness,
        best_fitness=best_fitness,
        improvement=improvement,
        improvement_percent=improvement_percent,
        best_generation=best_generation,
        final_generation=final_generation,
        duration_seconds=duration_seconds,
        route_count=route_count,
        fitness_history=history,
    )


def run_experiment_suite(
    deliveries_file: str | Path,
    vehicles_file: str | Path,
    *,
    config_dir: str | Path = "config",
    config_names: Iterable[str] = DEFAULT_EXPERIMENT_CONFIGS,
    mode: str = "vrp",
    vehicle_id: str | None = None,
    vehicle_ids: list[str] | None = None,
    seed: int | None = 7,
) -> list[ExperimentResult]:
    deliveries = load_deliveries_csv(deliveries_file)
    vehicles = load_vehicles_csv(vehicles_file)
    cases = load_experiment_cases(config_dir, config_names)

    return [
        run_single_experiment(
            case,
            deliveries,
            vehicles,
            mode=mode,
            vehicle_id=vehicle_id,
            vehicle_ids=vehicle_ids,
            seed=seed,
            deliveries_file=deliveries_file,
        )
        for case in cases
    ]
