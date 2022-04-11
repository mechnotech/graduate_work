import pytest

@pytest.mark.skip
@pytest.mark.asyncio
async def test_interface():
    interface = Interface()
    assert await interface.say() == 'Hello world'
    print("check test message", end='\t')
