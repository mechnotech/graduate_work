"""
Test main broker
"""

import pytest
import uuid

from ipaddress import IPv4Address
from typing import (List,
                    Optional)

from service.balancer.models import (FilmRequest,
                                     FilmResponse,
                                     CDNServerRecord)
from service.balancer.iprouter import AbstractIpRouter
from service.balancer.cdnmanager import AbstractCDNManager
from service.balancer.broker import MainBroker

FILE_UUID = str(uuid.uuid4())


class TestIpRouter(AbstractIpRouter):

    async def select_cdn(self,
                         cdn_request: FilmRequest,
                         cdn_servers: List[CDNServerRecord]) -> CDNServerRecord:
        return cdn_servers[0]


class TestCDNManager(AbstractCDNManager):

    async def find(self,
                   cdn_request: FilmRequest) -> Optional[List[CDNServerRecord]]:
        if cdn_request.file_uuid.startswith('1'):
            return None
        if cdn_request.file_uuid.startswith('2'):
            return [CDNServerRecord(cdn_server_id='cdn_1',
                                    cdn_server_ip=IPv4Address('192.168.1.222'),
                                    loading=0.5,
                                    file_uuid=FILE_UUID,
                                    quality=["240", "360"]), ]

    async def prepare(self,
                      cdn_request: FilmRequest,
                      cdn_server_select: CDNServerRecord) -> FilmResponse:
        return FilmResponse(path=cdn_request.file_uuid,
                            cdn_server_url=cdn_server_select.cdn_server_id,
                            cdn_server_key='secure_key',
                            length_sec=2500)


@pytest.fixture(scope='function')
def ip_router():
    return TestIpRouter()


@pytest.fixture(scope='function')
def cdn_manager():
    return TestCDNManager()


@pytest.mark.asyncio
async def test_get_link(ip_router, cdn_manager):

    broker = MainBroker(ip_router, cdn_manager)

    film_request = FilmRequest(user_ip=IPv4Address('127.0.0.1'),
                               file_uuid='1a3b298e-d679-4f88-be71-4d1522d4542d',
                               quality='360')

    film_response = await broker.get_link(film_request)
    assert film_response is None

    file_uuid = '2a3b298e-d679-4f88-be71-4d1522d4542d'
    film_request = FilmRequest(user_ip=IPv4Address('127.0.0.1'),
                               file_uuid=file_uuid,
                               quality='480')
    film_response = await broker.get_link(film_request)
    assert film_response.path == file_uuid
    assert film_response.cdn_server_url == 'cdn_1'
