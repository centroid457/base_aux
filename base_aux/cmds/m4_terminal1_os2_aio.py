import asyncio

from base_aux.cmds.m2_history import *
from base_aux.cmds.m4_terminal0_base import *


# =====================================================================================================================
class CmdTerminal_OsAio(Base_CmdTerminalAio):
    """
    Асинхронная версия CmdTerminal_OsSync на asyncio.subprocess.
    """
    _conn: asyncio.subprocess.Process | None
    EOL_SEND: str = "\n"

    # -----------------------------------------------------------------------------------------------------------------
    async def _create_conn(self) -> None | NoReturn:
        self._conn = await asyncio.create_subprocess_exec(
            self._shell_cmd,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=self.cwd,
            # text=True,                                            # not appropriate!
            # encoding="cp866" if os.name == "nt" else "utf8",      # not appropriate!
        )

    def _create_tasks(self) -> None:
        self._bg_tasks = [
            asyncio.create_task(self._bg_reading_buffer__stdout()),
            asyncio.create_task(self._bg_reading_buffer__stderr()),
        ]

    # -----------------------------------------------------------------------------------------------------------------
    async def _del_conn(self) -> None:
        if self._conn is not None:
            try:
                self._conn.terminate()
                # Ждём завершения процесса с таймаутом
                try:
                    await asyncio.wait_for(self._conn.wait(), timeout=2.0)
                except asyncio.TimeoutError:
                    self._conn.kill()
                    await self._conn.wait()
            except Exception:
                pass
            self._conn = None

    async def _del_tasks(self) -> None:
        self._stop_reading = True

        # Отменяем задачи чтения
        for task in self._bg_tasks:
            task.cancel()
        # Ждём их завершения с таймаутом, игнорируя ошибки
        try:
            await asyncio.wait_for(
                asyncio.gather(*self._bg_tasks, return_exceptions=True),
                timeout=2
            )
        except asyncio.TimeoutError:
            # Если задачи не завершились, просто забудем о них
            pass
        self._bg_tasks.clear()

    # -----------------------------------------------------------------------------------------------------------------
    async def _read_byte_with_timeout(
            self,
            timeout: float = 0.05,
            buffer_type: EnumAdj_BufferType = EnumAdj_BufferType.STDOUT,
    ) -> bytes | NoReturn | Exc__Io | Exc__UnDefined | Exc__WrongUsage | asyncio.CancelledError:
        buffer: asyncio.StreamReader | None = None

        if self._conn is None:
            raise Exc__IoConnection(f"{self._conn=}")

        # init BUFFER -------------------
        if buffer_type == EnumAdj_BufferType.STDOUT:
            buffer = self._conn.stdout
        elif buffer_type == EnumAdj_BufferType.STDERR:
            buffer = self._conn.stderr
        else:
            raise Exc__WrongUsage(f'{buffer_type=}')

        if buffer is None:
            raise Exc__WrongUsage(f"{self._conn=}/{buffer_type=}/{buffer=}")

        # READ -------------------
        try:
            new_byte = await asyncio.wait_for(buffer.read(1), timeout=timeout)
            return new_byte
        except asyncio.CancelledError:
            raise
        except asyncio.TimeoutError as exc:
            raise Exc__IoTimeout(f"{exc!r}")
        except (BrokenPipeError, ConnectionResetError) as exc:
            raise Exc__IoConnection(f"{exc!r}")
        except BaseException as exc:
            raise Exc__UnDefined(f"{exc!r}")

    # -----------------------------------------------------------------------------------------------------------------
    async def send_command(
            self,
            cmd: str,
            timeout_start: float | None = None,
            timeout_finish: float | None = None
    ) -> CmdResult:
        self.history.add_data__stdin(cmd)
        try:
            self._conn.stdin.write(f"{cmd}\n".encode(self._encoding))
            await self._conn.stdin.drain()

            if await self._wait__finish_executing_cmd(timeout_start, timeout_finish):
                finished_status = EnumAdj_FinishedStatus.CORRECT
            else:
                finished_status = EnumAdj_FinishedStatus.TIMED_OUT
        except Exception as exc:
            print(f"{exc!r}")
            self.history.add_data__stderr(f"{exc!r}")
            finished_status = EnumAdj_FinishedStatus.EXCEPTION

        self.history.set_finished(status=finished_status)
        return self.history.last_result


# =====================================================================================================================
async def explore__ping():
    async with CmdTerminal_OsAio() as term:
        # await term.send_command("ping ya.ru -n 2", timeout_finish=1.1)

        # for i in range(3):
        #     await term.send_command(f"echo final {i}")

        await term.send_command("echo finish!")
        await asyncio.sleep(10)

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


async def explore__smth():
    async with CmdTerminal_OsAio() as term:
        await term.send_command("echo start!")
        await term.send_command("echo finish!")
        await asyncio.sleep(2)

    await asyncio.sleep(0.5)


# =====================================================================================================================
if __name__ == "__main__":
    # asyncio.run(explore__ping())
    # asyncio.run(explore__cd())
    # asyncio.run(explore__cd_reconnect())
    asyncio.run(explore__smth())


# =====================================================================================================================
