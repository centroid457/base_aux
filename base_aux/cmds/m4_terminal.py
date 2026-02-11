import subprocess
import threading
import queue
import time
import os

from base_aux.base_types.m2_info import ObjectInfo
from base_aux.cmds.m2_history import *


# =====================================================================================================================
class CmdSession:
    """
    GOAL
    ----
    access to terminal with continuous connection - keeping state!
    """
    def __init__(
            self,
            id: str | None = None,
    ):
        self.id: str | None = id
        self.history: CmdHistory = CmdHistory()

        self.connect()

    # -----------------------------------------------------------------------------------------------------------------
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    # -----------------------------------------------------------------------------------------------------------------
    def connect(self) -> bool:
        self.shell_cmd: str = "cmd" if os.name == "nt" else "bash"
        self._conn = subprocess.Popen(
            args=[self.shell_cmd, ],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
            encoding="cp866" if os.name == "nt" else "utf8",
            # creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
        )
        self.thread__read_stdout = threading.Thread(
            target=self._reading_stdout,
            daemon=True
        )
        self.thread__read_stderr = threading.Thread(
            target=self._reading_stderr,
            daemon=True
        )

        self.thread__read_stdout.start()
        self.thread__read_stderr.start()

        time.sleep(0.3)
        return True

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
        self.close()
        self.connect()

    def close(self) -> None:
        """
        GOAL
        ----
        close connection
        ready to exit
        """
        if self._conn:
            try:
                # think it very need! smth is not correct in output after restart without this block!!!
                self.send_command("exit\n")
            except:
                pass

            try:
                self._conn.terminate()
                self._conn.wait()
            except:
                pass

            # self.thread__read_stdout.join()

    def clear_history(self) -> None:
        """
        NOTE
        ----
        use only manually!
        """
        self.history.clear()

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
    def _reading_stdout(self):
        """Поток для непрерывного чтения вывода"""
        while self._conn.poll() is None:
            try:

                line = self._conn.stdout.readline()
                line = line and line.rstrip()
                if line:
                    # line = line.strip()
                    print(f"{line}")
                    self.history.append_stdout(line)

                self.history.set_retcode(self._conn.returncode)
            except Exception as exc:
                print(f"{exc!r}")
                # time.sleep(0.1)
                pass

    def _reading_stderr(self):
        """Поток для непрерывного чтения вывода"""
        while self._conn.poll() is None:
            try:
                line = self._conn.stderr.readline()
                line = line and line.rstrip()
                if line:
                    # line = line.strip()
                    print(f"{line}")
                    self.history.append_stderr(line)

                self.history.set_retcode(self._conn.returncode)
            except Exception as exc:
                print(f"{exc!r}")
                # time.sleep(0.1)
                pass

    # -----------------------------------------------------------------------------------------------------------------
    def send_command(self, cmd: str, timeout_start: float = 1, timeout_finish: float = 0.1) -> CmdResult:
        """Отправка команды и получение вывода"""
        print()
        print(f"--->{cmd}")

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

    def wait__finish_executing_cmd(self, timeout_start: float = 1, timeout_finish: float = 0.1) -> bool:
        """
        GOAL
        ----
        ensure finishing any buffer activity
        1. wait long timeout_start for start activity
        2. wait short timeout2 for close waiting any new line!
        """
        data_reseived: bool = False

        duration = self.history.last_result.duration

        timeout_active = timeout_start
        time_start = time.time()
        while time.time() - time_start < timeout_active:
            if duration != self.history.last_result.duration:
                data_reseived = True
                duration = self.history.last_result.duration
                time_start = time.time()
                timeout_active = timeout_finish
            else:
                time.sleep(timeout_finish / 3)   # at least we need to execute last check

        return data_reseived


# =====================================================================================================================
# Пример использования
if __name__ == "__main__":
    with CmdSession() as term:
        for cmd in [
            # "echo HELLO",
            # "echo 'Hello from persistent terminal'",
            # "dir",
            # "cd",
            # "cd ..",
            # "cd",
            "ping ya.ru -n 2",

            # "pwd",
            # "ls -la",
        ]:
            term.send_command(cmd, timeout_finish=1.1)

        # ObjectInfo(term._conn).print()
        # print(f"{term._send_ctrl_c()=}")
        # print(f"{term.reconnect()=}")
        for index in range(3):
            term.send_command(f"echo final {index}")
            time.sleep(0.5)

        term.send_command("echo finish!")

    time.sleep(2)


# =====================================================================================================================
