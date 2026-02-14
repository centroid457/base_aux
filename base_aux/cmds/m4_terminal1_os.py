import subprocess
import threading
import time
import os

from base_aux.cmds.m2_history import *
from base_aux.cmds.m4_terminal0_base import *


# =====================================================================================================================
class CmdTerminal_Os(Base_CmdTerminal):
    """
    GOAL
    ----
    access to terminal with continuous connection - keeping state!
    """
    _conn: subprocess.Popen | None
    _reader_tasks: list[threading.Thread]

    def __init__(
            self,
            *,
            cwd: str | None = None,

            **kwargs,
    ):
        super().__init__(**kwargs)

        self.cwd: str | None = cwd
        self._shell_cmd: str = "cmd" if os.name == "nt" else "bash"

    # -----------------------------------------------------------------------------------------------------------------
    def connect(self) -> bool:
        if self._conn is not None:
            return True

        print(f"{self.__class__.__name__}({self.id=}).connect")
        try:
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
        except Exception as exc:
            msg = f"{self.__class__.__name__}({self.id=}){exc!r}"
            print(msg)
            self.history.append_stderr(msg)
            return False

        self._stop_reading = False

        self._reader_tasks = [
            threading.Thread(target=self._reading_stdout, daemon=True),
            threading.Thread(target=self._reading_stderr, daemon=True),
        ]

        for reader_task in self._reader_tasks:
            reader_task.start()

        time.sleep(0.3)
        return True

    def disconnect(self) -> None:
        """
        GOAL
        ----
        close connection
        ready to exit
        """
        if self._conn is not None:
            try:
                # think it very need! smth is not correct in output after restart without this block!!!
                self.send_command("exit")
            except:
                pass

            try:
                self._conn.terminate()
                self._conn.wait(2)
            except:
                pass

        self._stop_reading = True

        for reader_task in self._reader_tasks:
            reader_task.join(timeout=1)

        self._reader_tasks.clear()
        self._conn = None

        print(f"{self.__class__.__name__}({self.id=}).disconnected")

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
            CTRL_C_EVENT = 0,
            # CTRL_BREAK_EVENT = 1,   #
            # SIGTERM=15,     # STOP!
            # SIG_DFL = 0,
            # SIG_IGN = 1,

            # ValueError: Unsupported signal -------------------------------
            # NSIG = 23,  # ValueError: Unsupported signal: 23
            # SIGABRT = 22,     ValueError: Unsupported signal: 22
            # SIGBREAK = 21,      ValueError: Unsupported signal: 21
            # SIGFPE = 8,
            # SIGILL = 4,
            # SIGINT = 2,
            # SIGSEGV = 11,
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

    # -----------------------------------------------------------------------------------------------------------------
    def _reading_stdout2_bytes(self):
        pass
        # while not self._stop_reading and self._conn is not None and self._conn.poll() is None:
        #     try:
        #         result_line: AnyStr = ""
        #         for
        #             line = self._conn.stdout.read(1)
        #
        #     except:
        #         pass
        #
        #     try:
        #         line = self._conn.stdout.readline()
        #         line = line and line.rstrip()
        #         if line:
        #             print(f"[STDOUT]{line}")
        #             self.history.append_stdout(line)
        #
        #         self.history.set_retcode(self._conn.returncode)
        #     except Exception as exc:
        #         print(f"{exc!r}")
        #         # time.sleep(0.1)
        #         pass

    # -----------------------------------------------------------------------------------------------------------------
    def _reading_stdout(self):
        """Поток для непрерывного чтения вывода"""
        while not self._stop_reading and self._conn is not None and self._conn.poll() is None:
            try:
                line = self._conn.stdout.readline()
                line = line and line.rstrip()
                if line:
                    print(f"[STDOUT]{line}")
                    self.history.append_stdout(line)

                self.history.set_retcode(self._conn.returncode)
            except Exception as exc:
                print(f"{exc!r}")
                # time.sleep(0.1)
                pass

    def _reading_stderr(self):
        """Поток для непрерывного чтения вывода"""
        while not self._stop_reading and self._conn is not None and  self._conn.poll() is None:
            try:
                line = self._conn.stderr.readline()
                line = line and line.rstrip()
                if line:
                    print(f"[STDERR]{line}")
                    self.history.append_stderr(line)

                self.history.set_retcode(self._conn.returncode)
            except Exception as exc:
                print(f"{exc!r}")
                # time.sleep(0.1)
                pass

    # -----------------------------------------------------------------------------------------------------------------
    def send_command(self, cmd: str, timeout_start: float | None = None, timeout_finish: float | None = None) -> CmdResult:
        print(f"\n[STD_IN]--->{cmd}")

        self.history.add_input(cmd)
        try:
            self._conn.stdin.write(f"{cmd}\n")
            self._conn.stdin.flush()
            if self.wait__finish_executing_cmd(timeout_start, timeout_finish):
                _finished_status = EnumAdj_FinishedStatus.CORRECT
            else:
                _finished_status = EnumAdj_FinishedStatus.TIMED_OUT
        except Exception as exc:
            print(f"{exc!r}")
            self.history.append_stderr(f"{exc!r}")
            _finished_status = EnumAdj_FinishedStatus.EXCEPTION

        self.history.set_finished(status=_finished_status)
        return self.history.last_result


# =====================================================================================================================
def _explore__ping():
    with CmdTerminal_Os() as term:
        if not term.connect():
            return

        term.send_command("ping ya.ru -n 2", timeout_finish=1.1)

        # ObjectInfo(term._conn).print()
        # print(f"{term._send_ctrl_c()=}")
        # print(f"{term.reconnect()=}")
        for index in range(3):
            term.send_command(f"echo final {index}")

        term.send_command("echo finish!")

    time.sleep(0.5)


def _explore__cd():
    with CmdTerminal_Os() as term:
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
    with CmdTerminal_Os() as term:
        if not term.connect():
            return

        for _ in range(3):
            term.send_command("cd ../..")
            term.send_command("cd")
            term.reconnect()

    time.sleep(0.5)


# =====================================================================================================================
# Пример использования
if __name__ == "__main__":
    _explore__ping()
    # _explore__cd()
    # _explore__cd_reconnect()


# =====================================================================================================================
