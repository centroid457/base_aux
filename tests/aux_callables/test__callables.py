import pytest

from base_aux.aux_pytester.m1_pytest_aux import PytestAux

from base_aux.base_objects.m0_primitives import *
from base_aux.aux_callable.m1_callable_aux import *
from base_aux.base_enums.enums import *


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="source, args, _EXPECTED",
    argvalues=[
        (Exception, (), (False, True,
                Exception, Exception, Exception, False, CallablesUse.SKIP_CALLABLE, Exception)),  # be careful here! exx in source return exx NO RAISE!!!!
        (Exception(), (), (False, True,
                Exception, Exception, Exception, False, Exception, Exception)),
        (LAMBDA_EXX, (), (False, True,
                Exception, Exception, Exception, False, CallablesUse.SKIP_CALLABLE, Exception)),
        (LAMBDA_RAISE, (), (True, False,
                Exception, None, Exception, False, CallablesUse.SKIP_CALLABLE, CallablesUse.SKIP_CALLABLE)),

        (LAMBDA_TRUE, (), (False, True,
                True, True, True, True, CallablesUse.SKIP_CALLABLE, True)),
        (LAMBDA_FALSE, (), (False, True,
                False, False, False, False, CallablesUse.SKIP_CALLABLE, False)),
        (LAMBDA_NONE, (), (False, True,
                None, None, None, False, CallablesUse.SKIP_CALLABLE, None)),

        (True, (), (False, True,
                True, True, True, True, True, True)),
        (False, (), (False, True,
                False, False, False, False, False, False)),
        (None, (), (False, True,
                None, None, None, False, None, None)),

        (INST_CALL_TRUE, (), (False, True,
                True, True, True, True, CallablesUse.SKIP_CALLABLE, True)),
        (INST_CALL_FALSE, (), (False, True,
                False, False, False, False, CallablesUse.SKIP_CALLABLE, False)),
        (INST_CALL_RAISE, (), (True, False,
                Exception, None, Exception, False, CallablesUse.SKIP_CALLABLE, CallablesUse.SKIP_CALLABLE)),

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
                [], [], [], False, CallablesUse.SKIP_CALLABLE, [])),

        ([None, ], (), (False, True,
                [None, ], [None, ], [None, ], True, [None, ], [None, ])),
        ([1, ], (), (False, True,
                [1, ], [1, ], [1, ], True, [1, ], [1, ])),
    ]
)
def test__get_result(source, args, _EXPECTED):
    PytestAux(CallableAux(source).check_raise, args).assert_check(_EXPECTED[0])
    PytestAux(CallableAux(source).check_no_raise, args).assert_check(_EXPECTED[1])
    PytestAux(CallableAux(source).resolve_raise, args).assert_check(_EXPECTED[2])
    PytestAux(CallableAux(source).resolve_raise_as_none, args).assert_check(_EXPECTED[3])
    PytestAux(CallableAux(source).resolve_exx, args).assert_check(_EXPECTED[4])
    PytestAux(CallableAux(source).resolve_bool, args).assert_check(_EXPECTED[5])
    PytestAux(CallableAux(source).resolve_skip_callables, args).assert_check(_EXPECTED[6])
    PytestAux(CallableAux(source).resolve_skip_raised, args).assert_check(_EXPECTED[7])


# =====================================================================================================================
