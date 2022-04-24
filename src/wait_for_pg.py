
import logging
import sys

import asyncio
import aiopg
import psycopg2
import async_timeout
from service.config import config


TRYS_SECONDS = 20


logging.basicConfig(level=logging.INFO)


async def try_connect():
    """ async test connection """
    logging.info("Try Postgresql connect")
    try:
        async with async_timeout.timeout(TRYS_SECONDS):
            while True:
                try:
                    conn = await aiopg.connect(user=config.db_user,
                                               password=config.db_password,
                                               host=config.db_host,
                                               timeout=1)
                    await conn.close()
                    logging.info('Postgresql ready')
                    sys.exit(0)
                except psycopg2.Error:
                    logging.warning("Can't connect waiting for next try")
                    await asyncio.sleep(1)

    except asyncio.TimeoutError:
        logging.critical("Can't connect")
        sys.exit(1)


def main():
    asyncio.run(try_connect())


if __name__ == '__main__':
    main()
