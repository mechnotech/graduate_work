import sys
import asyncio
import aiopg
import psycopg2
import async_timeout
from service.config import config


TRYS_SECONDS = 20


async def try_connect():
    """ async test connection """
    print("Try Postgresql connect")
    try:
        async with async_timeout.timeout(TRYS_SECONDS):
            while True:
                try:
                    conn = await aiopg.connect(user=config.db_user,
                                               password=config.db_password,
                                               host=config.db_host,
                                               timeout=1)
                    await conn.close()
                    print('Postgresql ready')
                    sys.exit(0)
                except psycopg2.Error:
                    print('Next try')
                    await asyncio.sleep(1)

    except asyncio.TimeoutError:
        sys.exit(1)


def main():
    asyncio.run(try_connect())


if __name__ == '__main__':
    main()
