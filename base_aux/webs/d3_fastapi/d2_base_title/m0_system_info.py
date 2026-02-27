from typing import *
import os
import sys
import platform
from dataclasses import dataclass
from datetime import datetime

import psutil
from starlette.requests import Request

from base_aux.devops.m1_git import Git

# FIXME
#   add multiton with singleton static??


# =====================================================================================================================
@dataclass
class SystemInfo:
    SERVICE_NAME: str = "TitleHeader"
    SERVICE_DESCRIPTION: str = "universal title header for any project"
    SERVICE_AUTHOR: str = "Andrey Starichenko"
    SERVICE_FRAMEWORK: str = "FastAPI+js"

    def __post_init__(self):
        self._static_cache: dict[str, Any] = {}
        self._load_static()

    # =================================================================================================================
    @staticmethod
    def calc_gb(source: float) -> float:
        return round(source / (1024**3), 2)

    # =================================================================================================================
    def get_all(self) -> dict[str, Any]:
        """Возвращает полную информацию (статику + динамику)."""
        return {
            "static": self.get_static(),
            "dynamic": self.get_dynamic(),
        }

    # =================================================================================================================
    def get_static(self) -> dict[str, Any]:
        """Возвращает кэшированную статическую информацию."""
        return self._static_cache.copy()  # защита от случайного изменения

    # -----------------------------------------------------------------------------------------------------------------
    def _load_static(self) -> None:
        self._static_cache["SERVICE_INFO"] = self._get_static__service()
        self._static_cache["OS_INFO"] = self._get_static__os()
        self._static_cache["USER_INFO"] = self._get_static__user()
        self._static_cache["NETWORK_INFO"] = self._get_static__network()
        self._static_cache["GIT_INFO"] = Git().get__full_info()
        # self._static_cache["ENVIRON"] = os.environ  # DANGER=not safe!

    # -----------------------------------------------------------------------------------------------------------------
    def _get__boot_time(self) -> str:
        """Время загрузки системы в ISO формате."""
        try:
            boot_timestamp = psutil.boot_time()
            # return datetime.fromtimestamp(boot_timestamp).strftime("%Y-%m-%d %H:%M:%S")
            return datetime.fromtimestamp(boot_timestamp).isoformat(timespec="seconds")
        except Exception as exc:
            return f"{exc!r}"

    def _get_static__service(self) -> dict[str, Any]:
        return {
            "start_time": datetime.now().isoformat(timespec="seconds"),
            # "start_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "name": self.SERVICE_NAME,
            "description": self.SERVICE_DESCRIPTION,
            "author": self.SERVICE_AUTHOR,
            "framework": self.SERVICE_FRAMEWORK,
            "python_version": sys.version,
            "python_executable": sys.executable,
            "script_path": os.path.abspath(sys.argv[0]),
        }

    def _get_static__os(self) -> dict[str, str]:
        return {
            "boot_time": self._get__boot_time(),
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "platform": platform.platform(),
            "architecture": platform.machine(),
            "hostname": platform.node(),
            "processor": platform.processor(),
        }

    def _get_static__user(self) -> dict[str, Any]:
        """Информация о пользователе, запустившем сервис."""
        try:
            username = os.getlogin()
            if platform.system() == "Windows":
                import ctypes
                is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
            else:
                is_admin = os.geteuid() == 0
        except Exception as exc:
            username = f"{exc!r}"
            is_admin = False

        return {
            "username": username,
            "is_admin": is_admin,
        }

    def _get_static__network(self) -> dict[str, Any]:
        """Список сетевых интерфейсов с MAC и IP адресами."""
        interfaces = {}
        try:
            if_addrs = psutil.net_if_addrs()
            if_stats = psutil.net_if_stats()

            for name, addrs in if_addrs.items():
                mac = None
                ipv4 = None
                ipv6 = None
                for addr in addrs:
                    if addr.family == psutil.AF_LINK:  # MAC
                        mac = addr.address
                    elif addr.family == 2:  # AF_INET (IPv4)
                        ipv4 = addr.address
                    elif addr.family == 23:  # AF_INET6 (IPv6)
                        ipv6 = addr.address

                stats = if_stats.get(name)
                is_up = stats.isup if stats else None

                interfaces[name] = {
                    "mac": mac,
                    "ipv4": ipv4,
                    "ipv6": ipv6,

                    "is_up": is_up,
                    "speed": stats.speed if stats else None,
                    "mtu": stats.mtu if stats else None,
                    "duplex": stats.duplex if stats else None,
                }

        except Exception as exc:
            interfaces["error"] = f"{exc!r}"
        return interfaces

    # =================================================================================================================
    def get_dynamic(self) -> dict[str, Any]:
        """Возвращает актуальную динамическую информацию."""
        return {
            "cpu": self._get_dynamic__cpu(),
            "memory": self._get_dynamic__memory(),
            "swap": self._get_dynamic__swap(),
            "disk": self._get_dynamic__disk(),
            "network": self._get_dynamic__network_stats(),
            "processes": self._get_process_count(),
            "uptime": self._get_uptime(),
        }

    # -----------------------------------------------------------------------------------------------------------------
    def _get_dynamic__cpu(self) -> dict[str, Any]:
        """Загрузка CPU и информация о ядрах."""
        result = {}
        try:
            # Загрузка в процентах за последний интервал (блокирующий вызов)
            result["percent_total"] = psutil.cpu_percent(interval=0.1)
            result["percent_per_cpu"] = psutil.cpu_percent(interval=0.1, percpu=True)

            result["count_logical"] = psutil.cpu_count(logical=True)
            result["count_physical"] = psutil.cpu_count(logical=False)

        except Exception as exc:
            result["error"] = f"{exc!r}"

        try:
            # Средняя загрузка (load average) — доступна не на Windows
            # if hasattr(psutil, "getloadavg"):
            load_avg = psutil.getloadavg()
            result["load_avg"] = {
                "load_1min": round(load_avg[0], 2),
                "load_5min": round(load_avg[1], 2),
                "load_15min": round(load_avg[2], 2),
            }
        except Exception as exc:
            result["load_avg"] = f"{exc!r}"

        try:
            # Текущая частота CPU (может отсутствовать на некоторых системах)
            freq = psutil.cpu_freq()
            # if freq:
            result["freq_current"] = round(freq.current, 2)
            result["freq_min"] = round(freq.min, 2) if freq.min else None
            result["freq_max"] = round(freq.max, 2) if freq.max else None
        except Exception as exc:
            result["freq_current"] = f"{exc!r}"
            result["freq_min"] = f"{exc!r}"
            result["freq_max"] = f"{exc!r}"

        return result

    def _get_dynamic__memory(self) -> dict[str, Any]:
        """Использование оперативной памяти (числа в байтах -> Гб)."""
        try:
            mem = psutil.virtual_memory()
            return {
                "total": self.calc_gb(mem.total),
                "used": self.calc_gb(mem.used),
                "available": self.calc_gb(mem.available),
                "free": self.calc_gb(mem.free),
                "percent": mem.percent,
            }
        except Exception as exc:
            return {"error": f"{exc!r}"}

    def _get_dynamic__swap(self) -> dict[str, Any]:
        """Использование swap (числа в байтах)."""
        try:
            swap = psutil.swap_memory()
            return {
                "total": self.calc_gb(swap.total),
                "used": self.calc_gb(swap.used),
                "free": self.calc_gb(swap.free),
                "percent": swap.percent,
                "sin": swap.sin,
                "sout": swap.sout,
            }
        except Exception as exc:
            return {"error": f"{exc!r}"}

    def _get_dynamic__disk(self) -> dict[str, Any]:
        """Использование дисков по разделам."""
        result = {}
        try:
            partitions = psutil.disk_partitions()
            result["current_device"] = None
            for part in partitions:
                try:
                    usage = psutil.disk_usage(part.mountpoint)
                    result[part.mountpoint] = {
                        "device": part.device,
                        "fstype": part.fstype,

                        "total": self.calc_gb(usage.total),
                        "used": self.calc_gb(usage.used),
                        "free": self.calc_gb(usage.free),

                        "percent": usage.percent,
                    }
                    try:
                        if os.path.commonpath([part.mountpoint, os.getcwd()]) == part.mountpoint:
                            result["current_device"] = part.mountpoint
                    except:
                        pass

                except PermissionError as exc:
                    # Некоторые разделы могут быть недоступны (например, монтированные с правами root)
                    result[part.mountpoint] = {"error": f"{exc!r}"}

        except Exception as exc:
            result["error"] = f"{exc!r}"
        return result

    def _get_dynamic__network_stats(self) -> dict[str, Any]:
        """Сетевая статистика (байты, пакеты, ошибки)."""
        try:
            net = psutil.net_io_counters()
            return {
                "bytes_sent": self.calc_gb(net.bytes_sent),
                "bytes_recv": self.calc_gb(net.bytes_recv),

                "packets_sent": net.packets_sent,
                "packets_recv": net.packets_recv,

                "errin": net.errin,
                "errout": net.errout,
                "dropin": net.dropin,
                "dropout": net.dropout,
            }
        except Exception as exc:
            return {"error": str(exc)}

    def _get_process_count(self) -> int:
        """Количество запущенных процессов."""
        try:
            return len(psutil.pids())
        except Exception as exc:
            return -1

    def _get_uptime(self) -> Optional[float]:
        """Время работы системы в секундах с момента загрузки."""
        try:
            return psutil.time() - psutil.boot_time()
        except Exception as exc:
            return None


# =====================================================================================================================
def get_client(request: Request | None = None) -> dict:
    result = {}

    # CLIENT будет заполнен на фронтенде в JS
    result["ip"] = "—"
    result["browser"] = "—"
    result["os"] = "—"
    result["local_time"] = "—"
    result["user_agent"] = "—"
    result["url"] = "—"

    if request is not None:
        client_ip = request.client.host
        if not client_ip:
            if "x-forwarded-for" in request.headers:
                client_ip = request.headers["x-forwarded-for"].split(",")[0].strip()

        result["client_ip"] = client_ip
        result["host_domain"] = request.url.hostname
        result["url"] = str(request.url)
        result["ip"] = request.client.host if request.client else None
        result["user_agent"] = request.headers.get("user-agent")

    return result


# =====================================================================================================================
