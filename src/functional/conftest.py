
import logging
import uuid

import pytest

from service.balancer.cdnmanager.files import gen_file_name

API_URL = 'http://localhost:8080'

# I haven't any mental health to read it ...
logging.getLogger('requests').setLevel(logging.CRITICAL)


@pytest.fixture(scope='session')
def data_set():
    file_uuid = str(uuid.uuid4())
    quality = 360
    files = [{'name': gen_file_name(file_uuid, quality),
              'file_uuid': file_uuid,
              'quality': quality}]
    ret_set = {'files': files,
               'user_ip': ['192.168.1.11', ],
               '404_file': str(uuid.uuid4())}

    yield ret_set
