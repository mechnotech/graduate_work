"""
config file
"""

import logging

from pydantic import (BaseSettings,
                      Field)


class BaseConfig(BaseSettings):
    api_host: str = Field(default='0.0.0.0', env='CDN_API_HOST')
    api_port: int = Field(default=8080, env='CDN_API_PORT')
    api_loglevel: int = Field(default=logging.DEBUG,
                              env='CDN_API_DEBUG_LEVEL')

    db_recreate: bool = Field(default=False, env='CDN_DB_RECREATE')
    db_user: str = Field(default='postgres', env='CDN_DB_USER')
    db_password: str = Field(default='password', env='CDN_DB_PASSWORD')
    db_host: str = Field(default='localhost', env='CDN_DB_HOST')
    db_base: str = Field(default='cdn', env='CDN_DB_BASE')

    redis_host: str = Field(default='localhost', env='CDN_REDIS_HOST')

    cdn_main: str = Field(default='data/cdn_main', env='CDN_STOR_MAIN')
    cdn_1: str = Field(default='data/cdn_1', env='CDN_STOR_1')
    cdn_2: str = Field(default='data/cdn_2', env='CDN_STOR_2')

    cdn_var_expiration_def: int = Field(default=60*180, env='CDN_V_EXPIRATION_DEF')
    cdn_var_expiration_mul: float = Field(default=1.2, env='CDN_V_EXPERATION_MUL')

    cdn_counter_expiration: int = Field(default=60*60, env='CDN_COUNTER_EXPIRATION')

    cdn_busy_limit: float = Field(default=0.95, env='CDN_BUSY_LIMIT')


config = BaseConfig()
