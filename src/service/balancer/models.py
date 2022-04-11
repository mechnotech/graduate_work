"""
Balancer data models
"""

from ipaddress import (IPv4Address,
                       IPv6Address)

from typing import (Optional,
                    Union,
                    List)

from pydantic import Field
from pydantic.dataclasses import dataclass


QUALITY = ['144', '240', '360', '480', '720', '1080', '1440', '2160']


@dataclass
class FilmRequest:
    user_ip: Union[IPv4Address, IPv6Address] = Field(description='user ip')
    file_uuid: str = Field(description='file uuid')
    quality: str = Field(default=QUALITY[-1], description='record quality')


@dataclass
class FilmResponse:
    path: str = Field(description='File path')
    cdn_server_url: str = Field(description='cdn server url')
    cdn_server_key: str = Field(description='key used with specific server')
    length_sec: Optional[int] = Field(default=None, description='record length in seconds')


@dataclass
class CDNServerRecord:
    cdn_server_id: str = Field(description='CDN server id')
    cdn_server_ip: Union[IPv4Address, IPv6Address] = Field(description='server ip')
    loading: float = Field(ge=0, le=1, description='Server load')
    file_uuid: str = Field(description='file uuid')
    quality: List[str] = Field(description='record quality')
