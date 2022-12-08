from pydantic import BaseSettings, PostgresDsn


class Settings(BaseSettings):
    database_url: PostgresDsn
    algorithm: str
    jwt_key: str

    class Config:
        env_file = ".env"


settings = Settings()
