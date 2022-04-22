"""
CDN Manager models
"""

from ipaddress import (IPv4Address,
                       IPv6Address)
from typing import Union


from pydantic import Field
from pydantic.dataclasses import dataclass


@dataclass
class CDNServerRecord:
    server_id: str = Field(description="Unique mnemo server name")
    server_ip: Union[IPv4Address,
                     IPv6Address] = Field(description="Sever ip address")
    server_path: str = Field(description='Server url for link')
    secret_key: str = Field(description='Secret key for file acccess coding')
    is_main: bool = Field(description='Mark for main server')
    description: str = Field(description='Server hint')


@dataclass
class CDNFileServerRecord(CDNServerRecord):
    url_path: str = Field(description='url to file exclude server part')


@dataclass
class CDNFilmFileRecord:
    film_uuid: str = Field(description='Film uuid same in database')
    quality: str = Field(description='Record quality')
    length_sec: int = Field(description='Film length in seconds')
    url_path: str = Field(description='url to file exclude server part')
    disk_path: str = Field(description='path in storage include file_name.ext')
