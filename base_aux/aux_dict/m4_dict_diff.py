from typing import *

from base_aux.base_nest_dunders.m1_init1_source import *
from base_aux.base_nest_dunders.m3_calls import *
from base_aux.aux_dict.m3_dict_ga1_simple import *
from base_aux.base_statics.m1_types import *
from base_aux.aux_eq.m1_eq_args import *


# =====================================================================================================================
class DictDiff(NestCall_Resolve):
    """
    GOAL
    ----
    get diffs from several states,
    dicts assumed like AttrDumped objects - so keys are STR.

    SPECIALLY CREATED FOR
    ---------------------
    cmp two objects by attr values
    """
    DICTS: tuple[TYPING.DICT_STR_ANY, ...]

    def __init__(self, *dicts: TYPING.DICT_STR_ANY):
        self.DICTS = dicts

    def resolve(self) -> dict[str, tuple[Any, ...]] | NoReturn:
        keys: list[str] = [key for DICT in self.DICTS for key in DICT]
        keys = sorted(keys)

        result = {}
        for key in keys:
            # values collect -------
            values = []
            for DICT in self.DICTS:
                if key not in DICT:
                    value = VALUE_SPECIAL.NOVALUE
                else:
                    try:
                        value = DICT[key]
                    except :
                        value = VALUE_SPECIAL.RAISED

                values.append(value)

            # values check eq -------
            if not EqArgs(*values):
                result.update({key: values})

        return result

    def __bool__(self) -> bool | NoReturn:
        """
        GOAL
        ----
        TRUE - if Diffs exists! (it looks from class name!)
        False - if NO Diffs!
        """
        return bool(self.resolve())


# =====================================================================================================================
if __name__ == "__main__":
    pass


# =====================================================================================================================
from base_aux.aux_expect.m1_expect_aux import *
from base_aux.base_nest_dunders.m7_cmp import *


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="dicts, _EXPECTED",
    argvalues=[
        # blank ------------
        ([{}, ], {}),
        ([{}, {}], {}),
        ([{}, {}, {}], {}),

        # diffs ------------
        ([{1:1}, {1:1}], {}),
        ([{1: 1}, {1: 11}], {1: [1, 11]}),
        ([{1: 1}, {1: 11}, {1: 111}], {1: [1, 11, 111]}),

        # NOVALUE ------------
        ([{1: 1}, {}], {1: [1, VALUE_SPECIAL.NOVALUE]}),
        ([{1: 1}, {}, {1:11}], {1: [1, VALUE_SPECIAL.NOVALUE, 11]}),
    ]
)
def test__resolve__eq(dicts, _EXPECTED):
    func_link = lambda: DictDiff(*dicts).resolve()
    ExpectAux(func_link).check_assert(_EXPECTED)


# =====================================================================================================================
