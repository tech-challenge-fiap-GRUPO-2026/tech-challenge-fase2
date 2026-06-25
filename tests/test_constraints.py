from src.ga.genetic_algorithm import (
    CAPACITY_EXCESS_PENALTY,
    HIGH_PRIORITY_DELAY_PENALTY,
    LOW_PRIORITY_DELAY_PENALTY,
    MEDIUM_PRIORITY_DELAY_PENALTY,
    calculate_fitness,
)
from src.models import City, Delivery, Priority


def test_high_priority_delivery_without_delay_does_not_add_penalty() -> None:
    route = [
        Delivery(id="origin", location=(0, 0), priority=Priority.LOW),
        Delivery(id="urgent", location=(3, 0), priority=Priority.HIGH, due_time=3),
        Delivery(id="end", location=(3, 4), priority=Priority.LOW),
    ]

    assert calculate_fitness(route) == 12


def test_first_delivery_can_receive_penalty_when_depot_is_present() -> None:
    depot = City(id="depot", location=(0, 0))
    route = [
        depot,
        Delivery(id="urgent", location=(3, 0), priority=Priority.HIGH, due_time=2),
        Delivery(id="end", location=(3, 4), priority=Priority.LOW),
    ]

    expected_penalty = 1 * HIGH_PRIORITY_DELAY_PENALTY

    assert calculate_fitness(route) == 12 + expected_penalty


def test_high_priority_delivery_with_delay_adds_penalty() -> None:
    route = [
        Delivery(id="origin", location=(0, 0), priority=Priority.LOW),
        Delivery(id="urgent", location=(3, 0), priority=Priority.HIGH, due_time=1),
        Delivery(id="end", location=(3, 4), priority=Priority.LOW),
    ]

    expected_penalty = 2 * HIGH_PRIORITY_DELAY_PENALTY

    assert calculate_fitness(route) == 12 + expected_penalty


def test_medium_priority_delivery_with_delay_adds_penalty() -> None:
    route = [
        Delivery(id="origin", location=(0, 0), priority=Priority.LOW),
        Delivery(id="medium", location=(3, 0), priority=Priority.MEDIUM, due_time=1),
        Delivery(id="end", location=(3, 4), priority=Priority.LOW),
    ]

    expected_penalty = 2 * MEDIUM_PRIORITY_DELAY_PENALTY

    assert calculate_fitness(route) == 12 + expected_penalty


def test_low_priority_delivery_with_delay_adds_penalty() -> None:
    route = [
        Delivery(id="origin", location=(0, 0), priority=Priority.LOW),
        Delivery(id="low", location=(3, 0), priority=Priority.LOW, due_time=1),
        Delivery(id="end", location=(3, 4), priority=Priority.LOW),
    ]

    expected_penalty = 2 * LOW_PRIORITY_DELAY_PENALTY

    assert calculate_fitness(route) == 12 + expected_penalty


def test_capacity_limit_adds_penalty_when_exceeded() -> None:
    route = [
        City(id="depot", location=(0, 0)),
        Delivery(id="a", location=(3, 0), priority=Priority.LOW, weight=4),
        Delivery(id="b", location=(3, 4), priority=Priority.MEDIUM, weight=5),
        Delivery(id="c", location=(0, 4), priority=Priority.HIGH, weight=6),
    ]

    expected_penalty = (4 + 5 + 6 - 10) * CAPACITY_EXCESS_PENALTY

    assert calculate_fitness(route, capacity_limit=10) == 14 + expected_penalty


def test_capacity_limit_does_not_add_penalty_when_within_limit() -> None:
    route = [
        City(id="depot", location=(0, 0)),
        Delivery(id="a", location=(3, 0), priority=Priority.LOW, weight=2),
        Delivery(id="b", location=(3, 4), priority=Priority.MEDIUM, weight=3),
    ]

    assert calculate_fitness(route, capacity_limit=10) == 12
