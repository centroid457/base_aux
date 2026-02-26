from datetime import datetime

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from base_aux.webs.d3_fastapi.d2_base_title.m0_details import ServiceDetails


# =====================================================================================================================
service_details = ServiceDetails()


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
        "any other": "123",
    })


@app.get("/service_details", response_class=HTMLResponse)
async def html__service_details(request: Request):
    return templates.TemplateResponse("service_details.html", {
        "request": request
    })


# ---------------------------------------------------------------------------------------------------------------------
@app.get("/api/info")
async def api__info(request: Request):
    data = service_details.get(request)
    return data


@app.get("/api/clock")
async def api__clock():
    return {"server_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}


# =====================================================================================================================
if __name__ == "__main__":
    uvicorn.run("m1_header:app", port=8000, reload=True)


# =====================================================================================================================
