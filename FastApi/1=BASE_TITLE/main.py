import os
import platform
import time
from datetime import datetime
from typing import Dict, Any
from dataclasses import dataclass

import psutil
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


# =====================================================================================================================
@dataclass
class ServiceDetails:
    SERVICE_NAME: str = "Base Info Title Header"
    SERVICE_DESCRIPTION: str = "gen/place a universal title header into any project"
    SERVICE_AUTHOR: str = "Andrey Starichenko"
    SERVICE_FRAMEWORK: str = "FastAPI"

    def __post_init__(self):
        self.SERVICE_INFO: dict[str, str] = {
            "name": self.SERVICE_NAME,
            "description": self.SERVICE_DESCRIPTION,
            "author": self.SERVICE_AUTHOR,
            "framework": self.SERVICE_FRAMEWORK,

        }
        self.OS_INFO: dict[str, str] = {
            "os": platform.system(),
            "os_version": platform.platform(),
            "hostname": platform.node(),
            "processor": platform.processor(),
            "architecture": platform.machine(),
        }
        self.RUNTIME: dict[str, str] = {
            "os__boot_time": self.get__boot_time(),
            "service__start_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            **self.get__user_info(),
        }

    def get(self, request: Request | None = None) -> dict[str, dict[str, Any | str | int | float | None]]:
        result = {
            "SERVICE_INFO": self.SERVICE_INFO,
            "OS_INFO": self.OS_INFO,
            "RUNTIME": self.RUNTIME,
            "LOAD": {
                "CPU_LOAD": self.CPU_LOAD,
                "MEMORY": self.get__memory_info(),
                "DISK": self.get__disk_info(),
            },
            "CLIENT": self.get__client_info(request),
        }
        return result

    def get__client_info(self, request: Request | None = None) -> dict:
        result = {}

        if request is not None:
            client_ip = request.client.host
            if not client_ip:
                if "x-forwarded-for" in request.headers:
                    client_ip = request.headers["x-forwarded-for"].split(",")[0].strip()

            result["client_ip"] = client_ip
            result["host_domain"] = request.url.hostname
            result["current_url"] = str(request.url)

        # CLIENT будет заполнен на фронтенде (браузер, ОС, локальное время)
        result["ip"] = "—",   # будет заполнено в JS
        result["browser"] = "—",   # будет заполнено в JS
        result["os"] = "—",   # будет заполнено в JS
        result["local_time"] = "—",   # будет заполнено в JS
        result["user_agent"] = "—",   # будет заполнено в JS

        return result

    def get__boot_time(self) -> str:
        try:
            boot_timestamp = psutil.boot_time()
            return datetime.fromtimestamp(boot_timestamp).strftime("%Y-%m-%d %H:%M:%S")
        except Exception:
            return "N/A"

    def get__user_info(self) -> dict[str, Any]:
        try:
            if platform.system() == "Windows":
                import ctypes
                is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
            else:
                is_admin = os.geteuid() == 0

            username = os.getlogin() if hasattr(os, 'getlogin') else os.environ.get('USER', 'Unknown')
        except Exception:
            username = "Unknown"
            is_admin = False

        return {
            "service_username": username,
            "service_userlevel": "администратор" if is_admin else "обычный пользователь",
        }

    @property
    def CPU_LOAD(self) -> dict:
        return self.get__system_load()

    def get__system_load(self) -> dict[str, Any]:
        try:
            load_avg = psutil.getloadavg()
            return {
                "load_1min": round(load_avg[0], 2),
                "load_5min": round(load_avg[1], 2),
                "load_15min": round(load_avg[2], 2),
            }
        except Exception:
            return {}

    def get__memory_info(self) -> dict[str, Any]:
        try:
            mem = psutil.virtual_memory()
            return {
                "total": f"{mem.total / (1024**3):.2f} GB",
                "available": f"{mem.available / (1024**3):.2f} GB",
                "used": f"{mem.used / (1024**3):.2f} GB",
                "percent": f"{mem.percent}%"
            }
        except Exception:
            return {"error": "N/A"}

    def get__disk_info(self) -> dict[str, Any]:
        try:
            disk = psutil.disk_usage('/')
            return {
                "total": f"{disk.total / (1024**3):.2f} GB",
                "used": f"{disk.used / (1024**3):.2f} GB",
                "free": f"{disk.free / (1024**3):.2f} GB",
                "percent": f"{disk.percent}%"
            }
        except Exception:
            return {"error": "N/A"}


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
        "author": service_details.SERVICE_AUTHOR,
        "any other": "123",
    })


@app.get("/service_details", response_class=HTMLResponse)
async def html__service_details(request: Request):
    """Страница с детальной информацией о системе и сервисе."""
    # Контекст для хедера не нужен, так как данные подгружаются через API
    return templates.TemplateResponse("service_details.html", {"request": request})


@app.get("/api/info")
async def api__info(request: Request):
    """Возвращает структурированный словарь со всей информацией."""
    data = service_details.get(request)
    return data


@app.get("/api/clock")
async def api__clock():
    return {"server_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}


# =====================================================================================================================
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


# =====================================================================================================================
