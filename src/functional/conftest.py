
import logging
import uuid

import pytest
import psycopg2

from service.config import config

CREATE_SQL_FILE = 'service/balancer/cdnmanager/create.sql'
API_URL = 'http://localhost:8080'

# I haven't any mental health to read it from requests ...
logging.getLogger('requests').setLevel(logging.CRITICAL)


TEST_DATA_SQL = """
-- server records
DELETE FROM cdn_server;
INSERT INTO cdn_server VALUES ('cdn_main', '192.168.1.2', 'localhost:8081', 'dc34ea0b-642d-4709-8b6e-07161aaed244', 'cdn_main', true, '');
INSERT INTO cdn_server VALUES ('cdn_1', '192.168.2.2', 'localhost:8082', '58591d34-0c4b-43ad-83dc-082165ddd4cf', 'cdn 1', false, '');
INSERT INTO cdn_server VALUES ('cdn_2', '192.168.3.2', 'localhost:8083', '7f768d32-a4fa-4086-98bd-708ed82cf69a', 'cdn 2', false, '');

-- file records
DELETE FROM film_file;
INSERT INTO film_file  VALUES ('63e1b243-2d2a-4aa1-aa20-5ee62b4af2f9', 'cdn_main', '22e7c14e-8c47-4155-aafc-a123d45fd357', '360', 100, '22e7c14e-8c47-4155-aafc-a123d45fd357.360.mp4', '22e7c14e-8c47-4155-aafc-a123d45fd357.360.mp4');
INSERT INTO film_file  VALUES ('90553348-db14-485e-8aa7-7e263c74f86b', 'cdn_main', '22e7c14e-8c47-4155-aafc-a123d45fd357', '720', 100, '22e7c14e-8c47-4155-aafc-a123d45fd357.720.mp4', '22e7c14e-8c47-4155-aafc-a123d45fd357.720.mp4');

INSERT INTO film_file  VALUES ('54c9669c-7102-4013-8c5e-ee7e15d32944', 'cdn_1', '22e7c14e-8c47-4155-aafc-a123d45fd357', '360', 100, '22e7c14e-8c47-4155-aafc-a123d45fd357.360.mp4', '22e7c14e-8c47-4155-aafc-a123d45fd357.360.mp4');
INSERT INTO film_file  VALUES ('81555db1-e697-40ae-a529-1853bc209614', 'cdn_2', '22e7c14e-8c47-4155-aafc-a123d45fd357', '360', 100, '22e7c14e-8c47-4155-aafc-a123d45fd357.360.mp4', '22e7c14e-8c47-4155-aafc-a123d45fd357.360.mp4');


INSERT INTO film_file  VALUES ('bd5e2ac8-65e4-42e0-8625-9ad7cf32eaf8', 'cdn_main', 'a4d0691a-9fa4-4157-afa9-a87a2a990823', '360', 100, 'a4d0691a-9fa4-4157-afa9-a87a2a990823.360.mp4', 'a4d0691a-9fa4-4157-afa9-a87a2a990823.360.mp4');
INSERT INTO film_file  VALUES ('de66450d-2a84-465b-b160-bf6a024f22b8', 'cdn_main', 'a4d0691a-9fa4-4157-afa9-a87a2a990823', '720', 100, 'a4d0691a-9fa4-4157-afa9-a87a2a990823.720.mp4', 'a4d0691a-9fa4-4157-afa9-a87a2a990823.720.mp4');
"""


@pytest.fixture(scope='function')
def data_set():

    conn = psycopg2.connect(user=config.db_user,
                            password=config.db_password,
                            host=config.db_host,
                            database=config.db_base)

    with conn.cursor() as cur:
        cur.execute(TEST_DATA_SQL)
    conn.close()
    # file uuid for test
    # 8f28972c-7644-4bbd-9e29-0d914912232a
    # a4d0691a-9fa4-4157-afa9-a87a2a990823
    # 22e7c14e-8c47-4155-aafc-a123d45fd357

    files = [{'name': '22e7c14e-8c47-4155-aafc-a123d45fd357.360.mp4',
              'file_uuid': '22e7c14e-8c47-4155-aafc-a123d45fd357',
              'quality': '360'}]
    ret_set = {'files': files,
               'user_ip': ['192.168.1.117', ],
               '404_file': str(uuid.uuid4())}

    yield ret_set
