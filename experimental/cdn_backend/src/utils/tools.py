import base64
import datetime
import hashlib
import os
from http import HTTPStatus
from typing import Optional, Any

from flask import make_response, jsonify, request
from werkzeug.exceptions import abort

from settings import SECRET_KEY, LINK_EXPIRES_HOURS


def show_error(text: Optional[Any], http_code: int):
    return abort(make_response(jsonify({'msg': text}), http_code))


def get_link_code(expiration: int, file_name: str, bitrate: int, real_ip: str):
    link = f'{expiration} /cdn/{bitrate}p/{file_name} {real_ip} {SECRET_KEY}'.encode('utf-8')
    hash_md5 = hashlib.md5(link).digest()
    base64_bytes = base64.urlsafe_b64encode(hash_md5)
    base64_message = base64_bytes.decode('utf-8')
    message = base64_message.replace('=', '')
    return f'http://localhost/cdn/{bitrate}p/{file_name}?md5={message}&expires={expiration}'


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
        for rate in [1080, 720, 480, 360, 240, 144]:
            link = get_link_code(expiration, file_name, rate, real_ip)
            result[f'{rate}-' + file_name] = link
    result['info'] = f'ip={ip_addr}, real ip={real_ip}, forwarded ip={forwarded}'
    result['fake-file'] = get_link_code(expiration, 'fake.mp4', 1080, real_ip)
    return result
