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

    @abc.abstractmethod
    def file_move(self,
                  cdn_id_recipient: str,
                  file_uuid: str,
                  quality: List[str]):
        pass

#   @abc.abstractmethod
#   def cdn_list(self) -> List[CDNFileServerRecord]:
#       pass

#   @abc.abstractmethod
#   def cdn_add(self, new_cdn: CDNFileServerRecord) -> bool:
#       pass

#   @abc.abstractmethod
#   def cdn_remove(self, server_id: str) -> bool:
#       pass

#   @abc.abstractmethod
#   def file_list(self,
#                 server_id: str,
#                 film_uuid: str = None) -> List[CDNFilmiFileRecord]:
#       pass

#   @abc.abstractmethod
#   def file_add(self, new_file: CDNFilmiFileRecord) -> bool:
#       pass

#   @abc.abstractmethod
#   def file_delete(self, server_id: str, film_uuid: str, quality: str) -> bool:
#       pass
