from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    HUBSPOT_API_KEY: str
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/crm_sync"
    POLL_INTERVAL_SECONDS: int = 60
    WEBHOOK_SECRET: str = "changeme"

    class Config:
        env_file = ".env"


settings = Settings()
