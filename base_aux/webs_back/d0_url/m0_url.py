from typing import *

from base_aux.base_nest_dunders.m3_calls import *
from base_aux.base_nest_dunders.m1_init2_annots1_attrs_by_args_kwargs import *


# =====================================================================================================================
class Url(NestInit_AnnotsAttr_ByArgsKwargs, NestCall_Resolve):
    PROTOCOL: str = "http"
    HOST: str = "localhost"
    PORT: int = 80
    ROUTE: str = ""

    _HIDE_PORT80: bool = None

    def resolve(
            self,
            protocol: Optional[str] = None,
            host: Optional[str] = None,
            port: Optional[int] = None,
            route: Optional[str | tuple[str|Any, ...]] = None,
    ) -> str:
        # ---------------------
        if protocol is None:
            protocol = self.PROTOCOL

        # ---------------------
        if host is None:
            host = self.HOST
        else:
            host = str(host)
        if host == "0.0.0.0":
            host = "localhost"

        # ---------------------
        if port is None:
            port = self.PORT

        # ---------------------
        if route is None:
            route = self.ROUTE

        if isinstance(route, (tuple, list)):
            route_new = ""
            for item in list(route):
                route_new += f"/{item}"
            route = route_new
        else:
            route = str(route)

        while route.startswith("/"):
            route = route[1:]

        # FINAL -------------------
        if self._HIDE_PORT80 and port == 80:
            result = f"{protocol}://{host}/{route}"
        else:
            result = f"{protocol}://{host}:{port}/{route}"
        return result

    def __str__(self) -> str:
        return self.resolve()


# =====================================================================================================================
