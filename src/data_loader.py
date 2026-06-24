from __future__ import annotations

import csv
from pathlib import Path

from src.models import Delivery, Priority


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
                    due_time=float(row["due_time"]) if row.get("due_time") else None,
                )
            )

    return deliveries
