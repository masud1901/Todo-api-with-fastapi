from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Configure environment variables here
    DATABASE_URL: str = "sqlite:///./todos.db"

    class Config:
        env_file = ".env"


settings = Settings()
