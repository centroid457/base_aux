import time
from typing import *

from base_aux.aux_eq.m4_eq_valid1_base import Base_EqValid
from base_aux.clients.m1_client_0__base import ClientBase


# ======================================================================================================================
class SshClient(ClientBase):
    """
    SSH client implementation that follows the same interface as ClientSerial.
    Uses paramiko for SSH connections.
    """
    # SETTINGS ------------------------------------------------
    PORT: int = 22

    # INIT =============================================================================================================
    def __init__(
            self,
            # MULTITON KEY ID ------------
            address: str,

            # SSH SETTINGS --------------
            username: str = None,
            password: str = None,
            port: int = None,
            timeout_read_initial: Optional[float] = None,
            timeout_read_continue: Optional[float] = None,
            eol__send: bytes = None,
            encoding: str = None,

            # OTHERS ---------------------
            history_enable: bool = False,
            _raise_if_occupied: bool = True,

            **kwargs,
    ):
        # freely create new instance with new settings if not occupied
        self._ssh_client = None
        self._channel = None

        super().__init__(
            address=address,
            history_enable=history_enable,
            _raise_if_occupied=_raise_if_occupied,
            **kwargs,
        )

        self.init_settings(
            username=username,
            password=password,
            port=port,
            timeout_read_initial=timeout_read_initial,
            timeout_read_continue=timeout_read_continue,
            eol__send=eol__send,
            encoding=encoding,
            _raise_if_occupied=_raise_if_occupied,
        )

    # ------------------------------------------------------------------
    def init_settings(
            self,
            username: str = None,
            password: str = None,
            port: int = None,
            timeout_read_initial: Optional[float] = None,
            timeout_read_continue: Optional[float] = None,
            eol__send: bytes = None,
            encoding: str = None,

            _raise_if_occupied: bool = True,
    ) -> None | NoReturn:
        if self.check__occupied():
            msg = f"[ERROR] cant change settings for already occupied {self}"
            if _raise_if_occupied:
                raise Exception(msg)
            return

        self.username = username
        self.password = password
        self.port = port or self.PORT
        self.encoding = encoding or self.ENCODING
        self.timeout_read_initial = timeout_read_initial or self.TIMEOUT_READ_INITIAL
        self.timeout_read_continue = timeout_read_continue or self.TIMEOUT_READ_CONTINUE
        self.eol__send = eol__send or self.EOL__SEND

    # CONNECT ==========================================================================================================
    def connect(self) -> bool:
        if self.check__connected():
            return True
        try:
            import paramiko

            self._ssh_client = paramiko.SSHClient()
            self._ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self._ssh_client.connect(
                hostname=self.ADDRESS,
                port=self.port,
                username=self.username,
                password=self.password,
                timeout=self.timeout_read_initial,
            )

            self._channel = self._ssh_client.invoke_shell()
            self._channel.settimeout(self.timeout_read_initial)

            return True
        except ImportError:
            print(f"paramiko module is required for SSH connections")
            return False
        except Exception as e:
            print(f"SSH connection error to {self.ADDRESS}: {e}")
            return False

    def disconnect(self) -> None:
        try:
            if self._channel:
                self._channel.close()
            if self._ssh_client:
                self._ssh_client.close()
        except:
            pass

    def check__connected(self) -> bool:
        try:
            return self._channel is not None and not self._channel.closed
        except:
            return False

    # BUFFERS ----------------------------------------------------------------------------------------------------------
    def buffers_clear(self) -> None:
        """useful to drop old previous incorrect send msg! in other words it is clear/reinit write buffer!

        here we need just finish line by correct/exact EOL if it was previously send without it or with incorrect.
        """
        if not self.check__connected():
            return

        # Read and discard any pending data
        try:
            while self._channel.recv_ready():
                self._channel.recv(1024)
        except:
            pass

    def check__buffer_is_blank(self) -> bool:
        return self._channel.recv_ready()

    # R ================================================================================================================
    def read_bytes(
            self,
            stop_line: AnyStr | Base_EqValid | None = None,

            timeout_start: Optional[float] = None,
            timeout_continue: Optional[float] = None,

            timeout_full_max: Optional[float] = None,
            timeout_full_min: Optional[float] = None,
    ) -> bytes:
        """
        MAIN METH!!!

        Прочитать все доступные данные из порта.
        Сначала ждём появления данных в течение timeout_start.
        Как только появились – читаем с паузами timeout_continue, пока данные не кончатся.
        Возвращает прочитанные байты.
        """
        with self._lock_r:
            if not self.check__connected():
                print("Port not connected")
                return b""

            if stop_line is not None:
                if isinstance(stop_line, str):
                    stop_line = self._to_bytes(stop_line)
                if not isinstance(stop_line, (Base_EqValid, bytes)):
                    msg = f"not expected type {stop_line=}"
                    raise Exception(msg)

            t_start = timeout_start if timeout_start is not None else self.timeout_read_initial
            t_cont = timeout_continue if timeout_continue is not None else self.timeout_read_continue

            # Сохраняем текущий таймаут, чтобы потом восстановить
            old_timeout = self._channel.gettimeout()

            time_start = time.time()
            result: bytes = b""
            _new_line: bytes = b""

            while True:
                # self._print_line(process="readSTART")

                # Ждём появления данных или таймаут
                self._channel.settimeout(t_start if result == b"" else t_cont)

                try:
                    _new_byte = self._channel.recv(1)
                except:
                    _new_byte = b""

                # 1=БАЙТА НЕТ ---------
                if not _new_byte:
                    if not timeout_full_min:
                        break
                    elif time.time() - time_start > timeout_full_min:
                        break
                    else:
                        pass

                # 2=БАЙТ ЕСТЬ ---------
                if _new_byte:
                    # 1=EOL - нет
                    if _new_byte not in self.EOL__UNI:
                        # 1.1=COLLECT ---------
                        _new_line += _new_byte
                        continue

                    # 2=EOL - получен
                    if _new_line:
                        self._print_line(process="readEOL", line=_new_line)
                        result += b"\n"
                        result += _new_line

                        # 1.2=STOP ON ---------
                        if stop_line is not None:
                            if _new_line == stop_line:
                                self._print_line(process="stop_line", extra=stop_line)
                                break

                        _new_line = b""

                # 3=MAX THRESH -----------
                if timeout_full_max and time.time() - time_start > timeout_full_max:
                    # if _new_byte in self.EOL__SEND:   # DONT USE IT HERE!!! stop is wary need whatever!!!
                    break

            # 4=finalize not ended EOL line like password: or terminal prompt
            if _new_line:
                self._print_line(process="readNoEOL", line=_new_line)
                result += _new_line
                _new_line = b""

            # 5=EXIT ------------------
            # Восстанавливаем таймаут
            self._channel.settimeout(old_timeout)

            msg = {"read": result}
            if self.history_enable:
                self.history.append(msg)

            return result.strip()

    # W ================================================================================================================
    def write_bytes(
            self,
            data: AnyStr | None = None,
            eol: bytes | None = None,
            clear_input_first: bool = True,
    ) -> bool:
        """
        just send data into bus!
        usually we dont need just send without reading! so it useful for debugging

        :return: result of sent

        args/kwargs - used only for single line!!!
        """
        with self._lock_w:
            if not self.check__connected():
                print("Port not connected")
                return False

            if clear_input_first:
                time.sleep(0.1)  # на всякий случай!!! 0.1 может не хватать!
                self.buffers_clear()

            raw = self._to_bytes(data)
            raw = self._eol_ensure(raw, eol)

            if not raw:
                return False

            written = 0
            try:
                written = self._channel.send(raw)
                self._print_line(process="write", line=raw)
            except Exception as exc:
                self._print_line(process="write", line=raw, success=False, extra=f"{exc!r}")

            if written > 0:
                msg = {"write": raw}
                if self.history_enable:
                    self.history.append(msg)

                return written == len(raw)
            else:
                return False

    # W=SPECIAL --------------------------------------------------------------------------------------------------------
    def send__break(self, duration: float = 0.25) -> None:
        """Send a BREAK condition."""
        # SSH doesn't have a native break signal, send Ctrl+C as alternative
        self.send__ctrl_c()

    def send__ctrl_c(self) -> None:
        """Send the Ctrl+C character (0x03)."""
        self.write_bytes(b'\x03', eol=b"")
        time.sleep(0.2)


# ======================================================================================================================
