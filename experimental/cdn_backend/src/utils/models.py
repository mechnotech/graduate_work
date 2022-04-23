import datetime
from typing import Optional

import orjson
from pydantic import BaseModel
from pydantic.types import UUID, conint


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode('utf-8')


class AdvancedJsonModel(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class UserUUID(AdvancedJsonModel):
    user_id: UUID


class Download(AdvancedJsonModel):
    film: str
    source_ip: Optional[str]






