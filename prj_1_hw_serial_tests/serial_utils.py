import serial
import serial.tools.list_ports
import time
import threading
from typing import Optional, List, Tuple
import logging


# =====================================================================================================================
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# =====================================================================================================================
def port_try_open(port: str) -> bool:
    try:
        conn = serial.Serial(port, timeout=1)
        conn.close()
        return True
    except:
        return False


# =====================================================================================================================
class DeviceConsole:
    """Управление подключением к устройству через serial-консоль."""

    def __init__(self, port: str, baudrate: int = 115200, timeout: float = 1):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.ser = None
        self.device_id = None

    def connect(self):
        """Открыть serial-порт."""
        self.ser = serial.Serial(self.port, self.baudrate, timeout=self.timeout)

    def login(self, username: str = "root", password: str = "1", login_timeout: int = 30):
        """
        Дождаться приглашения login, ввести логин и пароль,
        затем дождаться приглашения командной строки.
        Возвращает True, если успешно.
        """
        # Ждём появления приглашения "login:" или уже готовой консоли
        start = time.time()
        prompt_found = False
        while time.time() - start < login_timeout:
            data = self._read_all()
            if "login:" in data:
                prompt_found = True
                self.ser.write((username + "\r").encode())
                time.sleep(0.5)
                # ждём Password:
                data = self._read_until("Password:")
                if "Password:" in data:
                    self.ser.write((password + "\r").encode())
                break
            elif "root@" in data or "# " in data:
                # уже залогинены
                prompt_found = True
                break
            time.sleep(0.5)
        if not prompt_found:
            return False
        # Ожидаем приглашение после пароля
        self._wait_for_prompt(timeout=10)
        return True

    def _read_all(self) -> str:
        """Прочитать всё доступное из буфера."""
        if self.ser.in_waiting:
            return self.ser.read(self.ser.in_waiting).decode(errors='ignore')
        return ""

    def _read_until(self, expected: str, timeout: int = 10) -> str:
        """Читать, пока не встретится expected или таймаут."""
        start = time.time()
        buf = ""
        while time.time() - start < timeout:
            chunk = self._read_all()
            buf += chunk
            if expected in buf:
                break
            time.sleep(0.1)
        return buf

    def _wait_for_prompt(self, timeout: int = 5):
        """Ожидать появления стандартного приглашения #."""
        self._read_until("# ", timeout)

    def exec_command(self, cmd: str, wait_prompt: bool = True, timeout: int = 10) -> str:
        """
        Выполнить команду и вернуть вывод.
        Если wait_prompt=True, ждёт появления приглашения после команды.
        """
        self.ser.write((cmd + "\r").encode())
        if wait_prompt:
            self._wait_for_prompt(timeout)
        return self._read_all()

    def close(self):
        if self.ser and self.ser.is_open:
            self.ser.close()

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


def find_device_port(baudrate: int = 115200, timeout_per_port: float = 1) -> tuple[DeviceConsole, str]:
    """
    Сканировать доступные serial-порты, найти устройство.
    Возвращает объект DeviceConsole и имя порта.
    Если найдено больше одного – вызывает исключение.
    """
    ports = [port.device for port in serial.tools.list_ports.comports()]
    if not ports:
        return ports

    results = {}
    threads = []

    def worker(port):
        console = validate_port(port, baudrate, timeout_per_port)
        if console:
            results[port] = console

    for p in ports:
        t = threading.Thread(target=worker, args=(p,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    if len(results) == 1:
        port, console = list(results.items())[0]
        return console, port
    elif len(results) == 0:
        raise RuntimeError("Устройство не найдено ни на одном порту.")
    else:
        raise RuntimeError(f"Найдено несколько устройств на портах: {list(results.keys())}")


# =====================================================================================================================
