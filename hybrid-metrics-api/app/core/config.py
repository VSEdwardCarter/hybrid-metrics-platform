from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Hybrid Metrics API"
    environment: str = "dev"

    metrics_root_dir: str = "data/metrics"
    total_metrics_dir: str = "data/metrics/total"
    current_metrics_dir: str = "data/metrics/current"
    landing_signals_dir: str = "/tmp/landing-signals"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()