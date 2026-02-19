import asyncio

from base_aux.cmds.m2_history import *
from base_aux.cmds.m4_terminal0_base import *


# =====================================================================================================================
class CmdTerminal_OsAio(Abc_CmdTerminal):
    """
    Асинхронная версия CmdTerminal_OsSync на asyncio.subprocess.
    """
    _conn: asyncio.subprocess.Process | None
    _bg_tasks: list[asyncio.Task]

    # -----------------------------------------------------------------------------------------------------------------
    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.disconnect()

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
    async def connect(self) -> bool:
        if self._conn is not None:
            return True

        print(f"{self.__class__.__name__}({self.id=}).connect")

        try:
            await self._create_conn()
        except Exception as exc:
            msg = f"{self.__class__.__name__}({self.id=}){exc!r}"
            print(msg)
            self.history.add_data__stderr(msg)
            return False

        self._stop_reading = False
        self._create_tasks()
        self._last_byte_time = asyncio.get_event_loop().time()

        await asyncio.sleep(0.3)
        return True

    async def disconnect(self) -> None:
        """Корректное завершение процесса и остановка задач чтения."""
        self._stop_reading = True

        if self._conn:
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

        # Отменяем задачи чтения
        for task in self._bg_tasks:
            task.cancel()
        # Ждём их завершения с таймаутом, игнорируя ошибки
        try:
            await asyncio.wait_for(
                asyncio.gather(*self._bg_tasks, return_exceptions=True),
                timeout=3.0
            )
        except asyncio.TimeoutError:
            # Если задачи не завершились, просто забудем о них
            pass
        self._bg_tasks.clear()
        self._conn = None

        print(f"{self.__class__.__name__}({self.id=}).disconnected")

    async def reconnect(self) -> None:
        await self.disconnect()
        await self.connect()
        self.history._listeners__notify('msg_system__style', "🔄 Сессия переподключена")  # оповещаем о переподключении

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

    async def _bg_reading_buffer(self, buffer_type: EnumAdj_BufferType) -> Never | None:
        """
        Чтение потока по одному байту с двумя таймаутами.
        - timeout_start – ожидание первого байта строки.
        - timeout_finish – ожидание последующих байтов.
        - Любой EOL (\r или \n) завершает текущую строку, последующие EOL игнорируются.
        - По таймауту строка также завершается.
        - Добавление в историю через append_method.
        """
        buffer: asyncio.StreamReader | None = None

        if self._conn is None:
            return

        # init BUFFER -------------------
        if buffer_type == EnumAdj_BufferType.STDOUT:
            buffer = self._conn.stdout
            append_method = self.history.add_data__stdout
        elif buffer_type == EnumAdj_BufferType.STDERR:
            buffer = self._conn.stderr
            append_method = self.history.add_data__stderr
        else:
            raise Exc__WrongUsage(f'{buffer_type=}')

        if buffer is None:
            return

        # BUFFER -------------------
        while not self._stop_reading and self._conn is not None:
            bytes_accumulated = bytearray()
            timeout_active = self.timeout_start
            try:
                while True:
                    try:
                        new_byte = await self._read_byte_with_timeout(timeout=timeout_active, buffer_type=buffer_type)
                    except Exc__IoTimeout:
                        break
                    except Exc__IoConnection:
                        # Канал закрыт – выходим из цикла чтения
                        return

                    self._last_byte_time = asyncio.get_event_loop().time()
                    timeout_active = self.timeout_finish

                    if new_byte == b'':  # EOF
                        return

                    if new_byte in (b'\r', b'\n'):
                        if bytes_accumulated:
                            new_line : str = bytes_accumulated.decode(self._encoding).rstrip()
                            if new_line:
                                append_method(new_line)
                                self.history.set_retcode(self._conn.returncode)

                        bytes_accumulated = bytearray()
                        continue
                    else:
                        bytes_accumulated.extend(new_byte)

                if bytes_accumulated:
                    new_line: str  = bytes_accumulated.decode(self._encoding).rstrip()
                    if new_line:
                        append_method(new_line)
                        self.history.set_retcode(self._conn.returncode)

            except asyncio.CancelledError:
                break
            except BaseException as exc:
                print(f"UNEXPECTED _read_stream: {exc!r}")
                break

    async def _bg_reading_buffer__stdout(self):
        await self._bg_reading_buffer(EnumAdj_BufferType.STDOUT)

    async def _bg_reading_buffer__stderr(self):
        await self._bg_reading_buffer(EnumAdj_BufferType.STDERR)

    # -----------------------------------------------------------------------------------------------------------------
    async def _wait__finish_executing_cmd(
            self,
            timeout_start: float | None = None,
            timeout_finish: float | None = None
    ) -> bool:
        """Ожидание завершения вывода команды по таймаутам."""
        timeout_start = timeout_start or self.timeout_start
        timeout_finish = timeout_finish or self.timeout_finish

        start_wait = asyncio.get_event_loop().time()
        while asyncio.get_event_loop().time() - start_wait < timeout_start:
            # Если процесс завершился, сразу выходим
            if self._conn and self._conn.returncode is not None:
                return True
            if self._last_byte_time > start_wait:
                quiet_start = asyncio.get_event_loop().time()
                while asyncio.get_event_loop().time() - quiet_start < timeout_finish:
                    if self._conn and self._conn.returncode is not None:
                        return True
                    if self._last_byte_time > quiet_start:
                        quiet_start = asyncio.get_event_loop().time()
                    await asyncio.sleep(0.05)
                return True
            await asyncio.sleep(0.05)
        return False

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
        await term.send_command("echo finish!")
        await asyncio.sleep(10)

    await asyncio.sleep(0.5)


# =====================================================================================================================
if __name__ == "__main__":
    # asyncio.run(explore__ping())
    # asyncio.run(explore__cd())
    # asyncio.run(explore__cd_reconnect())
    asyncio.run(explore__smth())


# =====================================================================================================================
