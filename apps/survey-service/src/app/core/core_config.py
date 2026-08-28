from pathlib import Path

from pydantic import BaseModel
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


_BASE_DIR = Path(__file__).resolve()


class ApplicationConfig(BaseModel):
    name: str
    env: str
    version: str
    log_level: str


class DatabaseConfig(BaseModel):
    url: str


class JWTConfig(BaseModel):
    secret_key: str
    algorithm: str


class KafkaConfig(BaseModel):
    bootstrap_servers: str | None
    topic_prefix: str


class Settings(BaseSettings):
    app_name: str = Field(default="Enterprise Survey AI - Survey Service")
    app_env: str = Field(default="development")
    app_version: str = Field(default="1.0.0")
    log_level: str = Field(default="INFO")
    database_url: str = Field(default="postgresql+asyncpg://postgres:postgres@localhost:5432/enterprise_survey_ai")
    jwt_secret_key: str = Field(default="")
    jwt_algorithm: str = Field(default="HS256")
    kafka_bootstrap_servers: str | None = Field(default=None)
    kafka_topic_prefix: str = Field(default="survey-service")

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def app(self) -> ApplicationConfig:
        return ApplicationConfig(
            name=self.app_name,
            env=self.app_env,
            version=self.app_version,
            log_level=self.log_level,
        )

    @property
    def database(self) -> DatabaseConfig:
        return DatabaseConfig(url=self.database_url)

    @property
    def jwt(self) -> JWTConfig:
        return JWTConfig(secret_key=self.jwt_secret_key, algorithm=self.jwt_algorithm)

    @property
    def kafka(self) -> KafkaConfig:
        return KafkaConfig(
            bootstrap_servers=self.kafka_bootstrap_servers,
            topic_prefix=self.kafka_topic_prefix,
        )


settings = Settings()
