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


def get_redirecting():
    ip_addr = request.remote_addr
    real_ip = request.headers.get('X-Real-IP')
    forwarded = request.headers.get('X-Forwarded-For')
    ls = os.listdir(path="./cdn/")
    if not ls:
        show_error('В нашем CDN еще нет файлов! Добавьте в volume файлы', HTTPStatus.NOT_FOUND)
    expiration = int((datetime.datetime.now() + datetime.timedelta(hours=LINK_EXPIRES_HOURS)).timestamp())
    result = {}
    for l in ls:
        link = f'{expiration} /cdn/{l} {real_ip} {SECRET_KEY}'.encode('utf-8')
        hash_md5 = hashlib.md5(link).digest()
        base64_bytes = base64.urlsafe_b64encode(hash_md5)
        base64_message = base64_bytes.decode('utf-8')
        base64_message = base64_message.replace('=', '')
        result[l] = f'http://localhost/cdn/{l}?md5={base64_message}&expires={expiration}'
    result['info'] = f'ip={ip_addr}, real ip={real_ip}, forwarded ip={forwarded}'
    return result
