import asyncio

from base_aux.cmds.m2_history import *
from base_aux.cmds.m4_terminal0_base import *


# =====================================================================================================================
class CmdTerminal_OsAio(Base_CmdTerminal):
    """
    Асинхронная версия CmdTerminal_Os на asyncio.subprocess.
    """
    _conn: asyncio.subprocess.Process | None
    _bg_tasks: list[asyncio.Task]

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
            asyncio.create_task(self._reading_stdout()),
            asyncio.create_task(self._reading_stderr()),
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
        for task in self._bg_tasks:
            task.cancel()
        await asyncio.gather(*self._bg_tasks, return_exceptions=True)
        self._bg_tasks.clear()
        self._conn = None

        print(f"{self.__class__.__name__}({self.id=}).disconnected")

    # -----------------------------------------------------------------------------------------------------------------
    async def reconnect(self) -> None:
        await self.disconnect()
        await self.connect()

    # -----------------------------------------------------------------------------------------------------------------
    # async def _reading_stdout(self):
    #     """Асинхронное чтение stdout."""
    #     while not self._stop_reading and self._conn:
    #         try:
    #             line = await self._conn.stdout.readline()
    #             if not line:
    #                 break
    #             line = line.decode(self._encoding)
    #             line = line.rstrip()
    #             if line:
    #                 print(f"[STDOUT]{line}")
    #                 self.history.append_stdout(line)
    #             self.history.set_retcode(self._conn.returncode)
    #         except asyncio.CancelledError:
    #             break
    #         except Exception as exc:
    #             print(f"UNEXPECTED _reading_stdout: {exc!r}")
    #             break
    #
    # async def _reading_stderr(self):
    #     """Асинхронное чтение stderr."""
    #     while not self._stop_reading and self._conn:
    #         try:
    #             line = await self._conn.stderr.readline()
    #             if not line:
    #                 break
    #             line = line.decode(self._encoding)
    #             line = line.rstrip()
    #             if line:
    #                 print(f"[STDERR]{line}")
    #                 self.history.append_stderr(line)
    #             self.history.set_retcode(self._conn.returncode)
    #         except asyncio.CancelledError:
    #             break
    #         except Exception as exc:
    #             print(f"stderr reader error: {exc!r}")
    #             break

    # -----------------------------------------------------------------------------------------------------------------
    # -----------------------------------------------------------------------------------------------------------------
    # -----------------------------------------------------------------------------------------------------------------
    async def _read_stream(self, stream: asyncio.StreamReader, _buffer: EnumAdj_Buffer):
        """
        Чтение потока по одному байту с двумя таймаутами.
        - timeout_start – ожидание первого байта строки.
        - timeout_finish – ожидание последующих байтов.
        - Любой EOL (\r или \n) завершает текущую строку, последующие EOL игнорируются.
        - По таймауту строка также завершается.
        - Добавление в историю через append_method.
        """
        # init BUFFER -------------------
        if _buffer == EnumAdj_Buffer.STDOUT:
            append_method = self.history.add_data__stdout
        elif _buffer == EnumAdj_Buffer.STDERR:
            append_method = self.history.add_data__stderr
        else:
            raise Exc__WrongUsage(f'{_buffer=}')

        # BUFFER -------------------
        while not self._stop_reading and self._conn:
            bytes_accumulated = bytearray()
            timeout_active = self.timeout_start
            try:
                while True:
                    try:
                        new_byte = await asyncio.wait_for(stream.read(1), timeout=timeout_active)
                    except asyncio.TimeoutError:
                        # Таймаут – строка завершена (без EOL)
                        break

                    # Любой полученный байт фиксирует активность
                    self._last_byte_time = asyncio.get_event_loop().time()

                    # После первого байта переключаемся на finish-таймаут
                    timeout_active = self.timeout_finish

                    if new_byte == b'':  # EOF – канал закрыт
                        break

                    if new_byte in (b'\r', b'\n'):
                        # Встретили EOL – завершаем текущую строку (если были данные)
                        if bytes_accumulated:
                            new_line = bytes_accumulated.decode(self._encoding).rstrip()
                            if new_line:
                                append_method(new_line)
                        bytes_accumulated = bytearray()
                        continue
                    else:
                        bytes_accumulated.extend(new_byte)

                # Выход по таймауту – добавляем накопленное (если есть)
                if bytes_accumulated:
                    new_line = bytes_accumulated.decode(self._encoding).rstrip()
                    if new_line:
                        append_method(new_line)

            except asyncio.CancelledError:
                break
            except Exception as exc:
                print(f"UNEXPECTED _read_stream: {exc!r}")
                break

    async def _reading_stdout(self):
        await self._read_stream(self._conn.stdout, EnumAdj_Buffer.STDOUT)

    async def _reading_stderr(self):
        await self._read_stream(self._conn.stderr, EnumAdj_Buffer.STDERR)

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
        # Ждём первого байта (timeout_start)
        while asyncio.get_event_loop().time() - start_wait < timeout_start:
            if self._last_byte_time > start_wait:
                # Данные пошли – переходим в режим ожидания тишины (timeout_finish)
                quiet_start = asyncio.get_event_loop().time()
                while asyncio.get_event_loop().time() - quiet_start < timeout_finish:
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
        print(f"\n[STD_IN]--->{cmd}")
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
