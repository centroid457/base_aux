import uvicorn
from fastapi import FastAPI, Response, Request, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse
from starlette.exceptions import HTTPException


# app = FastAPI()
app = FastAPI(title="MinimalCode FastApi")


@app.get("/")
async def redirect() -> Response:
    return RedirectResponse(url="/docs")


@app.get("/echo/{path}")
async def echo_path(path):
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


@app.exception_handler(HTTPException)
async def handle_404(request: Request, exc: HTTPException):
    print(f"{exc!r}")
    # Редирект только для GET-запросов
    if exc.status_code == 404 and request.method == "GET":
        return RedirectResponse("/")
    # Для других HTTP-ошибок вызываем стандартный обработчик
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


# =====================================================================================================================
if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=80)


# =====================================================================================================================
