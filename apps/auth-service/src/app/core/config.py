from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

_FILE_PATH = Path(__file__).resolve()
BASE_DIR = next(
    (parent for parent in _FILE_PATH.parents if (parent / ".env").exists()),
    _FILE_PATH.parents[4],
)


# ======================================================
# Grouped Models
# ======================================================

class ApplicationConfig(BaseModel):
    name: str
    env: str
    version: str
    log_level: str


class DatabaseConfig(BaseModel):
    host: str
    port: int
    db: str
    user: str
    password: str
    database_schema: str
    url: str


class RedisConfig(BaseModel):
    host: str
    port: int
    password: str


class JWTConfig(BaseModel):
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    refresh_token_expire_days: int


# ======================================================
# Main Settings
# ======================================================

class Settings(BaseSettings):

    # ---------- Application ----------
    app_name: str
    app_env: str
    app_version: str
    log_level: str

    # ---------- PostgreSQL ----------
    postgres_host: str
    postgres_port: int
    postgres_db: str
    postgres_user: str
    postgres_password: str
    database_schema: str
    database_url: str

    # ---------- Redis ----------
    redis_host: str
    redis_port: int
    redis_password: str = ""

    # ---------- JWT ----------
    jwt_secret_key: str
    jwt_algorithm: str
    access_token_expire_minutes: int
    refresh_token_expire_days: int

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
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
        return DatabaseConfig(
            host=self.postgres_host,
            port=self.postgres_port,
            db=self.postgres_db,
            user=self.postgres_user,
            password=self.postgres_password,
            database_schema=self.database_schema,
            url=self.database_url,
        )

    @property
    def redis(self) -> RedisConfig:
        return RedisConfig(
            host=self.redis_host,
            port=self.redis_port,
            password=self.redis_password,
        )

    @property
    def jwt(self) -> JWTConfig:
        return JWTConfig(
            secret_key=self.jwt_secret_key,
            algorithm=self.jwt_algorithm,
            access_token_expire_minutes=self.access_token_expire_minutes,
            refresh_token_expire_days=self.refresh_token_expire_days,
        )


settings = Settings()
