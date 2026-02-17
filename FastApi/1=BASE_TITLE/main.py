import os
import platform
import time
from datetime import datetime
from typing import Dict, Any

import psutil
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


# =====================================================================================================================
SERVICE_NAME = "My Universal Service"
SERVICE_DESCRIPTION = "A handy web service template"
SERVICE_AUTHOR = "Your Name"
SERVICE_START_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

app = FastAPI(title=SERVICE_NAME, description=SERVICE_DESCRIPTION)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# =====================================================================================================================
def get_os_info() -> Dict[str, Any]:
    """Информация об ОС сервера."""
    return {
        "os": platform.system(),
        "os_version": platform.platform(),
        "hostname": platform.node(),
        "processor": platform.processor(),
        "machine": platform.machine(),
    }


def get_boot_time() -> str:
    try:
        boot_timestamp = psutil.boot_time()
        return datetime.fromtimestamp(boot_timestamp).strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        return "N/A"


def get_user_info() -> Dict[str, Any]:
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
        "username": username,
        "user_level": "администратор" if is_admin else "обычный пользователь"
    }


def get_system_load() -> Dict[str, Any]:
    try:
        load_avg = psutil.getloadavg()
        return {
            "load_1min": round(load_avg[0], 2),
            "load_5min": round(load_avg[1], 2),
            "load_15min": round(load_avg[2], 2),
        }
    except Exception:
        return {}


def get_memory_info() -> Dict[str, Any]:
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


def get_disk_info() -> Dict[str, Any]:
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


def get_server_time() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# =====================================================================================================================
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "service_name": SERVICE_NAME,
        "service_description": SERVICE_DESCRIPTION,
        "author": SERVICE_AUTHOR
    })


@app.get("/api/info")
async def api_info(request: Request):
    """Возвращает структурированный словарь со всей информацией."""
    client_ip = request.client.host
    if "x-forwarded-for" in request.headers:
        client_ip = request.headers["x-forwarded-for"].split(",")[0].strip()

    # Домен хоста (из запроса)
    host_domain = request.url.hostname

    os_info = get_os_info()
    boot_time = get_boot_time()
    user_info = get_user_info()
    load_info = get_system_load()

    # Формируем единый словарь
    data = {
        "SERVICE": {
            "name": SERVICE_NAME,
            "description": SERVICE_DESCRIPTION,
            "author": SERVICE_AUTHOR,
            "start_time": SERVICE_START_TIME,
            "framework": "FastAPI"
        },
        "SERVICE SYSTEM": {
            "host_domain": host_domain,
            "os": os_info["os"],
            "os_version": os_info["os_version"],
            "hostname": os_info["hostname"],
            "processor": os_info["processor"],
            "architecture": os_info["machine"],
            "boot_time": boot_time,
            "user": user_info["username"],
            "user_level": user_info["user_level"],
            "CpuLoad": get_system_load(),  # теперь это словарь с ключами 1min,5min,15min
            "Memory": get_memory_info(),
            "Disk (/)": get_disk_info(),
        },
        "NETWORK": {
            "client_ip": client_ip,
            "current_url": str(request.url),
            "server_hostname": platform.node(),
            "server_domain": host_domain,
        },
        # CLIENT будет заполнен на фронтенде (браузер, ОС, локальное время)
        "CLIENT": {
            "ip": client_ip,  # дублируем, но можно оставить
            "browser": "—",   # будет заполнено в JS
            "os": "—",
            "local_time": "—",
            "user_agent": "—",
        }
    }
    return data


@app.get("/api/clock")
async def api_clock():
    return {"server_time": get_server_time()}


# =====================================================================================================================
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


# =====================================================================================================================
