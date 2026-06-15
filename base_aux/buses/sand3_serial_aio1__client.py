import asyncio
import logging
from contextlib import asynccontextmanager
from typing import Optional, Callable, Awaitable

import serial_asyncio


# =====================================================================================================================
logger = logging.getLogger(__name__)


# =====================================================================================================================
class SerialClient_Aio:
    """Асинхронное соединение с последовательным портом.

    Параметры:
        port: устройство (например, 'COM3' или '/dev/ttyUSB0').
        baudrate: скорость.
        on_data: асинхронный callback при получении данных (bytes).
        read_timeout: тайм-аут чтения (сек).
        reconnect_delay: задержка перед переподключением (сек).
        max_reconnect_attempts: максимальное число попыток переподключения (0 - бесконечно).
    """

    def __init__(
        self,
        port: str,
        baudrate: int = 115200,
        on_data: Optional[Callable[[bytes], Awaitable[None]]] = None,
        read_timeout: float = 1.0,
        reconnect_delay: float = 2.0,
        max_reconnect_attempts: int = 5,
    ):
        self.port = port
        self.baudrate = baudrate
        self.on_data = on_data
        self.read_timeout = read_timeout
        self.reconnect_delay = reconnect_delay
        self.max_reconnect_attempts = max_reconnect_attempts

        self._reader: Optional[asyncio.StreamReader] = None
        self._writer: Optional[asyncio.StreamWriter] = None
        self._write_queue: asyncio.Queue[bytes] = asyncio.Queue()
        self._reader_task: Optional[asyncio.Task] = None
        self._writer_task: Optional[asyncio.Task] = None
        self._reconnect_task: Optional[asyncio.Task] = None
        self._stop_event = asyncio.Event()
        self._connected = False
        self._lock = asyncio.Lock()

    async def open(self) -> None:
        """Открыть порт и запустить задачи чтения/записи."""
        if self._connected:
            return
        await self._connect()
        self._reader_task = asyncio.create_task(self._reader_loop())
        self._writer_task = asyncio.create_task(self._writer_loop())
        self._connected = True
        logger.info(f"Порт {self.port} открыт")

    async def close(self) -> None:
        """Закрыть порт и остановить все задачи."""
        if not self._connected:
            return
        self._stop_event.set()          # сигнал остановки для циклов
        await self._cancel_tasks()
        await self._disconnect()
        self._connected = False
        logger.info(f"Порт {self.port} закрыт")

    async def send(self, data: bytes) -> None:
        """Поставить данные в очередь на отправку."""
        if not self._connected:
            raise ConnectionError("Порт не открыт")
        await self._write_queue.put(data)

    async def _connect(self) -> None:
        """Установить физическое соединение."""
        try:
            self._reader, self._writer = await serial_asyncio.open_serial_connection(
                url=self.port,
                baudrate=self.baudrate,
            )
        except Exception as e:
            logger.error(f"Ошибка подключения к {self.port}: {e}")
            raise

    async def _disconnect(self) -> None:
        """Закрыть stream'ы."""
        if self._writer:
            try:
                self._writer.close()
                await self._writer.wait_closed()
            except Exception:
                pass
        self._reader = None
        self._writer = None

    async def _reader_loop(self) -> None:
        """Цикл чтения данных."""
        while not self._stop_event.is_set():
            try:
                data = await asyncio.wait_for(
                    self._reader.read(1024),
                    timeout=self.read_timeout,
                )
                if data and self.on_data:
                    await self.on_data(data)
            except asyncio.TimeoutError:
                continue
            except (OSError, asyncio.IncompleteReadError) as e:
                logger.warning(f"Ошибка чтения: {e}")
                if not self._stop_event.is_set():
                    await self._reconnect()
            except Exception as e:
                logger.error(f"Неожиданная ошибка в reader loop: {e}", exc_info=True)
                break

    async def _writer_loop(self) -> None:
        """Цикл записи данных из очереди."""
        while not self._stop_event.is_set():
            try:
                data = await asyncio.wait_for(
                    self._write_queue.get(),
                    timeout=self.read_timeout,
                )
                self._writer.write(data)
                await self._writer.drain()
            except asyncio.TimeoutError:
                continue
            except (OSError, ConnectionError) as e:
                logger.warning(f"Ошибка записи: {e}")
                if not self._stop_event.is_set():
                    await self._reconnect()
            except Exception as e:
                logger.error(f"Неожиданная ошибка в writer loop: {e}", exc_info=True)
                break

    async def _cancel_tasks(self) -> None:
        """Аккуратно завершить все запущенные задачи."""
        tasks = [
            t for t in (self._reader_task, self._writer_task, self._reconnect_task)
            if t and not t.done()
        ]
        for t in tasks:
            t.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)

    async def _reconnect(self) -> None:
        """Переподключение с ограничением попыток."""
        async with self._lock:   # защита от параллельных вызовов reconnect
            if self._stop_event.is_set():
                return
            await self._disconnect()
            attempts = 0
            while not self._stop_event.is_set():
                if self.max_reconnect_attempts and attempts >= self.max_reconnect_attempts:
                    logger.error(f"Исчерпаны попытки переподключения к {self.port}")
                    self._stop_event.set()
                    return
                attempts += 1
                logger.info(f"Попытка переподключения {attempts}/{self.max_reconnect_attempts or '∞'}")
                try:
                    await self._connect()
                    logger.info(f"Переподключение к {self.port} успешно")
                    return
                except Exception as e:
                    logger.warning(f"Не удалось: {e}")
                    await asyncio.sleep(self.reconnect_delay)

    # --- Удобные менеджеры контекста ---
    @asynccontextmanager
    async def connection(self):
        """Асинхронный контекстный менеджер для автоматического открытия/закрытия."""
        await self.open()
        try:
            yield self
        finally:
            await self.close()


# =====================================================================================================================
async def handle_data(data: bytes):
    print(f"Получено: {data.hex()}")


async def main():
    conn = SerialClient_Aio(
        port="COM3",
        baudrate=9600,
        on_data=handle_data,
        reconnect_delay=3,
        max_reconnect_attempts=10,
    )
    async with conn.connection():
        await conn.send(b"Hello, device!\r\n")
        await asyncio.sleep(10)   # работаем 10 секунд
    # автоматическое закрытие даже при исключении


# =====================================================================================================================
asyncio.run(main())


# =====================================================================================================================
