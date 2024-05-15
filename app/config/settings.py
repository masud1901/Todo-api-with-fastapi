from pydantic import BaseSettings


class Settings(BaseSettings):
    # Configure environment variables here
    DATABASE_URL: str

    class Config:
        env_file = ".env"


settings = Settings()
