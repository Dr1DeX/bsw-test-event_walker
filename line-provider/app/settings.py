from pydantic_settings import BaseSettings


class Settings(BaseSettings):
   CACHE_HOST: str = 'localhost'
   CACHE_PORT: int = 6379
   CACHE_DB: int = 0

