import asyncio
import logging
from typing import Dict, Optional, Set, Callable, Awaitable

import serial.tools.list_ports
from contextlib import asynccontextmanager

from m3_serial_aio1__client import SerialClient_Aio
import contextlib

# =====================================================================================================================
logger = logging.getLogger(__name__)


# =====================================================================================================================
class ManagerSerialAio:
    """Асинхронный менеджер последовательных портов.

    Автоматически создаёт/удаляет объекты SerialClient_Aio
    при появлении/исчезновении портов в системе.

    Параметры:
        poll_interval: интервал опроса системы (сек).
        connection_kwargs: словарь аргументов по умолчанию для SerialClient_Aio
                           (port, baudrate, on_data и т.д.).
        on_port_added: опциональный асинхронный callback при добавлении порта (порт, соединение).
        on_port_removed: опциональный асинхронный callback при удалении порта (порт).
        connection_factory: опциональная асинхронная фабрика, которая получает порт и
                            connection_kwargs, возвращает SerialClient_Aio.
    """

    def __init__(
        self,
        poll_interval: float = 2.0,
        connection_kwargs: Optional[Dict] = None,
        on_port_added: Optional[Callable[[str, 'SerialClient_Aio'], Awaitable[None]]] = None,
        on_port_removed: Optional[Callable[[str], Awaitable[None]]] = None,
        connection_factory: Optional[Callable[..., Awaitable['SerialClient_Aio']]] = None,
    ):
        self._poll_interval = poll_interval
        self._connection_kwargs = connection_kwargs or {}
        self._on_port_added = on_port_added
        self._on_port_removed = on_port_removed
        self._connection_factory = connection_factory or self._default_factory

        self._connections: Dict[str, 'SerialClient_Aio'] = {}
        self._lock = asyncio.Lock()
        self._monitor_task: Optional[asyncio.Task] = None
        self._stop_event = asyncio.Event()

    async def start(self) -> None:
        """Запустить мониторинг портов."""
        if self._monitor_task is not None:
            return
        self._stop_event.clear()
        # Первичное заполнение без гонки
        await self._initial_scan()
        self._monitor_task = asyncio.create_task(self._monitor_loop())
        logger.info("Мониторинг портов запущен")

    async def stop(self) -> None:
        """Остановить мониторинг и закрыть все соединения."""
        if self._monitor_task is None:
            return
        self._stop_event.set()
        self._monitor_task.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await self._monitor_task
        self._monitor_task = None

        # Закрываем все активные соединения
        async with self._lock:
            for port in list(self._connections.keys()):
                await self._remove_port(port)
        logger.info("Мониторинг портов остановлен")

    async def get_connection(self, port: str) -> Optional['SerialClient_Aio']:
        """Получить объект соединения для указанного порта (если существует)."""
        async with self._lock:
            return self._connections.get(port)

    async def _default_factory(self, port: str, **kwargs) -> 'SerialClient_Aio':
        """Фабрика по умолчанию: создаёт SerialClient_Aio с переданными параметрами."""
        merged_kwargs = {**self._connection_kwargs, **kwargs, "port": port}
        return SerialClient_Aio(**merged_kwargs)

    async def _initial_scan(self) -> None:
        """Первоначальное сканирование портов (при старте)."""
        current_ports = self._list_ports()
        for port in current_ports:
            await self._add_port(port)

    async def _monitor_loop(self) -> None:
        """Фоновый цикл опроса портов."""
        while not self._stop_event.is_set():
            try:
                current_ports = self._list_ports()
                async with self._lock:
                    existing = set(self._connections.keys())
                new_ports = current_ports - existing
                removed_ports = existing - current_ports

                # Добавляем новые порты
                for port in new_ports:
                    await self._add_port(port)

                # Удаляем исчезнувшие порты
                for port in removed_ports:
                    await self._remove_port(port)

            except Exception as e:
                logger.error(f"Ошибка в цикле мониторинга: {e}", exc_info=True)

            await asyncio.sleep(self._poll_interval)

    def _list_ports(self) -> Set[str]:
        """Возвращает множество имён портов, доступных в системе."""
        return {comport.device for comport in serial.tools.list_ports.comports()}

    async def _add_port(self, port: str) -> None:
        """Создать и сохранить объект соединения для нового порта."""
        async with self._lock:
            if port in self._connections:
                return  # уже добавлен (гонка)

            logger.info(f"Обнаружен новый порт: {port}")
            try:
                conn = await self._connection_factory(port)
                await conn.open()
                self._connections[port] = conn
                logger.info(f"Соединение с портом {port} установлено")
                if self._on_port_added:
                    await self._on_port_added(port, conn)
            except Exception as e:
                logger.error(f"Не удалось открыть порт {port}: {e}")

    async def _remove_port(self, port: str) -> None:
        """Закрыть и удалить объект соединения для исчезнувшего порта."""
        async with self._lock:
            conn = self._connections.pop(port, None)
            if conn is None:
                return

            logger.info(f"Порт {port} удалён из системы, закрываем соединение")
            try:
                await conn.close()
            except Exception as e:
                logger.warning(f"Ошибка при закрытии порта {port}: {e}")
            finally:
                if self._on_port_removed:
                    await self._on_port_removed(port)

    # --- Удобный контекстный менеджер ---
    @asynccontextmanager
    async def run(self):
        """Асинхронный контекстный менеджер для автоматического запуска/остановки."""
        await self.start()
        try:
            yield self
        finally:
            await self.stop()


# =====================================================================================================================
async def handle_data(port: str, data: bytes):
    print(f"[{port}] Получено {len(data)} байт")

async def on_port_connected(port: str, conn: SerialClient_Aio):
    print(f"Порт {port} подключён, начинаем слушать")
    # Можно отправить приветствие
    await conn.send(b"AT\r\n")

async def on_port_disconnected(port: str):
    print(f"Порт {port} отключён от системы")

async def main():
    # Фабрика, которая создаёт соединения с индивидуальными настройками
    async def my_factory(port: str) -> SerialClient_Aio:
        return SerialClient_Aio(
            port=port,
            baudrate=9600,
            on_data=lambda data: handle_data(port, data),
            reconnect_delay=5,
            max_reconnect_attempts=10,
        )

    manager = ManagerSerialAio(
        poll_interval=3.0,
        connection_factory=my_factory,
        on_port_added=on_port_connected,
        on_port_removed=on_port_disconnected,
    )

    async with manager.run():
        # Работаем 60 секунд, менеджер сам следит за портами
        await asyncio.sleep(60)

    # При выходе из контекста все соединения будут корректно закрыты


# =====================================================================================================================
if __name__ == "__main__":
    asyncio.run(main())


# =====================================================================================================================
