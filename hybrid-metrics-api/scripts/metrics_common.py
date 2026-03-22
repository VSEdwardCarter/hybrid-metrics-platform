import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any


PARTITION_PATTERN = re.compile(r"dt=(\d{4}-\d{2}-\d{2})/hr=(\d{2})")


def get_nested(record: dict[str, Any], *keys: str, default: Any = None) -> Any:
    current: Any = record
    for key in keys:
        if not isinstance(current, dict):
            return default
        current = current.get(key)
        if current is None:
            return default
    return current


def parse_iso_ts(value: str | None) -> datetime | None:
    if not value or not isinstance(value, str):
        return None

    try:
        return datetime.fromisoformat(value)
    except ValueError:
        return None


def find_all_jsonl_files(base_dir: Path) -> list[Path]:
    if not base_dir.exists():
        return []
    return sorted(base_dir.rglob("*.jsonl"))


def find_latest_partition_dir(base_dir: Path) -> Path | None:
    if not base_dir.exists():
        return None

    candidates: list[tuple[datetime, Path]] = []

    for path in base_dir.rglob("hr=*"):
        if not path.is_dir():
            continue

        relative_path = path.relative_to(base_dir).as_posix()
        match = PARTITION_PATTERN.search(relative_path)
        if not match:
            continue

        dt_str, hr_str = match.groups()
        partition_dt = datetime.fromisoformat(f"{dt_str}T{hr_str}:00:00")
        candidates.append((partition_dt, path))

    if not candidates:
        return None

    candidates.sort(key=lambda x: x[0], reverse=True)
    return candidates[0][1]


def find_jsonl_files_in_partition(partition_dir: Path | None) -> list[Path]:
    if partition_dir is None or not partition_dir.exists():
        return []

    return sorted(partition_dir.glob("*.jsonl"))


def read_jsonl_records(files: list[Path]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []

    for file_path in files:
        with file_path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                try:
                    record = json.loads(line)
                    if isinstance(record, dict):
                        records.append(record)
                except json.JSONDecodeError:
                    continue

    return records


def build_throughput_metrics(records: list[dict[str, Any]], measurement_window: str) -> list[dict[str, Any]]:
    total_records = len(records)

    timestamps = [
        ts for ts in (parse_iso_ts(record.get("ts")) for record in records)
        if ts is not None
    ]

    if timestamps:
        window_start_dt = min(timestamps)
        window_end_dt = max(timestamps)
        window_start = window_start_dt.isoformat()
        window_end = window_end_dt.isoformat()

        duration_seconds = max((window_end_dt - window_start_dt).total_seconds(), 1.0)
        duration_minutes = duration_seconds / 60.0
        records_per_minute = round(total_records / duration_minutes, 2)
    else:
        window_start = "unknown"
        window_end = "unknown"
        records_per_minute = 0.0

    return [
        {
            "pipeline_name": "signals_landing_pipeline",
            "records_processed": total_records,
            "window_start": window_start,
            "window_end": window_end,
            "records_per_minute": records_per_minute,
            "measurement_window": measurement_window,
        }
    ]


def build_late_data_metrics(records: list[dict[str, Any]], measurement_window: str) -> list[dict[str, Any]]:
    total_records = len(records)

    late_records = 0
    latest_late_rate = 0.0
    latest_total_count = total_records

    for record in records:
        lateness_sec = get_nested(record, "_decision", "lateness_sec", default=0)
        if isinstance(lateness_sec, (int, float)) and lateness_sec > 0:
            late_records += 1

        late_rate = get_nested(record, "_decision", "ops", "late_rate", default=None)
        total_count = get_nested(record, "_decision", "ops", "total_count", default=None)

        if isinstance(late_rate, (int, float)):
            latest_late_rate = late_rate

        if isinstance(total_count, int):
            latest_total_count = total_count

    late_percentage = round((late_records / total_records) * 100, 2) if total_records else 0.0

    return [
        {
            "pipeline_name": "signals_landing_pipeline",
            "late_records": late_records,
            "total_records": total_records,
            "late_percentage": late_percentage,
            "measurement_window": measurement_window,
        },
        {
            "pipeline_name": "signals_ops_window",
            "late_records": round(latest_late_rate * latest_total_count),
            "total_records": latest_total_count,
            "late_percentage": round(latest_late_rate * 100, 2),
            "measurement_window": "latest_ops_window",
        },
    ]


def build_quarantine_metrics(records: list[dict[str, Any]], measurement_window: str) -> list[dict[str, Any]]:
    quarantined_records = 0

    for record in records:
        status_anomaly = get_nested(record, "_decision", "ops", "status_anomaly", default=False)
        if status_anomaly is True:
            quarantined_records += 1

    return [
        {
            "pipeline_name": "signals_landing_pipeline",
            "quarantined_records": quarantined_records,
            "reason_breakdown": {
                "ops_anomaly": quarantined_records
            },
            "measurement_window": measurement_window,
        }
    ]


def write_metrics_snapshot(output_dir: Path, records: list[dict[str, Any]], measurement_window: str) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    throughput = build_throughput_metrics(records, measurement_window)
    late_data = build_late_data_metrics(records, measurement_window)
    quarantine = build_quarantine_metrics(records, measurement_window)

    with (output_dir / "throughput.json").open("w", encoding="utf-8") as f:
        json.dump(throughput, f, indent=2)

    with (output_dir / "late_data.json").open("w", encoding="utf-8") as f:
        json.dump(late_data, f, indent=2)

    with (output_dir / "quarantine.json").open("w", encoding="utf-8") as f:
        json.dump(quarantine, f, indent=2)