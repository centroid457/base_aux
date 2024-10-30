import pathlib
from typing import *
from object_info import ObjectInfo

from server_templates import *
from aiohttp import web
from fastapi import FastAPI, Response
from fastapi.responses import RedirectResponse

from .models import *


# =====================================================================================================================
class TpApi_Aiohttp(ServerAiohttpBase):
    async def response_get_html__(self, request) -> web.Response:
        # --------------------------
        progress = 0
        if self.data and self.data.progress is not None:
            progress = self.data.progress
        # --------------------------
        html_block = f"[PROGRESS = {progress}%]<br /><br />" + self.html_block__api_index()

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
        body: dict = self.data.get__info__tp()      #FIXME:ADDMODEL???
        response = web.json_response(data=body)
        return response

    @decorator__log_request_response
    async def response_get_json__results(self, request) -> web.Response:
        # RESPONSE --------------------------------------------------
        body: dict = self.data.get__results()   #FIXME:ADDMODEL???
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
        return ModelTpInfo(**app.data.get__info__tp())

    @app.get("/results")
    async def results() -> ModelTpResults:
        return ModelTpResults(**app.data.get__results())

    return app


# =====================================================================================================================
class TpApi_FastApi(ServerFastApi_Thread):
    create_app = create_app__FastApi_Tp


# =====================================================================================================================
