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


# =====================================================================================================================
if __name__ == "__main__":
    pass
    # asyncio.run(explore__ping())
    # asyncio.run(explore__cd())
    # asyncio.run(explore__cd_reconnect())
    # asyncio.run(explore__smth())


# =====================================================================================================================
