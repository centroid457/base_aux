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
                try:
                    value = DICT[key]
                except Exception as exx:
                    value = exx

                values.append(value)

            # values check -------
            if not EqArgs(*values):
                result.update({key: values})

            return result


# =====================================================================================================================
if __name__ == "__main__":
    pass


# =====================================================================================================================
from base_aux.aux_expect.m1_expect_aux import *
from base_aux.base_nest_dunders.m7_cmp import *

# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="source, _EXPECTED",
    argvalues=[
        ((), ()),
        ([], ()),
        ({}, ()),

        ((1,), (1,)),
        ([1, ], (1,)),
        ({1: 1}, (1,)),

        # None --------------
        (None, (None,)),
        ((None,), (None,)),

        ((None, True), (None, True)),
        (((None,), True), ((None,), True)),

        # INT --------------
        (0, (0,)),
        ((0,), (0,)),
        (1, (1,)),
        (1 + 1, (2,)),

        # CALLABLES --------------
        (LAMBDA_TRUE, (LAMBDA_TRUE,)),
        (LAMBDA_NONE, (LAMBDA_NONE,)),
        (LAMBDA_EXX, (LAMBDA_EXX,)),

        (ClsGen, (ClsGen,)),
        (INST_GEN, (INST_GEN,)),

        (ArgsKwargs(1), (1,)),
        (ArgsKwargs(1, 2), (1, 2)),
    ]
)
def test__args(source, _EXPECTED):
    source = ArgsKwargsAux(source).resolve_args
    ExpectAux(source).check_assert(_EXPECTED)


# =====================================================================================================================
