import random
from ipaddress import IPv4Address
import uuid

from service.balancer.models import CDNServerRecord, QUALITY

file_uuid = 'move1.360.mp4'


def get_rand_id():
    return str(uuid.uuid4())


def get_rand_ip():
    return IPv4Address(random.randint(100000, 4294967295))


def get_rand_quality():
    return random.sample(QUALITY, random.randint(1, 8))


ls = []
for i in range(10):
    load = {
        'cdn_server_id': get_rand_id(),
        'cdn_server_ip': get_rand_ip(),
        'loading': round(random.random(), 2),
        'file_uuid': file_uuid,
        'quality': get_rand_quality(),
    }
    s1 = CDNServerRecord(**load)
    ls.append(s1)
