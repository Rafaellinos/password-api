from functools import lru_cache
from pydantic import BaseSettings, PostgresDsn, Field
import os

ENV_FILE = '.config'


class Settings(BaseSettings):
    DEBUG: bool = Field(..., env="debug")
    DATABASE_URL: PostgresDsn = Field(..., env="bd_url")
    SECRET_KEY: str = "afe99645a1078d18524d735a0915f354ed09db42443003938b32b200c802dc4a"
    APP_NAME = 'PasswordAPP'
    REGISTRATION_TOKEN_LIFETIME = 60 * 60 * 24 * 7  # one week
    TOKEN_ALGORITHM = 'HS256'
    API_PREFIX = '/api'
    HOST = '0.0.0.0'
    PORT = 8000
    BASE_URL = '{}:{}'.format(HOST, str(PORT))

    class Config:
        case_sensitive: bool = True


@lru_cache()
def get_settings():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    return Settings(
        _env_file=f'{dir_path}/{ENV_FILE}',
        _env_file_encoding='utf-8',
    )
