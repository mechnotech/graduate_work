"""
CDN File Manager
"""
from typing import (Optional,
                    List)
from ipaddress import IPv4Address

from service.balancer.models import (FilmRequest,
                                     FilmResponse,
                                     CDNServerRecord)

from .cdnmanager import AbstractCDNFileManager


class MainCDNManager(AbstractCDNFileManager):

    def __init__(self, db_connect):
        self.db_connect = db_connect

    async def find(self,
                   cdn_request: FilmRequest) -> Optional[List[CDNServerRecord]]:
        request = """SELECT ff.
                     FROM film_file ff

                     WHERE film_uuid=%s"""
        async with self.db_connect.cursor() as cur:
            await cur.execute(request, (cdn_request.file_uuid, ))
            print(list(await cur.fetchall()))


 #       if cdn_request.file_uuid.startswith('1'):
 #           return None
 #       if cdn_request.file_uuid.startswith('2'):
 #           return [CDNServerRecord(cdn_server_id='cdn_1',
 #                                   cdn_server_ip=IPv4Address('192.168.1.222'),
 #                                   loading=0.5,
 #                                   file_uuid='file_uuid',
 #                                   quality=["240", "360"]), ]

    async def prepare(self,
                      cdn_request: FilmRequest,
                      cdn_server_select: CDNServerRecord) -> FilmResponse:
        return FilmResponse(path=cdn_request.file_uuid,
                            cdn_server_url=cdn_server_select.cdn_server_id,
                            cdn_server_key='secure_key',
                            length_sec=2500)

    def file_move(self,
                  cdn_id_recipient: str,
                  file_uuid: str,
                  quality: List[str]):
        pass
