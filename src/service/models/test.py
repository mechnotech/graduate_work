from typing import Optional

from pydantic import BaseModel


class TestRet(BaseModel):
    kol_rec: Optional[int]
    mssg: Optional[str]
