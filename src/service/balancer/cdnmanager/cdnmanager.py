"""
CDN Servers manager
"""
import abc

from typing import (Optional,
                    List)

from service.balancer.models import (FilmRequest,
                                     FilmResponse,
                                     CDNServerRecord)

from .models import (CDNFileServerRecord,
                     CDNFilmFileRecord)


class AbstractCDNManager(abc.ABC):

    @abc.abstractmethod
    async def find(self,
                   cdn_request: FilmRequest) -> Optional[List[CDNServerRecord]]:
        """ prepare list with accessible cdn servers """

    @abc.abstractmethod
    async def prepare(self,
                      cdn_request: FilmRequest,
                      cdn_server_select: CDNServerRecord) -> FilmResponse:
        """ Return complete response for broker """


class AbstractCDNFileManager(AbstractCDNManager):
    """ Abstract CDN File Manager """
