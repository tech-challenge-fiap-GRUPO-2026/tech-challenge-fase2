from __future__ import annotations

from collections.abc import Sequence

from src.llm import (
    ChatMessage,
    OpenAIChatClient,
    answer_route_question,
    build_driver_instructions_prompt,
    build_messages,
    build_question_prompt,
    build_report_prompt,
    generate_driver_instructions,
    generate_operational_report,
    solution_context,
)
from src.models import City, Delivery, Priority, Vehicle
from src.routing.tsp import TSPSolution
from src.routing.vrp import VRPRoute, VRPSolution


class FakeLLMClient:
    def __init__(self) -> None:
        self.messages: Sequence[ChatMessage] = []

    def complete(self, messages: Sequence[ChatMessage]) -> str:
        self.messages = messages
        return "resposta gerada"


class FakeOpenAIClient:
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        self.chat = self
        self.completions = self
        self.request: dict[str, object] = {}

    def create(self, **kwargs: object) -> object:
        self.request = kwargs

        class Message:
            content = " resposta openai "

        class Choice:
            message = Message()

        class Response:
            choices = [Choice()]

        return Response()


def _tsp_solution() -> TSPSolution:
    depot = City(id="depot", location=(0, 0))
    delivery = Delivery(id="Hospital A", location=(1, 1), priority=Priority.HIGH, weight=5, due_time=10)
    return TSPSolution(route=[depot, delivery], distance=12.5, fitness_history=[20.0, 12.5])


def _vrp_solution() -> VRPSolution:
    depot = City(id="depot", location=(0, 0))
    vehicle = Vehicle(id="1", max_capacity=50, max_distance=120)
    delivery = Delivery(id="Hospital B", location=(2, 2), priority=Priority.MEDIUM, weight=7, due_time=20)
    route = VRPRoute(vehicle=vehicle, deliveries=(delivery,), route=[depot, delivery], fitness=18.0, fitness_history=[25.0, 18.0])
    return VRPSolution(routes=[route], total_fitness=18.0)


def test_solution_context_includes_tsp_route_details() -> None:
    context = solution_context(_tsp_solution())

    assert "Tipo: TSP" in context
    assert "Hospital A" in context
    assert "prioridade=HIGH" in context
    assert "Fitness/distancia final: 12.5" in context


def test_solution_context_includes_vrp_fleet_details() -> None:
    context = solution_context(_vrp_solution())

    assert "Tipo: VRP" in context
    assert "Fitness total da frota: 18.0" in context
    assert "Veiculo 1" in context
    assert "Hospital B" in context


def test_prompt_builders_include_operational_intent() -> None:
    solution = _vrp_solution()

    assert "relatorio operacional" in build_report_prompt(solution)
    assert "instrucoes praticas" in build_driver_instructions_prompt(solution)
    assert "Pergunta: Qual veiculo sera usado?" in build_question_prompt(solution, "Qual veiculo sera usado?")


def test_build_messages_adds_system_and_user_messages() -> None:
    messages = build_messages("prompt")

    assert [message.role for message in messages] == ["system", "user"]
    assert messages[1].content == "prompt"


def test_generate_operational_report_works_without_external_client() -> None:
    report = generate_operational_report(_vrp_solution())

    assert "Relatorio operacional da frota" in report
    assert "Veiculo 1" in report


def test_generate_driver_instructions_works_without_external_client() -> None:
    instructions = generate_driver_instructions(_tsp_solution())

    assert "Instrucoes para motorista" in instructions
    assert "Hospital A" in instructions


def test_report_generator_uses_injected_client() -> None:
    client = FakeLLMClient()

    response = generate_operational_report(_tsp_solution(), client)

    assert response == "resposta gerada"
    assert client.messages[0].role == "system"
    assert "Hospital A" in client.messages[1].content


def test_answer_route_question_has_offline_fallback() -> None:
    response = answer_route_question(_vrp_solution(), "Qual e o fitness?")

    assert response == "O fitness total da frota e 18.0."


def test_answer_route_question_uses_injected_client() -> None:
    client = FakeLLMClient()
    response = answer_route_question(_tsp_solution(), "Explique a rota", client)

    assert response == "resposta gerada"
    assert "Explique a rota" in client.messages[1].content


def test_openai_chat_client_uses_factory_and_formats_messages() -> None:
    created_clients: list[FakeOpenAIClient] = []

    def factory(api_key: str) -> FakeOpenAIClient:
        client = FakeOpenAIClient(api_key)
        created_clients.append(client)
        return client

    client = OpenAIChatClient(api_key="secret", model="test-model", client_factory=factory)
    response = client.complete([ChatMessage(role="user", content="Gerar relatorio")])

    assert response == "resposta openai"
    assert created_clients[0].api_key == "secret"
    assert created_clients[0].request["model"] == "test-model"
    assert created_clients[0].request["messages"] == [{"role": "user", "content": "Gerar relatorio"}]


def test_openai_chat_client_requires_api_key() -> None:
    try:
        OpenAIChatClient(api_key="", client_factory=lambda **_: object())
    except ValueError as exc:
        assert "OPENAI_API_KEY" in str(exc)
    else:  # pragma: no cover - explicit failure branch
        raise AssertionError("Expected ValueError")
