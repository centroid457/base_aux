import pytest
import time

from base_aux.classes.lambdas import *
from base_aux.pytester import *
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
def test__LambdaSleep_Ok():
    pause = 0.5

    start_time = time.time()
    victim = LambdaSleep(sec=pause, constructor=11)
    assert time.time() - start_time < 0.1
    assert victim == 11     # execute on EQ
    assert time.time() - start_time > pause * 0.9


def test__LambdaSleep_Raise():
    pause = 0.5
    start_time = time.time()
    victim = LambdaSleep(sec=pause, constructor=LAMBDA_RAISE)
    assert time.time() - start_time < 0.1
    try:
        result = victim == 11     # execute on EQ
    except:
        assert True
    else:
        assert False
    assert time.time() - start_time > pause * 0.9


# =====================================================================================================================
