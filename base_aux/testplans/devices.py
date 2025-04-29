from typing import *
import uuid

from base_aux.testplans import *
from base_aux.breeders.m2_breeder_objects import *
from base_aux.buses.m1_serial1_client import *

from .tc import Base_TestCase
from .models import *


# =====================================================================================================================
class Base_Device:
    # AUX -------------------------------------------------------------------------------------------------------------
    NAME: str = None
    DESCRIPTION: str = None
    INDEX: int = None

    # PROPERTIES ------------------------------------------------------------------------------------------------------
    DEV_FOUND: bool | None = None

    __sn: str = None
    __fw: str = None
    __model: str = None

    # TODO: LOAD INFO!!! ON CONNECTION/DETECTION!!!
    # TODO: LOAD INFO!!! ON CONNECTION/DETECTION!!!
    # TODO: LOAD INFO!!! ON CONNECTION/DETECTION!!!
    # TODO: LOAD INFO!!! ON CONNECTION/DETECTION!!!
    # TODO: LOAD INFO!!! ON CONNECTION/DETECTION!!!
    # TODO: LOAD INFO!!! ON CONNECTION/DETECTION!!!
    # TODO: LOAD INFO!!! ON CONNECTION/DETECTION!!!

    def get__SN(self) -> str:  # OVERWRITE!
        pass

    def get__FW(self) -> str:  # OVERWRITE!
        pass

    def get__MODEL(self) -> str:  # OVERWRITE!
        pass

    @property
    def SN(self) -> str:
        if not self.__sn:
            self.__sn = self.get__SN()
        return self.__sn

    @property
    def FW(self) -> str:
        if not self.__fw:
            self.__fw = self.get__FW()
        return self.__fw

    @property
    def MODEL(self) -> str:
        if not self.__model:
            self.__model = self.get__MODEL()
        return self.__model

    # DUT -------------------------------------------------------------------------------------------------------------
    SKIP: Optional[bool] = None

    def SKIP_reverse(self) -> None:
        """
        this is only for testing purpose
        """
        self.SKIP = not bool(self.SKIP)

    __dut_sn: str = None
    __dut_fw: str = None
    __dut_model: str = None

    def get__DUT_SN(self) -> str:  # OVERWRITE!
        pass

    def get__DUT_FW(self) -> str:  # OVERWRITE!
        pass

    def get__DUT_MODEL(self) -> str:  # OVERWRITE!
        pass

    @property
    def DUT_SN(self) -> str:
        if not self.__dut_sn:
            self.__dut_sn = self.get__DUT_SN()
        return self.__dut_sn

    @property
    def DUT_FW(self) -> str:
        if not self.__dut_fw:
            self.__dut_fw = self.get__DUT_FW()
        return self.__dut_fw

    @property
    def DUT_MODEL(self) -> str:
        if not self.__dut_model:
            self.__dut_model = self.get__DUT_MODEL()
        return self.__dut_model

    # -----------------------------------------------------------------------------------------------------------------
    def __init__(self, index: int = None, **kwargs):
        """
        :param index: None is only for SINGLE!
        """
        if index is not None:
            self.INDEX = index
        super().__init__(**kwargs)

    # CONNECT ---------------------------------------------------------------------------------------------------------
    def connect(self) -> bool:
        return True

    def disconnect(self) -> None:
        pass

    # INFO ------------------------------------------------------------------------------------------------------------
    def get__info__dev(self) -> dict[str, Any]:
        result = {
            "DEV_FOUND": self.DEV_FOUND,
            "INDEX": self.INDEX,

            "NAME": self.NAME or self.__class__.__name__,
            "DESCRIPTION": self.DESCRIPTION or self.__class__.__name__,
            "SN": self.SN or "",
            "FW": self.FW or "",
            "MODEL": self.MODEL or "",
            "SKIP": self.SKIP,
        }
        return result

    # -----------------------------------------------------------------------------------------------------------------
    def _debug__reset_sn(self) -> None:
        """this is only for testing middleware - reset DUT!!!"""
        self.__sn = uuid.uuid4().hex


# =====================================================================================================================
class DevicesBreeder(BreederObjectList):
    def __del__(self):
        self.disconnect__cls()

    @classmethod
    def connect__cls(cls) -> None:
        cls.group_call__("connect")

    @classmethod
    def disconnect__cls(cls) -> None:
        cls.group_call__("disconnect")

    # -----------------------------------------------------------------------------------------------------------------
    @classmethod
    def resolve_addresses__cls(cls) -> None:
        pass
        #
        # class Dev(SerialClient):
        #     pass
        #     BAUDRATE = 115200
        #     EOL__SEND = b"\n"
        #
        # for i in range(3):
        #     result = Dev.addresses_dump__answers("*:get name", "*:get addr")
        #     for port, responses in result.items():
        #         print(port, responses)
        #
        # # TODO: FINISH!!!

    # DEBUG PURPOSE ---------------------------------------------------------------------------------------------------
    @classmethod
    def _debug__duts__reset_sn(cls) -> None:
        cls.group_call__("_debug__reset_sn", "DUT")


# =====================================================================================================================
class DevicesBreeder_WithDut(DevicesBreeder):
    """
    READY TO USE WITH DUT
    """
    # DEFINITIONS ---------------
    CLS_LIST__DUT: type[Base_Device] = Base_Device

    # JUST SHOW NAMES -----------
    LIST__DUT: list[Base_Device]
    DUT: Base_Device


# =====================================================================================================================
class _DevicesBreeder_Example(DevicesBreeder_WithDut):
    """
    JUST an example DUT+some other single dev
    """
    # DEFINITIONS ---------------
    COUNT: int = 2
    CLS_SINGLE__ATC: type[Base_Device] = Base_Device

    # JUST SHOW NAMES -----------
    ATC: Base_Device


# =====================================================================================================================
