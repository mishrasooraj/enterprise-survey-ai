from pydantic import BaseModel
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

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
    app_name: str = Field(default="Enterprise Survey AI - Authentication Service")
    app_env: str = Field(default="development")
    app_version: str = Field(default="1.0.0")
    log_level: str = Field(default="INFO")

    postgres_host: str = Field(default="localhost")
    postgres_port: int = Field(default=5432)
    postgres_db: str = Field(default="enterprise_survey_ai")
    postgres_user: str = Field(default="postgres")
    postgres_password: str = Field(default="postgres")
    database_schema: str = Field(default="public")
    database_url: str = Field(
        default="postgresql+asyncpg://postgres:postgres@localhost:5432/enterprise_survey_ai"
    )

    redis_host: str = Field(default="localhost")
    redis_port: int = Field(default=6379)
    redis_password: str = Field(default="")

    jwt_secret_key: str = Field(default="")
    jwt_refresh_secret_key: str = Field(default="")
    jwt_algorithm: str = Field(default="HS256")
    access_token_expire_minutes: int = Field(default=30)
    refresh_token_expire_days: int = Field(default=7)

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

    @property
    def jwt_refresh_secret(self) -> str:
        return self.jwt_refresh_secret_key or self.jwt_secret_key


settings = Settings()
