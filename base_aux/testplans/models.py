from typing import *
from pydantic import BaseModel


# =====================================================================================================================
TYPES__DICT = dict[str, Union[None, str, bool, int, float, dict, list]]


# =====================================================================================================================
class ModelStandInfo(BaseModel):
    # STAND_NAME: str           # "StandPSU"
    # STAND_DESCRIPTION: str    # "test PSU for QCD"
    # STAND_SN: str
    STAND_SETTINGS: TYPES__DICT = {}     # main settings for all TCS


class ModelDeviceInfo(BaseModel):
    INDEX: int          # device position in stand

    NAME: str           # "PSU"
    DESCRIPTION: str    # "Power Supply Unit"
    SN: str


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
