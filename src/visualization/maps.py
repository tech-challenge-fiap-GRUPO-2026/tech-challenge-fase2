from __future__ import annotations

from typing import Sequence

import pygame

from src.ga.genetic_algorithm import Point


def _point(value: object) -> Point:
    location = getattr(value, "location", value)
    return location  # type: ignore[return-value]


DEFAULT_CITY_COLOR = (220, 60, 60)
DEFAULT_ROUTE_COLOR = (40, 90, 220)
DEFAULT_SECONDARY_ROUTE_COLOR = (130, 130, 130)


def scale_points(
    points: Sequence[object],
    target_width: int,
    target_height: int,
    padding: int = 20,
    offset_x: int = 0,
    offset_y: int = 0,
) -> list[Point]:
    scaled_points = [_point(point) for point in points]
    min_x = min(point[0] for point in scaled_points)
    max_x = max(point[0] for point in scaled_points)
    min_y = min(point[1] for point in scaled_points)
    max_y = max(point[1] for point in scaled_points)
    usable_width = max(1, target_width - padding * 2)
    usable_height = max(1, target_height - padding * 2)
    span_x = max(1e-9, max_x - min_x)
    span_y = max(1e-9, max_y - min_y)
    scale = min(usable_width / span_x, usable_height / span_y)
    return [
        (
            int((point[0] - min_x) * scale + padding + offset_x),
            int((point[1] - min_y) * scale + padding + offset_y),
        )
        for point in scaled_points
    ]


def draw_cities(
    screen: pygame.Surface,
    cities: Sequence[object],
    color: tuple[int, int, int] = DEFAULT_CITY_COLOR,
    radius: int = 8,
) -> None:
    for city in cities:
        point = _point(city)
        pygame.draw.circle(screen, color, (int(point[0]), int(point[1])), radius)


def draw_route(
    screen: pygame.Surface,
    route: Sequence[object],
    color: tuple[int, int, int] = DEFAULT_ROUTE_COLOR,
    width: int = 2,
    closed: bool = True,
) -> None:
    if len(route) >= 2:
        pygame.draw.lines(screen, color, closed, [_point(point) for point in route], width)
