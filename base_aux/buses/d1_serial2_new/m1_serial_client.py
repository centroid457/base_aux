# REASON: try to create clear separated classes!
from serial import Serial, SerialException
from threading import Lock
import re

from base_aux.aux_eq.m3_eq_valid3_derivatives import *
from base_aux.base_values.m3_exceptions import *


# ======================================================================================================================
TYPING__WR_SCHEMA_VALIDATE = list[tuple[AnyStr, str | Base_EqValid | list[str | Base_EqValid]]]


# ======================================================================================================================
class SerialClient2:
    """
    CONSTRAINTS
    1/ work with string for user!
        all unusual packages in bytes (CtrlC ...) send by special method!
    2/ history is not used usually! may be need to delete it!
        all you need - take result as read lines or line
        maybe keep history in device? not in this connection object
    3/
    """
    # SETTINGS ------------------------------------------------
    __address: str
    __occupied: str | None | Any = None

    # need NONE NOT 0!!! if wait always!!
    TIMEOUT_READ_INITIAL: float = 0.5   # время ожидания первого байта # 0.2 is too short!!! dont touch! in case of reading char by char 0.5 is the best!!! 0.3 is not enough!!!
    TIMEOUT_READ_CONTINUE: float = 0.05 # пауза между чтениями после появления данных
    BAUDRATE: int = 9600  # 115200

    # rare INFRASTRUCTURE -------
    ENCODING: str = "utf8"
    EOL__SEND: bytes = b"\r\n"  # "\r"=ENTER in PUTTY  but "\r\n"=is better in read Putty!
    EOL__UNI: bytes = b"\r\n"

    @property
    def ADDRESS(self) -> str:
        return self.__address

    # MULTITON =========================================================================================================
    _instances: dict[str, Self] = {}

    def __new__(cls, address: str, **kwargs):
        # Если экземпляр уже есть – возвращаем его (игнорируем kwargs, либо проверяем)
        if address in cls._instances:
            return cls._instances[address]
        # Иначе создаём новый
        instance = super().__new__(cls)
        cls._instances[address] = instance
        return instance

    # INIT =============================================================================================================
    def __init__(
            self,
            # MULTITON KEY ID ------------
            address: str,

            # PORT SETTINGS --------------
            baudrate: int = None,
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
        self.init_settings(
            baudrate=baudrate,
            timeout_read_initial=timeout_read_initial,
            timeout_read_continue=timeout_read_continue,
            eol__send=eol__send,
            encoding=encoding,
            _raise_if_occupied=_raise_if_occupied,
        )

        # защитить повторную инициализацию.
        if hasattr(self, "_initialized") and self._initialized:
            return
        self._initialized = True

        super().__init__(**kwargs)

        self.__address = address
        self.history_enable = history_enable
        self.history: list[dict[str, AnyStr]] = []
        self._conn: Optional[Serial] = None

        self._lock_wr: Lock = Lock()
        self._lock_w: Lock = Lock()
        self._lock_r: Lock = Lock()

    # ------------------------------------------------------------------
    def init_settings(
            self,
            baudrate: int = None,
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

        self.baudrate = baudrate or self.BAUDRATE
        self.encoding = encoding or self.ENCODING
        self.timeout_read_initial = timeout_read_initial or self.TIMEOUT_READ_INITIAL
        self.timeout_read_continue = timeout_read_continue or self.TIMEOUT_READ_CONTINUE
        self.eol__send = eol__send or self.EOL__SEND

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def occupied_name(self) -> str | None | Any:
        return self.__occupied

    def occupy(self, name: str | None | Any = True) -> None:
        if self.__occupied and name is not None:
            msg = f"[ERROR] attempt to occupy already {self.__occupied=}"
            raise Exception(msg)
        self.__occupied = name

    def check__occupied(self) -> bool:
        return self.__occupied is not None

    # ==================================================================================================================
    def __str__(self):
        return f"{self.__class__.__name__}({self.ADDRESS}.{self.baudrate},occupied={self.__occupied})"

    def __repr__(self):
        return str(self)

    # ==================================================================================================================
    def __enter__(self) -> Self:
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    # CONNECT ==========================================================================================================
    def connect(self) -> bool:
        if self.check__connected():
            return True
        try:
            self._conn = Serial(
                port=self.ADDRESS,
                baudrate=self.baudrate,
                timeout=self.timeout_read_initial,
                write_timeout=None,
            )
            return True
        except SerialException as e:
            cause = e.__cause__ or e.__context__
            if cause and isinstance(cause, FileNotFoundError):
                print(f"Port {self.ADDRESS} does not exist")
            elif cause and isinstance(cause, PermissionError):
                print(f"Permission denied for {self.ADDRESS} (maybe open)")
            else:
                # fallback на текст
                msg = str(e).lower()
                if "file not found" in msg or "no such file" in msg:
                    print(f"Port {self.ADDRESS} does not exist")
                elif "permission denied" in msg or "access denied" in msg:
                    print(f"Permission denied for {self.ADDRESS}")
                else:
                    print(f"Serial error on {self.ADDRESS}: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error: {e}")
            return False

    # -----------------------------------------------------------------
    def reconnect(self) -> bool:
        try:
            self.disconnect()
        except:
            pass

        return self.connect()

    def disconnect(self) -> None:
        try:
            self._conn.close()
        except:
            pass

    def __del__(self) -> None:
        self.disconnect()

    def check__connected(self) -> bool:
        try:
            return self._conn.is_open
        except:
            return False

    # RW CONVERTERS ====================================================================================================
    # BYTES/STR --------------------------------------------------------------------------------------------------------
    def _to_bytes(self, data: AnyStr | None) -> bytes:
        if data is None:
            data = b""

        if isinstance(data, bytes):
            return data

        return data.encode(self.encoding)

    @staticmethod
    def _strip_ansi(text: str) -> str:
        """
        GOAL
        Удалить CSI‑последовательности: \x1b[...m, \x1b[...h, \x1b[...l и т.д.

        DeviceConsole_Harvest(COM16.115200,occupied=None){'write': b'root\r\n'}
        DeviceConsole_Harvest(COM16.115200,occupied=None){'read': b'root\r\n\x1b[?2004l\r-bash: root: command not found\r\n\x1b[?2004hroot@harvest05:~# \r\n\x1b[?2004l\r\x1b[?2004hroot@harvest05:~# '}
        DeviceConsole_Harvest(COM16.115200,occupied=None){'write': b'hostname\r\n'}
        DeviceConsole_Harvest(COM16.115200,occupied=None){'read': b'hostname\r\n\x1b[?2004l\rharvest05\r\n\x1b[?2004hroot@harvest05:~# \r\n\x1b[?2004l\r\x1b[?2004hroot@harvest05:~# '}
        DeviceConsole_Harvest(COM16.115200,occupied=None){'write': b'hostname\r\n'}
        DeviceConsole_Harvest(COM16.115200,occupied=None){'read': b'hostname\r\n\x1b[?2004l\rharvest05\r\n\x1b[?2004hroot@harvest05:~# \r\n\x1b[?2004l\r\x1b[?2004hroot@harvest05:~# '}

        [HARVEST_FOUND]DeviceConsole_Harvest(COM16.115200,occupied=None)/dev_id='harvest05'
        """
        ansi_escape = re.compile(r'\x1b\[[0-9;?]*[A-Za-z]')
        return ansi_escape.sub('', text)

    def _decoder__bytes_to_str(self, data: bytes) -> str:
        if not isinstance(data, bytes):
            msg = f"{data=}"
            raise TypeError(msg)

        result = data.decode(self.encoding, errors="replace")
        result = self._strip_ansi(result)
        return result

    def _to_str(self, data: AnyStr) -> str | NoReturn:
        """
        EXCEPTION ORIGINAL VARIANT
        --------------------------
            cls = <class 'test__serial_server.Victim'>, data = b'\\x85RR__NAME_CMD_OR_PARAM

                @classmethod
                def _data_ensure__string(cls, data: AnyStr) -> Union[str, NoReturn]:
                    if isinstance(data, bytes):
            >           return data.decode(encoding=cls.encoding)
            E           UnicodeDecodeError: 'utf-8' codec can't decode byte 0x85 in position 0: invalid start byte

            buses\\serial_client.py:722: UnicodeDecodeError
        """
        try:
            if isinstance(data, bytes):
                return self._decoder__bytes_to_str(data)
            else:
                result = str(data)
        except Exception as exc:
            print(f"[FAIL] decoding{exc!r}")
            raise exc

        return result

    # BYTES ------------------------------------------------------------------------------------------------------------
    def _eol_ensure(self, data: bytes, eol: bytes | None = None) -> bytes | NoReturn:
        """
        GOAL
        prepare line for write
        """
        if eol is None:
            eol = self.eol__send
        if eol == b"":
            return data
        data = self._eol_strip(data) + eol
        return data

    def _eol_strip(self, data: bytes) -> AnyStr | NoReturn:
        """
        GOAL
        prepare line for write
        """
        result: bytes = data
        while True:
            data_new = data.strip()
            data_new = data_new.strip(self.EOL__UNI)
            if not result or result == data_new:
                break
            result = data_new

        return result

    def _split_lines(self, data: bytes) -> list[str]:
        """
        GOAL
        separate lines for read
        """
        data_str = self._to_str(data)
        data_list = re.split(r'[\r\n]+', data_str)
        result = [*filter(lambda x: x != "", data_list)]
        result = result or ["", ]
        return result

    # BUFFERS ----------------------------------------------------------------------------------------------------------
    # def _buffers_clear_1__write(self) -> None:
    #     """useful to drop old previous incorrect send msg! in other words it is clear/reinit write buffer!
    #
    #     here we need just finish line by correct/exact EOL if it was previously send without it or with incorrect.
    #     """
    #     try:
    #         # self._write__eol()    # danger!
    #         self._conn.reset_input_buffer()
    #     except:
    #         pass
    #
    # def _buffers_clear_2__read(self, _timeout: Optional[float] = None) -> None:
    #     # self._conn.timeout = _timeout or self.TIMEOUT_READ_INITIAL or None
    #     # while True:
    #     #     try:
    #     #         if not self._conn.readall():
    #     #             break
    #     #     except:
    #     #         pass
    #     #     time.sleep(0.1)
    #     #
    #     # self._conn.timeout = self.TIMEOUT_READ_INITIAL or None  # set back - final
    #     self._conn.reset_output_buffer()

    def buffers_clear(self) -> None:
        """useful to drop old previous incorrect send msg! in other words it is clear/reinit write buffer!

        here we need just finish line by correct/exact EOL if it was previously send without it or with incorrect.
        """
        if not self.check__connected():
            return

        self._conn.reset_input_buffer()
        self._conn.reset_output_buffer()

    def check__buffer_is_blank(self) -> bool:
        return bool(self._conn.in_waiting)

    # R ================================================================================================================
    def read_bytes(
            self,
            until_expected: AnyStr | Base_EqValid | None = None,

            timeout_start: Optional[float] = None,
            timeout_continue: Optional[float] = None,

            timeout_full_max: Optional[float] = None,
            timeout_full_min: Optional[float] = None,
    ) -> bytes:
        """
        Прочитать все доступные данные из порта.
        Сначала ждём появления данных в течение timeout_start.
        Как только появились – читаем с паузами timeout_continue, пока данные не кончатся.
        Возвращает прочитанные байты.
        """
        with self._lock_r:
            if not self.check__connected():
                print("Port not connected")
                return b""

            if until_expected is not None:
                if isinstance(until_expected, str):
                    until_expected = self._to_bytes(until_expected)
                if not isinstance(until_expected, (Base_EqValid, bytes)):
                    msg = f"not expected type {until_expected=}"
                    raise Exception(msg)

            t_start = timeout_start if timeout_start is not None else self.timeout_read_initial
            t_cont = timeout_continue if timeout_continue is not None else self.timeout_read_continue

            # Сохраняем текущий таймаут, чтобы потом восстановить
            old_timeout = self._conn.timeout

            time_start = time.time()
            data = b""
            while True:
                # Ждём появления данных или таймаут
                self._conn.timeout = t_start if data == b"" else t_cont
                if until_expected is None:
                    chunk = self._conn.read(self._conn.in_waiting or 1)
                else:
                    chunk = self._conn.read(1)

                if not chunk:
                    if not timeout_full_min:
                        break
                    elif time.time() - time_start > timeout_full_min:
                        break

                data += chunk
                if until_expected is not None:
                    if data in until_expected:
                        break

                # MAX THRESH
                if timeout_full_max and time.time() - time_start > timeout_full_max:
                    # if chunk in self.EOL__SEND:   # DONT USE IT HERE!!! stop is wary need whatever!!!
                    break

            # Восстанавливаем таймаут
            self._conn.timeout = old_timeout

            msg = {"read": data}
            if self.history_enable:
                self.history.append(msg)
            print(f"{self}{msg}")
            return data

    def read_lines(self, **kwargs) -> Union[str, list[str]]:
        """
        Прочитать данные и разбить на строки.
        Если получена одна строка – возвращает str, иначе список строк.
        """
        raw = self.read_bytes(**kwargs)
        lines = self._split_lines(raw)
        return lines[0] if len(lines) == 1 else lines

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
                self._conn.reset_input_buffer()

            raw = self._to_bytes(data)
            raw = self._eol_ensure(raw, eol)

            if not raw:
                return False

            written = 0
            try:
                written = self._conn.write(raw)
                msg = f"[OK]write={raw}/{written=}"
            except Exception as exc:
                msg = f"[FAIL]write={raw}/{exc!r}"

            if written > 0:
                msg = {"write": raw}
                if self.history_enable:
                    self.history.append(msg)
                print(f"{self}{msg}")
                return written == len(raw)
            else:
                msg = f"[ERROR] write {raw}"
                return False

    # W=SPECIAL --------------------------------------------------------------------------------------------------------
    def _write__eol(self, eol: bytes = None) -> bool:
        """
        write without any conditions (no prefixes! no suffixes)!
        GOAL
        ----
        finish any writen cmd and clear buffer
        """
        return self.write_bytes(eol=eol)

    def send__break(self, duration: float = 0.25) -> None:
        """Send a BREAK condition."""
        self._conn.send_break(duration)

    def send__ctrl_c(self) -> bool:
        """Send the Ctrl+C character (0x03)."""
        return self.write_bytes(b'\x03', eol=b"")

    def send__ctrl(self, char: Union[str, int]) -> bool:
        """
        Send a control character: e.g. send_ctrl('C') -> 0x03,
        send_ctrl(0x1A) -> 0x1A.
        """
        if isinstance(char, str) and len(char) == 1:
            code = (ord(char.upper()) - ord('A') + 1) & 0x1F
        else:
            code = int(char) & 0x1F
        return self.write_bytes(bytes([code]), eol=b"")

    # WR ===============================================================================================================
    def write_read_bytes(
        self,
        data: AnyStr | None = None,
        eol: Optional[bytes] = None,
        clear_input_first: bool = True,
        **read_kwargs
    ) -> bytes:
        """Записать команду и сразу прочитать ответ (строки)."""
        with self._lock_wr:
            self.write_bytes(data, eol, clear_input_first)
            return self.read_bytes(**read_kwargs)

    def write_read_lines(
            self,
            data: AnyStr | None = None,
            eol: Optional[bytes] = None,
            clear_input_first: bool = True,
            **read_kwargs
    ) -> str | list[str]:
        """Записать (с автоматическим преобразованием) и прочитать строки."""
        with self._lock_wr:
            self.write_bytes(data, eol, clear_input_first)
            return self.read_lines(**read_kwargs)

    # ------------------------------------------------------------------------------------------------------------------
    def get__wr_responses(self, lines: list[AnyStr]) -> dict[AnyStr, list[str]]:
        result = {}
        for line in lines:
            try:
                responce = self.write_read_lines(line)
            except Exception as exc:
                responce = f"{exc!r}"

            result[line] = responce
        return result

    def validate__wr_schema(self, schema: TYPING__WR_SCHEMA_VALIDATE) -> bool:
        for (request, response_expected) in schema:
            response_actual = self.write_read_lines(request)
            if response_actual != response_expected:
                msg = f"{request!r}:{response_actual=}/{response_expected=}"
                print(msg)
                return False
        return True


# ======================================================================================================================
def _explore1():
    pass


# ======================================================================================================================
if __name__ == "__main__":
    _explore1()
    pass


# ======================================================================================================================
