import pytest

from base_aux.base_objects.primitives import *
from base_aux.base_enums import *
from base_aux.aux_callable import *

from base_aux.aux_pytester import *


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
    pytest_func_tester__no_kwargs(CallableAux(source).check_raise, args, _EXPECTED[0])
    pytest_func_tester__no_kwargs(CallableAux(source).check_no_raise, args, _EXPECTED[1])

    pytest_func_tester__no_kwargs(CallableAux(source).resolve_raise, args, _EXPECTED[2])
    pytest_func_tester__no_kwargs(CallableAux(source).resolve_raise_as_none, args, _EXPECTED[3])
    pytest_func_tester__no_kwargs(CallableAux(source).resolve_exx, args, _EXPECTED[4])

    pytest_func_tester__no_kwargs(CallableAux(source).resolve_bool, args, _EXPECTED[5])
    pytest_func_tester__no_kwargs(CallableAux(source).resolve_skip_callables, args, _EXPECTED[6])
    pytest_func_tester__no_kwargs(CallableAux(source).resolve_skip_raised, args, _EXPECTED[7])


# =====================================================================================================================
