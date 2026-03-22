from pathlib import Path

from app.core.config import settings
from scripts.metrics_common import (
    find_all_jsonl_files,
    read_jsonl_records,
    write_metrics_snapshot,
)


def main() -> None:
    input_dir = Path(settings.landing_signals_dir)
    output_dir = Path(settings.metrics_root_dir) / "baseline"

    files = find_all_jsonl_files(input_dir)
    records = read_jsonl_records(files)

    write_metrics_snapshot(
        output_dir=output_dir,
        records=records,
        measurement_window="historical_baseline",
    )

    print(f"Mode: initial_load")
    print(f"Scanned files: {len(files)}")
    print(f"Loaded records: {len(records)}")
    print(f"Wrote baseline metrics to: {output_dir.resolve()}")


if __name__ == "__main__":
    main()