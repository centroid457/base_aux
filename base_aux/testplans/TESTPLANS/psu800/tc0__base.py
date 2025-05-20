from typing import *

from base_aux.testplans.devices import *
from base_aux.testplans.tc_types import *
from base_aux.testplans.tc import *

from base_aux.valid.m1_aux_valid_lg import *
from base_aux.valid.m2_valid_base import *
from base_aux.valid.m2_valid_base2_derivatives import *
from base_aux.valid.m3_valid_chains import *
from base_aux.aux_values.m1_value_valid_eq import *


# =====================================================================================================================
# class Enum_TcGroup(NestEq_Enum):
#     NONE = None


# =====================================================================================================================
class _Base_TcAtc(Base_TestCase):
    # SETTINGS -------------------------------
    ATC_VOUT: int | None = None

    # INTERNAL AUX ---------------------------
    @classmethod
    @property
    def _EQ_CLS__VALUE(cls) -> str:
        """
        GOAL
        ----
        REDEFINE TO USE AS CMP VALUE
        """
        return f"Atc{cls.ATC_VOUT}"

    # -----------------------------------------------------------------------------------------------------------------
    @classmethod
    def startup__cls__wrapped(cls) -> TYPING__RESULT_W_NORETURN:
        result_chain = ValidChains(
            chains=[
                ValidBreak(not cls.ATC_VOUT),
                Valid(
                    value_link=cls.DEV_LINES.ATC[0].connect__only_if_address_resolved,
                    name="ATC.connect__only_if_address_resolved",
                ),
                Valid(
                    value_link=cls.DEV_LINES.ATC[0].GET,
                    args__value="VSNS1",
                    validate_link=1,
                    name="GET",
                ),
                Valid(
                    value_link=cls.DEV_LINES.ATC[0].GET,
                    args__value="VSNS2",
                    validate_link=1,
                    name="GET",
                ),
                Valid(
                    value_link=cls.DEV_LINES.ATC[0].SET,
                    kwargs__value={"VINPIN": 230, "__timeout": 10},
                    validate_link="OK",
                    name="SET",
                ),
                Valid(
                    value_link=cls.DEV_LINES.ATC[0].SET,
                    kwargs__value={"VOUTPIN": cls.ATC_VOUT, "__timeout": 10},
                    validate_link="OK",
                    name="SET",
                ),
                Valid(
                    value_link=cls.DEV_LINES.ATC[0].SET,
                    kwargs__value={"PWR": "ON"},
                    validate_link="OK",
                    name="SET",
                ),
                ValidSleep(0.5),
                # Valid(
                #     value_link=cls.DEV_LINES.ATC[0].GET,
                #     args__value="VOUT",
                #     validate_link=lambda source: ValidAux.lege(source, cls.ATC_VOUT * 0.9, cls.ATC_VOUT * 1.1),
                #     name="GET+lege",
                # ),
                Valid(
                    value_link=cls.DEV_LINES.ATC[0]._buffers_clear__read,
                    validate_link=lambda value: value is None,
                    name="_buffers_clear__read",
                ),
            ],
        )
        return result_chain

    # -----------------------------------------------------------------------------------------------------------------
    @classmethod
    def teardown__cls__wrapped(cls) -> TYPING__RESULT_W_NORETURN:
        result_chain = ValidChains(
            chains=[
                ValidBreak(not cls.ATC_VOUT),
                Valid(
                    value_link=cls.DEV_LINES.ATC[0].connect__only_if_address_resolved,
                    name="ATC.connect__only_if_address_resolved",
                ),
                Valid(
                    value_link=cls.DEV_LINES.ATC[0].reset,
                    validate_link=lambda value: value is None,
                    name="RESET",
                ),
            ]
        )
        return result_chain


# =====================================================================================================================
class Base_TcAtcPtb(_Base_TcAtc):
    ATC_VOUT: int | None = 0
    PTB_SET_EXTON: bool = False
    PTB_SET_HVON: bool = False
    PTB_SET_PSON: bool = False

    ASYNC = True
    INFO_STR__ADD_ATTRS = ["ATC_VOUT", "PTB_SET_EXTON", "PTB_SET_HVON", "PTB_SET_PSON"]

    _DESCRIPTION = "[base] for testing params in different states"

    # -----------------------------------------------------------------------------------------------------------------
    @classmethod
    @property
    def DESCRIPTION_prefix(cls) -> str:
        result = "["
        result += f"Atc{cls.ATC_VOUT},"
        result += f"Ext{'On' if cls.PTB_SET_EXTON else 'Off'},"
        result += f"Hv{'On' if cls.PTB_SET_HVON else 'Off'},"
        result += f"Ps{'On' if cls.PTB_SET_PSON else 'Off'}"
        result += "]"
        # result += "\n"    # dont use here! use in _DESCR* directly!
        return result

    @classmethod
    @property
    def DESCRIPTION(cls) -> str:
        return cls.DESCRIPTION_prefix + cls._DESCRIPTION

    # -----------------------------------------------------------------------------------------------------------------
    def expect__psu_may_start__hv(self) -> bool:
        """
        show if PSU must run correctly
        """
        return all([150 < self.ATC_VOUT < 260, self.PTB_SET_HVON])

    def expect__psu_may_start__hv_or_ext(self) -> bool:
        """
        show if PSU must run correctly
        """
        return self.expect__psu_may_start__hv() or self.PTB_SET_EXTON

    def expect__psu_started_hv__ok(self) -> bool:
        """
        show if PSU must run correctly
        """
        return all([150 < self.ATC_VOUT < 260, self.PTB_SET_HVON, self.PTB_SET_PSON])

    def expect__psu_started_hv__fail(self) -> bool:
        """
        WHY NOT - USE JUST SIMPLE NOT*
        ------------------------------
        cause i need link!
        """
        return not self.expect__psu_started_hv__ok()

    # -----------------------------------------------------------------------------------------------------------------
    def steps__check_params(self) -> list[Valid]:
        """
        GOAL
        ----
        separate list Valid steps to use in any TC
        :return:
        """
        result = [
                ValidNoCum(
                    value_link=self.DEV_COLUMN.DUT.GET,
                    args__value="VINOK",
                    validate_link=1 if self.expect__psu_may_start__hv() else 0,
                    name="GET",
                ),
                ValidFailContinue(
                    value_link=self.DEV_COLUMN.DUT.GET,
                    args__value="PWOK",
                    validate_link=1 if self.expect__psu_started_hv__ok() else 0,
                    name="GET",
                ),

                # HV ----
                ValidNoCum(
                    value_link=self.DEV_COLUMN.DUT.GET,
                    args__value="VIN",
                    validate_link=EqValid_LeGe_NumParsedSingle(
                        *((210, 230)
                        if self.expect__psu_may_start__hv()
                        else
                        (0, 0.1))
                    ).validate,
                    name="GET+valid diapason",
                ),

                # LV ----
                ValidFailContinue(
                    value_link=self.DEV_COLUMN.DUT.GET,
                    args__value="V12S",
                    validate_link=EqValid_LeGe_NumParsedSingle(
                        *((11, 13)
                        if self.expect__psu_may_start__hv_or_ext()
                        else
                        (0, 0.1))
                    ).validate,
                    name="GET+valid diapason",
                ),
                ValidFailContinue(
                    value_link=self.DEV_COLUMN.DUT.GET,
                    args__value="V12M",
                    validate_link=EqValid_LeGe_NumParsedSingle(
                        *((11, 13)
                        if self.expect__psu_may_start__hv_or_ext() and self.PTB_SET_PSON
                        else
                        (0, 0.1))
                    ).validate,
                    name="GET+valid diapason",
                ),

                # currents ----
                ValidNoCum(
                    value_link=self.DEV_COLUMN.DUT.GET,
                    args__value="IIN",
                    validate_link=EqValid_LeGe_NumParsedSingle(0, 0.1).validate,
                    name="GET+valid diapason",
                ),
                ValidFailContinue(
                    value_link=self.DEV_COLUMN.DUT.GET,
                    args__value="IOUT",
                    validate_link=EqValid_LeGe_NumParsedSingle(0, 0.1).validate,
                    name="GET+valid diapason",
                ),
            ]
        return result

    # -----------------------------------------------------------------------------------------------------------------
    def run__wrapped(self) -> TYPING__RESULT_W_EXX:
        # BY DEFAULT PARAMS WOULD CHECK!!!
        result_chain = ValidChains(
            chains=self.steps__check_params()
        )
        return result_chain

    # =================================================================================================================
    def startup__wrapped(self) -> TYPING__RESULT_W_EXX:
        result_chain = ValidChains(
            [
                # ValidBreak(not any([self.PTB_SET_EXTON, self.PTB_SET_HVON, self.PTB_SET_PSON])),

                Valid(
                    value_link=self.DEV_COLUMN.DUT.connect__only_if_address_resolved,
                    name="DUT.connect__only_if_address_resolved",
                ),

                # LED ----------------------------------------------------
                ValidNoCum(
                    value_link=self.DEV_COLUMN.DUT.SET,
                    kwargs__value={"LED2": "BLINK"},
                    validate_link="OK",
                    name="SET",
                ),

                # PTB_SET_EXTON ----------------------------------------------------
                Valid(
                    skip_link=not self.PTB_SET_EXTON,
                    value_link=self.DEV_COLUMN.DUT.SET,
                    kwargs__value={"EXT12": "ON"},
                    validate_link="OK",
                    name="SET",
                ),
                ValidSleep(0.5, skip_link=not self.PTB_SET_EXTON),

                # HV0 --------------------------------------------------------------
                Valid(
                    value_link=self.DEV_COLUMN.DUT.GET,
                    args__value="HV0",
                    validate_link=1 if self.ATC_VOUT else 0,
                    name="GET",
                ),

                # PTB_SET_HVON
                Valid(
                    skip_link=not self.PTB_SET_HVON or self.PTB_SET_EXTON,
                    value_link=self.DEV_COLUMN.DUT.SET,
                    kwargs__value={"HV": "ON"},
                    validate_link="OK",
                    name="SET",
                ),
                ValidSleep(0.5, skip_link=not self.PTB_SET_HVON),

                # HV1 -----------
                Valid(
                    value_link=self.DEV_COLUMN.DUT.GET,
                    args__value="HV1",
                    validate_link=1 if self.expect__psu_started_hv__ok() else 0,
                    name="GET",
                ),

                # PTB_SET_PSON ------------------------------------------------------
                Valid(
                    skip_link=not self.PTB_SET_PSON,
                    value_link=self.DEV_COLUMN.DUT.SET,
                    kwargs__value={"PSON": "ON", "__timeout": 10},
                    validate_link="OK" if self.expect__psu_may_start__hv_or_ext() else "ERR",
                    name="ON",
                ),
                ValidSleep(0.5, skip_link=not self.PTB_SET_PSON),
            ],
        )
        return result_chain

    # -----------------------------------------------------------------------------------------------------------------
    def teardown__wrapped(self) -> TYPING__RESULT_W_EXX:
        result_chain = ValidChains(
            chains=[
                # ValidBreak(not any([self.PTB_SET_EXTON, self.PTB_SET_HVON, self.PTB_SET_PSON])),

                Valid(
                    value_link=self.DEV_COLUMN.DUT.connect__only_if_address_resolved,
                    name="DUT.connect__only_if_address_resolved",
                ),
                Valid(
                    value_link=self.DEV_COLUMN.DUT.reset,
                    validate_link=lambda value: value is None,
                    name="RESET",
                ),

            ]
        )
        return result_chain


# =====================================================================================================================
