from typing import Optional

from fastapi import (APIRouter, Depends, Request)
from pydantic import parse_obj_as

from models.test import TestRet
from services.test import (TestService,
                           get_test_service)

router = APIRouter()


@router.get('/test/{path_part}', response_model=TestRet)
async def test_backend(request: Request,
                       path_part: str,
                       param_var: Optional[str],
                       services: TestService = Depends(get_test_service)
                       ) -> TestRet:
    test_ret = await services.get(path_part, param_var)
    return TestRet(**test_ret)
