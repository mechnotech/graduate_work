"""
Only for presentation
"""
import logging

import requests

URL = "http://localhost:8080/api/v1/link/{uuid}/{quality}?user_ip={ip}"


logging.basicConfig(level=logging.INFO)


def test_demo(data_set):
    film_uuid = "22e7c14e-8c47-4155-aafc-a123d45fd357"
    quality = '360'
    user_ip = '192.168.1.117'
    response = requests.get(URL.format(uuid=film_uuid,
                                       quality=quality,
                                       ip=user_ip))
    response_json = response.json()
    assert 'localhost:8081' in response_json['link']
    logging.info("ip 192.168.1.117 перенаправил на cdn_main ip 192.168.1.2")

    user_ip = '192.168.3.177'
    response = requests.get(URL.format(uuid=film_uuid,
                                       quality=quality,
                                       ip=user_ip))
    response_json = response.json()
    assert 'localhost:8083' in response_json['link']
    logging.info("ip 192.168.3.117 перенаправил на cdn_main ip 192.168.3.2")
