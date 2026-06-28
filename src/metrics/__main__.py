from __future__ import annotations

import argparse
from pathlib import Path

from src.metrics.experiment_logger import write_experiment_charts, write_json_summary, write_markdown_summary, write_summary_csv
from src.metrics.experiments import DEFAULT_EXPERIMENT_CONFIGS, run_experiment_suite


DEFAULT_DELIVERIES_FILE = Path(__file__).resolve().parents[2] / "data" / "deliveries_sample.csv"
DEFAULT_VEHICLES_FILE = Path(__file__).resolve().parents[2] / "data" / "vehicles_sample.csv"
DEFAULT_OUTPUT_DIR = Path(__file__).resolve().parents[2] / "artifacts"


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


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    results = run_experiment_suite(
        args.deliveries_file,
        args.vehicles_file,
        config_dir=args.config_dir,
        config_names=DEFAULT_EXPERIMENT_CONFIGS,
        mode=args.mode,
        vehicle_id=args.vehicle_id,
        vehicle_ids=args.vehicle_ids,
        seed=args.seed,
    )

    experiments_dir = args.output_dir / "experiments"
    charts_dir = args.output_dir / "charts"
    write_summary_csv(results, experiments_dir / "sprint8_summary.csv")
    write_json_summary(results, experiments_dir / "sprint8_summary.json")
    write_markdown_summary(results, experiments_dir / "sprint8_summary.md", "Sprint 8 - Experimentos")
    write_experiment_charts(results, charts_dir)

    best = min(results, key=lambda result: result.best_fitness)
    print(f"Melhor configuracao: {best.name} ({best.best_fitness:.2f})")
    print(f"Artefatos salvos em: {args.output_dir}")


if __name__ == "__main__":
    main()
