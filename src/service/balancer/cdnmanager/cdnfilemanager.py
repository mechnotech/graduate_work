"""
CDN File Manager
"""
import shutil

from typing import (Optional,
                    List)

from service.balancer.models import (FilmRequest,
                                     FilmResponse,
                                     CDNServerRecord)

from .cdnmanager import AbstractCDNFileManager


class MainCDNManager(AbstractCDNFileManager):

    def __init__(self, db_connect):
        self.db_connect = db_connect

    async def find(self,
                   cdn_request: FilmRequest) -> Optional[List[CDNServerRecord]]:
        file_uuid = cdn_request.file_uuid
        request = """SELECT cs.server_id,
                            cs.server_ip,
                            array_agg(DISTINCT ff.quality) as quality
                     FROM film_file ff,
                          cdn_server cs
                     WHERE cs.server_id = ff.server_id AND film_uuid=%s
                     GROUP BY cs.server_id
                     ORDER BY cs.server_id"""

        async with self.db_connect.cursor() as cur:
            await cur.execute(request, (file_uuid, ))
            sql_result = await cur.fetchall()
        return list(map(lambda x: CDNServerRecord(cdn_server_id=x[0],
                                                  cdn_server_ip=x[1],
                                                  loading=0.5,
                                                  file_uuid=file_uuid,
                                                  quality=x[2]),
                        sql_result))

    async def prepare(self,
                      cdn_request: FilmRequest,
                      cdn_server_select: CDNServerRecord) -> FilmResponse:
        request = """SELECT ff.url_path,
                            cs.server_path,
                            cs.secret_key,
                            ff.length_sec
                      FROM film_file ff,
                           cdn_server cs
                      WHERE cs.server_id = ff.server_id AND
                            cs.server_id = %s AND
                            ff.film_uuid = %s AND
                            ff.quality= %s"""
        async with self.db_connect.cursor() as cur:
            await cur.execute(request,
                              (cdn_server_select.cdn_server_id,
                               cdn_request.file_uuid,
                               cdn_server_select.quality[-1], ))
            sql_result = await cur.fetchone()

        return FilmResponse(path=sql_result[0],
                            cdn_server_url=sql_result[1],
                            cdn_server_key=sql_result[2],
                            length_sec=sql_result[3])

    async def file_move(self,
                        cdn_id_recipient: str,
                        file_uuid: str,
                        quality: str):

        request = """SELECT cs.stor_path,
                            ff.disk_path
                     FROM cdn_server cs,
                          film_file ff
                     WHERE cs.is_main = true AND
                           cs.server_id = ff.server_id AND
                           ff.film_uuid = %s AND
                           ff.quality = %s"""

        async with self.db_connect.cursor() as cur:
            await cur.execute(request, (file_uuid, quality, ))
            main_result = await cur.fetchone()
        if not main_result:
            raise ValueError()
