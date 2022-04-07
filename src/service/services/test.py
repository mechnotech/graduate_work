from functools import lru_cache

from balancer.broker import Interface


class TestService():

    async def get(self, path_part: str, param_var: str) -> dict:
        interface = Interface()
        return {'kol_rec': 5, 'mssg': await interface.say()}


@lru_cache()
def get_test_service() -> TestService:
    return TestService()
