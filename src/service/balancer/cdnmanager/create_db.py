"""
create db
"""
import aiopg
import logging

from service.config import config

CREATE_SQL_FILE = 'service/balancer/cdnmanager/create.sql'


async def recreate(extra_sql: list[str] = None) -> None:
    """ drop database and create new copy
    """
    conn = await aiopg.connect(user=config.db_user,
                               password=config.db_password,
                               host=config.db_host,
                               timeout=10)
    async with conn.cursor() as cur:
        await cur.execute("DROP DATABASE IF EXISTS cdn;")
    # await conn.commit()
    async with conn.cursor() as cur:
        await cur.execute("CREATE DATABASE cdn;")
    await conn.close()
    logging.info('Recreate database')

    conn = await aiopg.connect(user=config.db_user,
                               password=config.db_password,
                               host=config.db_host,
                               database=config.db_base,
                               timeout=10)

    with open(CREATE_SQL_FILE, 'rt') as file_obj:
        sql_text = file_obj.read()
    async with conn.cursor() as cur:
        await cur.execute(sql_text)
    logging.info('Create tables')

    await conn.close()
