from typing import *
import uuid

from base_aux.testplans import *
from base_aux.breeders.m2_breeder_objects import *

from .tc import TestCaseBase
from .models import *


# =====================================================================================================================
class DeviceBase:
    # AUX -----------------------------------
    conn: Any = None
    INDEX: int = None

    # AUX -----------------------------------
    NAME: str = None
    DESCRIPTION: str = None
    SN: str = None
    DEV_FOUND: bool | None = None

    def __init__(self, index: int = None, **kwargs):
        """
        :param index: None is only for SINGLE!
        """
        if index is not None:
            self.INDEX = index
        super().__init__(**kwargs)

    # CONNECT ---------------------------------
    def connect(self) -> bool:
        if self.conn:
            try:
                return self.conn.connect()
            except:
                return False
        return True

    def disconnect(self) -> None:
        try:
            return self.conn.disconnect()
        except:
            pass

    def get__info__dev(self) -> dict[str, Any]:
        result = {
            "DUT_INDEX": self.INDEX,

            "DUT_NAME": self.NAME or self.__class__.__name__,
            "DUT_DESCRIPTION": self.DESCRIPTION or self.__class__.__name__,
            "DUT_SN": self.SN or "",
        }
        return result


# =====================================================================================================================
class DutBase(DeviceBase):
    SKIP: Optional[bool] = None

    def SKIP_reverse(self) -> None:
        """
        this is only for testing purpose
        """
        self.SKIP = not bool(self.SKIP)

    def _debug__reset_sn(self) -> None:
        """this is only for testing middleware"""
        self.SN = uuid.uuid4().hex


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
    CLS_LIST__DUT: type[DutBase] = DutBase

    # JUST SHOW NAMES -----------
    LIST__DUT: list[DutBase]
    DUT: DutBase


# =====================================================================================================================
class DevicesBreeder_Example(DevicesBreeder_WithDut):
    """
    JUST an example DUT+some other single dev
    """
    # DEFINITIONS ---------------
    COUNT: int = 2
    CLS_SINGLE__ATC: type[DeviceBase] = DeviceBase

    # JUST SHOW NAMES -----------
    ATC: DeviceBase


# =====================================================================================================================
