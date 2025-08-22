from pydantic_settings import BaseSettings


class ConfigModule(BaseSettings):
    username: str
    password: str
    baseurl: str
    pin: str
    email: str
    msisdn: str
    pmla: str
    pmgs: str
