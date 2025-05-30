from typing import *
from pydantic import BaseModel


# =====================================================================================================================
TYPES__DICT = dict[str, Union[None, str, bool, int, float, dict, list]]


# =====================================================================================================================
class Model_StandInfo(BaseModel):
    # STAND_NAME: str           # "StandPSU"
    # STAND_DESCRIPTION: str    # "test PSU for QCD"
    # STAND_SN: str
    STAND_SETTINGS: TYPES__DICT = {}     # main settings for all TCS


class Model_DeviceInfo(BaseModel):
    INDEX: int          # device position in stand

    NAME: str           # "PSU"
    DESCRIPTION: str    # "Power Supply Unit"
    SN: str


class Model_TcInfo(BaseModel):
    TC_NAME: str
    TC_DESCRIPTION: str

    TC_ASYNC: bool
    TC_SKIP: bool

    TC_SETTINGS: TYPES__DICT = {
        # CONTENT IS NOT SPECIFIED!
        # "ANY_1": Any,
    }


class Model_TcResult(BaseModel):
    tc_timestamp: float | None = None

    tc_active: bool = False
    tc_result: bool | None = None
    tc_details: TYPES__DICT = {
        # CONTENT IS NOT SPECIFIED!
        # "ANY_2": Any,
    }


# =====================================================================================================================
class Model_TcResultFull(Model_TcResult, Model_TcInfo, Model_DeviceInfo):
    pass


class Model_TpInfo(Model_StandInfo):
    TESTCASES: list[Model_TcInfo]


class Model_TpResults(Model_StandInfo):
    TESTCASES: list[list[Model_TcResultFull]]


# =====================================================================================================================
