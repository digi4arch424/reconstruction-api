from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # ── Database ──────────────────────────────────────────────────────────────
    database_url: str

    # ── Redis ─────────────────────────────────────────────────────────────────
    redis_url: str

    # ── Object storage ────────────────────────────────────────────────────────
    s3_endpoint:   str
    s3_bucket:     str = "spatialrecon"
    s3_access_key: str
    s3_secret_key: str
    s3_region:     str = "auto"

    # ── App ───────────────────────────────────────────────────────────────────
    environment: str = "development"
    api_port:    int = 8000

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
