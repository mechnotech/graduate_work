
"""
swager - http://localhost:8080/api/openapi
"""
import aiopg

from fastapi import (FastAPI,
                     Request)
from fastapi.responses import JSONResponse

from service.api.v1 import link

from service.balancer.broker import MainBroker
from service.balancer.iprouter import IpRouter
from service.balancer.cdnmanager import MainCDNManager

from service.config import config
from service.balancer.cdnmanager.create_db import recreate

class BrokerWrap():

    def __init__(self):
        self.broker = None
        self.db_conn = None

    async def connect(self):
        if self.broker is None:
            self.db_conn = await aiopg.connect(user=config.db_user,
                                               password=config.db_password,
                                               host=config.db_host,
                                               database=config.db_base,
                                               timeout=1)
            ip_router = IpRouter()
            cdn_manager = MainCDNManager(self.db_conn)

            self.broker = MainBroker(ip_router=ip_router,
                                     cdn_manager=cdn_manager)


def create_app():
    app = FastAPI(title='CDN API',
                  docs_url='/api/openapi',
                  openapi_url='/api/openapi.json',
                  default_response_class=JSONResponse)

    broker_wrap = BrokerWrap()

    @app.middleware("http")
    async def broker_session_middleware(request: Request, call_next):
        request.state.broker = broker_wrap.broker
        response = await call_next(request)
        return response

    @app.on_event('startup')
    async def startup():
        if config.db_recreate:
            await recreate()
        await broker_wrap.connect()

    @app.on_event('shutdown')
    async def shutdown():
        await broker_wrap.db_conn.close()

    app.include_router(link.router, prefix='/api/v1', tags=['link'])

    return app
