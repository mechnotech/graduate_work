"""
Only for presentation
"""
import logging

import requests
import pytest

URL = "http://localhost:8080/api/v1/link/{uuid}/{quality}?user_ip={ip}"


def test_demo(data_set):
    film_uuid = "22e7c14e-8c47-4155-aafc-a123d45fd357"
    quality = '360'
    user_ip = '192.168.1.117'
    response = requests.get(URL.format(uuid=film_uuid,
                                       quality=quality,
                                       ip=user_ip))
    print(response)
    logging.info("Демо")
