import pytest

from base_aux.base_lambdas.m1_lambda import *
from base_aux.cmds.m3_timeout_def import *


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="def_values, new_values, _EXPECTED",
    argvalues=[
        ((None, None, None), (None, None, None), (None, None, None)),
        ((1, 2, 3), (None, None, None), (1, 2, 3)),
        ((1, 2, 3), (11, None, None), (11, 2, 3)),
        ((1, 2, 3), (None, 22, None), (1, 22, 3)),
        ((1, 2, 3), (None, None, 33), (1, 2, 33)),
    ]
)
def test__change_get_active(def_values, new_values, _EXPECTED):
    victim: TimeoutDef = TimeoutDef(*def_values)

    assert victim.WRITE == def_values[0]
    assert victim.READ_START == def_values[1]
    assert victim.READ_FINISH == def_values[2]

    assert victim.get_active__write(new_values[0]) == _EXPECTED[0]
    assert victim.get_active__read_start(new_values[1]) == _EXPECTED[1]
    assert victim.get_active__read_finish(new_values[2]) == _EXPECTED[2]

    victim.change(*new_values)
    assert victim.WRITE == _EXPECTED[0]
    assert victim.READ_START == _EXPECTED[1]
    assert victim.READ_FINISH == _EXPECTED[2]

    # Lambda(func_link, args).check_expected__assert(_EXPECTED)


# =====================================================================================================================
