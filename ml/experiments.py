"""Small JSON experiment log for reproducible learning notes."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict


def record_experiment(
    name: str,
    parameters: Dict,
    metrics: Dict,
    path: str = "data/experiments.jsonl",
) -> None:
    """Append one timestamped experiment record."""
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "name": name,
        "parameters": parameters,
        "metrics": metrics,
    }
    with destination.open("a", encoding="utf-8") as file:
        file.write(json.dumps(record, sort_keys=True) + "\n")
