from typing import *
import pytest

from base_aux.aux_dict.m2_dict_ic import *


# =====================================================================================================================
class NestInit_ParamsDict_UpdateKwargs:
    """
    GOAL
    ----
    when we have PARAMS like DictIc-as defParams and want to update it by Kwargs on init!

    SPECIALLY CREATED FOR
    ---------------------
    indics
    """
    PARAMS: DictIc_LockedKeys

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args)
        self.PARAMS.update(**kwargs)


# =====================================================================================================================
def test__():
    class Victim(NestInit_ParamsDict_UpdateKwargs):
        PARAMS = DictIc_LockedKeys(attr1=1, attr2=2)

    victim = Victim(attr2=22)
    assert victim.PARAMS["attr1"] == 1
    assert victim.PARAMS["attr2"] == 22


# =====================================================================================================================
if __name__ == "__main__":
    pass


# =====================================================================================================================
