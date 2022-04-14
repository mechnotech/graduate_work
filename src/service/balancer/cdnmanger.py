"""
CDN Servers manager
"""
import abc
from typing import (Optional,
                    List)

from .models import (FilmRequest,
                     FilmResponse,
                     CDNServerRecord)


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

    @abc.abstractmethod
    def cdn_list(self):
        pass

    @abc.abstractmethod
    def cdn_add(self):
        pass

    @abc.abstractmethod
    def cdn_remove():
        pass

    @abc.abstractmethod
    def file_list(self, cdn_id: str):
        pass

    @abc.abstractmethod
    def file_move(self,
                  cdn_id_recipient: str,
                  file_uuid: str,
                  quality: List[str]):
        pass


class SimpleCDNManager(AbstractCDNManager):
    pass
