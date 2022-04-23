"""
Link business logic
"""
import base64
import datetime
import hashlib
import logging

from functools import lru_cache
from http import HTTPStatus
from typing import (Union,
                    Optional)

from ipaddress import (IPv4Address,
                       IPv6Address)

from fastapi import HTTPException

from service.config import config
from service.models.link import LinkResponse
from service.balancer.broker import AbstractBroker
from service.balancer.models import FilmRequest

LINK_MASK = "http://{server}/{path}?md5={key}&expires={expiration}&start={start}"


class LinkService():

    async def get(self,
                  broker: AbstractBroker,
                  user_ip: Union[IPv4Address, IPv6Address],
                  file_uuid: str,
                  quality: int,
                  start_position: Optional[int]) -> LinkResponse:

        film_request = FilmRequest(user_ip=user_ip,
                                   file_uuid=file_uuid,
                                   quality=quality)
        file_response = await broker.get_link(film_request)

        if file_response is None:
            logging.warning(f"file_uuid {file_uuid} not found")
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                                detail='File not found')

        start_position = 0 if start_position is None else start_position
        if file_response.length_sec is None:
            length_sec = config.cdn_var_expiration_def
        else:
            length_sec = file_response.length_sec * config.cdn_var_expiration_mul
        expiration = int((datetime.datetime.now() + datetime.timedelta(seconds=length_sec)).timestamp())

        lock = f'{expiration} /{file_response.path} {user_ip} {file_response.cdn_server_key}'.encode('utf-8')
        hash_md5 = hashlib.md5(lock).digest()
        base64_bytes = base64.urlsafe_b64encode(hash_md5)
        base64_message = base64_bytes.decode('utf-8')
        lock = base64_message.replace('=', '')

        link = LINK_MASK.format(server=file_response.cdn_server_url,
                                path=file_response.path,
                                key=lock,
                                expiration=expiration,
                                start=start_position)

        ret = LinkResponse(link=link,
                           length_sec=length_sec,
                           start_position=start_position)

        return ret


@lru_cache
def get_link_service() -> LinkService:
    return LinkService()
