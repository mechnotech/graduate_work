"""
CDN Servers manager
"""
import abc
from typing import  (Optional,
                     List)

from .models import (FilmRequest,
                     CDNServerRecord)


class AbstractCDNManager(abc.ABC):

    @abc.abstractmethod
    def find_film(self,
                  cdn_request: FilmRequest) -> Optional(List[CDNServerRecord]):
        """ prepare list with accessible cdn servers """
