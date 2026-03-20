import time
import json
from copy import deepcopy
from pathlib import Path


class EvidenceLedger:
    """
    Append-only evidence ledger with disk persistence (JSONL).
    """

    def __init__(self, path: str | None = None):
        self.path = Path(path) if path else None
        if self.path is not None:
            self.path.parent.mkdir(parents=True, exist_ok=True)

        # Load existing events
        self._events = []
        if self.path is not None and self.path.exists():
            with open(self.path, "r") as f:
                for line in f:
                    self._events.append(json.loads(line))

    def record(
        self,
        *,
        world: dict,
        prediction: dict,
        outcome: dict,
        confidence: float,
        notes: str = "",
    ):
        expected = prediction.get("expected_strain")
        observed = outcome.get("strain")

        error = None
        if expected is not None and observed is not None:
            error = abs(observed - expected)

        event = {
            "time": time.time(),
            "world": deepcopy(world),
            "prediction": deepcopy(prediction),
            "outcome": deepcopy(outcome),
            "error": error,
            "confidence": confidence,
            "notes": notes,
        }

        self._events.append(event)

        if self.path is not None:
            with open(self.path, "a") as f:
                f.write(json.dumps(event) + "\n")

        return event

    def all(self):
        return list(self._events)

    def recent(self, n: int = 10):
        return self._events[-n:]
