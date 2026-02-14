import asyncio
import os

from base_aux.cmds.m2_history import *
from base_aux.cmds.m4_terminal0_base import *


# =====================================================================================================================
class CmdTerminal_OsAio(Base_CmdTerminal):
    """
    Асинхронная версия CmdTerminal_Os на asyncio.subprocess.
    """
    _conn: asyncio.subprocess.Process | None
    _reader_tasks: list[asyncio.Task]

    def __init__(
            self,
            *,
            cwd: str | None = None,
            **kwargs,
    ):
        super().__init__(**kwargs)

        self.cwd: str | None = cwd
        self.shell_cmd: str = "cmd" if os.name == "nt" else "bash"

    # -----------------------------------------------------------------------------------------------------------------
    async def connect(self) -> bool:
        if self._conn is not None:
            return True

        print(f"{self.__class__.__name__}({self.id=}).connect")

        try:
            self._conn = await asyncio.create_subprocess_exec(
                self.shell_cmd,
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=self.cwd,
                # text=True,                                            # not appropriate!
                # encoding="cp866" if os.name == "nt" else "utf8",      # not appropriate!
            )
        except Exception as exc:
            msg = f"{self.__class__.__name__}({self.id=}){exc!r}"
            print(msg)
            self.history.append_stderr(msg)
            return False

        self._stop_reading = False

        self._reader_tasks = [
            asyncio.create_task(self._reading_stdout()),
            asyncio.create_task(self._reading_stderr()),
        ]

        await asyncio.sleep(0.3)
        return True

    # -----------------------------------------------------------------------------------------------------------------
    async def disconnect(self) -> None:
        """Корректное завершение процесса и остановка задач чтения."""
        if self._conn is not None:
            # Попытка отправить exit перед закрытием
            try:
                await self.send_command("exit")
            except Exception:
                pass

            try:
                self._conn.terminate()
                try:
                    await asyncio.wait_for(self._conn.wait(), timeout=1.0)
                except asyncio.TimeoutError:
                    self._conn.kill()
                    await self._conn.wait()
            except Exception:
                pass

        self._stop_reading = True

        # Отменяем задачи чтения и ждём их завершения
        for task in self._reader_tasks:
            task.cancel()
        await asyncio.gather(*self._reader_tasks, return_exceptions=True)
        self._reader_tasks.clear()
        self._conn = None

        print(f"{self.__class__.__name__}({self.id=}).disconnected")

    # -----------------------------------------------------------------------------------------------------------------
    async def reconnect(self) -> None:
        await self.disconnect()
        await self.connect()

    # -----------------------------------------------------------------------------------------------------------------
    async def _reading_stdout(self):
        """Асинхронное чтение stdout."""
        while not self._stop_reading and self._conn:
            try:
                line = await self._conn.stdout.readline()
                if not line:
                    break
                line = line.decode(self._encoding)
                line = line.rstrip()
                if line:
                    print(f"[STDOUT]{line}")
                    self.history.append_stdout(line)
                self.history.set_retcode(self._conn.returncode)
            except asyncio.CancelledError:
                break
            except Exception as exc:
                print(f"stdout reader error: {exc!r}")
                break

    async def _reading_stderr(self):
        """Асинхронное чтение stderr."""
        while not self._stop_reading and self._conn:
            try:
                line = await self._conn.stderr.readline()
                if not line:
                    break
                line = line.decode(self._encoding)
                line = line.rstrip()
                if line:
                    print(f"[STDERR]{line}")
                    self.history.append_stderr(line)
                self.history.set_retcode(self._conn.returncode)
            except asyncio.CancelledError:
                break
            except Exception as exc:
                print(f"stderr reader error: {exc!r}")
                break

    # -----------------------------------------------------------------------------------------------------------------
    async def wait__finish_executing_cmd(
            self,
            timeout_start: float | None = None,
            timeout_finish: float | None = None
    ) -> bool:
        """
        Ожидание завершения активности команды.
        Асинхронная версия: проверяет изменение времени последнего вывода.
        """
        timeout_start = timeout_start or self.timeout_start
        timeout_finish = timeout_finish or self.timeout_finish

        data_received = False
        last_duration = self.history.last_result.duration

        # Первый этап – ждём начала активности (timeout_start)
        time_start = asyncio.get_event_loop().time()
        while asyncio.get_event_loop().time() - time_start < timeout_start:
            if self.history.last_result.duration != last_duration:
                data_received = True
                last_duration = self.history.last_result.duration
                # Переключаемся на ожидание тишины
                time_start = asyncio.get_event_loop().time()
                timeout_start = timeout_finish
            else:
                await asyncio.sleep(timeout_finish / 3)

        return data_received

    # -----------------------------------------------------------------------------------------------------------------
    async def send_command(
            self,
            cmd: str,
            timeout_start: float | None = None,
            timeout_finish: float | None = None
    ) -> CmdResult:
        print(f"\n[STD_IN]--->{cmd}")
        self.history.add_input(cmd)
        try:
            # Запись в stdin процесса
            self._conn.stdin.write(f"{cmd}\n".encode(self._encoding))
            await self._conn.stdin.drain()

            # Ожидание завершения вывода команды
            if await self.wait__finish_executing_cmd(timeout_start, timeout_finish):
                finished_status = EnumAdj_FinishedStatus.CORRECT
            else:
                finished_status = EnumAdj_FinishedStatus.TIMED_OUT
        except Exception as exc:
            print(f"{exc!r}")
            self.history.append_stderr(f"{exc!r}")
            finished_status = EnumAdj_FinishedStatus.EXCEPTION

        self.history.set_finished(status=finished_status)
        return self.history.last_result

    # -----------------------------------------------------------------------------------------------------------------
    # Асинхронный контекстный менеджер
    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.disconnect()


# =====================================================================================================================
async def explore__ping():
    async with CmdTerminal_OsAio() as term:
        if not await term.connect():
            return

        await term.send_command("ping ya.ru -n 2", timeout_finish=1.1)

        for i in range(3):
            await term.send_command(f"echo final {i}")

        await term.send_command("echo finish!")

    await asyncio.sleep(0.5)


async def explore__cd():
    async with CmdTerminal_OsAio() as term:
        if not await term.connect():
            return

        commands = [
            "cd ..",
            "cd",
            "dir" if os.name == "nt" else "ls -la",
            "cd ..",
            "cd",
            "dir" if os.name == "nt" else "ls -la",
            "echo привет!!!"
        ]
        for cmd in commands:
            await term.send_command(cmd)

    await asyncio.sleep(0.5)


async def explore__cd_reconnect():
    async with CmdTerminal_OsAio() as term:
        if not await term.connect():
            return

        for _ in range(3):
            await term.send_command("cd ../..")
            await term.send_command("cd")
            await term.reconnect()

    await asyncio.sleep(0.5)


# =====================================================================================================================
if __name__ == "__main__":
    asyncio.run(explore__ping())
    # asyncio.run(explore__cd())
    # asyncio.run(explore__cd_reconnect())


# =====================================================================================================================
