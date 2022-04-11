"""
Link endpoin models
"""

from pydantic import BaseModel


class LinkResponse(BaseModel):
    link: str
    length_sec: int
    start_position: int
