from typing import *
import subprocess
import threading
import os
import time
import errno

from base_aux.cmds.m2_history import *
from base_aux.cmds.m4_terminal0_base import *


# =====================================================================================================================
class CmdTerminal_OsSync(Base_CmdTerminalSync):
    """
    GOAL
    ----
    access to terminal with continuous connection - keeping state!
    """
    _conn: subprocess.Popen | None
    EOL_SEND: str = "\n"

    # -----------------------------------------------------------------------------------------------------------------
    def _create_conn(self) -> None | NoReturn:
        self._conn = subprocess.Popen(
            args=[self._shell_cmd, ],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
            encoding=self._encoding,
            # creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
            cwd=self.cwd,
            # timeout=1,    № is not accesible here in Popen!!!!
        )

    def _create_tasks(self) -> None:
        # setup settings for buffers
        # Неблокирующий режим должен быть установлен один раз до входа в цикл. Например, в начале метода _reading_stream:
        for buffer in [self._conn.stdout, self._conn.stderr]:
            pass
            fd = buffer.fileno()
            os.set_blocking(fd, False)

        self._bg_tasks = [
            threading.Thread(target=self._bg_reading_buffer__stdout, daemon=True),
            threading.Thread(target=self._bg_reading_buffer__stderr, daemon=True),
        ]

        for reader_task in self._bg_tasks:
            reader_task.start()

    # -----------------------------------------------------------------------------------------------------------------
    def _del_conn(self) -> None:
        if self._conn is not None:
            # try:
            #     # think it very need! smth is not correct in output after restart without this block!!!
            #     self.send_command("exit")
            # except:
            #     pass

            try:
                self._conn.terminate()
                self._conn.wait(2)
            except:
                pass
            self._conn = None

    def _del_tasks(self) -> None:
        self._stop_reading = True
        for reader_task in self._bg_tasks:
            reader_task.join(timeout=1)

        self._bg_tasks.clear()

    # -----------------------------------------------------------------------------------------------------------------
    def _read_byte_with_timeout(
            self,
            timeout: float = 0.05,
            buffer_type: EnumAdj_BufferType = EnumAdj_BufferType.STDOUT,
    ) -> bytes | NoReturn | Exc__Io | Exc__UnDefined | Exc__WrongUsage:
        buffer: IO | None = None

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
        fd = buffer.fileno()
        start = time.monotonic()
        while True:
            try:
                new_byte = os.read(fd, 1)
                # Если прочитано 0 байт – EOF
                return new_byte
            except BlockingIOError as exc:
                # Нет данных в данный момент
                if exc.errno not in (errno.EAGAIN, errno.EWOULDBLOCK):
                    pass
                    # raise   # FIXME: ИЛИ CONTINUE/BREAK????
                    # continue
                    break
                # Проверяем, истёк ли таймаут
                if time.monotonic() - start >= timeout:
                    raise Exc__IoTimeout(f"{timeout=}/{exc!r}")  # сигнализирует об окончании ожидания строки
                # Небольшая пауза, чтобы не грузить процессор
                time.sleep(0.05)
            except OSError as exc:
                # Ошибки, связанные с закрытием канала или разрывом соединения
                pass
                raise Exc__IoConnection(f"{exc!r}")
                # if exc.errno in (errno.EPIPE, errno.ECONNRESET, errno.EBADF):
                #     raise BrokenPipeError from exc
                # else:
                #     raise
            except BaseException as exc:
                raise Exc__UnDefined(f"{exc!r}")

    # -----------------------------------------------------------------------------------------------------------------
    def send_command(
            self,
            cmd: str,
            timeout_start: float | None = None,
            timeout_finish: float | None = None,
            eol: str | None = None,
    ) -> CmdResult:
        EOL: str = eol if eol is not None else self.EOL_SEND

        self.history.add_data__stdin(cmd)
        try:
            self._conn.stdin.write(f"{cmd}{EOL}")
            self._conn.stdin.flush()
            if self._wait__finish_executing_cmd(timeout_start, timeout_finish):
                _finished_status = EnumAdj_FinishedStatus.CORRECT
            else:
                _finished_status = EnumAdj_FinishedStatus.TIMED_OUT
        except Exception as exc:
            print(f"{exc!r}")
            self.history.add_data__stderr(f"{exc!r}")
            _finished_status = EnumAdj_FinishedStatus.EXCEPTION

        self.history.set_finished(status=_finished_status)
        return self.history.last_result

    # -----------------------------------------------------------------------------------------------------------------
    def _send_ctrl_c(self):
        """
        DONT USE IT!!!
        NOT ALWAYS working and actually only ones!

        GOAL
        ----
        Отправка Ctrl+C в терминал для прерывания текущей команды
        без закрытия сессии
        """
        self._conn.terminate()

        # import signal
        # import ctypes
        # ctypes.windll.kernel32.GenerateConsoleCtrlEvent(0, self._conn.pid)     # вообще не работает!!!

        # SIGNALS -----------------------------
        sigs = dict(
            # SUPPORTED --------------------
            CTRL_C_EVENT=0,
            CTRL_BREAK_EVENT=1,   #
            SIGTERM=15,     # STOP!
            SIG_DFL=0,
            SIG_IGN=1,

            # ValueError: Unsupported signal -------------------------------
            # NSIG=23,  # ValueError: Unsupported signal: 23
            # SIGABRT=22,     ValueError: Unsupported signal: 22
            # SIGBREAK=21,      ValueError: Unsupported signal: 21
            # SIGFPE=8,
            # SIGILL=4,
            # SIGINT=2,
            # SIGSEGV=11,
        )
        # for sname, svalue in sigs.items():
        #     print(f"{sname=}")
        #     self._conn.send_signal(1)
        #     time.sleep(0.5)
        #     self._conn.send_signal(0)
        #     time.sleep(0.5)
        #     self._conn.send_signal(1)
        #     time.sleep(0.5)
        #     self._conn.send_signal(0)
        #     time.sleep(0.5)
        # self._conn.send_signal(subprocess.signal.CTRL_C_EVENT)
        # self._conn.send_signal(0)  # работает НО закрывает вообще возможность работы дальнейшей с self._conn!!!
        # И ТО ПОСЛЕ ЗАВЕРШЕНИЯ САМОЙ КОМАНДЫ! ПРИНУДИТЕЛЬНО НЕ ЗАВЕРШАЕТСЯ!!!!

        # # self.send_command("Stop-Process -Name ping -Force -ErrorAction SilentlyContinue")   # НЕТ ТАКОЙ КОМАНДЫ

        # ВООБЩЕ НИ НА ЧТО НЕ ВЛИЯЕТ!!!
        # self._conn.stdin.write('^C')
        # self._conn.stdin.write('^C\n')
        # self._conn.stdin.write('Control-C\n')
        # self._conn.stdin.write('\x03')   # Ctrl+C через stdin (ASCII код 3)
        # self._conn.stdin.write('\n')
        # self._conn.stdin.write('\x03\n')

        # self._conn.stdin.flush()
        return


# =====================================================================================================================
def _explore__ping():
    with CmdTerminal_OsSync() as term:
        term.send_command("ping ya.ru -n 2", timeout_finish=1.1)

        # ObjectInfo(term._conn).print()
        # print(f"{term._send_ctrl_c()=}")
        # print(f"{term.reconnect()=}")
        for index in range(3):
            term.send_command(f"echo final {index}")

        term.send_command("echo finish!")

    time.sleep(0.5)


def _explore__cd():
    with CmdTerminal_OsSync() as term:
        if not term.connect():
            return

        for cmd in [
            # "cd",
            # "dir",

            "cd ..",
            "cd",
            "dir",

            "cd ..",
            "cd",
            "dir",

            # "pwd",
            # "ls -la",
        ]:
            term.send_command(cmd)

    time.sleep(0.5)


def _explore__cd_reconnect():
    with CmdTerminal_OsSync() as term:
        if not term.connect():
            return

        for _ in range(3):
            term.send_command("cd ../..")
            term.send_command("cd")
            term.reconnect()

    time.sleep(0.5)


def explore__smth():
    with CmdTerminal_OsSync() as term:
        term.send_command("echo start")
        term.send_command("echo finish!")
        time.sleep(2)

        term.history.print_io()

    time.sleep(0.5)


# =====================================================================================================================
if __name__ == "__main__":
    # _explore__ping()
    # _explore__cd()
    # _explore__cd_reconnect()
    explore__smth()


# =====================================================================================================================
