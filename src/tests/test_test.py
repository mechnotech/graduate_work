import pytest
from service.balancer.broker import Interface


@pytest.mark.asyncio
async def test_interface():
    interface = Interface()
    assert await interface.say() == 'Hello world'
    print("check test message", end='\t')
