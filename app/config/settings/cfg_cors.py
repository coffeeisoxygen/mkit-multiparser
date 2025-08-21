from pydantic_settings import BaseSettings


class ConfigCors(BaseSettings):
    allow_origins: list[str] = ["*"]
    allow_credentials: bool = True
    allow_methods: list[str] = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    allow_headers: list[str] = ["*"]
