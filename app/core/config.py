from pydantic_settings import BaseSettings

class AppConfig(BaseSettings):
    app_name: str = "FastAPI Employee App"
    debug: bool = True
    version: str = "1.0.0"
    db_url: str = "sqlite:///./employees.db"
    api_token: str = "secrettoken123"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = AppConfig()
