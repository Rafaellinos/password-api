import os
from functools import lru_cache
from secrets import token_hex
from pydantic import BaseSettings, PostgresDsn, Field

ENV_FILE = '.config'


class Settings(BaseSettings):
    DEBUG: bool = Field(..., env="debug")
    DATABASE_URL: PostgresDsn = Field(..., env="bd_url")
    SECRET_KEY: str = Field(..., env="secret")
    APP_NAME: str = Field(..., env="name")
    REGISTRATION_TOKEN_LIFETIME: int = 60 * 60 * 24 * 7  # one week
    TOKEN_ALGORITHM: str = 'HS256'
    API_PREFIX: str = '/api'
    HOST: str = Field(..., env="host")
    PORT: int = Field(..., env="port")
    BASE_URL = '{}:{}'.format(HOST, str(PORT))
    ALLOWED_HOSTS: str = ""

    class Config:
        case_sensitive: bool = True


@lru_cache()
def get_settings():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    settings = Settings(
        _env_file=f'{dir_path}/{ENV_FILE}',
        _env_file_encoding='utf-8',
    )
    if not settings.SECRET_KEY:
        settings.SECRET_KEY = token_hex(32)
    return settings
