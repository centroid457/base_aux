import asyncio
from types import SimpleNamespace

from base_aux.cmds.m5_terminal0_abc1_user import *
from base_aux.cmds.m5_terminal2_serial0_base import *
from base_aux.cmds.m5_terminal0_abc3_paradigm import BaseAio_CmdTerminal

import serial_asyncio


# =====================================================================================================================
class CmdTerminal_SerialAio(Base_CmdTerminal_Serial, BaseAio_CmdTerminal):

    _conn: SimpleNamespace | None

    # -----------------------------------------------------------------------------------------------------------------
    async def _create_conn(self) -> None:
        """
        Открывает асинхронное serial‑соединение.
        """
        reader, writer = await serial_asyncio.open_serial_connection(
            url=self._serial_port,
            baudrate=self._serial_baudrate,
            bytesize=self._serial_bytesize,
            parity=self._serial_parity,
            stopbits=self._serial_stopbits,
        )
        # Эмулируем структуру asyncio.subprocess.Process для совместимости с _bg_reading_buffer
        self._conn = SimpleNamespace(
            stdout=reader,    # именно отсюда будет читать _bg_reading_buffer
            stderr=None,      # stderr отсутствует в serial
            stdin=writer,
            returncode=None,  # serial не возвращает код завершения
        )

    def _create_tasks(self) -> None:
        """
        Запускает только чтение stdout (stderr для serial не нужен).
        """
        self._bg_tasks = [
            asyncio.create_task(self._bg_reading_buffer__stdout()),
        ]
        
    # -----------------------------------------------------------------------------------------------------------------
    async def _del_conn(self) -> None:
        """Закрывает serial‑соединение."""
        if self._conn is not None:
            writer = self._conn.stdin
            if writer is not None:
                writer.close()
                try:
                    await writer.wait_closed()
                except Exception:
                    pass
            self._conn = None

    # -----------------------------------------------------------------------------------------------------------------
    async def _read_byte_with_timeout(
            self,
            timeout: float = 0.05,
            *args, **kwargs,
    ) -> bytes:
        """Читает один байт из reader с таймаутом."""
        if self._conn is None:
            raise Exc__IoConnection(f"{self._conn=}")
        reader = self._conn.stdout
        if reader is None:
            raise Exc__IoConnection("reader is None")

        try:
            new_byte = await asyncio.wait_for(reader.read(1), timeout=timeout)
            return new_byte
        except asyncio.CancelledError:
            raise
        except asyncio.TimeoutError as exc:
            raise Exc__IoTimeout(f"{timeout=}/{exc!r}", noprint=True)
        except (BrokenPipeError, ConnectionResetError) as exc:
            raise Exc__IoConnection(f"{exc!r}")
        except BaseException as exc:
            raise Exc__UnDefined(f"{exc!r}")

    # -----------------------------------------------------------------------------------------------------------------
    async def _write_line(
            self,
            cmd: str,
            timeout: float | None = None,
            eol: str | None = None,
    ) -> None:
        """Отправляет строку в последовательный порт."""
        EOL = eol if eol is not None else self.EOL_SEND

        self._conn.stdin.write(f"{cmd}{EOL}".encode(self._encoding))
        await self._conn.stdin.drain()

    # -----------------------------------------------------------------------------------------------------------------
    async def _wait__finish_executing_cmd(
            self,
            timeout_read_start: float | None = None,
            timeout_read_finish: float | None = None,
    ) -> bool:
        """
        Ожидание завершения вывода команды.
        Аналог версии для ОС, но без проверки returncode (в serial его нет).
        """
        timeout_read_start = self.timeout_def.get_active__read_start(timeout_read_start)
        timeout_read_finish = self.timeout_def.get_active__read_finish(timeout_read_finish)

        start_wait = asyncio.get_event_loop().time()
        while asyncio.get_event_loop().time() - start_wait < timeout_read_start:
            # Как только получили хотя бы один байт – переходим к короткому таймауту
            if self._last_byte_time != start_wait:
                quiet_start = asyncio.get_event_loop().time()
                while asyncio.get_event_loop().time() - quiet_start < timeout_read_finish:
                    if self._last_byte_time != quiet_start:
                        quiet_start = asyncio.get_event_loop().time()
                    await asyncio.sleep(0.05)
                return True
            await asyncio.sleep(0.05)
        return False


# =====================================================================================================================
if __name__ == "__main__":
    pass
    # asyncio.run(explore__ping())
    # asyncio.run(explore__cd())
    # asyncio.run(explore__cd_reconnect())
    # asyncio.run(explore__smth())


# =====================================================================================================================
