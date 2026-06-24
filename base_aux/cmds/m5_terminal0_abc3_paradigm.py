from typing import *
import asyncio
import time
from abc import abstractmethod

from base_aux.base_enums.m2_enum1_adj import EnumAdj_StdioeType, EnumAdj_FinishedStatus
from base_aux.base_values.m3_exceptions import *

from base_aux.cmds.m1_result import CmdResult
from base_aux.cmds.m5_terminal0_abc2_conn import AbcConn_CmdTerminal
from base_aux.tasks.m1_tasks_bg import Nest_TasksBg_AbcSync, Nest_TasksBg_AbcAio


# =====================================================================================================================
class AbcParadigm_CmdTerminal(AbcConn_CmdTerminal):
    def __init__(
            self,
            *args,
            **kwargs,
    ):
        super().__init__(*args, **kwargs)

    # -----------------------------------------------------------------------------------------------------------------
    @abstractmethod
    def connect(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    def disconnect(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    def reconnect(self) -> None:
        raise NotImplementedError()

    # -----------------------------------------------------------------------------------------------------------------
    @abstractmethod
    def send_cmd(
            self,
            cmd: str,
            timeout_write: float | None = None,
            timeout_read_start: float | None = None,
            timeout_read_finish: float | None = None,
            eol: str | None = None,
    ) -> CmdResult:
        raise NotImplementedError()

    @abstractmethod
    def send_cmds__all_success(
            self,
            cmds: list[str],
    ) -> bool:
        """
        GOAL
        ----
        detect exact cmd which will not get fail

        send some cmds to check that all results are ok
        when you dont mind to check exact response line but want to be sure
        - no bad retcode
        - no data in stderr
        - no timed out
        """
        raise NotImplementedError()

    # @abstractmethod
    # def send_cmds__till_first_fail(
    #         self,
    #         cmds: list[str],
    # ) -> bool:
    #     """
    #     GOAL
    #     ----
    #     detect exact cmd which will get fail
    #     """
    #     raise NotImplementedError()
    #
    # @abstractmethod
    # def send_cmds__till_first_success(
    #         self,
    #         cmds: list[str],
    # ) -> bool:
    #     """
    #     GOAL
    #     ----
    #     detect exact cmd which will not get fail
    #     """
    #     raise NotImplementedError()

    # -----------------------------------------------------------------------------------------------------------------
    @abstractmethod
    def _wait__finish_executing_cmd(
            self,
            timeout_read_start: float | None = None,
            timeout_read_finish: float | None = None,
    ) -> bool:
        raise NotImplementedError()


# =====================================================================================================================
class BaseSync_CmdTerminal(AbcParadigm_CmdTerminal, Nest_TasksBg_AbcSync):
    """
    DEPRECATE!!! dont use!! use only AIO!!!
    """
    # -----------------------------------------------------------------------------------------------------------------
    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    # -----------------------------------------------------------------------------------------------------------------
    def connect(self) -> bool:
        if self._event_connected.is_set():
            return True

        print(f"{self.__class__.__name__}({self.idn=}).connect")
        try:
            self._create_conn()
        except Exception as exc:
            msg = f"{self.__class__.__name__}({self.idn=}){exc!r}"
            print(msg)
            self.history.add_data__stderr(msg)  # fixme: USE SYSTEM level!
            return False

        self._event_connected.set()     # ВКЛЮЧИТЬ ДО ЗАПУСКА ЗАДАЧ
        self._tasks_bg__create_start()

        time.sleep(0.3)
        return True

    # -----------------------------------------------------------------------------------------------------------------
    def disconnect(self) -> None:
        """
        GOAL
        ----
        close connection
        ready to exit
        """
        self._event_connected.clear()
        self._tasks_bg__stop_delete()
        self._del_conn()
        print(f"{self.__class__.__name__}({self.idn=}).disconnected")

    def reconnect(self) -> None:
        """
        GOAL
        ----
        apply closing and opening again
        without clear history (if need do it manually!)

        SPECIALLY CREATED FOR
        ---------------------
        for case when we send continious infinitive cmd and cant stop it
        so the only way is stop process/connection and open it again!
        this is the only way to do it cause sending Ctrl+С is not working correctly!
        """
        self.disconnect()
        self.connect()

    # -----------------------------------------------------------------------------------------------------------------
    def _bg_reading_buffer(self, buffer_type: EnumAdj_StdioeType) -> Never | None:
        """
        Чтение потока по одному байту с двумя таймаутами.
        - timeout_read_start – ожидание первого байта строки.
        - timeout_read_finish – ожидание последующих байтов.
        - Любой EOL (\r или \n) завершает текущую строку, последующие EOL игнорируются.
        - По таймауту строка также завершается.
        - Добавление в историю через append_method.

        ОСОБЕННОСТИ СИНХРОНКИ
        почему просто не сделать поток на чтение 1байта и ждать его с темже таймаутом???
        1. Создание потока на каждый байт приведёт к огромным накладным расходам (потоки тяжелее корутин, их создание и уничтожение занимает много ресурсов). Для реального вывода процесса это катастрофически медленно.
        2. Невозможность безопасно прервать поток по истечении таймаута. В Python нет механизма принудительной остановки потока, который выполняет блокирующий системный вызов. Если поток застрял в read(), его нельзя убить извне без риска повредить состояние интерпретатора или оставить ресурсы открытыми. Придётся использовать сложные трюки (например, закрыть pipe из другого потока), что добавит гонок и неопределённости.
        3. Исключения из потока нужно передавать в основной код через очередь или другие механизмы синхронизации – это усложняет логику.
        ВЫВОД=Правильный подход – использовать неблокирующий режим файлового дескриптора и цикл проверки времени, как было предложено ранее. Это даёт точный контроль над таймаутами, не создаёт лишних потоков и полностью повторяет логику асинхронного кода (по сути, мы реализуем тот же самый цикл событий вручную).
        """
        buffer: IO | None = None

        if self._conn is None:
            return

        # init BUFFER -------------------
        if buffer_type == EnumAdj_StdioeType.STDOUT:
            buffer = self._conn.stdout
            append_method = self.history.add_data__stdout
        elif buffer_type == EnumAdj_StdioeType.STDERR:
            buffer = self._conn.stderr
            append_method = self.history.add_data__stderr
        else:
            raise Exc__WrongUsage(f'{buffer_type=}')

        if buffer is None:
            return

        # BUFFER -------------------
        while self._event_connected.is_set():
            bytes_accumulated = bytearray()
            timeout_active = self.timeout_def.READ_START
            try:
                while True:
                    try:
                        new_byte = self._read_byte_with_timeout(buffer=buffer, timeout=timeout_active)
                    except Exc__IoTimeout:
                        break
                    except Exc__IoConnection:
                        # Канал закрыт – выходим из цикла чтения
                        return

                    self._last_byte_time = time.time()
                    timeout_active = self.timeout_def.READ_FINISH

                    if new_byte == b'':  # EOF
                        return

                    if new_byte in (b'\r', b'\n'):
                        if bytes_accumulated:
                            new_line: str = bytes_accumulated.decode(self._encoding).rstrip()
                            if new_line:
                                append_method(new_line)
                                self.history.set_retcode(self._conn.returncode)

                        bytes_accumulated = bytearray()
                        continue
                    else:
                        bytes_accumulated.extend(new_byte)

                if bytes_accumulated:
                    new_line: str = bytes_accumulated.decode(self._encoding).rstrip()
                    if new_line:
                        append_method(new_line)
                        self.history.set_retcode(self._conn.returncode)

            except BaseException as exc:
                print(f"UNEXPECTED _read_stream: {exc!r}")
                break

    def _bg_reading_buffer__stdout(self) -> Never | None:
        self._bg_reading_buffer(EnumAdj_StdioeType.STDOUT)

    def _bg_reading_buffer__stderr(self) -> Never | None:
        self._bg_reading_buffer(EnumAdj_StdioeType.STDERR)

    # -----------------------------------------------------------------------------------------------------------------
    def _wait__finish_executing_cmd(
            self,
            timeout_read_start: float | None = None,
            timeout_read_finish: float | None = None,
    ) -> bool:
        """
        GOAL
        ----
        ensure finishing any buffer activity
        1. wait long timeout_read_start for start activity
        2. wait short timeout2 for close waiting any new line!
        """
        timeout_read_start = self.timeout_def.get_active__read_start(timeout_read_start)
        timeout_read_finish = self.timeout_def.get_active__read_finish(timeout_read_finish)

        data_received: bool = False
        last_duration: float = self.history.last_result.duration

        timeout_active = timeout_read_start
        time_start = time.time()
        while time.time() - time_start < timeout_active:
            if last_duration != self.history.last_result.duration:
                data_received = True
                last_duration = self.history.last_result.duration
                time_start = time.time()
                timeout_active = timeout_read_finish
            else:
                time.sleep(timeout_read_finish / 3)   # at least we need to execute last check

        return data_received

    # -----------------------------------------------------------------------------------------------------------------
    def send_cmd(
            self,
            cmd: str,
            timeout_write: float | None = None,
            timeout_read_start: float | None = None,
            timeout_read_finish: float | None = None,
            eol: str | None = None,
    ) -> CmdResult:
        if self._conn is None:
            raise Exc__WrongUsage_YouForgotSmth(f"CONNECT()")

        self.history.add_data__stdin(cmd)
        try:
            self._write_line(cmd=cmd, timeout=timeout_write, eol=eol)

            if self._wait__finish_executing_cmd(timeout_read_start, timeout_read_finish):
                _finished_status = EnumAdj_FinishedStatus.CORRECT
            else:
                _finished_status = EnumAdj_FinishedStatus.TIMED_OUT
        except Exception as exc:
            print(f"{exc!r}")
            self.history.add_data__stderr(f"{exc!r}")
            _finished_status = EnumAdj_FinishedStatus.EXCEPTION

        self.history.set_finished(status=_finished_status)
        return self.history.last_result

    def send_cmds__all_success(
            self,
            cmds: list[str],
    ) -> bool:
        for cmd in cmds:
            result = self.send_cmd(cmd)
            if result.check__fail():
                return False

        return True
        # TODO: add timeout!
        # TODO: add timeout!
        # TODO: add timeout!
        # TODO: add timeout!
        # TODO: add timeout!
        # TODO: add timeout!


# =====================================================================================================================
class BaseAio_CmdTerminal(AbcParadigm_CmdTerminal, Nest_TasksBg_AbcAio):
    _lock_stdin: asyncio.Lock

    def __init__(
            self,
            *args,
            **kwargs,
    ):
        self._lock_stdin = asyncio.Lock()

        super().__init__(*args, **kwargs)

    # -----------------------------------------------------------------------------------------------------------------
    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.disconnect()

    # -----------------------------------------------------------------------------------------------------------------
    async def connect(self) -> bool:
        if self._event_connected.is_set():
            return True

        async with self._lock_stdin:
            if self._event_connected.is_set():
                return True

            print(f"{self.__class__.__name__}({self.idn=}).connect")

            try:
                await self._create_conn()
            except Exception as exc:
                msg = f"{self.__class__.__name__}({self.idn=}){exc!r}"
                print(msg)
                await self.history.add_data__stderr(msg)
                return False

            if not self.history._history:
                await self.history.add_data__stdin("")

            # self.history.add_data__debug("🔄connected")

            self._event_connected.set()  # ВКЛЮЧИТЬ ДО ЗАПУСКА ЗАДАЧ
            self._tasks_bg__create_start()
            self._last_byte_time = asyncio.get_event_loop().time()

            await asyncio.sleep(0.3)
            return True

    # -----------------------------------------------------------------------------------------------------------------
    async def disconnect(self) -> None:
        self._event_connected.clear()

        async with self._lock_stdin:
            await self._tasks_bg__stop_delete()
            await self._del_conn()
            # self.history.add_data__debug("disconnected")
            print(f"{self.__class__.__name__}({self.idn=}).disconnected")

    async def reconnect(self) -> None:
        await self.disconnect()
        await self.connect()

    # -----------------------------------------------------------------------------------------------------------------
    def bytes_decode(self, source: bytes) -> str | None:
        try:
            result = source.decode(self._encoding).rstrip()
        except Exception as exc:
            result = None
            self.history.add_data__stderr(f"[bytes_decode]{source=}/{exc!r}")
        return result

    async def _process_received_line(
            self,
            raw: bytearray,
            append_method: Callable[[str], Awaitable[None]],
    ) -> None:
        """Декодирует накопленные байты, добавляет строку в историю и фиксирует retcode."""
        line: str = self.bytes_decode(raw)  # bytes_decode делает decode + rstrip
        if line:
            await append_method(line)
            if self._conn is not None:
                self.history.set_retcode(self._conn.returncode)

    async def _bg_reading_buffer(self, buffer_type: EnumAdj_StdioeType) -> Never | None:
        """
        Чтение потока по одному байту с двумя таймаутами.
        - timeout_read_start – ожидание первого байта строки.
        - timeout_read_finish – ожидание последующих байтов.
        - Любой EOL (\r или \n) завершает текущую строку, последующие EOL игнорируются.
        - По таймауту строка также завершается.
        - Добавление в историю через append_method.
        """
        if self._conn is None:
            return

        # выбор буфера и метода добавления -------------------
        if buffer_type == EnumAdj_StdioeType.STDOUT:
            buffer = self._conn.stdout
            append_method = self.history.add_data__stdout
        elif buffer_type == EnumAdj_StdioeType.STDERR:
            buffer = self._conn.stderr
            append_method = self.history.add_data__stderr
        else:
            raise Exc__WrongUsage(f'{buffer_type=}')

        if buffer is None:
            return

        # главный цикл жизни соединения -------------------
        while self._event_connected.is_set():
            bytes_accumulated = bytearray()
            first_byte = True

            try:
                while True:
                    # выбираем таймаут в зависимости от стадии
                    timeout = (
                        self.timeout_def.READ_START
                        if first_byte
                        else self.timeout_def.READ_FINISH
                    )
                    try:
                        new_byte = await self._read_byte_with_timeout(
                            buffer=buffer, timeout=timeout
                        )
                    except Exc__IoTimeout:
                        if bytes_accumulated:
                            await self._process_received_line(bytes_accumulated, append_method)
                        break
                    except Exc__IoConnection:
                        return  # канал закрыт, полностью выходим

                    # байт успешно получен -----------------------
                    first_byte = False
                    self._last_byte_time = asyncio.get_event_loop().time()

                    if new_byte == b'':
                        return  # EOF

                    if new_byte in (b'\r', b'\n'):
                        if bytes_accumulated:
                            await self._process_received_line(bytes_accumulated, append_method)
                            bytes_accumulated.clear()
                    else:
                        bytes_accumulated.extend(new_byte)

            except asyncio.CancelledError:
                break
            except BaseException as exc:
                print(f"UNEXPECTED _read_stream: {exc!r}")
                break

    async def _bg_reading_buffer__stdout(self):
        await self._bg_reading_buffer(EnumAdj_StdioeType.STDOUT)

    async def _bg_reading_buffer__stderr(self):
        await self._bg_reading_buffer(EnumAdj_StdioeType.STDERR)

    # -----------------------------------------------------------------------------------------------------------------
    async def _wait__finish_executing_cmd(
            self,
            timeout_read_start: float | None = None,
            timeout_read_finish: float | None = None
    ) -> bool:
        """
        GOAL
        Ожидание завершения отработки отправленной команды по таймаутам.
        """
        timeout_read_start = self.timeout_def.get_active__read_start(timeout_read_start)
        timeout_read_finish = self.timeout_def.get_active__read_finish(timeout_read_finish)

        start_wait = asyncio.get_event_loop().time()
        while asyncio.get_event_loop().time() - start_wait < timeout_read_start:
            if not self._event_connected.is_set():
                return False
            # Если процесс завершился, сразу выходим
            if self._conn is not None and self._conn.returncode is not None:
                return True
            if self._last_byte_time > start_wait:
                quiet_start = asyncio.get_event_loop().time()
                while asyncio.get_event_loop().time() - quiet_start < timeout_read_finish:
                    if not self._event_connected.is_set():
                        return False
                    if self._conn is not None and self._conn.returncode is not None:
                        return True
                    if self._last_byte_time > quiet_start:      # DONT USE [!=] !!! its make freezes
                        quiet_start = asyncio.get_event_loop().time()
                    await asyncio.sleep(0.05)
                return True
            await asyncio.sleep(0.05)
        return False

    # -----------------------------------------------------------------------------------------------------------------
    async def send_cmd(
            self,
            cmd: str,
            timeout_write: float | None = None,
            timeout_read_start: float | None = None,
            timeout_read_finish: float | None = None,
            eol: str | None = None,
    ) -> CmdResult | NoReturn:
        if not self._event_connected.is_set():
            await self.connect()

        async with self._lock_stdin:
            if not self._event_connected.is_set():
                raise Exc__NotReady(f"not connected")

            await self.history.add_data__stdin(cmd)
            try:
                await self._write_line(cmd=cmd, timeout=timeout_write, eol=eol)

                if await self._wait__finish_executing_cmd(timeout_read_start, timeout_read_finish):
                    finished_status = EnumAdj_FinishedStatus.CORRECT
                else:
                    finished_status = EnumAdj_FinishedStatus.TIMED_OUT
            except Exception as exc:
                print(f"{exc!r}")
                await self.history.add_data__stderr(f"{exc!r}")
                finished_status = EnumAdj_FinishedStatus.EXCEPTION

            self.history.set_finished(status=finished_status)
            return self.history.last_result

    async def send_cmds__all_success(
            self,
            cmds: list[str],
    ) -> bool:
        for cmd in cmds:
            result = await self.send_cmd(cmd)
            if result.check__fail():
                return False

        return True
        # TODO: add timeout!
        # TODO: add timeout!
        # TODO: add timeout!
        # TODO: add timeout!
        # TODO: add timeout!
        # TODO: add timeout!


# =====================================================================================================================
