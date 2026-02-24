import threading
import time

import serial
import serial.tools.list_ports

from base_aux.cmds.m2_history import *
from base_aux.cmds.m4_terminal0_base import *


# =====================================================================================================================
class CmdTerminal_SerialSync(BaseSync_CmdTerminal):
    # FIXME: need fool ref!!!
    # FIXME: need fool ref!!!
    # FIXME: need fool ref!!!
    # FIXME: need fool ref!!!
    # FIXME: need fool ref!!!

    def __init__(
            self,
            *,
            port: str = None,
            baudrate: int = 115200,
            bytesize: int = serial.EIGHTBITS,
            parity: str = serial.PARITY_NONE,
            stopbits: int = serial.STOPBITS_ONE,
            timeout: float = 1.0,
            write_timeout: float = 1.0,
            eol: str = '\n',
            encoding: str = 'utf-8',

            **kwargs,
    ):
        super().__init__(**kwargs)

        self.port = port
        self.baudrate = baudrate
        self.bytesize = bytesize
        self.parity = parity
        self.stopbits = stopbits
        self.timeout = timeout
        self.write_timeout = write_timeout
        self.eol = eol
        self.encoding = encoding

        self._conn: serial.Serial | None = None
        self._thread__reading_stdout: threading.Thread | None = None
        self._stop_reading = False

    # -----------------------------------------------------------------------------------------------------------------
    def connect(self) -> bool:
        try:
            if self._conn is None:
                self._conn = serial.Serial(
                    port=self.port,
                    baudrate=self.baudrate,
                    bytesize=self.bytesize,
                    parity=self.parity,
                    stopbits=self.stopbits,
                    timeout=self.timeout,
                    write_timeout=self.write_timeout,
                )
            if self._conn.is_open:
                return True

            self._conn.open()
        except Exception as exc:
            msg = f"[{self.port=}]{exc!r}"
            print(msg)
            self.history.add_data__stderr(msg)
            return False

        self._stop_reading = False
        self._thread__reading_stdout = threading.Thread(target=self._reading_stdout, daemon=True)
        self._thread__reading_stdout.start()

        time.sleep(0.3)
        return self._conn.is_open

    def disconnect(self) -> None:
        if self._conn is not None:

            self._stop_reading = True

            if self._thread__reading_stdout is not None:
                self._thread__reading_stdout.join(timeout=1)

            try:
                self._conn.close()
            except:
                pass
            self._conn = None

    # -----------------------------------------------------------------------------------------------------------------
    def _reading_stdout(self):
        while not self._stop_reading and self._conn is not None and self._conn.is_open:
            try:
                # Читаем строку до символа конца строки (или по таймауту)
                line_bytes = self._conn.readline()
                if line_bytes:
                    line = line_bytes.decode(self.encoding, errors='replace').rstrip('\r').rstrip('\n').rstrip('\r').rstrip('\n')
                    if line:
                        print(f"{line}")
                        self.history.add_data__stdout(line)

                # Для совместимости с методом wait__finish_executing_cmd обновляем duration
                # просто факт добавления строки уже обновит last_result.duration
            except serial.SerialException as e:
                print(f"Ошибка последовательного порта: {e!r}")
                self.history.add_data__stderr(f"Serial error: {e!r}")
                break
            except Exception as e:
                print(f"Неизвестная ошибка чтения: {e!r}")
                self.history.add_data__stderr(f"Read error: {e!r}")
                break

    # -----------------------------------------------------------------------------------------------------------------
    def send_command(
            self,
            cmd: str,
            timeout_start: float | None = None,
            timeout_finish: float | None = None,
            eol: str | None = None,
    ) -> CmdResult:
        """
        Отправляет команду в последовательный порт.
        По умолчанию добавляет self.eol (например, '\n').
        """
        EOL: str = eol if eol is not None else self.EOL_SEND

        self.history.add_data__stdin(cmd)
        try:
            # Отправка команды
            data = (cmd + self.eol).encode(self.encoding)
            self._conn.write(data)
            self._conn.flush()

            # Ожидание завершения вывода
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
    def send_ctrl_c(self):
        """Отправляет символ Ctrl+C (0x03) для прерывания текущей команды"""
        try:
            self._conn.write(b'\x03')
            self._conn.flush()
            # Можно добавить короткую паузу
            time.sleep(0.1)
        except Exception as e:
            print(f"Ошибка отправки Ctrl+C: {e!r}")

    def send_break(self, duration=0.25):
        """Отправляет условие BREAK (удерживает линию в 0)"""
        try:
            self._conn.send_break(duration=duration)
        except Exception as e:
            print(f"Ошибка отправки BREAK: {e!r}")


# =====================================================================================================================
def _explore__serial_basic():
    """Пример использования: открыть порт, отправить несколько команд"""
    # Автоматически ищем доступные порты (для демонстрации)
    ports = serial.tools.list_ports.comports()
    if not ports:
        print("Нет доступных COM-портов")
        return

    # Берём первый найденный порт
    port_name = ports[0].device
    print(f"Используем порт: {port_name}")

    with CmdTerminal_SerialSync(
            port=port_name,
            baudrate=115200,
            timeout=1.0,
            eol='\n',
            encoding='utf-8'
    ) as term:
        if not term.connect():
            return

        # Пример команд для типичного терминала
        term.send_command("help", timeout_finish=2.0)
        term.send_command("?", timeout_finish=1.0)
        term.send_command("version", timeout_finish=1.0)

        # Прерывание текущей команды (если зависло)
        # term.send_ctrl_c()

    time.sleep(0.5)


def _explore__serial_custom():
    """Пример с ручным указанием порта и скорости"""
    with CmdTerminal_SerialSync(
            port="COM3",
            baudrate=9600,
            timeout=2.0,
            eol='\r\n',          # для устройств, ожидающих CR+LF
            encoding='ascii'
    ) as term:
        if not term.connect():
            return

        term.send_command("AT", timeout_finish=2.0)
        term.send_command("ATI", timeout_finish=2.0)
        term.send_command("AT+CSQ", timeout_finish=2.0)


# =====================================================================================================================
if __name__ == "__main__":
    _explore__serial_basic()
    # _explore__serial_custom()


# =====================================================================================================================
