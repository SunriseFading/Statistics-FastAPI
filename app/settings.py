from dotenv import load_dotenv
from pydantic import BaseSettings, Field

load_dotenv(dotenv_path="../")


class Settings(BaseSettings):
    DATABASE_URL: str = Field(env="DATABASE_URL")

    class Config:
        env_file = "../.env"
        env_file_encoding = "utf-8"


settings = Settings()
