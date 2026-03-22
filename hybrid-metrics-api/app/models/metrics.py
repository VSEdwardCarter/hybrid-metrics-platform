from pydantic import BaseModel, Field
from typing import List


class ThroughputMetric(BaseModel):
    pipeline_name: str = Field(..., example="signals_landing_pipeline")
    records_processed: int = Field(..., example=125000)
    window_start: str = Field(..., example="2026-03-21T23:00:00+00:00")
    window_end: str = Field(..., example="2026-03-21T23:59:59+00:00")
    records_per_minute: float = Field(..., example=2083.33)
    measurement_window: str = Field(..., example="total_cumulative")


class LateDataMetric(BaseModel):
    pipeline_name: str = Field(..., example="signals_landing_pipeline")
    late_records: int = Field(..., example=342)
    total_records: int = Field(..., example=25000)
    late_percentage: float = Field(..., example=1.37)
    measurement_window: str = Field(..., example="total_cumulative")


class QuarantineMetric(BaseModel):
    pipeline_name: str = Field(..., example="signals_landing_pipeline")
    quarantined_records: int = Field(..., example=89)
    reason_breakdown: dict[str, int] = Field(
        ...,
        example={
            "ops_anomaly": 35,
        },
    )
    measurement_window: str = Field(..., example="total_cumulative")


class ThroughputResponse(BaseModel):
    data: List[ThroughputMetric]


class LateDataResponse(BaseModel):
    data: List[LateDataMetric]


class QuarantineResponse(BaseModel):
    data: List[QuarantineMetric]