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

    SN: str = None
    FW: str = None
    MODEL: str = None

    # INFO -------------------------------
    def load__INFO(self) -> None:
        pass

    # DUT -------------------------------------------------------------------------------------------------------------
    SKIP: Optional[bool] = None

    DUT_SN: str = None
    DUT_FW: str = None
    DUT_MODEL: str = None

    def SKIP_reverse(self) -> None:
        """
        this is only for testing purpose
        """
        self.SKIP = not bool(self.SKIP)

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
            "SKIP": self.SKIP,

            "NAME": self.NAME or self.__class__.__name__,
            "DESCRIPTION": self.DESCRIPTION or self.__class__.__name__,
            "SN": self.SN or "",
            "FW": self.FW or "",
            "MODEL": self.MODEL or "",

            "DUT_SN": self.DUT_SN or "",
            "DUT_FW": self.DUT_FW or "",
            "DUT_MODEL": self.DUT_MODEL or "",
        }
        return result

    # -----------------------------------------------------------------------------------------------------------------
    def _debug__reset_sn(self) -> None:
        """this is only for testing middleware - reset DUT!!!"""
        self.__sn = uuid.uuid4().hex


# =====================================================================================================================
class DevicesBreeder(BreederObj):
    def __del__(self):
        self.disconnect__cls()

    @classmethod
    def connect__cls(cls) -> None:
        cls.group_call__("connect")

    @classmethod
    def disconnect__cls(cls) -> None:
        try:
            cls.group_call__("disconnect")
        except:
            pass

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
