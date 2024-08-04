from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_HOST: str = 'localhost'
    DB_PORT: int = 5431
    DB_NAME: str = 'db-test'
    DB_USER: str = 'postgres'
    DB_PASSWORD: str = 'password'
