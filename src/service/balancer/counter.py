"""
Считаем что и откуда отадли
работате через aioredis
https://aioredis.readthedocs.io/en/latest/getting-started/
"""

import abc
from typing import Optional

from aioredis import Redis


class AbstractCounter(abc.ABC):

    @abc.abstractmethod
    async def put(self, server_id: str, film_uuid: str, quality: str) -> bool:
        """ Save link request """

    @abc.abstractmethod
    async def get_counter(self,
                          server_id: str,
                          film_uuid: Optional[str],
                          quality: Optional[str]) -> int:
        """ Return request count"""


class RedisCounter(AbstractCounter):

    def __init__(self, redis: Redis, ttl: int = 5):
        self.redis = redis
        self.ttl = ttl

    async def put(self, server_id: str, film_uuid: str, quality: str) -> bool:
        key = f'{server_id}.{film_uuid}.{quality}'
        await self.redis.incr(name=key)
        await self.redis.expire(name=key, time=self.ttl)
        return True

    async def get_counter(self,
                          server_id: str,
                          film_uuid: Optional[str] = None,
                          quality: Optional[str] = None) -> int:

        async def scan_values(key):
            cnt = 0
            async for k in self.redis.scan_iter(match=key + '*'):
                res = await self.redis.get(name=k)
                if res:
                    cnt += int(res)
            return cnt

        if not film_uuid and quality:
            return 0

        if film_uuid and not quality:
            result = await scan_values(f'{server_id}.{film_uuid}')

        elif not film_uuid and not quality:
            result = await scan_values(f'{server_id}')

        else:
            result = await self.redis.get(name=f'{server_id}.{film_uuid}.{quality}')

        if result is None:
            return 0
        return int(result)

    """
    ключ в редисе вида server_id.film_uuid.quality

    фукция put в идеале должна кинуть запрос и не дожидаясь ответа от redis
    отдать управление

    get_counter показывает запросы по серверу если остальное None +
                            запросы по фильму независимо от качества +
                            запросы по фильму с конкретным качеством +
                            спросить про качество без фильма нельзя +
    """
