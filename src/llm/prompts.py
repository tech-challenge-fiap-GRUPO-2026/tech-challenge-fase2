from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, Sequence

from src.routing.tsp import TSPSolution
from src.routing.vrp import VRPRoute, VRPSolution


SYSTEM_PROMPT = (
    "Voce e um assistente operacional de logistica medica. "
    "Responda em portugues, com objetividade, priorizando entregas criticas, "
    "restricoes de capacidade, autonomia e atrasos."
)


@dataclass(frozen=True)
class ChatMessage:
    role: str
    content: str


class LLMClient(Protocol):
    def complete(self, messages: Sequence[ChatMessage]) -> str:
        pass


def gene_label(gene: object) -> str:
    return str(getattr(gene, "id", gene))


def delivery_details(delivery: object) -> str:
    priority = getattr(delivery, "priority", None)
    priority_value = getattr(priority, "value", priority) or "N/A"
    weight = getattr(delivery, "weight", 0.0)
    due_time = getattr(delivery, "due_time", None)
    due_time_value = "sem prazo" if due_time is None else str(due_time)
    return f"{gene_label(delivery)} | prioridade={priority_value} | peso={weight} | prazo={due_time_value}"


def tsp_solution_context(solution: TSPSolution) -> str:
    deliveries = [gene for gene in solution.route if gene_label(gene).lower() != "depot"]
    route = " -> ".join(gene_label(gene) for gene in solution.route)
    details = "\n".join(f"- {delivery_details(delivery)}" for delivery in deliveries)
    return (
        "Tipo: TSP\n"
        f"Fitness/distancia final: {round(solution.distance, 2)}\n"
        f"Rota: {route}\n"
        "Entregas:\n"
        f"{details or '- nenhuma entrega'}"
    )


def vrp_route_context(route: VRPRoute) -> str:
    route_path = " -> ".join(gene_label(gene) for gene in route.route)
    deliveries = "\n".join(f"  - {delivery_details(delivery)}" for delivery in route.deliveries)
    max_distance = "sem limite" if route.vehicle.max_distance is None else str(route.vehicle.max_distance)
    return (
        f"Veiculo {route.vehicle.id}\n"
        f"Capacidade maxima: {route.vehicle.max_capacity}\n"
        f"Autonomia maxima: {max_distance}\n"
        f"Fitness da rota: {round(route.fitness, 2)}\n"
        f"Rota: {route_path}\n"
        "Entregas:\n"
        f"{deliveries or '  - nenhuma entrega'}"
    )


def vrp_solution_context(solution: VRPSolution) -> str:
    routes_context = "\n\n".join(vrp_route_context(route) for route in solution.routes)
    return f"Tipo: VRP\nFitness total da frota: {round(solution.total_fitness, 2)}\n\n{routes_context}"


def solution_context(solution: TSPSolution | VRPSolution) -> str:
    if isinstance(solution, VRPSolution):
        return vrp_solution_context(solution)

    return tsp_solution_context(solution)


def build_report_prompt(solution: TSPSolution | VRPSolution) -> str:
    return (
        "Gere um relatorio operacional da solucao de rota abaixo. "
        "Inclua resumo, pontos de atencao e recomendacoes para a operacao.\n\n"
        f"{solution_context(solution)}"
    )


def build_driver_instructions_prompt(solution: TSPSolution | VRPSolution) -> str:
    return (
        "Gere instrucoes praticas para os motoristas executarem as rotas abaixo. "
        "Destaque prioridades altas, prazos e restricoes dos veiculos.\n\n"
        f"{solution_context(solution)}"
    )


def build_question_prompt(solution: TSPSolution | VRPSolution, question: str) -> str:
    return f"Responda a pergunta com base na solucao de rota.\n\n{solution_context(solution)}\n\nPergunta: {question}"


def build_messages(prompt: str) -> list[ChatMessage]:
    return [ChatMessage(role="system", content=SYSTEM_PROMPT), ChatMessage(role="user", content=prompt)]
