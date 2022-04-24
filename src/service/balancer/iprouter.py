"""
Ip router class
"""

import abc

from typing import List

from service.config import config

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


async def closest_distance(servers: List[CDNServerRecord], film_request: FilmRequest) -> List:
    """
    Pseudo Geo IP функция.
    Исходя из предположения, что разница по модулю между IP будет минимальна для адресов из одной подсети.
    Возвращает сервер с ближайшим IP к IP пользователя расчетным путем.

    :param servers: Список записей кандидатов CDNServerRecord
    :param film_request: Запрос пользователя FilmRequest
    :return: Сортированный по близости к пользователю CDNServerRecord
    """
    return sorted(servers, key=lambda x: abs(int(x.cdn_server_ip) - int(film_request.user_ip)))


class IpRouter(AbstractIpRouter):

    async def select_cdn(self,
                         cdn_request: FilmRequest,
                         cdn_servers: List[CDNServerRecord]) -> CDNServerRecord:

        def no_less_quality(server):
            parsed_quality = cdn_request.quality
            for rate in server.quality:
                if int(parsed_quality) <= int(rate):
                    return server.quality

        if len(cdn_servers) == 1:
            return cdn_servers[0]

        best_servers = list(filter(no_less_quality, cdn_servers))

        if best_servers:
            closest = await closest_distance(best_servers, cdn_request)
        else:
            closest = await closest_distance(cdn_servers, cdn_request)

        for serv in closest:
            if serv.loading < config.cdn_busy_limit:
                return serv

        closest.sort(key=lambda x: x.loading)
        return closest[0]
