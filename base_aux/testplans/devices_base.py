from base_aux.buses.m1_serial2_client_derivatives import *

from .models import *


# =====================================================================================================================
class Base_Device:
    NAME: str = None
    DESCRIPTION: str = None
    INDEX: int = None

    # PROPERTIES ------------------------------------------------------------------------------------------------------
    DEV_FOUND: bool | None = None

    SN: str = None
    FW: str = None
    MODEL: str = None

    # DUT --------------------
    SKIP: Optional[bool] = None

    DUT_SN: str = None
    DUT_FW: str = None
    DUT_MODEL: str = None

    # -----------------------------------------------------------------------------------------------------------------
    def __init__(self, index: int = None, **kwargs):
        """
        :param index: None is only for SINGLE! - TRY NOT TO USE IT!!!
        """
        if index is not None:
            self.INDEX = index
        super().__init__(**kwargs)

    # -----------------------------------------------------------------------------------------------------------------
    def SKIP_reverse(self) -> None:
        """
        this is only for testing purpose
        """
        self.SKIP = not bool(self.SKIP)

    # CONNECT ---------------------------------------------------------------------------------------------------------
    def connect(self) -> bool:
        return True

    def disconnect(self) -> None:
        pass

    # INFO ------------------------------------------------------------------------------------------------------------
    def dev__load_info(self) -> None:
        """
        GOAL
        ----
        load all important attrs in object.
        for further identification.

        WHERE
        -----
        useful in connect_validate
        """
        pass

    def dev__get_info(self) -> dict[str, Any]:
        """
        GOAL
        ----
        get already loaded data!
        """
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
class Base__DeviceUart_ETech(SerialClient_FirstFree_AnswerValid, Base_Device):
    """
    GOAL
    ----
    make a dev class for ETech UART devices
    """
    LOG_ENABLE = True
    RAISE_CONNECT = False
    BAUDRATE = 115200
    EOL__SEND = b"\n"

    REWRITEIF_READNOANSWER = 0
    REWRITEIF_NOVALID = 0

    @property
    def PREFIX(self) -> str:
        return f"{self.NAME}:{self.INDEX+1:02d}:"

    def dev__load_info(self) -> None:
        if not self.SN:
            self.SN = self.write_read__last("get SN")
            self.FW = self.write_read__last("get FW")
            self.MODEL = self.write_read__last("get MODEL")

    # DETECT --------------------------------
    @property
    def DEV_FOUND(self) -> bool:
        return self.address_check__resolved()

    # ---------------------------------------
    def connect__validate(self) -> bool:
        result = self.address_check__resolved()  # fixme: is it really need here???

        if result:
            if self.NAME == "PTB":
                self.write_read__last_validate("get prsnt", "1")

            self.dev__load_info()

        return result

    # def address__validate(self) -> bool:  # NO NEED! only for manual!
    #     result = (
    #             self.write_read__last_validate("get name", self.NAME, prefix="*:")
    #             and
    #             self.write_read__last_validate("get addr", EqValid_NumParsedSingle_Success(self.INDEX+1), prefix="*:")
    #             # and
    #             # self.write_read__last_validate("get prsnt", "0")
    #     )
    #     if result:
    #         self.dev__load_info()
    #
    #     return result


# =====================================================================================================================
class Base_DeviceDummy(Base__DeviceUart_ETech):  # IMPORTANT! KEEP Serial FIRST Nesting!
    """
    GOAL
    ----
    use to make final Dummy
    """
    @property
    def DEV_FOUND(self) -> bool:
        return True

    def address__validate(self) -> bool:
        return True

    def connect__validate(self) -> bool:
        return True

    def connect(self, *args, **kwargs) -> bool:
        return True


# =====================================================================================================================
