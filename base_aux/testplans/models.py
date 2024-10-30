from typing import *
from pydantic import BaseModel


# =====================================================================================================================
TYPES__DICT = dict[str, Union[None, str, bool, int, float, dict, list]]


# =====================================================================================================================
class ModelStandInfo(BaseModel):
    STAND_NAME: str           # "StandPSU"
    STAND_DESCRIPTION: str    # "test PSU for QCD"
    STAND_SN: str
    STAND_SETTINGS: TYPES__DICT = {}     # main settings for all TCS


class ModelDeviceInfo(BaseModel):
    DUT_INDEX: int          # device position in stand

    DUT_NAME: str           # "PSU"
    DUT_DESCRIPTION: str    # "Power Supply Unit"
    DUT_SN: str


class ModelTcInfo(BaseModel):
    TC_NAME: str
    TC_DESCRIPTION: str

    TC_ASYNC: bool
    TC_SKIP: bool

    TC_SETTINGS: TYPES__DICT = {
        # CONTENT IS NOT SPECIFIED!
        # "ANY_1": Any,
    }


class ModelTcResult(BaseModel):
    tc_timestamp: float | None = None

    tc_active: bool = False
    tc_progress: int = 0
    tc_result: bool | None = None
    tc_details: TYPES__DICT = {
        # CONTENT IS NOT SPECIFIED!
        # "ANY_2": Any,
    }


# =====================================================================================================================
class ModelTcResultFull(ModelTcResult, ModelTcInfo, ModelDeviceInfo):
    pass


class ModelTpInfo(ModelStandInfo):
    TESTCASES: list[ModelTcInfo]


class ModelTpResults(ModelStandInfo):
    TESTCASES: list[list[ModelTcResultFull]]


# =====================================================================================================================
