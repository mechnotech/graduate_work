"""
Ip router class
"""

import abc

from typing import List

from .models import (FilmRequest,
                     CDNServerRecord)


class AbstractIpRouter(abc.ABC):

    @abc.abstractmethod
    async def select_cdn(self,
                         cdn_request: FilmRequest,
                         cdn_servers: List[CDNServerRecord]) -> CDNServerRecord:
        """ select better cdn server """


class SimpleIpRouter(AbstractIpRouter):
    async def select_cdn(self,
                         cdn_request: FilmRequest,
                         cdn_servers: List[CDNServerRecord]) -> CDNServerRecord:
        return cdn_servers[0]
