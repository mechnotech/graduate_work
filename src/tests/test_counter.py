import uuid

import pytest
import pytest_asyncio
import aioredis

from service.balancer.counter import RedisCounter
from service.config import config


REDIS_LINK = f'redis://{config.redis_host}'


@pytest_asyncio.fixture(scope='function')
async def redis_connect():

    connection = await aioredis.from_url(REDIS_LINK)
    yield connection
    await connection.flushall(asynchronous=True)
    await connection.close()


@pytest.mark.asyncio
async def test_example(redis_connect):
    """ """
    assert await redis_connect.ping()


@pytest.mark.asyncio
async def test_simple_put(redis_connect):
    counter = RedisCounter(redis_connect)
    server_id = str(uuid.uuid4())
    film_uuid = str(uuid.uuid4())
    quality = '360'
    key = f'{server_id}.{film_uuid}.{quality}'
    value = 1
    await counter.put(server_id=server_id, film_uuid=film_uuid, quality=quality)
    result = await redis_connect.get(name=key)
    assert int(result) == value


@pytest.mark.asyncio
async def test_put_return_bool(redis_connect):
    counter = RedisCounter(redis_connect)
    server_id = str(uuid.uuid4())
    film_uuid = str(uuid.uuid4())
    quality = '360'
    result = await counter.put(server_id=server_id, film_uuid=film_uuid, quality=quality)
    assert isinstance(result, bool)


@pytest.mark.asyncio
async def test_simple_get(redis_connect):
    counter = RedisCounter(redis_connect)
    server_id = str(uuid.uuid4())
    film_uuid = str(uuid.uuid4())
    quality = '360'
    value = 1
    await counter.put(server_id=server_id, film_uuid=film_uuid, quality=quality)
    result = await counter.get_counter(server_id=server_id, film_uuid=film_uuid, quality=quality)
    assert result == value


@pytest.mark.asyncio
async def test_get_nonexistent_key(redis_connect):
    counter = RedisCounter(redis_connect)
    server_id = str(uuid.uuid4())
    film_uuid = str(uuid.uuid4())
    quality = '360'
    result = await counter.get_counter(server_id=server_id, film_uuid=film_uuid, quality=quality)
    assert result == 0


@pytest.mark.asyncio
async def test_get_none(redis_connect):
    counter = RedisCounter(redis_connect)
    result = await counter.get_counter(server_id=None)
    assert result == 0


@pytest.mark.asyncio
async def test_value_update(redis_connect):
    counter = RedisCounter(redis_connect)
    server_id = str(uuid.uuid4())
    film_uuid = str(uuid.uuid4())
    quality = '360'
    key = f'{server_id}.{film_uuid}.{quality}'
    value = 2
    await counter.put(server_id=server_id, film_uuid=film_uuid, quality=quality)
    await counter.put(server_id=server_id, film_uuid=film_uuid, quality=quality)
    result = await redis_connect.get(name=key)
    assert int(result) == value


@pytest.mark.asyncio
async def test_get_without_quality(redis_connect):
    counter = RedisCounter(redis_connect)
    server_id = str(uuid.uuid4())
    film_uuid = str(uuid.uuid4())
    quality = '360'
    await counter.put(server_id=server_id, film_uuid=film_uuid, quality=quality)
    quality = '720'
    await counter.put(server_id=server_id, film_uuid=film_uuid, quality=quality)
    result = await counter.get_counter(server_id=server_id, film_uuid=film_uuid)
    assert result == 2


@pytest.mark.asyncio
async def test_get_sever_stats_only(redis_connect):
    counter = RedisCounter(redis_connect)
    server_id = str(uuid.uuid4())
    film_uuid = str(uuid.uuid4())
    quality = '360'
    await counter.put(server_id=server_id, film_uuid=film_uuid, quality=quality)
    film_uuid = str(uuid.uuid4())
    quality = '1080'
    await counter.put(server_id=server_id, film_uuid=film_uuid, quality=quality)
    await counter.put(server_id=server_id, film_uuid=film_uuid, quality=quality)
    result = await counter.get_counter(server_id=server_id)
    assert result == 3
