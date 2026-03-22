from pathlib import Path

from app.core.config import settings
from scripts.metrics_common import (
    find_all_jsonl_files,
    find_jsonl_files_in_partition,
    find_latest_partition_dir,
    read_jsonl_records,
    write_metrics_snapshot,
)


def main() -> None:
    input_dir = Path(settings.landing_signals_dir)
    metrics_root_dir = Path(settings.metrics_root_dir)

    total_output_dir = metrics_root_dir / "total"
    current_output_dir = metrics_root_dir / "current"

    latest_partition_dir = find_latest_partition_dir(input_dir)

    current_files = find_jsonl_files_in_partition(latest_partition_dir)
    current_records = read_jsonl_records(current_files)

    total_files = find_all_jsonl_files(input_dir)
    total_records = read_jsonl_records(total_files)

    write_metrics_snapshot(
        output_dir=current_output_dir,
        records=current_records,
        measurement_window="latest_partition",
    )

    write_metrics_snapshot(
        output_dir=total_output_dir,
        records=total_records,
        measurement_window="total_cumulative",
    )

    print("Mode: incremental_load")
    print(f"Latest partition: {latest_partition_dir}")
    print(f"Current files: {len(current_files)}")
    print(f"Current records: {len(current_records)}")
    print(f"Total files: {len(total_files)}")
    print(f"Total records: {len(total_records)}")
    print(f"Wrote current metrics to: {current_output_dir.resolve()}")
    print(f"Wrote total metrics to: {total_output_dir.resolve()}")


if __name__ == "__main__":
    main()