# REASON: try to create clear separated classes!

import sys
import glob
import string
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
    # SETTINGS ------------------------------------------------
    __ADDRESS: str

    TIMEOUT__READ: float = 0.3  # 0.2 is too short!!! dont touch! in case of reading char by char 0.5 is the best!!! 0.3 is not enough!!!
    # need NONE NOT 0!!! if wait always!!
    BAUDRATE: int = 9600  # 115200

    # rare INFRASTRUCTURE -------
    ENCODING: str = "utf8"
    EOL__SEND: bytes = b"\r\n"  # "\r"=ENTER in PUTTY  but "\r\n"=is better in read Putty!
    EOL__UNI_SET: bytes = b"\r\n"

    # AUX -----------------------------------------------------
    history: CmdHistory_Sync
    _conn: Serial = None

    @property
    def ADDRESS(self) -> str:
        return self.__ADDRESS

    # INIT ============================================================================================================
    def __init__(
            self,
            address: str,
            baudrate: int = None,
            timeout__read: int = None,
            eol__send: bytes = None,
            **kwargs,
    ):
        super().__init__(**kwargs)

        self.__ADDRESS = address
        if baudrate is not None:
            self.BAUDRATE = baudrate
        if timeout__read is not None:
            self.TIMEOUT__READ = timeout__read
        if eol__send is not None:
            self.EOL__SEND = eol__send

        self.history = CmdHistory_Sync()

    # ------------------------------------------------------------------
    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    # CONNECT ==========================================================================================================
    def connect(self) -> bool:
        try:
            self._conn = Serial(
                port=self.ADDRESS,
                baudrate=self.BAUDRATE,
                timeout=self.TIMEOUT__READ,
            )
            return True
        except Exception as exc:
            print(f"{exc!r}")

            if "FileNotFoundError" in str(exc):
                msg = f"[ERROR] PORT NOT EXISTS IN SYSTEM {self._conn}"
            elif "Port must be configured before" in str(exc):
                msg = f"[ERROR] PORT NOT CONFIGURED {self._conn}"
            elif "PermissionError" in str(exc):
                msg = f"[ERROR] PORT ALREADY OPENED {self._conn}"
            else:
                msg = f"[ERROR] PORT OTHER ERROR {self._conn}"

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

    # RW ===============================================================================================================
    # CONVERTERS -------------------------------------------------------------------------------------------------------
    # BYTES ------------------------------------------------------------------------------------------------------------
    @classmethod
    def _data_bytes__eol_ensure(cls, data: bytes) -> bytes | NoReturn:
        data = cls._data_any__eol_clear(data) + cls.EOL__SEND
        return data

    @classmethod
    def _data_any__eol_clear(cls, data: AnyStr) -> Union[AnyStr, NoReturn]:
        result: bytes = cls._data_ensure__bytes(data)
        while True:
            data_new = result.strip()
            data_new = data_new.strip(cls.EOL__UNI_SET)
            if not result or result == data_new:
                break
            result = data_new

        if isinstance(data, str):
            return cls._data_ensure__string(result)

        return result

    # BYTES/STR --------------------------------------------------------------------------------------------------------
    @classmethod
    def _data_ensure__bytes(cls, data: AnyStr) -> bytes:
        if isinstance(data, bytes):
            return data
        else:
            return bytes(data, encoding=cls.ENCODING)

    @classmethod
    def _data_ensure__string(cls, data: AnyStr) -> str | NoReturn:
        """
        EXCEPTION ORIGINAL VARIANT
        --------------------------
            cls = <class 'test__serial_server.Victim'>, data = b'\\x85RR__NAME_CMD_OR_PARAM

                @classmethod
                def _data_ensure__string(cls, data: AnyStr) -> Union[str, NoReturn]:
                    if isinstance(data, bytes):
            >           return data.decode(encoding=cls.ENCODING)
            E           UnicodeDecodeError: 'utf-8' codec can't decode byte 0x85 in position 0: invalid start byte

            buses\serial_client.py:722: UnicodeDecodeError
        """
        # TODO: move to separated module!
        try:
            if isinstance(data, bytes):
                result = data.decode(encoding=cls.ENCODING)
            else:
                result = str(data)
        except Exception as exc:
            print(f"{exc!r}")
            msg = f"[FAIL] decoding {data=}"
            raise Exc_SerialRead_FailDecoding(msg)

        # check printable ascii ------------------
        for char in result:
            if isinstance(char, bytes):
                char = chr(char)
            if char not in string.printable:
                msg = f"[FAIL] decoding [{char=}]"
                raise Exc_SerialRead_FailDecoding(msg)

        # ----------------------------------------
        return result

    # BUFFERS ----------------------------------------------------------------------------------------------------------
    def _buffers_clear_1__write(self) -> None:
        """useful to drop old previous incorrect send msg! in other words it is clear/reinit write buffer!

        here we need just finish line by correct/exact EOL if it was previously send without it or with incorrect.
        """
        try:
            self._write__eol()
            self._conn.reset_input_buffer()
        except:
            pass

    def _buffers_clear_2__read(self, _timeout: Optional[float] = None) -> None:
        self._conn.timeout = _timeout or self.TIMEOUT__READ or None
        while True:
            try:
                if not self._conn.readline(1):
                    break
            except:
                pass
            time.sleep(0.1)

        self._conn.timeout = self.TIMEOUT__READ or None  # set back - final
        self._conn.reset_output_buffer()

    def buffers_clear(self) -> None:
        """useful to drop old previous incorrect send msg! in other words it is clear/reinit write buffer!

        here we need just finish line by correct/exact EOL if it was previously send without it or with incorrect.
        """
        self._buffers_clear_1__write()
        self._buffers_clear_2__read()

    # R ---------------------------------------------------------------------------------------------------------------
    # TODO: use wrapper for connect/disconnect!??? - NO!
    def read_lines(self, _timeout: Optional[float] = None) -> list[TYPE__RW_ANSWER_SINGLE] | NoReturn:
        result: list[str] = []
        while True:
            line = self.read_line(_timeout)
            _timeout = self.TIMEOUT__READ or None
            if line is None or str(line) == "":
                break
            else:
                result.append(line)

        return result

    def read_line(self, _timeout: Optional[float] = None) -> Union[str, ValueUnit, NoReturn]:
        """
        read line from bus buffer,

        CAREFUL
        -------
        DONT USE! IF WANT TO BE SURE!
        instead use write_read__last_validate!!! it would rewrite data if not valid answer (even with incorrect but good decoding)!!!

        TODO: here possible rewrite by getting from history!!!
        """
        # FIXME: return Object??? need keep exc for not finished readline!!!
        # var1: just read as usual - could cause error with not full bytes read in ONE CHAR!!!
        # data = self._conn.readline()

        # var2: char by char
        data = b""
        eol_received = False

        self._conn.timeout = _timeout or self.TIMEOUT__READ or None
        while True:
            new_char = None
            for i in range(2):
                new_char = self._conn.readline(1)
                self._conn.timeout = self.TIMEOUT__READ or None  # set back - no need repiatiting
                if new_char:
                    break

            if not new_char:
                # print(f"detected finish line")
                break
            if new_char == b'\x7f':  # BACKSPACE
                # LINE EDITION --------------
                data = data[:-1]
                continue

            if new_char in self.EOL__UNI_SET:
                # LINE FINISHED --------------
                eol_received = True
                if data:
                    break
                else:
                    continue

            data += new_char

        self._conn.timeout = self.TIMEOUT__READ or None  # set back - final

        # RESULT ----------------------
        if data:
            if not eol_received:
                msg = f"[ERROR]NotFullLine read_line={data}->CLEAR!!!"
                exc = Exc_SerialRead_NotFullLine(msg)
                data = b""
            else:
                msg = f"[OK]read_line={data}"

        else:
            msg = f"[WARN]BLANK read_line={data}"

        self.LOGGER.info(f"[{self._conn.port}.{self._conn.baudrate}]{msg}")

        data = self._bytes_edition__apply(data)
        data = self._data_any__eol_clear(data)
        data = self._data_ensure__string(data)
        self.history.add_data__stdout(data)
        self.answer_is_fail(data)

        # NOTE: dont delete! need to direct cmp
        try:
            # pass
            data = ValueUnit_NoMulty(data)
        except:
            pass

        return data
    # W=SPECIAL --------------------------- ----------------------------------------------------------------------------
    def _write__eol(self, eol: bytes = None) -> bool:
        """
        write without any conditions (no prefixes! no suffixes)!
        GOAL
        ----
        finish any writen cmd and clear buffer
        """
        eol = eol or self.EOL__SEND
        try:
            return bool(self._conn.write(eol))
        except:
            return False

    def send__break(self, duration: float = 0.25) -> None:
        """Send a BREAK condition."""
        if self.check__connected():
            self._conn.send_break(duration)

    def send__ctrl_c(self) -> None:
        """Send the Ctrl+C character (0x03)."""
        self.write_bytes(b'\x03')

    def send__ctrl(self, char: Union[str, int]) -> None:
        """
        Send a control character: e.g. send_ctrl('C') -> 0x03,
        send_ctrl(0x1A) -> 0x1A.
        """
        if isinstance(char, str) and len(char) == 1:
            # ASCII control: uppercase letter
            code = ord(char.upper()) - ord('A') + 1
        else:
            code = int(char) & 0x1F
        self.write_bytes(bytes([code]))

    # ------------------------------------------------------------------------------------------------------------------
    def validate__wr_schema(self, schema: dict[str, str]) -> bool:
        pass







# ======================================================================================================================
# TODO: SINGLETON!!!
class SerialManager:
    _ADDRESSES__SYSTEM: list[str] | None = None
    _ADDRESSES__SHORTED: list[str] | None = None
    _ADDRESSES__PAIRED: list[tuple[str, str]] | None = None

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
            return True
        except Exception as exc:
            print(f"{exc!r}")

            if "FileNotFoundError" in str(exc):
                return False
            else:
                return True

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

    # ------------------------------------------------------------------------------------------------------------------





















# =====================================================================================================================
class OLD__SerialClient:
    # -------------------------------------------------------------------------------------------------------------------
    @classmethod
    def ___addresses_shorted__detect(cls) -> list[str]:
        # WORK ----------------------------------------------
        result = []
        for address in cls.detect__addresses_system():
            obj = SerialClient2()
            if obj.connect(address=address, _raise=False):
                if obj._address__validate_shorted():
                    result.append(address)
                obj.disconnect()

        SerialClient2.ADDRESSES__SHORTED = result
        print(f"{SerialClient2.ADDRESSES__SHORTED=}")
        return result

    @classmethod
    def ___addresses_paired__detect(cls) -> list[tuple[str, str]]:
        # FIXME: IT SEEMS NOT WORKING!!!
        if cls.count__addresses_system() < 2:
            return []

        # WORK ----------------------------------------------
        load = "EXPECT_ANSWER__PAIRED"
        result = []
        instances_free_remain = []

        system_ports = cls.detect__addresses_system()

        # CONNECT ALL -----
        for address in system_ports:
            instance = SerialClient2()
            if instance.connect(address=address, _raise=False):
                instances_free_remain.append(instance)

        while len(instances_free_remain) > 1:
            # take one port --------
            master = instances_free_remain.pop(0)
            _write_success = master._write(load)
            master.disconnect()
            time.sleep(0.5)

            # try found pair ------
            for index, slave in enumerate(instances_free_remain):
                read_lines = slave.read_lines(_timeout=2)
                if read_lines:
                    if read_lines[-1] == load or list(read_lines)[-1] == load:
                        result.append((master._conn.port, slave._conn.port))
                        instances_free_remain.pop(index)
                        slave.disconnect()
                        break

        # disconnect all remain ---------
        for remain in instances_free_remain:
            remain.disconnect()

        SerialClient2.ADDRESSES__PAIRED = result
        print(f"{SerialClient2.ADDRESSES__PAIRED=}")
        return result

    # COUNTS -----------------------------------------
    @classmethod
    def ___addresses_shorted__count(cls) -> int:
        return len(cls.addresses_shorted__detect())

    @classmethod
    def ___addresses_paired__count(cls) -> int:
        return len(cls.addresses_paired__detect())

    @classmethod
    def ___addresses_free__count(cls) -> int:
        return len(cls.ADDRESSES__FREE)
    # AUTODETECT ------------------------------------------------------------------------------------------------------
    pass  # dont move this all to CLASSMETHOD!!!

    def address_get__first_free(self) -> str | None:
        result = None
        for address in self.ADDRESSES__FREE:
            if self.connect(address=address, _raise=False):
                result = address

            self.disconnect()
            if result:
                break

        msg = f"[{result=}]_address_apply__first_free"
        if result:
            self.LOGGER.info(msg)
        else:
            self.LOGGER.warning(msg)

        return result

    def address_get__first_free__shorted(self) -> str | None:
        """
        dont overwrite! dont mess with address__autodetect_logic!
        used to find exact device in all comport by some special logic like IDN/NAME value
        """
        result = None
        for address in self.addresses_shorted__detect():
            if self.address_check__occupied(address):
                continue

            if self.connect(address=address, _raise=False):
                result = address

            self.disconnect()
            if result:
                break

        msg = f"[{result=}]_address_apply__first_free__shorted"
        if result:
            self.LOGGER.info(msg)
        else:
            self.LOGGER.warning(msg)

        return result

    def address_get__first_free__valid(self) -> str | None:
        """
        dont overwrite! dont mess with address__autodetect_logic!
        used to find exact device in all comport by some special logic like IDN/NAME value
        """
        result = None
        for address in self.ADDRESSES__FREE:
            if self.connect(address=address, _raise=False):
                try:
                    if self.address__validate():
                        result = address
                except Exception as exc:
                    print(f"finding address {exc!r}")
                    pass

                self.disconnect()
                if result:
                    break

        msg = f"[{result=}]_address_apply__first_free__answer_valid"
        if result:
            self.LOGGER.info(msg)
        else:
            self.LOGGER.warning(msg)

        return result

    def address_get__first_free__paired(self) -> str | None:
        """
        connect only for first address!
        need for occupy addresses by several servers before starting main process!!!
        in case of any address we could occupy by two servers whole pair!

        secondary address you should get by special methods for pair or by address_validating

        cls.pairs = {
            0: (COM1, COM2),
            1: (COM3, COM4),
        }

        cls.pairs = {
            "ATC": (COM1, COM2),    # change name
            1: (COM3, COM4),
        }
        """
        result = None
        for address, _ in self.addresses_paired__detect():
            if self.connect(address=address, _raise=False):
                result = address

            self.disconnect()
            if result:
                break

        # FINISH -------------
        msg = f"[{result=}]address_get__first_free__paired"
        if result:
            self.LOGGER.info(msg)
        else:
            self.LOGGER.warning(msg)

        return result

    # VALIDATION ------------------------------------------------------------------------------------------------------
    def _address__validate_shorted(self) -> bool | None:
        """
        this is the internal method! for autodetect shorted address
        """
        load = "FIND__SHORTED"
        return self.write_read__last_validate(load, load)

    # =================================================================================================================
    @classmethod
    def addresses_dump__answers(cls, *cmds: str | Any) -> dict[str, dict[str, str]]:
        """
        GOAL
        ----
        get several answers from all ports
        for further decisions

        SPECIALLY CREATED FOR
        ---------------------
        quick detecting devices on testplans

        NOTE
        ----
        basically used common requests
        """
        cmds = [*map(str, cmds)]

        # THREADS ---------
        threads = {}
        for address in cls.ADDRESSES__FREE:

            obj = cls()
            obj.baudrate = cls.BAUDRATE
            obj.timeout = cls.TIMEOUT__READ
            obj.REWRITEIF_READNOANSWER = 0
            obj.REWRITEIF_READFAILDECODE = 1
            obj.REWRITEIF_NOVALID = 0

            lambda_list = LambdaListThread([
                Lambda(obj.connect, address),
                *[Lambda(obj.write_read__last, cmd) for cmd in cmds],
                obj._address__release,
                obj.disconnect,
                ],
            )
            threads.update({address: lambda_list})
            lambda_list.start()

        # RESULTS ---------
        result = {}
        for port, thread in threads.items():
            thread.wait()
            result.update({port: {}})
            for obj in thread.LAMBDAS:
                if obj.ARGS and obj.ARGS[0] in cmds:
                    result[port].update({obj.ARGS[0]: obj.RESULT})

        return result

    # RW ==============================================================================================================
    pass
    pass
    pass
    pass
    pass
    pass
    pass

    # W ---------------------------------------------------------------------------------------------------------------
    def _write(
            self,
            data: Union[AnyStr, list[AnyStr]],
            prefix: Optional[str] = None,
            args: Optional[list] = None,
            kwargs: Optional[dict] = None
    ) -> bool:
        """
        just send data into bus!
        usually we dont need just send without reading! so it useful for debugging

        :return: result of sent

        args/kwargs - used only for single line!!!
        """
        print(f"{self._COUNT_OPEN_EXCEPTIONS=}")

        args = args or []
        kwargs = kwargs or {}

        data = data or ""

        # LIST -----------------------
        if isinstance(data, (list, tuple,)):
            if len(data) > 1:
                for data_i in data:
                    if not self._write(data=data_i, prefix=prefix, args=args, kwargs=kwargs):
                        return False
                return True
            else:
                data = data[0]

        # SINGLE ---------------------
        data = self._create_cmd_line(cmd=data, prefix=prefix, args=args, kwargs=kwargs)
        self.history.add_data__stdin(self._data_ensure__string(data))

        data = self._data_ensure__bytes(data)
        data = self._data_bytes__eol_ensure(data)

        try:
            data_length = self._conn.write(data)
            msg = f"[OK]write={data}/{data_length=}"
        except Exception as exc:
            msg = f"[FAIL]write={data}/{exc!r}"
            self.LOGGER.warning(f"[{self._conn.port}]{msg}")

            if isinstance(exc, (PortNotOpenError, SerialException)):
                self._COUNT_OPEN_EXCEPTIONS += 1
                try:
                    self._conn.open()
                    # self.connect()
                except:
                    return False
                    # raise exc
                # raise exc   # here need reconnection!

            return False

        if data_length > 0:
            self.LOGGER.info(f"[{self._conn.port}]{msg}")
            return True
        else:
            msg = f"[ERROR] write {data}"
            self.LOGGER.error(f"[{self._conn.port}]{msg}")
            return False



    def write_read(
            self,
            data: Union[AnyStr, list[AnyStr]],
            prefix: Optional[str] = None,
            args: Optional[list] = None,
            kwargs: Optional[dict] = None,

            retry_noanswer: int | None = None,
            _timeout: Optional[float] = None,
    ) -> Union[CmdHistory_Sync, NoReturn]:
        """
        send data and return history

        CAREFUL
        -------
        in this case you can get incorrect but printable chars!!!
        DONT USE! IF WANT TO BE SURE!
        instead use write_read__last_validate!!! it would rewrite data if not valid answer (even with incorrect but good decoding)!!!
        """
        history = CmdHistory_Sync()
        if retry_noanswer is None:
            retry_noanswer = self.REWRITEIF_READNOANSWER
        remain__retry_noanswer = retry_noanswer or 0

        # LIST -------------------------
        if isinstance(data, (list, tuple,)):
            for data_i in data:
                history_i = self.write_read(data_i, prefix=prefix, args=args, kwargs=kwargs,
                                            retry_noanswer=retry_noanswer)
                history._add_history(history_i)
        else:
            # SINGLE LAST -----------------------
            data_o = []
            remain__retry_decode = self.REWRITEIF_READFAILDECODE or 0
            while remain__retry_decode >= 0 and remain__retry_noanswer >= 0:
                # if self._COUNT_OPEN_EXCEPTIONS > 0:
                #     return

                if self._write(data=data, prefix=prefix, args=args, kwargs=kwargs):
                    try:
                        data_o = self.read_lines(_timeout=_timeout)
                        if data_o:  # here are validated string data!   # NEED ALWAYS GET ANYTHING IN RESPONSE
                            break
                        else:
                            remain__retry_noanswer -= 1

                    except Exc_SerialRead_FailDecoding:
                        remain__retry_decode -= 1

                    self.buffers_clear()
            history.add_data__stdioe(self._data_ensure__string(data), data_o)

        # RESULT ----------------------------
        return history

    def write_read__last(
            self,
            data: Union[AnyStr, list[AnyStr]],
            prefix: Optional[str] = None,
            args: Optional[list] = None,
            kwargs: Optional[dict] = None,

            retry_noanswer: int | None = None,
            _timeout: Optional[float] = None,
    ) -> Union[str, NoReturn]:
        """
        it is created specially for single cmd usage! but decided leave multy cmd usage as feature.
        return always last_output

        CAREFUL
        -------
        in this case you can get incorrect but printable chars!!!
        DONT USE! IF WANT TO BE SURE!
        instead use write_read__last_validate!!! it would rewrite data if not valid answer (even with incorrect but good decoding)!!!
        """
        return self.write_read(
            data=data,
            prefix=prefix,
            args=args,
            kwargs=kwargs,
            retry_noanswer=retry_noanswer,
            _timeout=_timeout,
        ).last_stdout_line

    # =================================================================================================================
    def test__shorted(self):
        if not self.connect():
            msg = f"[ERROR] not found PORT shorted by Rx+Tx"
            print(msg)
            raise Exception(msg)

        # START WORKING ------------------
        index = 0
        while True:
            index += 1
            load = f"step{index}"
            print(load)
            assert self.write_read__last(load) == load


# =====================================================================================================================
def _explore():
    class Dev(SerialClient2):
        pass
        BAUDRATE = 115200
        EOL__SEND = b"\n"

    result = Dev.addresses_dump__answers("*:get name", "*:get addr")

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
