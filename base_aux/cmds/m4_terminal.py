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
            shell="cmd" if os.name == "nt" else "bash",
    ):
        self.shell = shell
        self.sp = subprocess.Popen(
            [shell, ],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True,
            encoding="cp866" if os.name == "nt" else "utf8",
            # creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
        )

        # Очередь для чтения вывода
        self.output_queue = queue.Queue()

        # Запускаем поток для чтения вывода
        self.reader_thread = threading.Thread(
            target=self._output_reader,
            daemon=True
        )
        self.reader_thread.start()

        # Даем оболочке время на инициализацию
        time.sleep(0.3)
        # self._clear_buffer()

    def _output_reader(self):
        """Поток для непрерывного чтения вывода"""
        while self.sp.poll() is None:
            line = self.sp.stdout.readline()
            if line:
                line = line.strip()
                print(f"{line}")
                self.output_queue.put(line)

    def _clear_buffer(self):
        """Очистка буфера от начального вывода"""
        while not self.output_queue.empty():
            self.output_queue.get()

    def send_command(self, command):
        """Отправка команды и получение вывода"""
        print(f"--->{command}")
        # Отправляем команду
        try:
            self.sp.stdin.write(command + "\n")
            self.sp.stdin.flush()
        except:
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

    def close(self):
        """Корректное закрытие"""
        if self.sp:
            try:
                self.sp.stdin.write("exit\n")
                self.sp.stdin.flush()
            except:
                pass
            self.sp.terminate()
            self.sp.wait()

    def send_ctrl_c(self):
        """
        DONT USE IT!!!
        NOT ALWAYS working and actually only ones!

        Отправка Ctrl+C в терминал для прерывания текущей команды
        без закрытия сессии
        """
        self.sp.terminate()

        # import signal
        # import ctypes
        # ctypes.windll.kernel32.GenerateConsoleCtrlEvent(0, self.sp.pid)     # вообще не работает!!!

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
        #     self.sp.send_signal(1)
        #     time.sleep(0.5)
        #     self.sp.send_signal(0)
        #     time.sleep(0.5)
        #     self.sp.send_signal(1)
        #     time.sleep(0.5)
        #     self.sp.send_signal(0)
        #     time.sleep(0.5)
        # self.sp.send_signal(subprocess.signal.CTRL_C_EVENT)
        # self.sp.send_signal(0)  # работает НО закрывает вообще возможность работы дальнейшей с self.sp!!!
        # И ТО ПОСЛЕ ЗАВЕРШЕНИЯ САМОЙ КОМАНДЫ! ПРИНУДИТЕЛЬНО НЕ ЗАВЕРШАЕТСЯ!!!!

        # # self.send_command("Stop-Process -Name ping -Force -ErrorAction SilentlyContinue")   # НЕТ ТАКОЙ КОМАНДЫ

        # ВООБЩЕ НИ НА ЧТО НЕ ВЛИЯЕТ!!!
        # self.sp.stdin.write('^C')
        # self.sp.stdin.write('^C\n')
        # self.sp.stdin.write('Control-C\n')
        # self.sp.stdin.write('\x03')   # Ctrl+C через stdin (ASCII код 3)
        # self.sp.stdin.write('\n')
        # self.sp.stdin.write('\x03\n')

        # self.sp.stdin.flush()
        return


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

        # ObjectInfo(term.sp).print()
        print(f"{term.send_ctrl_c()=}")
        for index in range(3):
            term.send_command(f"echo final {index}")
            time.sleep(0.5)

        term.send_command("echo finish!")
        time.sleep(1)

    finally:
        term.close()


# =====================================================================================================================
