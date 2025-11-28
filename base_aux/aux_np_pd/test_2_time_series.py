from typing import *
import pytest

from base_aux.base_lambdas.m1_lambda import *
from base_aux.aux_dict.m2_dict_ic import *
from base_aux.aux_dict.m3_dict_ga import *


# # =====================================================================================================================
# @pytest.mark.parametrize(
#     argnames="source, key, keys_all_str, _EXPECTED",
#     argvalues=[
#         (dict(attr1=1), "attr1", True, [None, None]),
#         (dict(attr1=1), "ATTR1", True, [None, None]),
#         (dict(ATTR1=1), "ATTR1", True, [None, None]),
#         (dict(attr1=1), "hello", True, [None, Exception]),
#
#         (dict(attr1=1), 0, False, [None, Exception]),
#         ({1:1}, 0, False, [None, Exception]),
#         ({1:1}, 1, False, [None, None]),
#     ]
# )
# @pytest.mark.parametrize(argnames="VictimClsPair", argvalues=[(DictIcKeys, DictIc_LockedKeys), (DictIcKeys_Ga, DictIc_LockedKeys_Ga)])
# def test__si_update(VictimClsPair, source, key, keys_all_str, _EXPECTED):
#     # -------------------------------------------------
#     victim = VictimClsPair[0](source)
#     Lambda(victim.update({key: 11})).expect__check_assert(_EXPECTED[0])
#
#
# # =====================================================================================================================
