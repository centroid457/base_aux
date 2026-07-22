from typing import *

import glob
import sys
from serial import Serial, SerialException
from serial.tools import list_ports
from threading import Lock

from base_aux.aux_eq.m3_eq_valid3_derivatives import EqValid_EQ_StrIc
from base_aux.base_values.m3_exceptions import Exc__SerialPL2303IncorrectDriver
from base_aux.buses.d1_serial2_new.m1_serial_client import SerialClient2, TYPING__WR_SCHEMA_VALIDATE


# ======================================================================================================================
class SerialManager:
    __addresses_cached: list[str] = None
    _lock_detect: Lock = Lock()
    SCHEMA_SHORTED: TYPING__WR_SCHEMA_VALIDATE = [("echoTest", "echoTest"), ]

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

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def ADDRESSES_CASHED(self) -> list[str]:
        if self.__addresses_cached is None:
            self.detect__addresses_system()

        return list(self.__addresses_cached)

    def count__addresses_system(self) -> int:
        return len(self.ADDRESSES_CASHED)

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
        # FIXME: separate with os depandant
        try:
            s = Serial(address)
            s.close()
            return True
        except SerialException as e:
            msg = str(e).lower()
            # Признаки того, что порта нет
            if "file not found" in msg or "no such file" in msg or "не удается найти" in msg:
                return False
            # Если порт занят, нет прав, или другая ошибка – считаем, что порт существует
            return True
        except Exception:
            # Любая другая неожиданная ошибка – считаем, что порта нет (безопаснее)
            return False

    # GEN ==============================================================================================================
    def _iter__objects(self, **init_kwargs) -> Iterable[SerialClient2]:
        """
        GOAL
        BASE for fither GENs
        """
        for addr in self.ADDRESSES_CASHED:
            yield SerialClient2(addr, _raise_if_occupied=False, **init_kwargs)

    def make__existed(
            self,
            count: int | None = None,
            **init_kwargs,
    ) -> list[SerialClient2]:
        result = []
        for obj in self._iter__objects(**init_kwargs):
            result.append(obj)
            if len(result) == count:
                break
        return result

    def make__existed__first(
            self,
            **init_kwargs,
    ) -> SerialClient2 | None:
        data = self.make__existed(count=1, **init_kwargs)
        if data:
            return data[0]

    # ------------------------------------------------------------------------------------------------------------------
    def make__not_occupied(
            self,
            count: int | None = None,
            **init_kwargs,
    ) -> list[SerialClient2]:
        result = []
        for obj in self._iter__objects(**init_kwargs):
            if not obj.check__occupied():
                result.append(obj)
                if len(result) == count:
                    break
        return result

    def make__not_occupied__first(
            self,
            **init_kwargs,
    ) -> SerialClient2 | None:
        data = self.make__not_occupied(count=1, **init_kwargs)
        if data:
            return data[0]

    # ------------------------------------------------------------------------------------------------------------------
    def make__not_occupied__validated(
            self,
            schema: TYPING__WR_SCHEMA_VALIDATE,
            count: int | None = None,
            **init_kwargs,
    ) -> list[SerialClient2]:
        result = []
        for obj in self.make__not_occupied(**init_kwargs):
            with obj:
                if obj.validate__wr_schema(schema):
                    result.append(obj)
                    if len(result) == count:
                        break
        return result

    def make__not_occupied__validated_first(
            self,
            schema: TYPING__WR_SCHEMA_VALIDATE,
            **init_kwargs,
    ) -> SerialClient2 | None:
        data = self.make__not_occupied__validated(schema=schema, count=1, **init_kwargs)
        if data:
            return data[0]

    # ------------------------------------------------------------------------------------------------------------------
    def make__not_occupied__shorted(
            self,
            count: int | None = None,
            **init_kwargs,
    ) -> list[SerialClient2]:
        return self.make__not_occupied__validated(schema=self.SCHEMA_SHORTED, count=count, **init_kwargs)

    def make__not_occupied__shorted_first(
            self,
            **init_kwargs,
    ) -> SerialClient2 | None:
        data = self.make__not_occupied__validated(schema=self.SCHEMA_SHORTED, count=1, **init_kwargs)
        if data:
            return data[0]

    # DETECT ===========================================================================================================
    def detect__addresses_system(self) -> list[str]:
        with self._lock_detect:

            # WORK -------------------------------------------------------
            if self.__addresses_cached is None:
                self.__addresses_cached = []

            self.__addresses_cached.clear()
            self.__addresses_cached.extend(self._detect__addresses_system_1__standard_method())
            for name in self._detect__addresses_system_2__direct_access():
                if name not in self.__addresses_cached:
                    self.__addresses_cached.append(name)

            # result -------------------------------------------------------
            if self.ADDRESSES_CASHED:
                print(f"[OK] {self.ADDRESSES_CASHED=}")
            else:
                print("[WARN] detected no serial ports")

            return self.__addresses_cached

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


# ======================================================================================================================
def _explore__shorted():
    victim = SerialManager().ADDRESSES_CASHED
    print(victim)
    victim = SerialManager().make__not_occupied__shorted()
    print(victim)

    return
    schema_validate_ate = [("*HELP", EqValid_EQ_StrIc("UNKN")), ]
    victim = SerialManager().make__not_occupied__validated_first(schema=schema_validate_ate, baudrate=115200, eol=b"\n")
    print(victim)


def _explore_Atc():
    class Ate(SerialClient2):
        pass
        BAUDRATE = 115200
        EOL__SEND = b"\n"

    result = Ate().get__wr_responses()

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


# ======================================================================================================================
if __name__ == "__main__":
    _explore__shorted()
    pass


# ======================================================================================================================
