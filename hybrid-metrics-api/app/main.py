from fastapi import FastAPI
from app.api.routes.metrics import router as metrics_router

app = FastAPI(
    title="Hybrid Metrics API",
    description="On-prem API exposing aggregated pipeline metrics for cloud dashboards",
    version="0.1.0",
)

app.include_router(metrics_router, prefix="/metrics", tags=["metrics"])


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}