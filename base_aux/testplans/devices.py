from typing import *
import uuid

from base_aux.testplans import *
from base_aux.buses.m1_serial1_client import *

from base_aux.breeders.m3_table_inst import *

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


# =====================================================================================================================
class DevicesKit(TableKit):
    def __del__(self):
        self.disconnect()

    def connect(self) -> None:
        self("connect")

    def disconnect(self) -> None:
        self("disconnect")

    # -----------------------------------------------------------------------------------------------------------------
    def resolve_addresses(self) -> None:
        """
        GOAL
        ----
        find all devices on Uart ports
        """
        pass


# =====================================================================================================================
