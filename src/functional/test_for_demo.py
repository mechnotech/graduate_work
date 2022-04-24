"""
Only for presentation
"""
import logging

import requests
import pytest

URL = "http://localhost:8080/api/v1/link/{uuid}/{quality}?user_ip={ip}"


logging.basicConfig(level=logging.INFO)

def test_demo(data_set):
    film_uuid = "22e7c14e-8c47-4155-aafc-a123d45fd357"
    quality = '360'
    user_ip = '172.27.0.1'

    response = requests.get(URL.format(uuid=film_uuid,
                                       quality=quality,
                                       ip=user_ip
                                       ))
    response_json = response.json()
    logging.info(f" Тест получил ссылку {response_json['link']}")

    my_link = requests.get(response_json['link'])
    # print(response.status_code)
    # print(response.text)

    #user_ip = '192.168.1.117'
    response = requests.get(f'{my_link}')
    response_json = response.json()
    assert 'localhost:8081' in response_json['link']

    print(response_json)
