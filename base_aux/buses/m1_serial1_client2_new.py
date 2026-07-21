# REASON: try to create clear separated classes!
import re
import sys
import glob
import string
import time
from enum import auto
from base_aux.loggers.m2_logger import Logger

from serial import Serial, PortNotOpenError, SerialException
from serial.tools import list_ports
from base_aux.base_values.m5_value_valid3_unit import *
from base_aux.aux_eq.m2_eq_aux import EqAux
from base_aux.base_lambdas.m3_lambda4_list import *
from base_aux.cmds.m2_history import CmdHistory_Sync


# =====================================================================================================================
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
    __ADDRESS: str

    # need NONE NOT 0!!! if wait always!!
    TIMEOUT_READ_INITIAL: float = 0.3   # время ожидания первого байта # 0.2 is too short!!! dont touch! in case of reading char by char 0.5 is the best!!! 0.3 is not enough!!!
    TIMEOUT_READ_CONTINUE: float = 0.05 # пауза между чтениями после появления данных
    BAUDRATE: int = 9600  # 115200

    # rare INFRASTRUCTURE -------
    ENCODING: str = "utf8"
    EOL__SEND: bytes = b"\r\n"  # "\r"=ENTER in PUTTY  but "\r\n"=is better in read Putty!
    EOL__UNI: bytes = b"\r\n"

    @property
    def ADDRESS(self) -> str:
        return self.__ADDRESS

    # INIT ============================================================================================================
    def __init__(
            self,
            address: str,
            baudrate: int = None,
            timeout_read_initial: Optional[float] = None,
            timeout_read_continue: Optional[float] = None,
            eol__send: bytes = None,
            encoding: str = None,
            **kwargs,
    ):
        super().__init__(**kwargs)

        self.__ADDRESS = address
        self.baudrate = baudrate or self.BAUDRATE
        self.encoding = encoding or self.ENCODING
        self.timeout_read_initial = timeout_read_initial or self.TIMEOUT_READ_INITIAL
        self.timeout_read_continue = timeout_read_continue or self.TIMEOUT_READ_CONTINUE
        self.eol__send = eol__send or self.EOL__SEND

        self.history: list[dict[str, AnyStr]] = []
        self._conn: Optional[Serial] = None

    # ------------------------------------------------------------------
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
                write_timeout=None,            # блокирующая запись
            )
            return True
        except FileNotFoundError as exc:
            print(f"Port {self.ADDRESS} does not exist{self._conn}/{exc!r}")
        except PermissionError as exc:
            print(f"Permission denied for port {self.ADDRESS} (maybe already open){self._conn}/{exc!r}")
        except SerialException as exc:
            print(f"Serial error on {self.ADDRESS}: {self._conn}/{exc!r}")
        except Exception as exc:
            print(f"[ERROR] PORT OTHER ERROR: {self._conn}/{exc!r}")
            if "Port must be configured before" in str(exc):
                msg = f"[ERROR] PORT NOT CONFIGURED {self._conn}"
                print(msg)

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

            buses\serial_client.py:722: UnicodeDecodeError
        """
        try:
            if isinstance(data, bytes):
                return data.decode(self.encoding, errors="replace")
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

    # R ================================================================================================================
    def read_bytes(
            self,
            timeout_start: Optional[float] = None,
            timeout_continue: Optional[float] = None,
            timeout_full: Optional[float] = None,
    ) -> bytes:
        """
        Прочитать все доступные данные из порта.
        Сначала ждём появления данных в течение timeout_start.
        Как только появились – читаем с паузами timeout_continue, пока данные не кончатся.
        Возвращает прочитанные байты.
        """
        if not self.check__connected():
            print("Port not connected")
            return b""

        t_start = timeout_start if timeout_start is not None else self.timeout_read_initial
        t_cont = timeout_continue if timeout_continue is not None else self.timeout_read_continue

        # Сохраняем текущий таймаут, чтобы потом восстановить
        old_timeout = self._conn.timeout

        time_start = time.time()
        data = b""
        while True:
            # Ждём появления данных или таймаут
            self._conn.timeout = t_start if data == b"" else t_cont
            chunk = self._conn.read(self._conn.in_waiting or 1)
            if not chunk:
                break
            data += chunk
            if timeout_full and time_start + timeout_full < time.time():
                # if chunk in self.EOL__SEND:   # DONT USE IT HERE!!! stop is wary need whatever!!!
                break

        # Восстанавливаем таймаут
        self._conn.timeout = old_timeout

        self.history.append({"read": data})
        print(f"Read {len(data)} bytes: {data!r}")
        return data

    def read_lines(self, **kwargs) -> Union[str, List[str]]:
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
            self.history.append({"write": raw})
            return written == len(raw)
        else:
            msg = f"[ERROR] write {raw}"
            return False

    # W=SPECIAL -------------------------------------------------------------------------------------------------------
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
        data: bytes | None = None,
        eol: Optional[bytes] = None,
        clear_input_first: bool = True,
        **read_kwargs
    ) -> bytes:
        """Записать команду и сразу прочитать ответ (строки)."""
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

    def validate__wr_schema(self, schema: dict[AnyStr, str | Base_EqValid | list[str | Base_EqValid]]) -> bool:
        for (request, response_expected) in schema.items():
            response_actual = self.write_read_lines(request)
            if response_actual != response_expected:
                return False
        return True


# ======================================================================================================================
class SerialManager:
    _ADDRESSES__SYSTEM: list[str] | None = None
    _ADDRESSES__SHORTED: list[str] | None = None
    _ADDRESSES__PAIRED: list[tuple[str, str]] | None = None

    # ------------------------------------------------------------------------------------------------------------------
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self._cached_ports: Optional[List[str]] = None

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def ADDRESSES__SYSTEM(self) -> list[str]:
        if self._ADDRESSES__SYSTEM is None:
            self.detect__addresses_system()

        return self._ADDRESSES__SYSTEM

    def get__addresses_free(self) -> list[str]:
        result = []
        for addr in self.ADDRESSES__SYSTEM:
            if self.check__address_could_open(addr):
                result.append(addr)
        return result

    def count__addresses_system(self) -> int:
        return len(self.ADDRESSES__SYSTEM)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def check__address_could_open(address: str) -> bool:
        try:
            conn = Serial(address)
            conn.close()
            return True
        except:
            return False

    @staticmethod
    def check__address_exists(address: str) -> bool:
        try:
            conn = Serial(address)
            conn.close()
        except FileNotFoundError as exc:
            print(f"{exc!r}")
            return False
        except Exception as exc:
            print(f"{exc!r}")
            pass    # any other exc is OK!

        return True

    # ------------------------------------------------------------------------------------------------------------------
    def gen__first_free(self) -> SerialClient2 | None:
        pass

    def gen__first_shorted(self) -> SerialClient2 | None:
        pass

    def gen__first_validated(self) -> SerialClient2| None:
        pass

    # DETECT ----------------------------------------------------------------------------------------------------------
    @classmethod
    def detect__addresses_system(cls) -> list[str]:
        # WORK -------------------------------------------------------
        result = []
        result.extend(cls._detect__addresses_system_1__standard_method())
        result.extend(cls._detect__addresses_system_2__direct_access())

        # result -------------------------------------------------------
        if result:
            print(f"[OK] detected serial ports {result}")
        else:
            print("[WARN] detected no serial ports")

        cls._ADDRESSES__SYSTEM.clear()
        return cls._ADDRESSES__SYSTEM

    @staticmethod
    def _detect__addresses_system_1__standard_method() -> list[str] | NoReturn:
        """
        WINDOWS - USB
            ==========OBJECTINFO.PRINT==========================================================================
            str=COM8 - PL2303HXA PHASED OUT SINCE 2012. PLEASE CONTACT YOUR SUPPLIER.
            repr=<serial.tools.list_ports_common.ListPortInfo object at 0x00000267B3A38200>
            ----------properties_ok-----------------------------------------------------------------------------
            description              	str       :COM8
            device                   	str       :COM8
            hwid                     	str       :USB VID:PID=067B:2303 SER= LOCATION=1-2.4.3
            interface                	NoneType  :None
            location                 	str       :1-2.4.3
            manufacturer             	str       :Prolific
            name                     	str       :COM8
            pid                      	int       :8963
            product                  	NoneType  :None
            serial_number            	str       :
            vid                      	int       :1659
            ----------properties_exc----------------------------------------------------------------------------
            ----------base_types-----------------------------------------------------------------------------------
            ----------methods_ok--------------------------------------------------------------------------------
            apply_usb_info           	NoneType  :None
            usb_description          	str       :COM8
            usb_info                 	str       :USB VID:PID=067B:2303 SER= LOCATION=1-2.4.3
            ----------methods_exc-------------------------------------------------------------------------------
            ====================================================================================================

        RASPBERRY - USB
        кажется не видит встроенный COM порт даже после его включения и перезагрузки - только USB!!!

            ==========OBJECTINFO.PRINT==========================================================================
            str=/dev/ttyUSB0 - USB-Serial Controller
            repr=<serial.tools.list_ports_linux.SysFS object at 0x7fb332d9d0>
            ----------properties_ok-----------------------------------------------------------------------------
            description                     str       :USB-Serial Controller
            device                          str       :/dev/ttyUSB0
            device_path                     str       :/sys/devices/platform/soc/3f980000.usb/usb1/1-1/1-1.4/1-1.4:1.0/ttyUSB0
            hwid                            str       :USB VID:PID=067B:2303 LOCATION=1-1.4
            interface                       NoneType  :None
            location                        str       :1-1.4
            manufacturer                    str       :Prolific Technology Inc.
            name                            str       :ttyUSB0
            pid                             int       :8963
            product                         str       :USB-Serial Controller
            serial_number                   NoneType  :None
            subsystem                       str       :usb-serial
            usb_device_path                 str       :/sys/devices/platform/soc/3f980000.usb/usb1/1-1/1-1.4
            usb_interface_path              str       :/sys/devices/platform/soc/3f980000.usb/usb1/1-1/1-1.4/1-1.4:1.0
            vid                             int       :1659
            ----------properties_exc----------------------------------------------------------------------------
            ----------base_types-----------------------------------------------------------------------------------
            ----------methods_ok--------------------------------------------------------------------------------
            apply_usb_info                  NoneType  :None
            usb_description                 str       :USB-Serial Controller
            usb_info                        str       :USB VID:PID=067B:2303 LOCATION=1-1.4
            ----------methods_exc-------------------------------------------------------------------------------
            read_line                       TypeError :join() missing 1 required positional argument: 'a'
            ====================================================================================================
        """
        result: list[str] = []

        # find not opened ports ----------------------------------------
        for obj in list_ports.comports():
            # ObjectInfo(obj).print(hide_skipped=True, skip__build_in=True)
            result.append(obj.device)
            if Exc__SerialPL2303IncorrectDriver.MARKER in str(obj):
                msg = f'[WARN] incorrect driver [{Exc__SerialPL2303IncorrectDriver.MARKER}]'
                raise Exc__SerialPL2303IncorrectDriver(msg)
        return result

    @classmethod
    def _detect__addresses_system_2__direct_access(cls) -> list[str] | NoReturn:
        """Определяет список портов (НЕОТКРЫТЫХ+ОТКРЫТЫХ!!!) - способом 2 (слепым тестом подключения и анализом исключений)
        Всегда срабатывает!
        """
        if sys.platform.startswith('win'):
            attempt_list = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            attempt_list = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            attempt_list = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('[ERROR]Unsupported platform')

        result: list[str] = []
        for name in attempt_list:
            if cls.check__address_exists(address=name):
                result.append(name)

        return result


# =====================================================================================================================
def _explore():
    class Dev(SerialClient2):
        pass
        BAUDRATE = 115200
        EOL__SEND = b"\n"

    result = Dev().get__wr_responses(["*:get name", "*:get addr"])

    print(f"="*100)
    print(f"="*100)
    print(f"="*100)

    for port, responses in result.items():
        print(port, responses)
    print()

    """
COM11 {'*:get name': 'PTB', '*:get addr': 1''/str(1)}
COM4 {'*:get name': '*:get name', '*:get addr': '*:get addr'}
COM3 {'*:get name': 'ATC', '*:get addr': 3''/str(3)}
    """


# =====================================================================================================================
if __name__ == "__main__":
    _explore()
    pass


# =====================================================================================================================
