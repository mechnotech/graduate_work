import base64
import datetime
import hashlib
import os
from http import HTTPStatus
from typing import Optional, Any

from flask import make_response, jsonify, request
from pydantic import ValidationError
from werkzeug.exceptions import abort

from settings import SECRET_KEY, LINK_EXPIRES_HOURS
import asyncio
from asyncio import ensure_future, gather, run

from aiofile import AIOFile
from aiohttp import ClientSession, ClientTimeout


def show_error(text: Optional[Any], http_code: int):
    return abort(make_response(jsonify({'msg': text}), http_code))


def post_load(obj):
    if not request.json:
        return abort(make_response(jsonify({'msg': 'Пустой запрос'}), HTTPStatus.BAD_REQUEST))
    try:
        entity = obj(**request.json)
    except ValidationError as e:
        return show_error(e.errors(), HTTPStatus.BAD_REQUEST)
    return entity


def get_load(obj):
    if not request.args:
        return abort(make_response(jsonify({'msg': 'Ожидаются аргументы'}), HTTPStatus.BAD_REQUEST))
    try:
        entity = obj(**request.args)
    except ValidationError as e:
        return show_error(e.errors(), HTTPStatus.BAD_REQUEST)
    return entity


def get_link_code(expiration: int, file_name: str, bitrate: str, real_ip: str):
    link = f'{expiration} /cdn/{bitrate}/{file_name} {real_ip} {SECRET_KEY}'.encode('utf-8')
    hash_md5 = hashlib.md5(link).digest()
    base64_bytes = base64.urlsafe_b64encode(hash_md5)
    base64_message = base64_bytes.decode('utf-8')
    message = base64_message.replace('=', '')
    return f'/cdn/{bitrate}/{file_name}?md5={message}&expires={expiration}'


def get_redirecting():
    ip_addr = request.remote_addr
    real_ip = request.headers.get('X-Real-IP')
    forwarded = request.headers.get('X-Forwarded-For')
    ls = os.listdir(path="./cdn/")
    if not ls:
        show_error('В нашем CDN еще нет файлов! Добавьте в volume файлы', HTTPStatus.NOT_FOUND)
    expiration = int((datetime.datetime.now() + datetime.timedelta(hours=LINK_EXPIRES_HOURS)).timestamp())
    result = {}
    for file_name in ls:
        for rate in ['1080p', '720p', '480p', '360p', '240p', '144p', 'master']:
            link = get_link_code(expiration, file_name, rate, real_ip)
            result[f'{rate}-' + file_name] = link
    result['info'] = f'ip={ip_addr}, real ip={real_ip}, forwarded ip={forwarded}'
    result['fake-file'] = get_link_code(expiration, 'fake.mp4', '1080p', real_ip)
    return result


async def download_one(link, session, file_name):
    print('start download')
    async with session.get(link) as response:
        if response.status != 200:
            show_error('Ошибка', response.status)
        content = await response.read()
    print('start writing')

    async with AIOFile(f'cdn/{file_name}', 'w') as fl:
        await fl.write_bytes(content)
    print('writing done!')
    return


async def get_my_ip(link):
    print('start check')
    timeout = ClientTimeout(total=60)
    async with ClientSession(timeout=timeout) as session:
        async with session.get(link) as response:
            if response.status != 200:
                show_error('Ошибка', response.status)
            content = await response.json()
            print(content)
    return content['source']


async def downloader(download_film):
    tasks = list()
    expiration = int((datetime.datetime.now() + datetime.timedelta(hours=LINK_EXPIRES_HOURS)).timestamp())
    rate = '1080p'
    file_name = download_film.film
    source_ip = download_film.source_ip

    link = f'http://{source_ip}/api/v1/links/whoami'
    my_ip = await get_my_ip(link)

    link = get_link_code(expiration=expiration, file_name=file_name, bitrate=rate, real_ip=my_ip)

    timeout = ClientTimeout(total=3600)
    async with ClientSession(timeout=timeout) as session:
        tasks.append(ensure_future(download_one(f'http://{source_ip}{link}', session, file_name)))
        await gather(*tasks)
    return {'source_ip': source_ip, 'mirror_ip': my_ip}
