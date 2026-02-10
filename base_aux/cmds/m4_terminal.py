import subprocess
import threading
import queue
import time
import os

from base_aux.base_types.m2_info import ObjectInfo


# =====================================================================================================================
class ContinuousTerminal:
    def __init__(
            self,
    ):
        # Очередь для чтения вывода
        self.output_queue = queue.Queue()
        self.connect()

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
        self.reader_thread = threading.Thread(
            target=self._reader_stdout,
            daemon=True
        )
        self.reader_thread.start()
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
                self._conn.stdin.write("exit\n")
                self._conn.stdin.flush()
            except:
                pass

            try:
                self._conn.terminate()
                self._conn.wait()
            except:
                pass

            # self.reader_thread.join()

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
    def _reader_stdout(self):
        """Поток для непрерывного чтения вывода"""
        while self._conn.poll() is None:
            line = self._conn.stdout.readline()
            if line:
                line = line.strip()
                print(f"{line}")
                self.output_queue.put(line)

    # -----------------------------------------------------------------------------------------------------------------
    def send_command(self, command):
        """Отправка команды и получение вывода"""
        print(f"--->{command}")
        try:
            self._conn.stdin.write(command + "\n")
            self._conn.stdin.flush()
        except Exception as exc:
            print(f"{exc!r}")
            return

        # Собираем вывод
        output = []
        time.sleep(0.1)  # Даем время на выполнение

        # Читаем вывод в течение 2 секунд
        start_time = time.time()
        while time.time() - start_time < 2:
            try:
                line = self.output_queue.get(timeout=0.1)
                output.append(line)
            except queue.Empty:
                if output:  # Если уже что-то получили, выходим
                    break

        result = "\n".join(output)
        # print(f"[{result}]")
        return result


# =====================================================================================================================
# Пример использования
if __name__ == "__main__":
    term = ContinuousTerminal()

    try:
        for cmd in [
            # "echo HELLO",
            # "echo 'Hello from persistent terminal'",
            # "dir",
            # "cd",
            # "cd ..",
            # "cd",
            "ping ya.ru -n 4",

            # "pwd",
            # "ls -la",
        ]:
            term.send_command(cmd)

        # ObjectInfo(term._conn).print()
        # print(f"{term._send_ctrl_c()=}")
        print(f"{term.reconnect()=}")
        for index in range(3):
            term.send_command(f"echo final {index}")
            time.sleep(0.5)

        term.send_command("echo finish!")
        time.sleep(1)

    finally:
        term.close()


# =====================================================================================================================
