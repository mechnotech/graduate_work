
"""
swager - http://localhost:8080/api/openapi
"""

from fastapi import (FastAPI,
                     Request)
from fastapi.responses import JSONResponse

from service.api.v1 import link

from service.balancer.broker import MainBroker


def create_app():
    app = FastAPI(title='CDN API',
                  docs_url='/api/openapi',
                  openapi_url='/api/openapi.json',
                  default_response_class=JSONResponse)
    broker = MainBroker()

    @app.middleware("http")
    async def broker_session_middleware(request: Request, call_next):
        request.state.broker = broker
        response = await call_next(request)
        return response

    @app.on_event('startup')
    async def startup():
        pass

    @app.on_event('shutdown')
    async def shutdown():
        pass

    app.include_router(link.router, prefix='/api/v1', tags=['link'])

    return app
