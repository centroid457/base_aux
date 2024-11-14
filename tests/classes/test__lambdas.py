import pytest
import time

from base_aux.classes.lambdas import *
from base_aux.funcs import *
from base_aux.objects.primitives import *


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="source, args, _EXPECTED",
    argvalues=[
        (1, (1,2,), (1, True, False, True, False)),
        (10, (1,2,), (10, True, False, True, False)),
        (LAMBDA_TRUE, (1,2,), (True, True, False, True, False)),
        (LAMBDA_RAISE, (1,2,), (Exception, Exception, Exception, False, True)),
        (INST_CALL_RAISE, (1,2,), (Exception, Exception, Exception, False, True)),
        (INST_BOOL_RAISE, (1,2,), (INST_BOOL_RAISE, Exception, Exception, True, False)),
    ]
)
def test__Lambdas(source, args, _EXPECTED):
    # for Cls, Expected in zip(, _EXPECTED):    # tis good idea but we cant see directly exact line!

    pytest_func_tester__no_args_kwargs(Lambda(source, *args), _EXPECTED[0])

    pytest_func_tester__no_args_kwargs(LambdaBool(source, *args), _EXPECTED[1])
    pytest_func_tester__no_args_kwargs(LambdaBoolReversed(source, *args), _EXPECTED[2])

    pytest_func_tester__no_args_kwargs(LambdaTrySuccess(source, *args), _EXPECTED[3])
    pytest_func_tester__no_args_kwargs(LambdaTryFail(source, *args), _EXPECTED[4])


# =====================================================================================================================
# TODO: finish!
# @pytest.mark.parametrize(
#     argnames="source, sec, _EXPECTED",
#     argvalues=[
#         (1, (1, 2,), 1),
#         (10, (1, 2,), (10, True, False, True, False)),
#         (LAMBDA_TRUE, (1, 2,), (True, True, False, True, False)),
#         (LAMBDA_RAISE, (1, 2,), (Exception, Exception, Exception, False, True)),
#         (INST_CALL_RAISE, (1, 2,), (Exception, Exception, Exception, False, True)),
#         (INST_BOOL_RAISE, (1, 2,), (INST_BOOL_RAISE, Exception, Exception, True, False)),
#     ]
# )
# def test__LambdaSleep(source, sec, _EXPECTED):
#     pass
#
#     pytest_func_tester__no_args_kwargs(LambdaSleep(source, *args), _EXPECTED[0])


# =====================================================================================================================
