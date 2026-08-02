from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    app_name: str = "Enterprise Survey AI"

    app_env: str = "development"

    postgres_host: str = "postgres"

    postgres_port: int = 5432

    postgres_user: str

    postgres_password: str

    postgres_db: str

    redis_host: str = "redis"

    redis_port: int = 6379

    kafka_bootstrap_servers: str = "kafka:9092"

    ollama_host: str = "http://ollama:11434"

    qdrant_host: str = "qdrant"

    qdrant_port: int = 6333

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()   