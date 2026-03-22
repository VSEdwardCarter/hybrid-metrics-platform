import json
from pathlib import Path

from app.core.config import settings
from app.models.metrics import (
    ThroughputMetric,
    LateDataMetric,
    QuarantineMetric,
)


class MetricsService:
    def __init__(self) -> None:
        self.total_metrics_dir = Path(settings.total_metrics_dir)
        self.current_metrics_dir = Path(settings.current_metrics_dir)

    def _read_json_file(self, base_dir: Path, filename: str) -> list[dict]:
        file_path = base_dir / filename

        if not file_path.exists():
            return []

        with file_path.open("r", encoding="utf-8") as f:
            return json.load(f)

    def get_throughput_metrics(self) -> list[ThroughputMetric]:
        rows = self._read_json_file(self.total_metrics_dir, "throughput.json")
        return [ThroughputMetric(**row) for row in rows]

    def get_current_throughput_metrics(self) -> list[ThroughputMetric]:
        rows = self._read_json_file(self.current_metrics_dir, "throughput.json")
        return [ThroughputMetric(**row) for row in rows]

    def get_late_data_metrics(self) -> list[LateDataMetric]:
        rows = self._read_json_file(self.total_metrics_dir, "late_data.json")
        return [LateDataMetric(**row) for row in rows]

    def get_current_late_data_metrics(self) -> list[LateDataMetric]:
        rows = self._read_json_file(self.current_metrics_dir, "late_data.json")
        return [LateDataMetric(**row) for row in rows]

    def get_quarantine_metrics(self) -> list[QuarantineMetric]:
        rows = self._read_json_file(self.total_metrics_dir, "quarantine.json")
        return [QuarantineMetric(**row) for row in rows]

    def get_current_quarantine_metrics(self) -> list[QuarantineMetric]:
        rows = self._read_json_file(self.current_metrics_dir, "quarantine.json")
        return [QuarantineMetric(**row) for row in rows]


metrics_service = MetricsService()