import pytest
import pytest_asyncio
import aioredis

from service.config import config


REDIS_LINK = f'redis://{config.redis_host}'


@pytest_asyncio.fixture(scope='function')
async def redis_connect():

    connection = await aioredis.from_url(REDIS_LINK)
    yield connection
    await connection.close()


@pytest.mark.asyncio
async def test_example(redis_connect):
    """ """
    assert await redis_connect.ping()
