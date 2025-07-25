from typing import *

import re
import sys
import glob
import time
import string
from enum import Enum, auto

from base_aux.loggers.m2_logger import Logger

from serial import Serial, PortNotOpenError, SerialException
from serial.tools import list_ports
from base_aux.base_values.m5_value_valid3_unit import *
from base_aux.aux_eq.m2_eq_aux import EqAux
from base_aux.base_lambdas.m3_lambda4_list import *

from base_aux.buses.m0_history import HistoryIO


# =====================================================================================================================
class Exx_SerialAddress_NotApplyed(Exception):
    """
        raise SerialException("Port must be configured before it can be used.")
    serial.serialutil.SerialException: Port must be configured before it can be used.
    """
    pass


class Exx_SerialAddress_NotExists(Exception):
    """
    SerialException("could not open port 'COM6': FileNotFoundError(2, 'Не удается найти указанный файл.', None, 2)") - всегда несуществующий порт в Windows!!!
    """
    pass


class Exx_SerialAddresses_NoVacant(Exception):
    pass


class Exx_SerialAddresses_NoAutodetected(Exception):
    pass


class Exx_SerialAddress_AlreadyOpened(Exception):
    """
    SerialException("could not open port 'COM7': PermissionError(13, 'Отказано в доступе.', None, 5)")
    """
    pass


class Exx_SerialAddress_AlreadyOpened_InOtherObject(Exception):
    """
    SerialException("could not open port 'COM7': PermissionError(13, 'Отказано в доступе.', None, 5)")
    """
    pass


class Exx_SerialAddress_OtherError(Exception):
    """
    SerialException("could not open port 'COM7': OSError(22, 'Указано несуществующее устройство.', None, 433)") - порт есть, но получена ошибка при открытии!!!
    """
    pass


class Exx_SerialRead_NotFullLine(Exception):
    pass


class Exx_SerialRead_FailPattern(Exception):
    """
    if read string which match error pattern
    """
    pass


class Exx_SerialRead_FailDecoding(Exception):
    """
    REASON
    ------
    some serial devices (depends on microchips model) not always give correct reading bytes

    SOLVATION
    ---------
    1. [BESTandONLY] just use other device on other appropriate microchip!
    """


class Exx_SerialPL2303IncorrectDriver(Exception):
    """
    REASON
    ------
    typical for windows

    SOLVATION
    ---------
    1. [BEST] just use other device on other microchip
    2. manually select other more OLD driver in driver/device manager
        version 3.3.2.105/27.10.2008 - is good!
        version 3.8.22.0/22.02.2023 - is not good!!!
    """
    MARKER: str = "PL2303HXA PHASED OUT SINCE 2012. PLEASE CONTACT YOUR SUPPLIER"


# =====================================================================================================================
TYPE__RW_ANSWER_SINGLE = Union[None, str, ValueUnit]
TYPE__RW_ANSWER = Union[TYPE__RW_ANSWER_SINGLE, list[TYPE__RW_ANSWER_SINGLE]]


class Enum__WrReturn(Enum):
    ALL_OUTPUT = auto()
    HISTORY_IO = auto()
    DICT = auto()


class Enum__AddressAutoAcceptVariant(Enum):
    NOT_FOUND = auto()
    FIRST_FREE = auto()
    FIRST_FREE__SHORTED = auto()
    FIRST_FREE__PAIRED = auto()
    FIRST_FREE__ANSWER_VALID = auto()


TYPING__ADDRESS = Union[None, Enum__AddressAutoAcceptVariant, str]


# =====================================================================================================================
class SerialClient(Logger):
    """
    GOOD ADAPTERS
    =============
    1. use good COM-port adapters!!!
        some bites may be lost (usually on started byte) or added extra chars (usually to start and end of line)!!!

        DECODING APPROPRIATE MODELS
        ---------------------------
        =WRONG=
        - driver PROFILIC PL2303(pcb SBT5329) - often +wrong driver
        - driver FTDI FT232RL(pcb msc-73lv) - sometimes but less than on Profilic=fail on step 0/11/20/3 3/9/95!!!
        - driver CP2102(pcb MostDense) - fail on step 3392/877/1141/!!! sometimes on step 1715 get SerialTimeoutException

        =GOOD=
        - driver CH340(pcb UsbToTtl) - no one error so far!
        - driver CH341A(pcb AllInOne/big universal) - no one error so far! more then steps about 50 minutes!!! tired of waiting
        - driver CH341A(pcb CH341T_V3) - no one error so far! more then steps about 35 minutes!!! tired of waiting

    CAREFUL
    -------
    IF YOU WANT TO BE SURE with WR methods with not good adapters
    use write_read__last_validate!!! it would rewrite data if not valid answer (even with incorrect but good decoding)!!!
    """
    pass
    pass
    pass

    # LOGGER --------------------------------------------------
    LOG_ENABLE = True

    # SETTINGS ------------------------------------------------
    _ADDRESS: TYPING__ADDRESS = None

    TIMEOUT__READ: float = 0.3  # 0.2 is too short!!! dont touch! in case of reading char by char 0.5 is the best!!! 0.3 is not enough!!!
    # need NONE NOT 0!!! if wait always!!
    BAUDRATE: int = 9600  # 115200

    REWRITEIF_READNOANSWER: int = 1
    REWRITEIF_READFAILDECODE: int = 1
    REWRITEIF_NOVALID: int = 0

    CMDS_DUMP: list[str] = []  # ["IDN", "ADR", "REV", "VIN", ]
    RAISE_CONNECT: bool = True
    RAISE_READ_FAIL_PATTERN: bool = False

    PREFIX: Optional[str] = None

    RELEASE_ON_DISCONNECT: bool | None = None

    # TODO: come up and apply ANSWER_SUCCESS??? may be not need cause of redundant
    ANSWER_SUCCESS: str = "OK"  # case insensitive
    ANSWER_FAIL_PATTERN: Union[str, list[str]] = [r".*FAIL.*", ]  # case insensitive!

    # rare INFRASTRUCTURE -----------------
    ENCODING: str = "utf8"
    EOL__SEND: bytes = b"\r\n"  # "\r"=ENTER in PUTTY  but "\r\n"=is better in read Putty!
    EOL__UNI_SET: bytes = b"\r\n"

    _GETATTR_STARTSWITH__SEND: str = "send__"
    _GETATTR_SPLITTER__ARGS: str = "__"

    # test purpose EMULATOR -----------------
    _EMULATOR__CLS: type[
        'SerialServer_Base'] = None  # IF USED - START it on PAIRED - it is exactly Emulator/Server! no need to use just another serialClient! _EMULATOR__INST could be used for test reason and check values in realtime!!
    _EMULATOR__INST: 'SerialServer_Base' = None
    _EMULATOR__START: bool = None  # DONT DELETE! it need when you reconnecting! cause of address replaced after disconnecting by exact str after PAIRED*

    # AUX -----------------------------------------------------
    history: HistoryIO = None
    _SERIAL: Serial

    ADDRESSES__SYSTEM: dict[str, Union[None, Self]] = {}
    ADDRESSES__SHORTED: list[str] = []
    ADDRESSES__PAIRED: list[tuple[str, str]] = []

    # CMDS -----------------------------------------------------
    CMD__RESET: str = "RST"

    # INIT ============================================================================================================
    pass
    pass
    pass
    pass
    pass
    pass
    pass

    def __init__(self, baudrate: int = None, timeout__read: int = None, eol__send: bytes = None, **kwargs):
        super().__init__(**kwargs)

        if baudrate is not None:
            self.BAUDRATE = baudrate
        if timeout__read is not None:
            self.TIMEOUT__READ = timeout__read
        if eol__send is not None:
            self.EOL__SEND = eol__send

        self.history = HistoryIO()
        self.init_serial()

        # self.addresses_system__detect()   # DONT USE in init!!!
        # self.addresses_shorted__detect()   # DONT USE in init!!!
        # self.addresses_paired__detect()   # DONT USE in init!!!

    def __del__(self):
        self._address__release()
        self.disconnect()

    def init_serial(self):
        """
        GOAL
        ----
        init exact connection  object
        """
        self._SERIAL = Serial()

        # apply settings
        # self._SERIAL.interCharTimeout = 0.8
        self._SERIAL.baudrate = self.BAUDRATE
        self._SERIAL.timeout = self.TIMEOUT__READ
        # self._SERIAL.write_timeout = self._TIMEOUT__WRITE

    def cmd_prefix__set(self) -> None:
        """
        OVERWRITE IF NEED/USED!
        """
        # self.PREFIX = ""
        return

    # CONNECT =========================================================================================================
    pass
    pass
    pass
    pass
    pass
    pass
    pass

    def check__connected(self) -> bool:
        try:
            return self._SERIAL.is_open
        except:
            return False

    def disconnect(self, release: bool = None) -> None:
        """
        for release - its better to use direct cls._addresses__release()
        """
        if release or self.RELEASE_ON_DISCONNECT:
            self._address__release()

        try:
            self._SERIAL.close()
        except:
            pass

        try:
            self._EMULATOR__INST.disconnect()
        except:
            pass

    def connect__only_if_address_resolved(self) -> Union[None, bool, NoReturn]:
        if self.address_check__resolved():
            return self.connect()

    def connect(
            self,
            address: TYPING__ADDRESS | None = None,
            _raise: bool | None = None,
            _touch_connection: bool | None = None
            # no final connection! specially keep ability to connect without Emu on cls main perpose (search ports)!
    ) -> Union[bool, NoReturn]:
        msg = None
        exx = None
        need_open = True

        # SETTINGS ---------------------------------
        if _raise is None:
            _raise = self.RAISE_CONNECT

        if address is None:
            address = self.ADDRESS

        if address in Enum__AddressAutoAcceptVariant:
            if address == Enum__AddressAutoAcceptVariant.NOT_FOUND: # not
                return False

            if not self.address__resolve(address):
                exx = Exx_SerialAddress_NotApplyed()
                need_open = False
            else:
                address = self.ADDRESS

        # need_open ==========================================================
        # CHANGE PORT OR USE SAME ---------------------------------
        if need_open:
            if self._SERIAL.port != address:
                # close old
                if self._SERIAL.is_open:
                    self._SERIAL.close()

                # set new
                self._SERIAL.port = address
                if self._SERIAL.is_open:
                    self._SERIAL.port = None
                    msg = f"[ERROR] Attempt to connect to already opened port IN OTHER OBJECT {self._SERIAL}"
                    exx = Exx_SerialAddress_AlreadyOpened_InOtherObject(msg)

                    need_open = False
            else:
                if self._SERIAL.is_open:
                    need_open = False

        # Try OPEN ===================================================================
        if need_open:
            try:
                self._SERIAL.open()
                # self.write_eol()
                # self.buffers_clear()
            except Exception as _exx:
                if not _touch_connection:
                    self.LOGGER.error(f"[{self._SERIAL.port}]{_exx!r}")

                if "FileNotFoundError" in str(_exx):
                    msg = f"[ERROR] PORT NOT EXISTS IN SYSTEM {self._SERIAL}"
                    exx = Exx_SerialAddress_NotExists(repr(_exx))

                    # self.detect_available_ports()

                elif "Port must be configured before" in str(_exx):
                    msg = f"[ERROR] PORT NOT CONFIGURED {self._SERIAL}"
                    exx = Exx_SerialAddress_NotApplyed(repr(_exx))

                elif "PermissionError" in str(_exx):
                    msg = f"[ERROR] PORT ALREADY OPENED {self._SERIAL}"
                    exx = Exx_SerialAddress_AlreadyOpened(repr(_exx))

                else:
                    msg = f"[ERROR] PORT OTHER ERROR {self._SERIAL}"
                    exx = Exx_SerialAddress_OtherError(repr(_exx))

        # FINISH -----------------------------------------------
        # FAIL -----------------------------
        if exx:
            if not _touch_connection:
                self.LOGGER.error(f"[{self._SERIAL.port}]{msg}")

            if _raise:
                raise exx
            else:
                return False

        # OK -----------------------------
        if not _touch_connection:
            if not self.connect__validate():
                self.disconnect()
                return False

            self._address__occupy(address)
            self.emulator_start()
            self.cmd_prefix__set()

        return True

    def connect__validate(self) -> bool:
        """
        DIFFERENCE
        ----------
        connect validation used always!
        address validation used only in step of detecting address (after execution address would be set to exact string value)
        """
        return True

    def emulator_start(self) -> None:
        if not self._EMULATOR__START:
            return

        if self._EMULATOR__CLS:
            self._EMULATOR__INST = self._EMULATOR__CLS(self.address_paired__get())

        if self._EMULATOR__INST.connect():
            self._EMULATOR__INST.start()
            self._EMULATOR__INST.wait__cycle_active()
            self._buffers_clear__read()

    # ADDRESS =========================================================================================================
    """
    THIS IS USED for applying by SIMPLE WAY just exact address! 
    """
    pass
    pass
    pass
    pass
    pass
    pass
    pass

    @property
    def ADDRESS(self) -> TYPING__ADDRESS:
        return self._ADDRESS

    @ADDRESS.setter
    def ADDRESS(self, value: TYPING__ADDRESS) -> None:
        if value == self.ADDRESS:
            return

        self._address__release()
        # self.disconnect()     # dont place here! incorrect logic!
        self._ADDRESS = value
        self._address__occupy(value)

    @classmethod
    @property
    def ADDRESSES__FREE(cls) -> list[str]:
        cls.addresses_system__detect()
        result = []
        for port_name, port_owner in cls.ADDRESSES__SYSTEM.items():
            if port_owner is None:
                result.append(port_name)
        return result

    # OCCUPATION ------------------------------------------------------------------------------------------------------
    def _address__occupy(self, address: TYPING__ADDRESS | None = None) -> None:
        """
        USAGE
        -----
        usually when start module we have exact and only one set of UartDevices!
        ones we connect exact device - it would occupy the port.
        port must be occupied even if Serial is not open!
        """
        if address is None:
            address = self.ADDRESS

        if address in SerialClient.ADDRESSES__SYSTEM:
            SerialClient.ADDRESSES__SYSTEM[address] = self

        self.LOGGER.info(f"[{self._SERIAL.port}][OK] connected/locked/occupy {self._SERIAL}")

    def _address__release(self) -> None:
        """
        USE ONLY when change address!
        """
        if self in SerialClient.ADDRESSES__SYSTEM.values():
            for address, owner in SerialClient.ADDRESSES__SYSTEM.items():
                if owner is self:
                    SerialClient.ADDRESSES__SYSTEM[address] = None
                    # self.disconnect()
                    break

    @classmethod
    def _addresses__release(cls) -> None:
        """
        make all ports vacant for autodetect.
        use direct Clear() if need reinit items.

        CREATED SPECIALLY FOR
        ---------------------
        test issues (testing this module!)
        when set of tests is finished for one connection schema - release all
        """
        for key in cls.ADDRESSES__SYSTEM:
            cls.ADDRESSES__SYSTEM[key] = None

    def address_forget(self) -> None:
        """
        GOAL
        ----
        get default address for derivatives or else just clear to None.

        SPECIAL CREATED FOR
        -------------------
        testplans module - to drop all devices for manually refind devices

        CONSTRAINTS
        -----------
        be sure to use Base class from Derivatives so method would work correctly (as designed)!
        """
        self.ADDRESS = None

        # CAREFUL ---- here we will get curriculum import!
        # from . import SerialClient_FirstFree, SerialClient_FirstFree_Shorted, SerialClient_FirstFree_Paired, SerialClient_FirstFree_AnswerValid
        # if isinstance(self, SerialClient_FirstFree):
        #     self.ADDRESS = Enum__AddressAutoAcceptVariant.FIRST_FREE
        # elif isinstance(self, SerialClient_FirstFree_Shorted):
        #     self.ADDRESS = Enum__AddressAutoAcceptVariant.FIRST_FREE__SHORTED
        # elif isinstance(self, SerialClient_FirstFree_Paired):
        #     self.ADDRESS = Enum__AddressAutoAcceptVariant.FIRST_FREE__PAIRED
        # elif isinstance(self, SerialClient_FirstFree_AnswerValid):
        #     self.ADDRESS = Enum__AddressAutoAcceptVariant.FIRST_FREE__ANSWER_VALID

    def address__resolve(self, address: TYPING__ADDRESS | None = None) -> bool:
        """
        GOAL
        ----
        resolve address passed as Enum__AddressAutoAcceptVariant
        could be call separately! before connect!

        SPECIALLY CREATED FOR
        ---------------------
        separate address resolve and connect

        NOTE
        ----
        :param address: if result if True - ALWAYS APPLY final value in instance!
        """
        if address is None:
            address = self.ADDRESS

        # RESOLVE ---------------------------------
        if address in Enum__AddressAutoAcceptVariant:
            if address == Enum__AddressAutoAcceptVariant.FIRST_FREE:
                address = self.address_get__first_free()
            elif address == Enum__AddressAutoAcceptVariant.FIRST_FREE__SHORTED:
                address = self.address_get__first_free__shorted()
            elif address == Enum__AddressAutoAcceptVariant.FIRST_FREE__ANSWER_VALID:
                address = self.address_get__first_free__valid()
            elif address == Enum__AddressAutoAcceptVariant.FIRST_FREE__PAIRED:
                address = self.address_get__first_free__paired()

        # APPLY -----------------------------------
        result = isinstance(address, str)
        if result:
            self.ADDRESS = address
        return result

    def address_check__resolved(self, address: TYPING__ADDRESS | None = None) -> bool:
        if address is None:
            address = self.ADDRESS
        return isinstance(address, str)

    def address_check__occupied(self, address: TYPING__ADDRESS | None = None) -> bool:
        if not self.address_check__resolved(address):
            return False

        if address is None:
            address = self.ADDRESS
        owner = self.ADDRESSES__SYSTEM.get(address)
        return owner is not None

    # AUTODETECT ------------------------------------------------------------------------------------------------------
    pass  # dont move this all to CLASSMETHOD!!!

    def address_get__first_free(self) -> str | None:
        result = None
        for address in self.ADDRESSES__FREE:
            if self.connect(address=address, _raise=False, _touch_connection=True):
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

            if self.connect(address=address, _raise=False, _touch_connection=True):
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
            if self.connect(address=address, _raise=False, _touch_connection=True):
                try:
                    if self.address__validate():
                        result = address
                except Exception as exx:
                    print(f"finding address {exx!r}")
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
            if self.connect(address=address, _raise=False, _touch_connection=True):
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
    def address__validate(self) -> bool | None | NoReturn:
        """
        overwrite for you case!
        used to find exact device in all comport by some special logic like IDN/NAME value.

        IDEA:
        1. this func will exec on every accessible address
        2. if this func return True - address would be accepted!
        3. raiseExx/NoReturn - equivalent as False!
        """

    def _address__validate_shorted(self) -> bool | None:
        """
        this is the internal method! for autodetect shorted address
        """
        load = "FIND__SHORTED"
        return self.write_read__last_validate(load, load)

    # DETECT ----------------------------------------------------------------------------------------------------------
    @staticmethod
    def address__check_exists(address: str) -> bool:
        try:
            inst = SerialClient()
            inst.connect(address=address, _raise=True, _touch_connection=True)
            inst.disconnect()
        except Exx_SerialAddress_NotExists:
            return False
        except:
            return False
        return True

    @classmethod
    def addresses_system__detect(cls) -> dict[str, Union[None, Self]]:
        if SerialClient.ADDRESSES__SYSTEM:
            return SerialClient.ADDRESSES__SYSTEM

        # WORK -------------------------------------------------------
        result = cls._addresses_system__detect_1__standard_method()
        for port in cls._addresses_system__detect_2__direct_access():
            if port not in result:
                result.append(port)

        # result -------------------------------------------------------
        if result:
            print(f"[OK] detected serial ports {result}")
        else:
            print("[WARN] detected no serial ports")

        SerialClient.ADDRESSES__SYSTEM.clear()
        SerialClient.ADDRESSES__SYSTEM.update(**dict.fromkeys(result, None))
        return SerialClient.ADDRESSES__SYSTEM

    @staticmethod
    def _addresses_system__detect_1__standard_method() -> Union[list[str], NoReturn]:
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
            ----------properties_exx----------------------------------------------------------------------------
            ----------base_types-----------------------------------------------------------------------------------
            ----------methods_ok--------------------------------------------------------------------------------
            apply_usb_info           	NoneType  :None
            usb_description          	str       :COM8
            usb_info                 	str       :USB VID:PID=067B:2303 SER= LOCATION=1-2.4.3
            ----------methods_exx-------------------------------------------------------------------------------
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
            ----------properties_exx----------------------------------------------------------------------------
            ----------base_types-----------------------------------------------------------------------------------
            ----------methods_ok--------------------------------------------------------------------------------
            apply_usb_info                  NoneType  :None
            usb_description                 str       :USB-Serial Controller
            usb_info                        str       :USB VID:PID=067B:2303 LOCATION=1-1.4
            ----------methods_exx-------------------------------------------------------------------------------
            read_line                       TypeError :join() missing 1 required positional argument: 'a'
            ====================================================================================================
        """
        result: list[str] = []

        # find not opened ports ----------------------------------------
        for obj in list_ports.comports():
            # ObjectInfo(obj).print(hide_skipped=True, skip__build_in=True)
            result.append(obj.device)
            if Exx_SerialPL2303IncorrectDriver.MARKER in str(obj):
                msg = f'[WARN] incorrect driver [{Exx_SerialPL2303IncorrectDriver.MARKER}]'
                raise Exx_SerialPL2303IncorrectDriver(msg)
        return result

    @staticmethod
    def _addresses_system__detect_2__direct_access() -> Union[list[str], NoReturn]:
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
            if SerialClient.address__check_exists(address=name):
                result.append(name)

        return result

    @classmethod
    def addresses_shorted__detect(cls) -> list[str]:
        if SerialClient.ADDRESSES__SHORTED:
            return SerialClient.ADDRESSES__SHORTED

        # WORK ----------------------------------------------
        result = []
        for address in cls.addresses_system__detect():
            obj = SerialClient()
            if obj.connect(address=address, _raise=False, _touch_connection=True):
                if obj._address__validate_shorted():
                    result.append(address)
                obj.disconnect()

        SerialClient.ADDRESSES__SHORTED = result
        print(f"{SerialClient.ADDRESSES__SHORTED=}")
        return result

    @classmethod
    def addresses_paired__detect(cls) -> list[tuple[str, str]]:
        # FIXME: IT SEEMS NOT WORKING!!!
        if cls.addresses_system__count() < 2:
            return []

        if SerialClient.ADDRESSES__PAIRED:
            return SerialClient.ADDRESSES__PAIRED

        # WORK ----------------------------------------------
        load = "EXPECT_ANSWER__PAIRED"
        result = []
        instances_free_remain = []

        system_ports = cls.addresses_system__detect()

        # CONNECT ALL -----
        for address in system_ports:
            instance = SerialClient()
            if instance.connect(address=address, _raise=False, _touch_connection=True):
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
                        result.append((master._SERIAL.port, slave._SERIAL.port))
                        instances_free_remain.pop(index)
                        slave.disconnect()
                        break

        # disconnect all remain ---------
        for remain in instances_free_remain:
            remain.disconnect()

        SerialClient.ADDRESSES__PAIRED = result
        print(f"{SerialClient.ADDRESSES__PAIRED=}")
        return result

    def addresses_paired__get_used(self) -> Optional[tuple[str, str]]:
        for pair in self.addresses_paired__detect():
            if self._SERIAL.port in pair:
                return pair

    def address_paired__get(self) -> str | None:
        if not SerialClient.ADDRESSES__PAIRED:
            SerialClient.addresses_paired__detect()

        if not self.address_check__resolved():
            return

        for pair in SerialClient.ADDRESSES__PAIRED:
            if self.ADDRESS in pair:
                addr1, addr2 = pair
                if self.ADDRESS == addr1:
                    return addr2
                else:
                    return addr1

    # COUNTS -----------------------------------------
    @classmethod
    def addresses_system__count(cls) -> int:
        return len(cls.addresses_system__detect())

    @classmethod
    def addresses_shorted__count(cls) -> int:
        return len(cls.addresses_shorted__detect())

    @classmethod
    def addresses_paired__count(cls) -> int:
        return len(cls.addresses_paired__detect())

    @classmethod
    def addresses_free__count(cls) -> int:
        return len(cls.ADDRESSES__FREE)

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
                Lambda(obj.connect, address, _touch_connection=True),
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

    # BUFFERS ---------------------------------------------------------------------------------------------------------
    def _buffers_clear__read(self, _timeout: Optional[float] = None) -> None:
        self._SERIAL.timeout = _timeout or self.TIMEOUT__READ or None
        while True:
            try:
                if not self._SERIAL.readline(1):
                    break
            except:
                pass
            time.sleep(0.1)

        self._SERIAL.timeout = self.TIMEOUT__READ or None  # set back - final

    def _buffers_clear__write(self) -> None:
        """useful to drop old previous incorrect send msg! in other words it is clear/reinit write buffer!

        here we need just finish line by correct/exact EOL if it was previously send without it or with incorrect.
        """
        try:
            self.write_eol()
        except:
            pass

    def buffers_clear(self) -> None:
        """useful to drop old previous incorrect send msg! in other words it is clear/reinit write buffer!

        here we need just finish line by correct/exact EOL if it was previously send without it or with incorrect.
        """
        self._buffers_clear__write()
        self._buffers_clear__read()

    # CMD -------------------------------------------------------------------------------------------------------------
    def _create_cmd_line(self, cmd: str, prefix: Optional[str] = None, args: list[Any] = None,
                         kwargs: dict[Any, Any] = None) -> str:
        result = ""

        cmd = self._data_ensure__string(cmd)
        cmd = self._data_eol__clear(cmd)

        if prefix is None:
            prefix = self.PREFIX or ""

        if prefix and not cmd.startswith(prefix):
            result += f"{prefix}"

        result += f"{cmd}"

        if args:
            for arg in args:
                result += f" {arg}"

        if kwargs:
            for key, value in kwargs.items():
                result += f" {key}={value}"
        return result

    # SUCCESS ---------------------------------------------------------------------------------------------------------
    def answer_is_success(self, data: AnyStr) -> bool:
        data = self._data_ensure__string(data)
        return self.ANSWER_SUCCESS.upper() == data.upper()

    def answer_is_fail(self, data: AnyStr, _raise: Optional[bool] = None) -> Union[bool, NoReturn]:
        if _raise is None:
            _raise = self.RAISE_READ_FAIL_PATTERN

        data = self._data_ensure__string(data)
        if isinstance(self.ANSWER_FAIL_PATTERN, str):
            patterns = [self.ANSWER_FAIL_PATTERN, ]
        else:
            patterns = self.ANSWER_FAIL_PATTERN

        for pattern in patterns:
            if re.search(pattern, data, flags=re.IGNORECASE):
                if _raise:
                    msg = f"[ERROR] match fail [{pattern=}/{data=}]"
                    self.LOGGER.error(f"[{self._SERIAL.port}]{msg}")
                    raise Exx_SerialRead_FailPattern(msg)
                else:
                    return True

        return False

    # BYTES -----------------------------------------------------------------------------------------------------------
    @classmethod
    def _bytes_eol__ensure(cls, data: bytes) -> Union[bytes, NoReturn]:
        data = cls._data_eol__clear(data) + cls.EOL__SEND
        return data

    @classmethod
    def _data_eol__clear(cls, data: AnyStr) -> Union[AnyStr, NoReturn]:
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

    @classmethod
    def _bytes_edition__apply(cls, data: bytes) -> bytes:
        """not used so far!!!
        need to handle editions used by hand in manual typing from terminal!
        """
        # TODO: finish or leave blank! its not so necessary!!! and seems a little bit hard to apply
        return data

    # BYTES/STR -------------------------------------------------------------------------------------------------------
    @classmethod
    def _data_ensure__bytes(cls, data: AnyStr) -> bytes:
        if isinstance(data, bytes):
            return data
        else:
            return bytes(data, encoding=cls.ENCODING)

    @classmethod
    def _data_ensure__string(cls, data: AnyStr) -> Union[str, NoReturn]:
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
        # TODO: move to sepaarted module!
        try:
            if isinstance(data, bytes):
                result = data.decode(encoding=cls.ENCODING)
            else:
                result = str(data)
        except Exception as exx:
            print(f"{exx!r}")
            msg = f"[FAIL] decoding {data=}"
            raise Exx_SerialRead_FailDecoding(msg)

        # check printable ascii ------------------
        for char in result:
            if isinstance(char, bytes):
                char = chr(char)
            if char not in string.printable:
                msg = f"[FAIL] decoding [{char=}]"
                raise Exx_SerialRead_FailDecoding(msg)
        # ----------------------------------------

        return result

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
        # FIXME: return Object??? need keep exx for not finished readline!!!
        # var1: just read as usual - could cause error with not full bytes read in ONE CHAR!!!
        # data = self._SERIAL.readline()

        # var2: char by char
        data = b""
        eol_received = False

        self._SERIAL.timeout = _timeout or self.TIMEOUT__READ or None
        while True:
            new_char = None
            for i in range(2):
                new_char = self._SERIAL.readline(1)
                self._SERIAL.timeout = self.TIMEOUT__READ or None  # set back - no need repiatiting
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

        self._SERIAL.timeout = self.TIMEOUT__READ or None  # set back - final

        # RESULT ----------------------
        if data:
            if not eol_received:
                msg = f"[ERROR]NotFullLine read_line={data}->CLEAR!!!"
                exx = Exx_SerialRead_NotFullLine(msg)
                data = b""
            else:
                msg = f"[OK]read_line={data}"

        else:
            msg = f"[WARN]BLANK read_line={data}"

        self.LOGGER.info(f"[{self._SERIAL.port}.{self._SERIAL.baudrate}]{msg}")

        data = self._bytes_edition__apply(data)
        data = self._data_eol__clear(data)
        data = self._data_ensure__string(data)
        self.history.add_output(data)
        self.answer_is_fail(data)

        # NOTE: dont delete! need to direct cmp
        try:
            # pass
            data = ValueUnit_NoMulty(data)
        except:
            pass

        return data

    # W ---------------------------------------------------------------------------------------------------------------
    _COUNT_OPEN_EXCEPTIONS: int = 0  # this is just for testing/log meanings

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
        self.history.add_input(self._data_ensure__string(data))

        data = self._data_ensure__bytes(data)
        data = self._bytes_eol__ensure(data)

        try:
            data_length = self._SERIAL.write(data)
            msg = f"[OK]write={data}/{data_length=}"
        except Exception as exx:
            msg = f"[FAIL]write={data}/{exx!r}"
            self.LOGGER.warning(f"[{self._SERIAL.port}]{msg}")

            if isinstance(exx, (PortNotOpenError, SerialException)):
                self._COUNT_OPEN_EXCEPTIONS += 1
                try:
                    self._SERIAL.open()
                    # self.connect()
                except:
                    return False
                    # raise exx
                # raise exx   # here need reconnection!

            return False

        if data_length > 0:
            self.LOGGER.info(f"[{self._SERIAL.port}]{msg}")
            return True
        else:
            msg = f"[ERROR] write {data}"
            self.LOGGER.error(f"[{self._SERIAL.port}]{msg}")
            return False

    def write_eol(self, eol: bytes = None) -> bool:
        """
        write without any conditions (no prefixes! no suffixes)!
        GOAL
        ----
        finish any writen cmd and clear buffer
        """
        eol = eol or self.EOL__SEND
        try:
            return bool(self._SERIAL.write(eol))
        except:
            return False

    def write_read(
            self,
            data: Union[AnyStr, list[AnyStr]],
            prefix: Optional[str] = None,
            args: Optional[list] = None,
            kwargs: Optional[dict] = None,

            retry_noanswer: int | None = None,
            _timeout: Optional[float] = None,
    ) -> Union[HistoryIO, NoReturn]:
        """
        send data and return history

        CAREFUL
        -------
        in this case you can get incorrect but printable chars!!!
        DONT USE! IF WANT TO BE SURE!
        instead use write_read__last_validate!!! it would rewrite data if not valid answer (even with incorrect but good decoding)!!!
        """
        history = HistoryIO()
        if retry_noanswer is None:
            retry_noanswer = self.REWRITEIF_READNOANSWER
        remain__retry_noanswer = retry_noanswer or 0

        # LIST -------------------------
        if isinstance(data, (list, tuple,)):
            for data_i in data:
                history_i = self.write_read(data_i, prefix=prefix, args=args, kwargs=kwargs,
                                            retry_noanswer=retry_noanswer)
                history.add_history(history_i)
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

                    except Exx_SerialRead_FailDecoding:
                        remain__retry_decode -= 1

                    self.buffers_clear()
            history.add_io(self._data_ensure__string(data), data_o)

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
        ).last_output

    def write_read__last_validate(
            self,
            input: Union[str, list[str]] | None,
            expect: Union[Any, list[Any]],
            prefix: Optional[str] = None,
            args: Optional[list] = None,
            kwargs: Optional[dict] = None,

            retry_novalid: int | None = None,
            _timeout: Optional[float] = None,
            _as_regexp: Optional[bool] = None,
    ) -> bool:
        """
        CREATED SPECIALLY FOR
        ---------------------
        1. address__validate

        SOLVE PROBLEMS
        --------------
        communicate with wrong working devices!

        :param expect: can be Any! even Valid/ValueUbit/ValueVariants as validation object!
        """
        if retry_novalid is None:
            retry_novalid = self.REWRITEIF_NOVALID or 0

        if isinstance(expect, (tuple, list, set, dict)):
            expect_list = expect
        else:
            expect_list = [expect, ]

        while retry_novalid >= 0:
            if input:
                output_last = self.write_read__last(
                    data=input,
                    prefix=prefix,
                    args=args,
                    kwargs=kwargs,
                    retry_noanswer=0,  # use only retry_noanswer=0! so it would not multiplyed iterations
                    _timeout=_timeout,
                )
            else:
                outputs = self.read_lines(_timeout=_timeout)
                if outputs:
                    output_last = outputs[-1]
                else:
                    output_last = ""

            for expect_var in expect_list:
                if _as_regexp:
                    if re.fullmatch(expect_var, str(output_last), flags=re.IGNORECASE):
                        return True
                else:
                    if (
                            str(output_last).lower() == str(expect_var).lower()
                            or
                            EqAux(output_last).check_doubleside__bool(expect_var)
                    ):
                        return True

            retry_novalid -= 1
            print(f"{retry_novalid=}")

        return False

    def write_read__last_validate_regexp(self, *args, **kwargs) -> bool:
        """
        created specially for address__validate
        """
        return self.write_read__last_validate(*args, **kwargs, _as_regexp=True)

    def dump_cmds(self, cmds: list[str] = None) -> Union[HistoryIO, NoReturn]:
        """
        useful to get results for standard cmds list
        if you need to read all params from device!
        """
        cmds = cmds or self.CMDS_DUMP
        history = self.write_read(cmds)
        history.print_io()
        return history

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

    # =================================================================================================================
    def __getattr__(self, item: str) -> Callable[..., Union[str, NoReturn]]:
        """if no exists attr/meth

        USAGE COMMANDS MAP
        ==================

        1. SHOW (optional) COMMANDS EXPLICITLY by annotations without values!
        -----------------------------------------------------------------
            class MySerialDevice(SerialClient):
                IDN: Callable[[Any], TYPE__RW_ANSWER]
                ADDR: Callable[[Any], TYPE__RW_ANSWER]
                DUMP: Callable[[Any], TYPE__RW_ANSWER]

        2. USE in code
        --------------
            dev = MySerialDevice()
            dev.connect()
            dev.IDN()       --> dev.write_read__last("IDN")
            dev.VIN()       # dev.write_read__last("VIN")
            dev.VIN(12)     # dev.write_read__last("VIN 12")
            dev.VIN("12")   # dev.write_read__last("VIN 12")
            dev.VIN("12 13")  # dev.write_read__last("VIN 12 13")
            dev.VIN(12, 13)   # dev.write_read__last("VIN 12 13")
            dev.VIN(CH1=12, CH2=13) # dev.write_read__last("VIN CH1=12 CH2=13")
            dev.VIN(12, CH2=13)     # dev.write_read__last("VIN 12 CH2=13") by args/kwargs

            # ALL VARIANTS
            dev.VIN(11, CH2=13)
            dev.VIN__11(22, CH2=13)
            dev.send__VIN(11, CH2=13)
            dev.send__VIN__11(22, CH2=13)

            # KWARGS for WriteRead method
            dev.TEST("HELLO", CH2=13, __timeout=5) --> dev.write_read__last("TEST CH2=13", _timeout=5) # note underscore

        """
        item_args = []  # args in getattr name

        # 1=apply _GETATTR_STARTSWITH__SEND
        if self._GETATTR_STARTSWITH__SEND and item.startswith(self._GETATTR_STARTSWITH__SEND):
            item = item.replace(self._GETATTR_STARTSWITH__SEND, "")

        # 2=apply args in getattrs name
        if "__" in item:
            item_splited = item.split(self._GETATTR_SPLITTER__ARGS)
            item = item_splited[0]
            item_args = item_splited[1:]

        # 3=separate cmd/meth kwargs
        # cand to it in here!

        # 4=apply direct cmd
        result = lambda *_args, **_kwargs: self.write_read__last(
            data=self._create_cmd_line(
                cmd=item,
                args=[*item_args, *_args],
                kwargs={k: v for k, v in _kwargs.items() if not k.startswith("_")}
            ),
            **{k[1:]: v for k, v in _kwargs.items() if k.startswith("_")}
        )
        return result

    # =================================================================================================================
    # USER COMMANDS
    # -----------------------------------------------------------------------------------------------------------------
    def reset(self, sleep_after: float = 1) -> None:
        if self.connect__only_if_address_resolved():
            self.write_read(self.CMD__RESET)
            self._buffers_clear__read(sleep_after)
        pass


# =====================================================================================================================
def _explore():
    class Dev(SerialClient):
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
