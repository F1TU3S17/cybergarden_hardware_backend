from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Hack Backend"
    DEBUG: bool = True
    DATABASE_URL: str = "sqlite:///./test.db"

    class Config:
        env_file = ".env"


settings = Settings()
