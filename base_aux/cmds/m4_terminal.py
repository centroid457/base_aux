import subprocess
import threading
import queue
import time
import os


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
        self.sp.stdin.write(command + "\n")
        self.sp.stdin.flush()

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
            self.sp.stdin.write("exit\n")
            self.sp.stdin.flush()
            self.sp.terminate()
            self.sp.wait()

    def send_ctrl_c(self):
        """
        Отправка Ctrl+C в терминал для прерывания текущей команды
        без закрытия сессии
        """
        # if not self.sp:     # not self.is_running or
        #     raise RuntimeError("Сессия терминала не активна")

        self.sp.stdin.write('\x03\n')
        self.sp.stdin.flush()

        # # self.send_command("Stop-Process -Name ping -Force -ErrorAction SilentlyContinue")
        #
        # # self.sp.send_signal(0)
        #
        # # Способ 1: Прямая отправка Ctrl+C через stdin (ASCII код 3)
        # self.sp.stdin.write('\x03')
        # self.sp.stdin.flush()
        # time.sleep(0.2)
        #
        # # Способ 2: Отправка Enter для сброса
        # self.sp.stdin.write('\n')
        # self.sp.stdin.flush()
        # time.sleep(0.2)



        return

        if os.name == "nt":  # Windows
            # Для Windows отправляем Ctrl+C через send_signal
            print(1)
            self.sp.send_signal(0)
            print(2)
            time.sleep(0.3)  # Даем время на обработку
            print(3)
            return

            try:
                # CTRL_C_EVENT = 0
                # self.sp.send_signal(subprocess.signal.CTRL_C_EVENT)
                self.sp.send_signal(0)
                time.sleep(0.3)  # Даем время на обработку
                return True
            except (AttributeError, OSError):
                # Альтернативный способ для Windows
                try:
                    import ctypes
                    ctypes.windll.kernel32.GenerateConsoleCtrlEvent(0, self.sp.pid)
                    time.sleep(0.3)
                    return True
                except:
                    return False


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
            "ping ya.ru",

            # "pwd",
            # "ls -la",
        ]:
            term.send_command(cmd)

        # Демонстрация сохранения состояния
        # term.send_command("touch test_file.txt")
        # print(term.send_command("ls test_file.txt"))

        # time.sleep(1)
        print(f"{term.send_ctrl_c()=}")
        term.send_command("echo hello")
        for index in range(5):
            term.send_command(f"echo {index}")
            time.sleep(0.5)

    finally:
        term.close()


# =====================================================================================================================
