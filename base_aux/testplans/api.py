from typing import *

from aiohttp import web
from fastapi import FastAPI, Response
from fastapi.responses import RedirectResponse

from base_aux.servers.m2_server1_aiohttp import *
from base_aux.servers.m3_server2_fastapi import *

from .models import *


# =====================================================================================================================
class TpApi_Aiohttp(ServerAiohttpBase):
    async def response_get_html__(self, request) -> web.Response:
        # --------------------------
        html_block = self.html_block__api_index()

        # RESPONSE --------------------------------------------------
        page_name = "API_INDEX"
        html = self.html_create(data=html_block, redirect_time=2, request=request)
        return web.Response(text=html, content_type='text/html')

    @decorator__log_request_response
    async def response_post__start(self, request) -> web.Response:
        # return self.response_get__start(request)  # this is will not work!
        self.data.signal__tp_start.emit()

        # RESPONSE --------------------------------------------------
        response = web.json_response(data={})
        return response

    @decorator__log_request_response
    async def response_post__stop(self, request) -> web.Response:
        self.data.signal__tp_stop.emit()

        # RESPONSE --------------------------------------------------
        response = web.json_response(data={})
        return response

    @decorator__log_request_response
    async def response_post___reset_duts_sn(self, request) -> web.Response:
        self.data._signal__tp_reset_duts_sn.emit()

        # RESPONSE --------------------------------------------------
        response = web.json_response(data={})
        return response

    # ---------------------------------------------------------
    @decorator__log_request_response
    async def response_get_json__info(self, request) -> web.Response:
        body: dict = self.data.STAND.stand__get_info__general_tcsc()      #FIXME:ADDMODEL???
        response = web.json_response(data=body)
        return response

    @decorator__log_request_response
    async def response_get_json__results(self, request) -> web.Response:
        # RESPONSE --------------------------------------------------
        body: dict = self.data.STAND.tci__get_result()   #FIXME:ADDMODEL???
        return web.json_response(data=body)


# =====================================================================================================================
def create_app__FastApi_Tp(self=None, data: Any = None) -> FastAPI:
    # UNIVERSAL ------------------------------------------------------
    app = FastAPI()
    app.data = data

    # WORK -----------------------------------------------------------
    @app.get("/")
    async def redirect() -> Response:
        return RedirectResponse(url="/docs")

    @app.post("/start")
    async def start() -> bool:
        print(f"access async start")
        # print(f"1=EMIT")
        # app.data.signal__tp_start.emit()
        print(f"2=DIRECT START!")
        app.data.start()
        return True

    @app.post("/stop")
    async def stop() -> bool:
        app.data.signal__tp_stop.emit()
        return True

    @app.get("/info")
    async def info() -> ModelTpInfo:
        return ModelTpInfo(**app.data.STAND.stand__get_info__general_tcsc())

    @app.get("/results")
    async def results() -> ModelTpResults:
        return ModelTpResults(**app.data.STAND.tci__get_result())

    return app


# =====================================================================================================================
class TpApi_FastApi(ServerFastApi_Thread):
    create_app = create_app__FastApi_Tp


# =====================================================================================================================
