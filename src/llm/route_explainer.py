from __future__ import annotations

from src.llm.prompts import LLMClient, build_messages, build_question_prompt, solution_context
from src.routing.tsp import TSPSolution
from src.routing.vrp import VRPSolution


def answer_route_question(solution: TSPSolution | VRPSolution, question: str, client: LLMClient | None = None) -> str:
    if client is not None:
        return client.complete(build_messages(build_question_prompt(solution, question)))

    normalized_question = question.lower()
    if isinstance(solution, VRPSolution):
        if "fitness" in normalized_question or "custo" in normalized_question:
            return f"O fitness total da frota e {round(solution.total_fitness, 2)}."
        if "veiculo" in normalized_question or "frota" in normalized_question:
            return f"A solucao usa {len(solution.routes)} veiculo(s)."
    else:
        if "fitness" in normalized_question or "distancia" in normalized_question or "custo" in normalized_question:
            return f"O fitness/distancia da rota e {round(solution.distance, 2)}."

    return "Resumo da solucao:\n" + solution_context(solution)


def explain_route(solution: TSPSolution | VRPSolution, client: LLMClient | None = None) -> str:
    return answer_route_question(solution, "Explique os principais pontos da rota.", client)
