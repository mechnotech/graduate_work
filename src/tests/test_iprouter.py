import random
from ipaddress import IPv4Address
import uuid

import pytest

from service.balancer.iprouter import IpRouter, CDN_BUSY_LIMIT
from service.balancer.models import CDNServerRecord, QUALITY, FilmRequest


def get_rand_id():
    return str(uuid.uuid4())


def get_rand_ip():
    return IPv4Address(random.randint(100000, 4294967295))


def get_rand_quality():
    return random.sample(QUALITY, random.randint(1, 8))


@pytest.fixture(scope='function')
def init_params():
    def get_server_records(quantity):
        server_records = []
        for i in range(quantity):
            body = {
                'cdn_server_id': get_rand_id(),
                'cdn_server_ip': get_rand_ip(),
                'loading': round(random.random(), 2),
                'file_uuid': get_rand_id(),
                'quality': get_rand_quality(),
            }

            server_records.append(CDNServerRecord(**body))
        return server_records

    def get_film_request():
        body = {
            'user_ip': IPv4Address('190.129.19.9'),
            'file_uuid': get_rand_id(),
            'quality': '360',
        }
        return FilmRequest(**body)

    servers = get_server_records(10)
    film_request = get_film_request()
    router = IpRouter()
    ret = [servers, film_request, router]
    return ret


@pytest.mark.asyncio
async def test_sever_not_busy(init_params):
    """
    Выбран сервер с допустимой загруженностью CDN_BUSY_LIMIT (все остальные заняты)
    """
    less_load_score = 0.1
    servers = init_params[0]
    for serv in servers:
        serv.loading = 1
    servers[-1].loading = less_load_score
    film_request = init_params[1]
    router = init_params[2]
    res = await router.select_cdn(cdn_servers=servers, cdn_request=film_request)
    assert res.loading < CDN_BUSY_LIMIT


@pytest.mark.asyncio
async def test_barely_live_server(init_params):
    """
    Выбран сервер с минимальной загруженностью даже если он выше CDN_BUSY_LIMIT (все остальные заняты)
    """
    load_score = 0.99
    servers = init_params[0]
    for serv in servers:
        serv.loading = 1
    servers[-1].loading = load_score
    film_request = init_params[1]
    router = init_params[2]
    res = await router.select_cdn(cdn_servers=servers, cdn_request=film_request)
    assert res.loading == load_score


@pytest.mark.asyncio
async def test_sever_has_quality(init_params):
    """
    Сервер имеет фильм в качестве не менее чем запрошенное
    """
    servers = init_params[0]
    film_request = init_params[1]
    router = init_params[2]
    res = await router.select_cdn(cdn_servers=servers, cdn_request=film_request)
    server_quality = [int(x) for x in res.quality]
    server_quality.sort(reverse=True)
    assert server_quality[0] >= int(film_request.quality)


@pytest.mark.asyncio
async def test_sever_closest(init_params):
    """
    Сервер выбирается ближайший к пользователю (тест: из одной подсети)
    """
    servers = init_params[0]
    film_request = init_params[1]
    film_request.user_ip = IPv4Address('217.117.176.19')
    candidate = servers[0]
    candidate.cdn_server_ip = IPv4Address('217.117.178.200')
    candidate.loading = 0.70
    router = init_params[2]
    res = await router.select_cdn(cdn_servers=servers, cdn_request=film_request)
    assert res.cdn_server_ip == candidate.cdn_server_ip
