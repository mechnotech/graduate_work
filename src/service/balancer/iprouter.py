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


async def closest_distance(servers: List[CDNServerRecord], film_request: FilmRequest) -> CDNServerRecord:
    simple_closest = 2**32
    pos = 0
    for i, server in enumerate(servers):
        distance = abs(int(server.cdn_server_id) - int(film_request.user_ip))
        if simple_closest > distance and server.loading < 0.85:
            simple_closest = distance
            pos = i
    return servers[pos]


class IpRouter(AbstractIpRouter):

    async def select_cdn(self,
                         cdn_request: FilmRequest,
                         cdn_servers: List[CDNServerRecord]) -> CDNServerRecord:

        def no_less_quality(serv):
            parsed_quality = cdn_request.quality
            for rate in serv.quality:
                if int(parsed_quality) <= int(rate):
                    return serv.quality

        if len(cdn_servers) == 1:
            return cdn_servers[0]

        # cdn_servers = sorted(cdn_servers, key=lambda x: x.loading)
        best_servers = list(filter(no_less_quality, cdn_servers))

        if best_servers:
            closest = await closest_distance(best_servers, cdn_request)
        else:
            closest = await closest_distance(cdn_servers, cdn_request)

        return closest
