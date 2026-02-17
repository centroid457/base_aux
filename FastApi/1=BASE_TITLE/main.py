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

# ---------- Конфигурация сервиса ----------
SERVICE_NAME = "My Universal Service"
SERVICE_DESCRIPTION = "A handy web service template"
SERVICE_AUTHOR = "Your Name"
# Время запуска сервиса (фиксируется при старте)
SERVICE_START_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# ---------- Создание приложения ----------
app = FastAPI(title=SERVICE_NAME, description=SERVICE_DESCRIPTION)

# Подключаем статику и шаблоны
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# ---------- Вспомогательные функции для сбора информации о системе ----------
def get_os_info() -> Dict[str, Any]:
    """Собирает информацию об операционной системе."""
    info = {
        "os": platform.system(),
        "os_version": platform.platform(),
        "hostname": platform.node(),
        "processor": platform.processor(),
        "machine": platform.machine(),
    }
    return info


def get_boot_time() -> str:
    """Возвращает время последней загрузки системы."""
    try:
        boot_timestamp = psutil.boot_time()
        boot_time = datetime.fromtimestamp(boot_timestamp).strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        boot_time = "N/A"
    return boot_time


def get_user_info() -> Dict[str, Any]:
    """Определяет имя пользователя и уровень прав (админ/обычный)."""
    try:
        # Для Windows проверка администратора
        if platform.system() == "Windows":
            import ctypes
            is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
        else:  # Linux, macOS
            is_admin = os.geteuid() == 0

        # Имя пользователя
        username = os.getlogin() if hasattr(os, 'getlogin') else os.environ.get('USER', 'Unknown')
    except Exception:
        username = "Unknown"
        is_admin = False

    return {
        "username": username,
        "is_admin": is_admin,
        "user_level": "администратор" if is_admin else "обычный пользователь"
    }


def get_system_load() -> Dict[str, Any]:
    """Возвращает среднюю загрузку системы (если доступно)."""
    try:
        load_avg = psutil.getloadavg()
        return {
            "load_1min": round(load_avg[0], 2),
            "load_5min": round(load_avg[1], 2),
            "load_15min": round(load_avg[2], 2),
        }
    except Exception:
        return {}


def get_server_time() -> str:
    """Текущее серверное время."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# ---------- Эндпоинты ----------
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Главная страница."""
    return templates.TemplateResponse("index.html", {
        "request": request,
        "service_name": SERVICE_NAME,
        "service_description": SERVICE_DESCRIPTION,
        "author": SERVICE_AUTHOR
    })


@app.get("/api/info")
async def api_info(request: Request):
    """
    Возвращает детальную информацию о системе и сервисе.
    Используется клиентским JavaScript для заполнения блока "Подробнее".
    """
    client_ip = request.client.host
    # Попытка получить реальный IP за прокси
    if "x-forwarded-for" in request.headers:
        client_ip = request.headers["x-forwarded-for"].split(",")[0].strip()

    os_info = get_os_info()
    boot_time = get_boot_time()
    user_info = get_user_info()
    load_info = get_system_load()

    return {
        "service": {
            "name": SERVICE_NAME,
            "description": SERVICE_DESCRIPTION,
            "author": SERVICE_AUTHOR,
            "start_time": SERVICE_START_TIME,
            "framework": "FastAPI"
        },
        "system": {
            **os_info,
            "boot_time": boot_time,
            **user_info,
            "load": load_info
        },
        "network": {
            "client_ip": client_ip,
            "server_hostname": platform.node()
        },
        "server_time": get_server_time()
    }


@app.get("/api/clock")
async def api_clock():
    """Возвращает текущее серверное время (используется для обновления часов)."""
    return {"server_time": get_server_time()}


# Запуск (для отладки)
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)