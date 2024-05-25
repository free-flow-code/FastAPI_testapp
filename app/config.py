from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_ignore_empty=True,
        extra="ignore"
    )

    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str = "postgres"
    DB_PASS: str = "root"
    DB_NAME: str = "mydb"
    JWT_SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ORIGINS: list = ["localhost:8000", "127.0.0.1:8000"]
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379


settings = Settings()
