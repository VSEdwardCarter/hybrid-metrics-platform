from fastapi import APIRouter
from app.models.metrics import (
    ThroughputResponse,
    LateDataResponse,
    QuarantineResponse,
)
from app.services.metrics_service import metrics_service

router = APIRouter()


# -------------------------
# Total / cumulative metrics
# -------------------------

@router.get("/throughput", response_model=ThroughputResponse)
def get_throughput_metrics() -> ThroughputResponse:
    return ThroughputResponse(data=metrics_service.get_throughput_metrics())


@router.get("/late-data", response_model=LateDataResponse)
def get_late_data_metrics() -> LateDataResponse:
    return LateDataResponse(data=metrics_service.get_late_data_metrics())


@router.get("/quarantine", response_model=QuarantineResponse)
def get_quarantine_metrics() -> QuarantineResponse:
    return QuarantineResponse(data=metrics_service.get_quarantine_metrics())


# -------------------------
# Current / latest-window metrics
# -------------------------

@router.get("/current/throughput", response_model=ThroughputResponse)
def get_current_throughput_metrics() -> ThroughputResponse:
    return ThroughputResponse(data=metrics_service.get_current_throughput_metrics())


@router.get("/current/late-data", response_model=LateDataResponse)
def get_current_late_data_metrics() -> LateDataResponse:
    return LateDataResponse(data=metrics_service.get_current_late_data_metrics())


@router.get("/current/quarantine", response_model=QuarantineResponse)
def get_current_quarantine_metrics() -> QuarantineResponse:
    return QuarantineResponse(data=metrics_service.get_current_quarantine_metrics())