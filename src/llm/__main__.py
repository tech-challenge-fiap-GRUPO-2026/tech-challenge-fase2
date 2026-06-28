from __future__ import annotations

import argparse
import random
from pathlib import Path

from src.data_loader import load_deliveries_csv, load_vehicles_csv
from src.ga.genetic_algorithm import GeneticAlgorithmConfig
from src.llm.openai_client import OpenAIChatClient, load_dotenv_if_available
from src.llm.prompts import LLMClient
from src.llm.report_generator import generate_driver_instructions, generate_operational_report
from src.llm.route_explainer import answer_route_question
from src.models import City
from src.routing.tsp import TSPProblem, TSPSolution, solve_tsp
from src.routing.vrp import VRPProblem, VRPSolution, solve_vrp


ROOT_PATH = Path(__file__).resolve().parents[2]
DELIVERIES_SAMPLE_PATH = ROOT_PATH / "data" / "deliveries_sample.csv"
BRAZIL_CAPITALS_SAMPLE_PATH = ROOT_PATH / "data" / "brazil_capitals_sample.csv"
VEHICLES_SAMPLE_PATH = ROOT_PATH / "data" / "vehicles_sample.csv"
DEPOT_LOCATION = (-1.4615, -48.4968)
BRAZIL_CAPITALS_DEPOT_LOCATION = (50, 28)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="LLM text demo for optimized medical delivery routes")
    parser.add_argument("--mode", choices=("tsp", "vrp"), default="vrp", help="Route mode used to build the LLM context")
    parser.add_argument("--output", choices=("report", "instructions", "question"), default="report", help="Text output to generate")
    parser.add_argument("--question", default="Qual e o resumo da rota?", help="Question used when --output question is selected")
    parser.add_argument("--provider", choices=("offline", "openai"), default="offline", help="Text generation provider. Default: offline deterministic fallback")
    parser.add_argument("--model", default="gpt-4o-mini", help="OpenAI model used when --provider openai is selected")
    parser.add_argument("--vehicle-id", default=None, help="Vehicle id used in TSP mode. Default: first vehicle from CSV")
    parser.add_argument("--vehicle-ids", nargs="+", default=None, help="Vehicle ids used in VRP mode. Default: all vehicles from CSV")
    parser.add_argument("--population-size", type=int, default=80, help="Population size for route optimization")
    parser.add_argument("--generations", type=int, default=80, help="Number of generations before generating LLM text")
    parser.add_argument("--mutation-probability", type=float, default=0.3, help="Mutation probability for route optimization")
    parser.add_argument("--elite-size", type=int, default=1, help="Number of best individuals preserved between generations")
    parser.add_argument("--deliveries-file", type=Path, default=BRAZIL_CAPITALS_SAMPLE_PATH, help="Path to deliveries CSV")
    parser.add_argument("--vehicles-file", type=Path, default=VEHICLES_SAMPLE_PATH, help="Path to vehicles CSV")
    parser.add_argument("--seed", type=int, default=7, help="Random seed for reproducible demos")
    return parser


def _select_vehicle(vehicles: list[object], vehicle_id: str | None) -> object | None:
    if vehicle_id is None:
        return vehicles[0] if vehicles else None

    for vehicle in vehicles:
        if getattr(vehicle, "id", None) == vehicle_id:
            return vehicle

    available = ", ".join(str(getattr(vehicle, "id", "?")) for vehicle in vehicles)
    raise SystemExit(f'Vehiculo "{vehicle_id}" nao encontrado. Disponiveis: {available or "nenhum"}.')


def _select_vehicles(vehicles: list[object], vehicle_ids: list[str] | None) -> list[object]:
    if vehicle_ids is None:
        return vehicles

    return [vehicle for vehicle_id in vehicle_ids if (vehicle := _select_vehicle(vehicles, vehicle_id)) is not None]


def _select_depot_location(deliveries_file: Path) -> tuple[float, float]:
    if deliveries_file.resolve() == BRAZIL_CAPITALS_SAMPLE_PATH.resolve():
        return BRAZIL_CAPITALS_DEPOT_LOCATION

    return DEPOT_LOCATION


def solve_demo_solution(args: argparse.Namespace) -> TSPSolution | VRPSolution:
    deliveries = load_deliveries_csv(args.deliveries_file)
    vehicles = load_vehicles_csv(args.vehicles_file)
    depot = City(id="depot", location=_select_depot_location(args.deliveries_file))
    config = GeneticAlgorithmConfig(
        population_size=args.population_size,
        generations=args.generations,
        mutation_probability=args.mutation_probability,
        elite_size=args.elite_size,
    )
    rng = random.Random(args.seed)

    if args.mode == "vrp":
        selected_vehicles = _select_vehicles(vehicles, args.vehicle_ids)
        if not selected_vehicles:
            raise SystemExit("Modo VRP requer ao menos um veiculo no arquivo de veiculos.")
        return solve_vrp(VRPProblem(deliveries=tuple(deliveries), vehicles=tuple(selected_vehicles), depot=depot), config, rng)

    vehicle = _select_vehicle(vehicles, args.vehicle_id)
    return solve_tsp(TSPProblem(cities=tuple(deliveries), depot=depot, vehicle=vehicle), config, rng)


def build_llm_client(args: argparse.Namespace) -> LLMClient | None:
    if args.provider == "offline":
        return None

    load_dotenv_if_available()
    try:
        return OpenAIChatClient(model=args.model)
    except (RuntimeError, ValueError) as exc:
        raise SystemExit(str(exc)) from exc


def generate_text(args: argparse.Namespace) -> str:
    solution = solve_demo_solution(args)
    client = build_llm_client(args)
    if args.output == "instructions":
        return generate_driver_instructions(solution, client)
    if args.output == "question":
        return answer_route_question(solution, args.question, client)

    return generate_operational_report(solution, client)


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    print(generate_text(args))


if __name__ == "__main__":
    main()
