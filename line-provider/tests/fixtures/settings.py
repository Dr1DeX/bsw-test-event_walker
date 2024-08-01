from pydantic_settings import BaseSettings


class Settings(BaseSettings):
   CACHE_HOST: str = 'localhost'
   CACHE_PORT: int = 6378
   CACHE_DB: int = 1

