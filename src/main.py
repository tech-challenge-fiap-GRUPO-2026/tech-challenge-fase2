from __future__ import annotations

from pathlib import Path

import itertools

from src.ga.genetic_algorithm import GeneticAlgorithmConfig
from src.data_loader import load_deliveries_csv
from src.routing.tsp import TSPProblem, iterate_tsp
from src.visualization import DEFAULT_SECONDARY_ROUTE_COLOR, draw_cities, draw_fitness_plot, draw_route, scale_points
from src.models import City, Delivery


WIDTH = 800
HEIGHT = 400
PLOT_WIDTH = 450
NODE_RADIUS = 10
FPS = 30

WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
RED = (220, 60, 60)
BLUE = (40, 90, 220)
GRAY = (130, 130, 130)
PLOT_X_OFFSET = 450

POPULATION_SIZE = 100
N_GENERATIONS = None
MUTATION_PROBABILITY = 0.5
DELIVERIES_SAMPLE_PATH = Path(__file__).resolve().parents[1] / "data" / "deliveries_sample.csv"
DEPOT_LOCATION = (-1.4615, -48.4968)


def run_visual_demo() -> None:
    try:
        import pygame
    except ModuleNotFoundError as exc:  # pragma: no cover - runtime guard
        raise SystemExit("pygame nao esta instalado na virtualenv. Execute `.venv/bin/pip install pygame`.") from exc

    raw_deliveries = load_deliveries_csv(DELIVERIES_SAMPLE_PATH)
    depot = City(id="depot", location=DEPOT_LOCATION)
    scaled_locations = scale_points([depot, *raw_deliveries], WIDTH - PLOT_X_OFFSET, HEIGHT, padding=NODE_RADIUS, offset_x=PLOT_X_OFFSET)
    scaled_depot = scaled_locations[0]
    scaled_delivery_locations = scaled_locations[1:]
    visual_deliveries = [
        Delivery(id=delivery.id, location=location, priority=delivery.priority, due_time=delivery.due_time)
        for delivery, location in zip(raw_deliveries, scaled_delivery_locations)
    ]
    visual_depot = City(id=depot.id, location=scaled_depot)
    visual_by_id = {delivery.id: delivery for delivery in visual_deliveries}
    visual_by_id[visual_depot.id] = visual_depot

    config = GeneticAlgorithmConfig(
        population_size=POPULATION_SIZE,
        generations=None,
        mutation_probability=MUTATION_PROBABILITY,
    )
    problem = TSPProblem(depot=depot, cities=tuple(raw_deliveries))
    generation_counter = itertools.count(start=1)

    def translate_route(route: list[object]) -> list[object]:
        translated_route: list[object] = []
        for gene in route:
            delivery_id = getattr(gene, "id", None)
            translated_route.append(visual_by_id.get(delivery_id, gene))
        return translated_route

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("TSP Solver using Pygame")
    clock = pygame.time.Clock()

    running = True

    for state in iterate_tsp(problem, config):
        if not running:
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                running = False

        generation = next(generation_counter)

        screen.fill(WHITE)
        print(f"Generation {generation}: Best fitness = {round(state.best_fitness, 2)}")

        draw_fitness_plot(
            screen,
            state.fitness_history,
            pygame.Rect(0, 0, PLOT_WIDTH, HEIGHT),
        )

        draw_cities(screen, [visual_depot], color=BLACK, radius=NODE_RADIUS + 2)
        draw_cities(screen, visual_deliveries, radius=NODE_RADIUS)
        draw_route(screen, translate_route(state.best_route), BLUE, 3)
        if len(state.population) > 1:
            draw_route(screen, translate_route(state.population[1]), DEFAULT_SECONDARY_ROUTE_COLOR, 2)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


def main() -> None:
    run_visual_demo()


if __name__ == "__main__":
    main()
