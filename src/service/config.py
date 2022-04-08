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

    cdn_main: str = Field(default='data/cdn_main', env='CDN_STOR_MAIN')
    cdn_1: str = Field(default='data/cdn_1', env='CDN_STOR_1')
    cdn_2: str = Field(default='data/cdn_2', env='CDN_STOR_2')


config = BaseConfig()