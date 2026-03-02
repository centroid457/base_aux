import pytest
from fastapi import FastAPI

from base_aux.webs.d3_fastapi.d1_templates.m1_minimal import app
from base_aux.webs.d3_fastapi.d0_info.m0_info import *
# from base_aux.base_types.m2_info import ObjectInfo


# =====================================================================================================================
def test__0():
    print()
    routes = FastApiAux(app).get_routes()
    for route in routes:
        print(route)


# =====================================================================================================================
