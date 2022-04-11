"""
Link balancer entry point

"""

import abc

from typing import Optional

from .models import (FilmRequest,
                     FilmResponse)


class AbstractBroker(abc.ABC):
    """ Abstract link broker """

    @abc.abstractmethod
    async def get_link(self,
                       cdn_request: FilmRequest) -> Optional[FilmResponse]:
        """ Return nearest cdn link
            If didn't find quality return nearest bette
            If didn't find film return None
        """


class MainBroker(AbstractBroker):

    def __init__(self):
        self.ip_router = None
        self.cdn_manager = None

    async def get_link(self,
                       cdn_request: FilmRequest) -> Optional[FilmResponse]:
        return "I'm live !"
