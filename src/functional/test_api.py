
import pprint
import uuid
import requests
from http import HTTPStatus
from functional.conftest import API_URL


def test_api_response(data_set):
    film_uuid = data_set['files'][0]['file_uuid']
    quality = data_set['files'][0]['quality']
    user_ip = data_set['user_ip'][0]

    url = f'{API_URL}/api/v1/link/{film_uuid}/{quality}?user_ip={user_ip}&start=3041'
    response = requests.get(url)
    assert response.status_code == HTTPStatus.OK


def test_api_response_bad_api(data_set):
    film_uuid = data_set['files'][0]['file_uuid']
    quality = data_set['files'][0]['quality']
    user_ip = 'xxx.xxx.12.1'

    url = f'{API_URL}/api/v1/link/{film_uuid}/{quality}?user_ip={user_ip}&start=3041'
    response = requests.get(url)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
