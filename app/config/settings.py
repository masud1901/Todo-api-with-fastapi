from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Configure environment variables here
    DATABASE_URL: str = "sqlite:///./sqlite3.db"
    SECRET_KEY: str
    ALGORITHM: str

    class Config:
        env_file = ".env"


settings = Settings()
