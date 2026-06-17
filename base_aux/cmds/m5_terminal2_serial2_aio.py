import asyncio
from abc import abstractmethod
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
            url=self.idn,
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

    def _tasks_bg__create_start(self) -> None:
        """
        Запускает только чтение stdout (stderr для serial не нужен).
        """
        self._tasks_bg = [
            asyncio.create_task(self._bg_reading_buffer__stdout()),
        ]
        
    # -----------------------------------------------------------------------------------------------------------------
    async def _del_conn(self) -> None:
        """Закрывает serial‑соединение."""
        self._event_connected.clear()

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
            buffer: asyncio.StreamReader,
            timeout: float = 0.05,
    ) -> bytes | NoReturn | Exc__Io | Exc__UnDefined | Exc__WrongUsage | asyncio.CancelledError:

        if self._conn is None:
            raise Exc__IoConnection(f"{self._conn=}")

        # init BUFFER -------------------
        if not isinstance(buffer, asyncio.StreamReader):
            raise Exc__WrongUsage(f'{buffer=}')

        if buffer is None:
            raise Exc__WrongUsage(f"{self._conn=}/{buffer=}")

        # READ -------------------
        try:
            new_byte = await asyncio.wait_for(buffer.read(1), timeout=timeout)
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
        if not self._event_connected.is_set():
            return

        EOL = eol if eol is not None else self.EOL_SEND

        self._conn.stdin.write(f"{cmd}{EOL}".encode(self._encoding))
        await self._conn.stdin.drain()


# =====================================================================================================================
async def explore__1():
    async with CmdTerminal_SerialAio(port="COM3") as term:
        print(await term.send_cmd("echo start!"))
        print(await term.send_cmd("echo finish!"))

    # await asyncio.sleep(0.5)


# =====================================================================================================================
if __name__ == "__main__":
    pass
    asyncio.run(explore__1())


# =====================================================================================================================
