from pydantic_settings import BaseSettings
from pydantic import validator
class Settings(BaseSettings):
    SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int
    ENCRYPTION_KEY: str
    EMAIL_SENDER: str
    EMAIL_PASSWORD: str

    @validator("REFRESH_TOKEN_EXPIRE_DAYS", pre=True)
    def parse_refresh_token_expire_days(cls, v):
        return int(v)  # Преобразуем значение в число, если оно передается строкой

    # База данных
    DB1_HOST: str
    DB1_PORT: int
    DB1_NAME: str
    DB1_USER: str
    DB1_PASSWORD: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "allow"
settings = Settings()