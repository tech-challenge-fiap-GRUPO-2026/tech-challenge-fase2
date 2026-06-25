from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Vehicle:
    id: str
    max_capacity: float
    max_distance: float | None = None
