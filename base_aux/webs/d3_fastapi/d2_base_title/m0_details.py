from typing import *
import os
import platform
from dataclasses import dataclass
from datetime import datetime

import psutil
from starlette.requests import Request


# =====================================================================================================================
@dataclass
class ServiceDetails:
    SERVICE_NAME: str = "TitleHeader"
    SERVICE_DESCRIPTION: str = "universal title header for any project"
    SERVICE_AUTHOR: str = "Andrey Starichenko"
    SERVICE_FRAMEWORK: str = "FastAPI+js"

    # -----------------------------------------------------------------------------------------------------------------
    def __post_init__(self):
        self._load_static()

    def _load_static(self) -> None:
        self.SERVICE_INFO: dict[str, str] = {
            "service__start_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "name": self.SERVICE_NAME,
            "description": self.SERVICE_DESCRIPTION,
            "author": self.SERVICE_AUTHOR,
            "framework": self.SERVICE_FRAMEWORK,
        }
        self.OS_INFO: dict[str, str] = {
            "os__boot_time": self.get__boot_time(),
            "os": platform.system(),
            "os_version": platform.platform(),
            "hostname": platform.node(),
            "processor": platform.processor(),
            "architecture": platform.machine(),
            **self.get__user_info(),
        }

    # -----------------------------------------------------------------------------------------------------------------
    def get(self, request: Request | None = None) -> dict[str, dict[str, Any | str | int | float | None]]:
        result = {}
        result.update(**self.get_static(request))
        result['DINAMIC'] = self.get_dinamic()
        return result

    def get_static(self, request: Request | None = None) -> dict[str, dict[str, Any | str | int | float | None]]:
        result = {
            "SERVICE_INFO": self.SERVICE_INFO,
            "OS_INFO": self.OS_INFO,
            "CLIENT": self.get__client_info(request),
        }
        return result

    def get_dinamic(self) -> dict[str, dict[str, Any | str | int | float | None]]:
        result = {
            "CPU_LOAD": self.get__system_load(),
            "MEMORY": self.get__memory_info(),
            "DISK": self.get__disk_info(),
        }
        return result

    # -----------------------------------------------------------------------------------------------------------------
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

    # -----------------------------------------------------------------------------------------------------------------
    def get__boot_time(self) -> str:
        try:
            boot_timestamp = psutil.boot_time()
            return datetime.fromtimestamp(boot_timestamp).strftime("%Y-%m-%d %H:%M:%S")
        except BaseException as exc:
            return f"{exc!r}"

    def get__user_info(self) -> dict[str, Any]:
        try:
            if platform.system() == "Windows":
                import ctypes
                is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
            else:
                is_admin = os.geteuid() == 0

            username = os.getlogin()
        except BaseException as exc:
            username = f"{exc!r}"
            is_admin = False

        return {
            "service_username": username,
            "service_userlevel": "администратор" if is_admin else "обычный пользователь",
        }

    def get__system_load(self) -> dict[str, Any]:
        try:
            load_avg = psutil.getloadavg()
            return {
                "load_1min": round(load_avg[0], 2),
                "load_5min": round(load_avg[1], 2),
                "load_15min": round(load_avg[2], 2),
            }
        except BaseException as exc:
            return {"error": f"{exc!r}"}

    def get__memory_info(self) -> dict[str, Any]:
        try:
            mem = psutil.virtual_memory()
            return {
                "total": f"{mem.total / (1024**3):.2f} GB",
                "available": f"{mem.available / (1024**3):.2f} GB",
                "used": f"{mem.used / (1024**3):.2f} GB",
                "percent": f"{mem.percent}%"
            }
        except BaseException as exc:
            return {"error": f"{exc!r}"}

    def get__disk_info(self) -> dict[str, Any]:
        try:
            disk = psutil.disk_usage('/')
            return {
                "total": f"{disk.total / (1024**3):.2f} GB",
                "used": f"{disk.used / (1024**3):.2f} GB",
                "free": f"{disk.free / (1024**3):.2f} GB",
                "percent": f"{disk.percent}%"
            }
        except BaseException as exc:
            return {"error": f"{exc!r}"}


# =====================================================================================================================
