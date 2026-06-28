from __future__ import annotations

from src.llm.prompts import LLMClient, build_driver_instructions_prompt, build_messages, build_report_prompt
from src.routing.tsp import TSPSolution
from src.routing.vrp import VRPSolution


def _solution_title(solution: TSPSolution | VRPSolution) -> str:
    return "Relatorio operacional da frota" if isinstance(solution, VRPSolution) else "Relatorio operacional da rota"


def _deterministic_report(solution: TSPSolution | VRPSolution) -> str:
    if isinstance(solution, VRPSolution):
        lines = [f"# {_solution_title(solution)}", f"Fitness total da frota: {round(solution.total_fitness, 2)}", "Rotas por veiculo:"]
        for route in solution.routes:
            deliveries = ", ".join(str(getattr(delivery, "id", delivery)) for delivery in route.deliveries) or "sem entregas"
            lines.append(f"- Veiculo {route.vehicle.id}: {deliveries}. Fitness: {round(route.fitness, 2)}.")
        lines.append("Recomendacao: acompanhar entregas de alta prioridade e rotas proximas dos limites de capacidade ou autonomia.")
        return "\n".join(lines)

    route = " -> ".join(str(getattr(gene, "id", gene)) for gene in solution.route)
    return "\n".join(
        [
            f"# {_solution_title(solution)}",
            f"Fitness/distancia final: {round(solution.distance, 2)}",
            f"Rota: {route}",
            "Recomendacao: executar a rota na ordem indicada e monitorar entregas com maior prioridade.",
        ]
    )


def _deterministic_driver_instructions(solution: TSPSolution | VRPSolution) -> str:
    if isinstance(solution, VRPSolution):
        lines = ["Instrucoes para motoristas:"]
        for route in solution.routes:
            route_path = " -> ".join(str(getattr(gene, "id", gene)) for gene in route.route)
            lines.append(f"- Veiculo {route.vehicle.id}: seguir {route_path}.")
        return "\n".join(lines)

    route_path = " -> ".join(str(getattr(gene, "id", gene)) for gene in solution.route)
    return f"Instrucoes para motorista:\n- Seguir a rota: {route_path}."


def generate_operational_report(solution: TSPSolution | VRPSolution, client: LLMClient | None = None) -> str:
    if client is None:
        return _deterministic_report(solution)

    return client.complete(build_messages(build_report_prompt(solution)))


def generate_driver_instructions(solution: TSPSolution | VRPSolution, client: LLMClient | None = None) -> str:
    if client is None:
        return _deterministic_driver_instructions(solution)

    return client.complete(build_messages(build_driver_instructions_prompt(solution)))
