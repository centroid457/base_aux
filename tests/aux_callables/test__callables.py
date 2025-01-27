import pytest

from base_aux.aux_expect.m1_expect_aux import ExpectAux

from base_aux.aux_types.m0_primitives import *
from base_aux.aux_callable.m1_callable_aux import *
from base_aux.base_enums.m0_enums import *


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="source, args, _EXPECTED",
    argvalues=[
        (Exception, (), (False, True,
                         Exception, Exception, Exception, False, Process.SKIPPED, Exception)),  # be careful here! exx in source return exx NO RAISE!!!!
        (Exception(), (), (False, True,
                Exception, Exception, Exception, False, Exception, Exception)),
        (LAMBDA_EXX, (), (False, True,
                          Exception, Exception, Exception, False, Process.SKIPPED, Exception)),
        (LAMBDA_RAISE, (), (True, False,
                            Exception, None, Exception, False, Process.SKIPPED, Process.SKIPPED)),

        (LAMBDA_TRUE, (), (False, True,
                           True, True, True, True, Process.SKIPPED, True)),
        (LAMBDA_FALSE, (), (False, True,
                            False, False, False, False, Process.SKIPPED, False)),
        (LAMBDA_NONE, (), (False, True,
                           None, None, None, False, Process.SKIPPED, None)),

        (True, (), (False, True,
                True, True, True, True, True, True)),
        (False, (), (False, True,
                False, False, False, False, False, False)),
        (None, (), (False, True,
                None, None, None, False, None, None)),

        (INST_CALL_TRUE, (), (False, True,
                              True, True, True, True, Process.SKIPPED, True)),
        (INST_CALL_FALSE, (), (False, True,
                               False, False, False, False, Process.SKIPPED, False)),
        (INST_CALL_RAISE, (), (True, False,
                               Exception, None, Exception, False, Process.SKIPPED, Process.SKIPPED)),

        (INST_BOOL_TRUE, (),  (False, True,
                INST_BOOL_TRUE, INST_BOOL_TRUE, INST_BOOL_TRUE, True, INST_BOOL_TRUE, INST_BOOL_TRUE)),
        (INST_BOOL_FALSE, (), (False, True,
                INST_BOOL_FALSE, INST_BOOL_FALSE, INST_BOOL_FALSE, False, INST_BOOL_FALSE, INST_BOOL_FALSE)),
        (INST_BOOL_RAISE, (), (False, True,
                INST_BOOL_RAISE, INST_BOOL_RAISE, INST_BOOL_RAISE, False, INST_BOOL_RAISE, INST_BOOL_RAISE)),

        # collections ----------
        ((), (), (False, True,
                (), (), (), False, (), ())),
        ([], (), (False, True,
                [], [], [], False, [], [])),
        (LAMBDA_LIST_DIRECT, (), (False, True,
                                  [], [], [], False, Process.SKIPPED, [])),

        ([None, ], (), (False, True,
                [None, ], [None, ], [None, ], True, [None, ], [None, ])),
        ([1, ], (), (False, True,
                [1, ], [1, ], [1, ], True, [1, ], [1, ])),
    ]
)
def test__get_result(source, args, _EXPECTED):
    ExpectAux(CallableAux(source).check_raise, args).check_assert(_EXPECTED[0])
    ExpectAux(CallableAux(source).check_no_raise, args).check_assert(_EXPECTED[1])
    ExpectAux(CallableAux(source).resolve_raise, args).check_assert(_EXPECTED[2])
    ExpectAux(CallableAux(source).resolve_raise_as_none, args).check_assert(_EXPECTED[3])
    ExpectAux(CallableAux(source).resolve_exx, args).check_assert(_EXPECTED[4])
    ExpectAux(CallableAux(source).resolve_bool, args).check_assert(_EXPECTED[5])
    ExpectAux(CallableAux(source).resolve_skip_callables, args).check_assert(_EXPECTED[6])
    ExpectAux(CallableAux(source).resolve_skip_raised, args).check_assert(_EXPECTED[7])


# =====================================================================================================================
