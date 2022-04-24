
import abc

from .counter import AbstractCounter
from .cdnmanager import AbstractCDNManager


class AbstractBalancer():

    def __init__(self,
                 counter: AbstractCounter,
                 cdn_manager: AbstractCDNManager):
        self.counter = counter
        self.cdn_manager = cdn_manager

    @abc.abstractmethod
    async def put(self):
        """ put requests stats server"""

    @abc.abstractmethod
    async def balance(self):
        """ balance file between cdn"""
