from typing import *

import time
import threading
import logging

from base_aux.buses.d1_serial2_new.m1_serial_client import *


# =====================================================================================================================
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ======================================================================================================================
class DeviceConsole(Serial):
    """Управление подключением к устройству через serial-консоль"""
    def __init__(self, port: str, baudrate: int = 115200, timeout: float = 1):
        super().__init__(port, baudrate, timeout)
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout

        self._conn = None
        self.device_id = None

    # ------------------------------------------------------------------------------------------------------------------
    def _wait_for_prompt(self, timeout: int = 2):
        """Ожидать появления стандартного приглашения #."""
        self._read_until("# ", timeout)

    # ------------------------------------------------------------------------------------------------------------------
    def exec_command(self, cmd: str, wait_prompt: bool = True, timeout: int = 2) -> str:
        """
        Выполнить команду и вернуть вывод.
        Если wait_prompt=True, ждёт появления приглашения после команды.
        """
        self._conn.write((cmd + "\r\n").encode())
        if wait_prompt:
            self._wait_for_prompt(timeout)
        return self._read_all()

    # ------------------------------------------------------------------------------------------------------------------
    def login(self, username: str = "root", password: str = "1", login_timeout: int = 2) -> bool:
        """
        Дождаться приглашения login, ввести логин и пароль,
        затем дождаться приглашения командной строки.
        Возвращает True, если успешно.
        """
        # Ждём появления приглашения "login:" или уже готовой консоли
        self.buffer_clear()
        time.sleep(0.3)
        if not self.check__buffer_is_blank():
            return False
        self._conn.write((username + "\r\n").encode())
        data = self._read_until("Password:", 2)
        if "Password:" in data:
            self._conn.write((password + "\r\n").encode())
        time.sleep(0.5)

        # Ожидаем приглашение после пароля
        self._wait_for_prompt(timeout=2)
        return True

    def get_device_id(self) -> str:
        """Получить уникальный идентификатор устройства (серийный номер процессора)."""
        if self.device_id is None:
            output = self.exec_command("cat /proc/cpuinfo | grep Serial | awk '{print $NF}'")
            # Если не получилось, попробовать альтернативы
            if not output or len(output) < 5:
                output = self.exec_command("cat /proc/device-tree/serial-number")
            self.device_id = output.strip()
        return self.device_id


# =====================================================================================================================
# Функции поиска порта устройства
def validate_port(port: str, baudrate: int = 115200, timeout: float = 1) -> Optional[DeviceConsole]:
    """Попытаться подключиться к порту, залогиниться и проверить идентификатор."""
    console = DeviceConsole(port, baudrate, timeout)
    try:
        console.connect()
        if console.login():
            # дополнительная проверка: выполнить команду hostname
            hostname = console.exec_command("hostname").strip()
            # можно проверить, что hostname соответствует ожидаемому (например, содержит "harvest")
            # но лучше полагаться на серийный номер
            if hostname:
                console.device_id = console.get_device_id()
                if console.device_id:
                    return console
        console.close()
    except Exception as e:
        logger.debug(f"Port {port} error: {e}")
    return None


# =====================================================================================================================
