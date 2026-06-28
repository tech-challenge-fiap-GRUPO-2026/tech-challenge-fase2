from __future__ import annotations

from types import SimpleNamespace

from src.ga.genetic_algorithm import GeneticAlgorithmConfig
from src.metrics.experiment_logger import build_markdown_summary, write_experiment_charts, write_json_summary, write_markdown_summary, write_summary_csv
from src.metrics.experiments import ExperimentCase, ExperimentResult, load_experiment_cases, load_simple_yaml, run_single_experiment
from src.models import Delivery, Priority, Vehicle


def test_load_simple_yaml_parses_numeric_values(tmp_path) -> None:
    config_path = tmp_path / "sample.yaml"
    config_path.write_text("population_size: 25\nmutation_rate: 0.1\ncrossover_rate: 0.8\nelitism_size: 2\nmax_generations: 40\n", encoding="utf-8")

    data = load_simple_yaml(config_path)

    assert data["population_size"] == 25
    assert data["mutation_rate"] == 0.1
    assert data["crossover_rate"] == 0.8
    assert data["elitism_size"] == 2
    assert data["max_generations"] == 40


def test_load_experiment_cases_reads_repository_configs() -> None:
    cases = load_experiment_cases("config", ["pop50.yaml"])

    assert len(cases) == 1
    assert cases[0].name == "pop50"
    assert cases[0].population_size == 50
    assert cases[0].mutation_rate == 0.14
    assert cases[0].parent_pool_size == 6
    assert cases[0].elitism_size == 1
    assert cases[0].max_generations == 500


def test_load_experiment_cases_reads_no_elitism_config() -> None:
    cases = load_experiment_cases("config", ["pop100_no_elitism.yaml"])

    assert len(cases) == 1
    assert cases[0].name == "pop100_no_elitism"
    assert cases[0].population_size == 100
    assert cases[0].mutation_rate == 0.08
    assert cases[0].elitism_size == 0
    assert cases[0].parent_pool_size == 10
    assert cases[0].max_generations == 500


def test_load_experiment_cases_reads_large_no_elitism_config() -> None:
    cases = load_experiment_cases("config", ["pop500_no_elitism.yaml"])

    assert len(cases) == 1
    assert cases[0].name == "pop500_no_elitism"
    assert cases[0].population_size == 500
    assert cases[0].mutation_rate == 0.02
    assert cases[0].elitism_size == 0
    assert cases[0].parent_pool_size == 20
    assert cases[0].max_generations == 500


def test_run_single_experiment_builds_vrp_summary(monkeypatch) -> None:
    deliveries = [Delivery(id="1", location=(0.0, 0.0), priority=Priority.MEDIUM), Delivery(id="2", location=(1.0, 1.0), priority=Priority.LOW)]
    vehicles = [Vehicle(id="v1", max_capacity=100, max_distance=500), Vehicle(id="v2", max_capacity=100, max_distance=500)]
    case = ExperimentCase(
        name="pop50",
        config_path=__file__,
        config=GeneticAlgorithmConfig(population_size=2, generations=2, mutation_probability=0.1, elite_size=1),
        crossover_rate=0.8,
        population_size=50,
        mutation_rate=0.05,
        elitism_size=2,
        parent_pool_size=10,
        max_generations=2,
    )

    fake_states = iter(
        [
            SimpleNamespace(fitness_history=[10.0], total_fitness=10.0, generation=1, routes=[SimpleNamespace(route=["depot", "a"])]),
            SimpleNamespace(fitness_history=[10.0, 8.0], total_fitness=8.0, generation=2, routes=[SimpleNamespace(route=["depot", "a"]), SimpleNamespace(route=["depot", "b"])]),
        ]
    )
    monkeypatch.setattr("src.metrics.experiments.iterate_vrp", lambda *args, **kwargs: fake_states)

    result = run_single_experiment(case, deliveries, vehicles, mode="vrp", vehicle_ids=["v1", "v2"], seed=7, deliveries_file="data/deliveries_sample.csv")

    assert result.name == "pop50"
    assert result.best_fitness == 8.0
    assert result.initial_fitness == 10.0
    assert result.improvement == 2.0
    assert result.best_generation == 2
    assert result.final_generation == 2
    assert result.route_count == 2


def test_experiment_logger_writes_summary_artifacts(tmp_path) -> None:
    result = ExperimentResult(
        name="pop50",
        config_path="config/pop50.yaml",
        population_size=50,
        mutation_rate=0.05,
        crossover_rate=0.8,
        elitism_size=2,
        parent_pool_size=10,
        max_generations=500,
        initial_fitness=10.0,
        best_fitness=8.0,
        improvement=2.0,
        improvement_percent=20.0,
        best_generation=2,
        final_generation=2,
        duration_seconds=0.123,
        route_count=1,
        fitness_history=[10.0, 8.0],
    )

    csv_path = tmp_path / "summary.csv"
    md_path = tmp_path / "summary.md"
    json_path = tmp_path / "summary.json"
    charts_dir = tmp_path / "charts"

    write_summary_csv([result], csv_path)
    write_markdown_summary([result], md_path, "Sprint 8 - Experimentos")
    write_json_summary([result], json_path)
    write_experiment_charts([result], charts_dir)

    assert csv_path.exists()
    assert md_path.exists()
    assert json_path.exists()
    assert (charts_dir / "fitness_curves.png").exists()
    assert (charts_dir / "final_fitness.png").exists()
    assert (charts_dir / "execution_time.png").exists()
    assert "pop50" in build_markdown_summary([result], "Sprint 8 - Experimentos")
