"""
Test service.services.link.get
"""

import uuid
from typing import Optional

import pytest
from fastapi import HTTPException

from service.balancer.broker import AbstractBroker
from service.balancer.models import (FilmRequest,
                                     FilmResponse)
from service.services.link import LinkService
from service.config import config


class TestBroker(AbstractBroker):

    async def get_link(self,
                       cdn_request: FilmRequest) -> Optional[FilmResponse]:
        if cdn_request.file_uuid.startswith('1'):
            return None
        elif cdn_request.file_uuid.startswith('2'):
            return FilmResponse(path='uuid-file.360.mp4',
                                cdn_server_url='http://10.10.10.1/',
                                cdn_server_key=str(uuid.uuid4()),
                                length_sec=None)
        elif cdn_request.file_uuid.startswith('3'):
            return FilmResponse(lpath='uuid-file.360.mp4',
                                cdn_server_url='http://10.10.10.1/',
                                cdn_server_key=str(uuid.uuid4()),
                                length_sec=8200)


@pytest.fixture(scope='function')
def init_params():

    broker = TestBroker()
    user_ip = '192.168.1.2'
    file_uuid = str(uuid.uuid4())
    quality = 360
    start = 0
    ret = list([broker, user_ip, file_uuid, quality, start])
    return ret


@pytest.mark.asyncio
async def test_link_get_404(init_params):
    link_service = LinkService()
    init_params[2] = '1' + init_params[2][1:]
    with pytest.raises(HTTPException):
        _ = await link_service.get(*init_params)


@pytest.mark.asyncio
async def test_link_get_start_position(init_params):
    link_service = LinkService()
    init_params[4] = 123456
    init_params[2] = '2' + init_params[2][1:]
    response = await link_service.get(*init_params)

    assert response.start_position == 123456
    assert '123456' in response.link


@pytest.mark.asyncio
async def test_lint_get_def_length_sec(init_params):
    link_service = LinkService()
    init_params[2] = '2' + init_params[2][1:]
    response = await link_service.get(*init_params)

    assert response.length_sec == config.cdn_var_expiration_def
