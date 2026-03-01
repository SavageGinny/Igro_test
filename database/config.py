from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    db_host: str = os.getenv('DB_HOST', 'localhost')
    db_port: int = int(os.getenv('DB_PORT', '5432'))
    db_name: str = os.getenv('DB_NAME', 'postgres')
    db_user: str = os.getenv('DB_USER', 'postgres')
    db_password: str = os.getenv('DB_PASSWORD', 'postgres')
    db_min_pool: int = int(os.getenv('DB_MIN_POOL', '1'))
    db_max_pool: int = int(os.getenv('DB_MAX_POOL', '1000'))

    @property
    def dsn(self) -> str:
        return (
            f"postgresql://{self.db_user}:"
            f"{self.db_password}@"
            f"{self.db_host}:"
            f"{self.db_port}/"
            f"{self.db_name}"
        )

    class Config:
        env_file = ".env"
        extra = "ignore"


settings: Settings = Settings()
