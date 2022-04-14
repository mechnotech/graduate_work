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

    def __init__(self, redis: Redis):
        self.redis = redis

    """
    ключ в редисе вида server_id.film_uuid.quality

    фукция put в идеале должна кинуть запрос и не дожидаясь ответа от redis
    отдать управление

    get_counter показывает запросы по серверу если остальное None
                            запросы по фильму независимо от качества
                            запросы по фильму с конкретным качеством
                            спросить про качество без фильма нельзя
    """
