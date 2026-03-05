from fastapi import FastAPI
from fastapi.routing import APIRoute, Mount
from starlette.routing import Route

from base_aux.devops.m0_system_info import *


# =====================================================================================================================
class FastApiAux:
    _app: FastAPI

    def __init__(self, app: FastAPI):
        self._app = app

    def get_routes(self) -> dict[str, str]:
        result = dict()
        for route in self._app.routes:
            if isinstance(route, Mount):
                continue
            if not isinstance(route, (APIRoute, Route)):
                continue

            result.update({
                route.path: str(route)
                # route.path: dict(
                #     path=route.path,
                #     name=route.name,
                #     methods=route.methods,
                # )
            })

        return result


# =====================================================================================================================
