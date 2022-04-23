"""
script prepare database before functional tests
"""

import asyncio
import logging

from service.balancer.cdnmanager.create_db import recreate

logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    asyncio.run(recreate())
    logging.info('Database recreated')
