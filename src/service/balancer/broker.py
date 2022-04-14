"""
Link balancer entry point

"""

import abc
import logging
from typing import Optional

from .models import (FilmRequest,
                     FilmResponse,
                     CDNServerRecord)
from .iprouter import AbstractIpRouter
from .cdnmanger import AbstractCDNManager


class AbstractBroker(abc.ABC):
    """ Abstract link broker """

    @abc.abstractmethod
    async def calc_link(self,
                        film_response: FilmResponse,
                        cdn_server_select: CDNServerRecord) -> bool:
        """ mark link in cache for balancer  """
        pass

    @abc.abstractmethod
    async def get_link(self,
                       cdn_request: FilmRequest) -> Optional[FilmResponse]:
        """ Return nearest cdn link
            If didn't find quality return nearest bette
            If didn't find film return None
        """
        pass


class MainBroker(AbstractBroker):

    def __init__(self,
                 ip_router: AbstractIpRouter,
                 cdn_manager: AbstractCDNManager):
        self.ip_router = ip_router
        self.cdn_manager = cdn_manager

    async def calc_link(self,
                        film_response: FilmResponse,
                        cdn_server_select: CDNServerRecord) -> bool:
        msg = "generata link for server {cdn_server_select.cdn_server_id}"
        logging.info(msg)
        return True

    async def get_link(self,
                       cdn_request: FilmRequest) -> Optional[FilmResponse]:

        cdn_server_records = await self.cdn_manager.find(cdn_request)

        if cdn_server_records is None or not cdn_server_records:
            return None

        cdn_server_select = await self.ip_router.select_cdn(cdn_request,
                                                            cdn_server_records)

        film_response = await self.cdn_manager.prepare(cdn_request,
                                                       cdn_server_select)
        await self.calc_link(film_response, cdn_server_select)
        return film_response
