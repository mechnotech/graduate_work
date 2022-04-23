import pytest
import requests
from http import HTTPStatus
from functional.conftest import API_URL


@pytest.mark.skip
def test_check():
    response = requests.get(f'{API_URL}/api/v1/test/uuid1234?param_var=abc')
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data['mssg'] == 'Hello world'

def test_volume():
    with open('data/cdn_1/hint.txt', 'rt') as fobj:
        text = fobj.read()
    assert text == 'cdn 1'
