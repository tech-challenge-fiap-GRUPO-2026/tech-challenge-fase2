from __future__ import annotations

import argparse
import sys
from pathlib import Path

from src.metrics.experiment_logger import write_experiment_charts, write_json_summary, write_markdown_summary, write_summary_csv
from src.metrics.experiments import DEFAULT_EXPERIMENT_CONFIGS, load_experiment_cases, run_single_experiment
from src.data_loader import load_deliveries_csv, load_vehicles_csv


DEFAULT_DELIVERIES_FILE = Path(__file__).resolve().parents[2] / "data" / "deliveries_sample.csv"
DEFAULT_VEHICLES_FILE = Path(__file__).resolve().parents[2] / "data" / "vehicles_sample.csv"
DEFAULT_OUTPUT_DIR = Path(__file__).resolve().parents[2] / "artifacts"

BAR_WIDTH = 30


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run GA experiments for Sprint 8")
    parser.add_argument("--mode", choices=("tsp", "vrp"), default="vrp", help="Experiment mode")
    parser.add_argument("--deliveries-file", type=Path, default=DEFAULT_DELIVERIES_FILE, help="Deliveries CSV file")
    parser.add_argument("--vehicles-file", type=Path, default=DEFAULT_VEHICLES_FILE, help="Vehicles CSV file")
    parser.add_argument("--config-dir", type=Path, default=Path(__file__).resolve().parents[2] / "config", help="Configuration directory")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR, help="Directory used for experiment artifacts")
    parser.add_argument("--vehicle-id", default=None, help="Vehicle id used in TSP mode")
    parser.add_argument("--vehicle-ids", nargs="+", default=None, help="Vehicle ids used in VRP mode")
    parser.add_argument("--seed", type=int, default=7, help="Random seed")
    return parser


def _print_progress(experiment_name: str, generation: int, max_generations: int, fitness: float) -> None:
    fraction = generation / max_generations
    filled = int(BAR_WIDTH * fraction)
    bar = "█" * filled + "░" * (BAR_WIDTH - filled)
    sys.stdout.write(f"\r  [{bar}] {generation}/{max_generations} | fitness: {fitness:.2f}")
    sys.stdout.flush()


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    deliveries = load_deliveries_csv(args.deliveries_file)
    vehicles = load_vehicles_csv(args.vehicles_file)
    cases = load_experiment_cases(args.config_dir, DEFAULT_EXPERIMENT_CONFIGS)

    results = []
    for index, case in enumerate(cases, 1):
        print(f"\n[{index}/{len(cases)}] {case.name} (pop={case.population_size}, mut={case.mutation_rate}, elite={case.elitism_size})")

        def on_progress(generation: int, max_generations: int, fitness: float) -> None:
            _print_progress(case.name, generation, max_generations, fitness)

        result = run_single_experiment(
            case,
            deliveries,
            vehicles,
            mode=args.mode,
            vehicle_id=args.vehicle_id,
            vehicle_ids=args.vehicle_ids,
            seed=args.seed,
            deliveries_file=args.deliveries_file,
            on_progress=on_progress,
        )
        results.append(result)
        print(f"\n  Concluido: fitness {result.best_fitness:.2f} ( {(result.best_fitness / result.initial_fitness) * 100:.1f} % em relacao a 1 gen ) | convergiu na gen {result.best_generation} | {result.duration_seconds:.2f}s")
        print(f"\n  1 GEN fitness {result.initial_fitness:.2f} ")

    experiments_dir = args.output_dir / "experiments"
    charts_dir = args.output_dir / "charts"
    write_summary_csv(results, experiments_dir / "sprint8_summary.csv")
    write_json_summary(results, experiments_dir / "sprint8_summary.json")
    write_markdown_summary(results, experiments_dir / "sprint8_summary.md", "Sprint 8 - Experimentos")
    write_experiment_charts(results, charts_dir)

    best = min(results, key=lambda result: result.best_fitness)
    print(f"\nMelhor configuracao: {best.name} ({best.best_fitness:.2f})")
    print(f"Artefatos salvos em: {args.output_dir}")


if __name__ == "__main__":
    main()
