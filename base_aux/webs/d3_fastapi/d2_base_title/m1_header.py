import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from base_aux.devops.m0_system_info import *
from base_aux.base_types.m2_info import ObjectInfo


# =====================================================================================================================
service_details = SystemInfo(
    SERVICE_NAME="BaseTitleHeader",
    SERVICE_DESCRIPTION="universal title header for any project",
    SERVICE_AUTHOR="Andrey Starichenko",
    SERVICE_FRAMEWORK="FastAPI+JS",
)


# =====================================================================================================================
app = FastAPI(title=service_details.SERVICE_NAME, description=service_details.SERVICE_DESCRIPTION)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# =====================================================================================================================
@app.get("/", response_class=HTMLResponse)
async def html__index(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,

        "service_name": service_details.SERVICE_NAME,
        "service_description": service_details.SERVICE_DESCRIPTION,
        "any_other": "123",
        "____not_existed": "ERRORRRRRRR",
    })


@app.get("/service_details", response_class=HTMLResponse)
async def html__service_details(request: Request):
    return templates.TemplateResponse("service_details.html", {
        "request": request
    })


# ---------------------------------------------------------------------------------------------------------------------
@app.get("/api/info")
async def api__info(request: Request):
    data = service_details.get_all()
    data["CLIENT_PY"] = get_client_info(request)

    # ObjectInfo(app.routes).print()
    # for route in app.routes:
    #     print(route)
    """
Route(path='/openapi.json', name='openapi', methods=['GET', 'HEAD'])
Route(path='/docs', name='swagger_ui_html', methods=['GET', 'HEAD'])
Route(path='/docs/oauth2-redirect', name='swagger_ui_redirect', methods=['GET', 'HEAD'])
Route(path='/redoc', name='redoc_html', methods=['GET', 'HEAD'])
Mount(path='/static', name='static', app=<starlette.staticfiles.StaticFiles object at 0x000001927A5D90D0>)
APIRoute(path='/', name='html__index', methods=['GET'])
APIRoute(path='/service_details', name='html__service_details', methods=['GET'])
APIRoute(path='/api/info', name='api__info', methods=['GET'])
APIRoute(path='/api/clock', name='api__clock', methods=['GET'])
    """
    #
    # ObjectInfo(route).print()

    return data


@app.get("/api/clock")
async def api__clock():
    return {"server_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}


# =====================================================================================================================
if __name__ == "__main__":
    uvicorn.run("m1_header:app", port=8000, reload=True)


# =====================================================================================================================
