"""
Service start point
"""

import uvicorn

from service.config import config
from service.logger import LOGGING
from service.app import create_app


app = create_app()

def volumes_check():
    # удалить после появления полноценных тестов
    with open('data/cdn_main/hint.txt', 'wt') as fobj:
        fobj.write('cdn main')
    with open('data/cdn_1/hint.txt', 'wt') as fobj:
        fobj.write('cdn 1')
    with open('data/cdn_2/hint.txt', 'wt') as fobj:
        fobj.write('cdn 2')


if __name__ == '__main__':
    volumes_check()
    uvicorn.run(
        'main:app',
        host=config.api_host,
        port=config.api_port,
        log_config=LOGGING,
        log_level=config.api_loglevel,
        reload=True,
    )
