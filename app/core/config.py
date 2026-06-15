from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "AWS Cost Guardian"
    database_url: str = "postgresql+psycopg://acg:acg-pass@db:5432/acg"
    aws_region: str = "us-east-1"
    aws_profile: str | None = None
    aws_cost_alert_threshold: float = 100.0

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore",
    }


settings = Settings()
