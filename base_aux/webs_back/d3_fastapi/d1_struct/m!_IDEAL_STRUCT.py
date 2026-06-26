import uvicorn
import asyncio
from contextlib import asynccontextmanager
from fastapi.responses import HTMLResponse
from fastapi import (
    FastAPI,
    WebSocket, WebSocketDisconnect,
    HTTPException,
    Response, Request,
)
from fastapi.responses import RedirectResponse, JSONResponse
from starlette.exceptions import HTTPException

from base_aux.webs_back.d3_fastapi.d0_info.m0_info import *


# =====================================================================================================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- STARTUP (бывший startup_event) -----------------------------------
    print(f"FastApi.STARTUP:")
    await asyncio.sleep(1)

    # async with manager_inst__termos:

    print(f"FastApi.MAIN:")
    yield  # <-- здесь сервер работает и обрабатывает запросы

    # --- SHUTDOWN (бывший shutdown_event) ---
    # for item_id, item in manager_inst__termos.items.items():
    #     print(f"FastApi.Shutdown: {item_id=}")
    #     await item.disconnect()

    print(f"FastApi.FINISHED")
    # ---------------------------------------------------------------------


# =====================================================================================================================
app = FastAPI(title="[FastApi] perfect structure", description="", lifespan=lifespan)


# =====================================================================================================================
# TODO: add PRE / POST logic


# ---------------------------------------------------------------------------------------------------------------------
@app.get("/")
async def root__redirect() -> Response:
    return RedirectResponse(url="/html/index")


# ---------------------------------------------------------------------------------------------------------------------
@app.get("/html/index", response_class=HTMLResponse)
async def html__index(request: Request):
    return "hello"


@app.get("/json/clock")
async def json__clock():
    return {"server_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}


@app.get("/str/echo_path/{path}")
async def str__echo_path(path):
    """
    docssasd
    INFO:     127.0.0.1:7818 - "GET /docssasd HTTP/1.1" 200 OK

    123
    INFO:     127.0.0.1:7819 - "GET /123 HTTP/1.1" 200 OK

    docs123
    INFO:     127.0.0.1:7902 - "GET /docs123 HTTP/1.1" 200 OK
    """
    print(f"{path=}")
    return path


# ---------------------------------------------------------------------------------------------------------------------
@app.websocket("/ws/ping")
async def ws__ping(websocket: WebSocket):
    await websocket.accept()
    try:
        # Держим соединение открытым, игнорируем входящие сообщения
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        pass


# ---------------------------------------------------------------------------------------------------------------------
@app.exception_handler(HTTPException)
async def handle_404(request: Request, exc: HTTPException):
    # TODO: fix all BODY bg color to RED!!! no special!!!

    print(f"{exc!r}")
    # Редирект только для GET-запросов
    if exc.status_code == 404 and request.method == "GET":
        return RedirectResponse("/")
    # Для других HTTP-ошибок вызываем стандартный обработчик
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


# =====================================================================================================================
if __name__ == "__main__":
    uvicorn.run(app, port=80, reload=False)


# =====================================================================================================================
