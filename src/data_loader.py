from __future__ import annotations

import csv
from pathlib import Path

from src.models import Delivery, Priority, Vehicle


def load_deliveries_csv(path: str | Path) -> list[Delivery]:
    deliveries: list[Delivery] = []

    with Path(path).open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            deliveries.append(
                Delivery(
                    id=str(row["delivery_id"]),
                    location=(float(row["latitude"]), float(row["longitude"])),
                    priority=Priority[row["priority"]],
                    weight=float(row["weight"]) if row.get("weight") else 0.0,
                    due_time=float(row["due_time"]) if row.get("due_time") else None,
                )
            )

    return deliveries


def load_vehicles_csv(path: str | Path) -> list[Vehicle]:
    vehicles: list[Vehicle] = []

    with Path(path).open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            vehicles.append(
                Vehicle(
                    id=str(row["vehicle_id"]),
                    max_capacity=float(row["max_capacity"]),
                    max_distance=float(row["max_distance"]) if row.get("max_distance") else None,
                )
            )

    return vehicles
