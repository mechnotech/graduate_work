from asyncio import run

from flask import Blueprint, request

from utils.models import Download
from utils.tools import get_redirecting, post_load, downloader

links = Blueprint('links', __name__)


@links.route('get_link_list', methods=['GET'])
async def get_link_list():
    result = get_redirecting()
    return result


@links.route('whoami', methods=['GET'])
def whoami():
    result = request.headers.get('X-Real-IP')
    if not result:
        result = request.remote_addr
    return {"source": result}


@links.route('download_link', methods=['POST'])
async def download_me():
    download_film = post_load(obj=Download)
    if download_film.source_ip:

        return await downloader(download_film)

    source_ip = request.headers.get('X-Real-IP')
    if not source_ip:
        source_ip = request.remote_addr
    download_film.source_ip = source_ip
    await downloader(download_film)
    return await downloader(download_film)


