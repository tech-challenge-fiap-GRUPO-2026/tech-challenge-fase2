from __future__ import annotations

import csv
import json
from dataclasses import asdict
from pathlib import Path
from typing import Iterable

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt

from src.metrics.statistics import format_seconds, mean, percent_change, standard_deviation


def ensure_directory(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def write_summary_csv(results: Iterable[object], path: Path) -> None:
    rows = [asdict(result) for result in results]
    ensure_directory(path.parent)

    if not rows:
        path.write_text("", encoding="utf-8")
        return

    fieldnames = [
        "name",
        "config_path",
        "population_size",
        "mutation_rate",
        "crossover_rate",
        "elitism_size",
        "parent_pool_size",
        "max_generations",
        "best_fitness",
        "initial_fitness",
        "improvement",
        "improvement_percent",
        "best_generation",
        "final_generation",
        "duration_seconds",
        "route_count",
    ]

    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def build_markdown_summary(results: list[object], title: str) -> str:
    if not results:
        return f"# {title}\n\nNenhum experimento foi executado.\n"

    best_result = min(results, key=lambda result: result.best_fitness)
    fitness_values = [result.best_fitness for result in results]
    duration_values = [result.duration_seconds for result in results]

    lines = [f"# {title}", "", "## Resumo", ""]
    lines.append(f"- Melhor fitness: {best_result.name} ({best_result.best_fitness:.2f})")
    lines.append(f"- Fitness medio final: {mean(fitness_values):.2f}")
    lines.append(f"- Desvio padrao do fitness final: {standard_deviation(fitness_values):.2f}")
    lines.append(f"- Tempo medio: {format_seconds(mean(duration_values))}")
    lines.append("")
    lines.append("## Configuracoes")
    lines.append("")
    lines.append("| Configuracao | Populacao | Mutacao | Crossover | Elitismo | Pool | Geracoes |")
    lines.append("| --- | ---: | ---: | ---: | ---: | ---: | ---: |")

    for result in sorted(results, key=lambda item: item.population_size):
        lines.append(
            f"| {result.name} | {result.population_size} | {result.mutation_rate:.2f} | {result.crossover_rate:.2f} | {result.elitism_size} | {result.parent_pool_size} | {result.max_generations} |"
        )

    lines.append("")
    lines.append("## Comparativo")
    lines.append("")
    lines.append("| Configuracao | Fitness final | Convergencia | Tempo | Melhoria |")
    lines.append("| --- | ---: | ---: | ---: | ---: |")

    for result in sorted(results, key=lambda item: item.best_fitness):
        lines.append(
            f"| {result.name} | {result.best_fitness:.2f} | {result.best_generation} | {format_seconds(result.duration_seconds)} | {result.improvement:.2f} |"
        )

    return "\n".join(lines) + "\n"


def write_markdown_summary(results: list[object], path: Path, title: str) -> None:
    ensure_directory(path.parent)
    path.write_text(build_markdown_summary(results, title), encoding="utf-8")


def write_json_summary(results: Iterable[object], path: Path) -> None:
    ensure_directory(path.parent)
    path.write_text(json.dumps([asdict(result) for result in results], indent=2, ensure_ascii=False), encoding="utf-8")


def _plot_metric_bars(results: list[object], path: Path, title: str, metric_name: str, color: str) -> None:
    fig, ax = plt.subplots(figsize=(8, 4.5), dpi=120)
    labels = [result.name for result in results]
    values = [getattr(result, metric_name) for result in results]
    ax.bar(labels, values, color=color)
    ax.set_title(title)
    ax.set_ylabel(metric_name.replace("_", " ").title())
    ax.grid(axis="y", alpha=0.25)
    plt.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def write_experiment_charts(results: list[object], output_dir: Path) -> None:
    ensure_directory(output_dir)
    if not results:
        return

    fig, ax = plt.subplots(figsize=(9, 5), dpi=120)
    for result in results:
        ax.plot(range(1, len(result.fitness_history) + 1), result.fitness_history, linewidth=2, label=result.name)
    ax.set_title("Convergencia do fitness")
    ax.set_xlabel("Geracao")
    ax.set_ylabel("Fitness")
    ax.grid(True, alpha=0.25)
    ax.legend()
    plt.tight_layout()
    fig.savefig(output_dir / "fitness_curves.png")
    plt.close(fig)

    _plot_metric_bars(results, output_dir / "final_fitness.png", "Fitness final por configuracao", "best_fitness", "#2f5bea")
    _plot_metric_bars(results, output_dir / "execution_time.png", "Tempo de execucao por configuracao", "duration_seconds", "#48a868")


def summarize_improvements(results: list[object]) -> dict[str, float]:
    improvements = [result.improvement for result in results]
    return {
        "mean_improvement": mean(improvements),
        "best_improvement": max(improvements) if improvements else 0.0,
        "percent_improvement_mean": mean([percent_change(result.initial_fitness, result.best_fitness) for result in results]),
    }
