from __future__ import annotations

from math import sqrt


def mean(values: list[float]) -> float:
    if not values:
        return 0.0

    return sum(values) / len(values)


def median(values: list[float]) -> float:
    if not values:
        return 0.0

    ordered = sorted(values)
    middle = len(ordered) // 2
    if len(ordered) % 2 == 1:
        return ordered[middle]

    return (ordered[middle - 1] + ordered[middle]) / 2


def standard_deviation(values: list[float]) -> float:
    if len(values) < 2:
        return 0.0

    avg = mean(values)
    variance = sum((value - avg) ** 2 for value in values) / len(values)
    return sqrt(variance)


def improvement(initial: float, final: float) -> float:
    return initial - final


def percent_change(initial: float, final: float) -> float:
    if initial == 0:
        return 0.0

    return (initial - final) / initial * 100


def format_seconds(seconds: float) -> str:
    return f"{seconds:.3f}s"
