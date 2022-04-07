
"""
swager - http://localhost:8080/api/openapi
"""

import logging
import uvicorn


from fastapi import FastAPI
from fastapi.responses import JSONResponse

from config import config
from logger import LOGGING

from api.v1 import test

app = FastAPI(
    title='CDN API',
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=JSONResponse)


@app.on_event('startup')
async def startup():
    pass


@app.on_event('shutdown')
async def shutdown():
    pass


app.include_router(test.router, prefix='/api/v1', tags=['test'])


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
