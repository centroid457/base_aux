import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from base_aux.devops.m0_system_info import *
from base_aux.base_types.m2_info import ObjectInfo
from base_aux.webs.d3_fastapi.d0_info.m0_info import *


# =====================================================================================================================
service_details = SystemInfo(
    SERVICE_NAME="BaseTitleHeader",
    SERVICE_DESCRIPTION="universal title header for any project",
    SERVICE_AUTHOR="Andrey Starichenko",
    SERVICE_FRAMEWORK="FastAPI+JS",
)


# =====================================================================================================================
app = FastAPI(title=service_details.SERVICE_NAME, description=service_details.SERVICE_DESCRIPTION)
# app.mount("/", StaticFiles(directory=""), name="static")
templates = Jinja2Templates(directory="templates")


# =====================================================================================================================
@app.get("/", response_class=HTMLResponse)
async def html__index(request: Request):
    return templates.TemplateResponse("fastapi_header_demo.html", {
        "request": request,

        "service_name": service_details.SERVICE_NAME,
        "service_description": service_details.SERVICE_DESCRIPTION,
        "any_other": "123",
        "____not_existed": "ERRORRRRRRR",
    })


# =====================================================================================================================
if __name__ == "__main__":
    uvicorn.run("m1_header:app", port=80, reload=True)


# =====================================================================================================================
