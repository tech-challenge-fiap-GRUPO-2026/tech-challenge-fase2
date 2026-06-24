from __future__ import annotations

from dataclasses import dataclass

from src.ga.genetic_algorithm import Point
from src.models.priority import Priority


@dataclass(frozen=True)
class City:
    id: str
    location: Point


@dataclass(frozen=True)
class Delivery:
    id: str
    location: Point
    priority: Priority = Priority.MEDIUM
    due_time: float | None = None
