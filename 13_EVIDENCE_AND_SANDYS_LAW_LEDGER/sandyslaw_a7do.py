import csv
import json
from pathlib import Path

from evidence_ledger import EvidenceLedger


class SandysLawA7DORecorder:
    """
    Records Sandy's Law evidence to JSONL and a CSV table for A7DO.
    """

    def __init__(
        self,
        jsonl_path: str = "13_EVIDENCE_AND_SANDYS_LAW_LEDGER/datasets/evidence.jsonl",
        table_path: str = "13_EVIDENCE_AND_SANDYS_LAW_LEDGER/datasets/sandyslaw_a7do_table.csv",
    ):
        self.ledger = EvidenceLedger(jsonl_path)
        self.table_path = Path(table_path)
        self.table_path.parent.mkdir(parents=True, exist_ok=True)
        self._ensure_table_header()

    def record(
        self,
        *,
        world: dict,
        prediction: dict,
        outcome: dict,
        confidence: float,
        notes: str = "",
    ):
        event = self.ledger.record(
            world=world,
            prediction=prediction,
            outcome=outcome,
            confidence=confidence,
            notes=notes,
        )
        self._append_table_row(event)
        return event

    def read_table(self):
        if not self.table_path.exists():
            return []
        with open(self.table_path, "r", newline="") as handle:
            return list(csv.DictReader(handle))

    def _ensure_table_header(self):
        if self.table_path.exists() and self.table_path.stat().st_size > 0:
            return
        with open(self.table_path, "w", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=self._fieldnames())
            writer.writeheader()

    def _append_table_row(self, event: dict):
        with open(self.table_path, "a", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=self._fieldnames())
            writer.writerow(self._format_row(event))

    def _fieldnames(self):
        return [
            "time",
            "expected_strain",
            "observed_strain",
            "error",
            "confidence",
            "notes",
            "world",
            "prediction",
            "outcome",
        ]

    def _format_row(self, event: dict):
        prediction = event.get("prediction", {})
        outcome = event.get("outcome", {})
        return {
            "time": event.get("time"),
            "expected_strain": prediction.get("expected_strain"),
            "observed_strain": outcome.get("strain"),
            "error": event.get("error"),
            "confidence": event.get("confidence"),
            "notes": event.get("notes"),
            "world": json.dumps(event.get("world"), ensure_ascii=False),
            "prediction": json.dumps(prediction, ensure_ascii=False),
            "outcome": json.dumps(outcome, ensure_ascii=False),
        }
