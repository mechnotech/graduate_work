"""
Link endpoint
"""

import ipaddress

from http import HTTPStatus
from typing import Optional

from fastapi import (APIRouter,
                     Depends,
                     Request,
                     HTTPException)

from service.models.link import LinkResponse
from service.services.link import (LinkService,
                           get_link_service)

router = APIRouter()


@router.get('/link/whoami')
async def whoami(request: Request):
    return {'ip', request.headers.get('X-Real-IP')}


@router.get('/link/{film_uuid}/{quality}', response_model=LinkResponse)
async def get_link(request: Request,
                   film_uuid: str,
                   quality: int,
                   user_ip: Optional[str],
                   start: Optional[int] = None,
                   services: LinkService = Depends(get_link_service)
                   ) -> LinkResponse:

    if not user_ip:
        user_ip = request.headers.get('X-Real-IP')
        if not user_ip:
            user_ip = request.client.host

    print('Перехвачен IP - ', user_ip)

    try:
        user_ip = ipaddress.ip_address(user_ip)
    except ValueError:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                            detail='invalid ip address')

    ret = await services.get(request.state.broker,
                             user_ip,
                             film_uuid,
                             quality,
                             start)
    return ret
