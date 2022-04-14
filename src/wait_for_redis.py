import sys

import asyncio
import aioredis
import async_timeout

from aioredis.exceptions import ConnectionError

from service.config import config

TRYS_SECONDS = 20
REDIS_LINK = f'redis://{config.redis_host}'


async def try_connect():
    """ async test connection """
    print("Try Redis connect")
    connection = await aioredis.from_url(REDIS_LINK)
    try:
        async with async_timeout.timeout(TRYS_SECONDS):
            while True:
                try:
                    await connection.ping()
                    print('Redis ready')
                    await connection.close()
                    sys.exit(0)
                except ConnectionError:
                    print('Next try')
                    await asyncio.sleep(1)
    except asyncio.TimeoutError:
        await connection.close()
        sys.exit(1)


def main():
    asyncio.run(try_connect())


if __name__ == '__main__':
    main()
