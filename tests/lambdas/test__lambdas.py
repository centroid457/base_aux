import pytest

from base_aux.lambdas.lambdas import *
from base_aux.pytester import *
from base_aux.base_objects.primitives import *


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="source, args, _EXPECTED",
    argvalues=[
        (Exception, (), (Exception, Exception, False)),
        (Exception(), (), (Exception, Exception, False)),
        (LAMBDA_EXX, (), (Exception, Exception, False)),

        (True, (), (True, True, True)),
        (False, (), (False, False, False)),
        (None, (), (None, None, False)),
        (LAMBDA_TRUE, (), (True, True, True)),
        (LAMBDA_FALSE, (), (False, False, False)),
        (LAMBDA_NONE, (), (None, None, False)),

        ((), (), (Exception, Exception, False)),    # ????
        ([], (), ([], [], False)),
        (LAMBDA_LIST_DIRECT, (), ([], [], False)),

        ([None, ], (), (None, None, False)),
        ([1, ], (), (1, 1, True)),

        (INST_CALL_TRUE, (), (True, True, True)),
        (INST_CALL_FALSE, (), (False, False, False)),
        (INST_CALL_RAISE, (), (Exception, Exception, False)),

        (INST_BOOL_TRUE, (), (INST_BOOL_TRUE, INST_BOOL_TRUE, True)),
        (INST_BOOL_FALSE, (), (INST_BOOL_FALSE, INST_BOOL_FALSE, False)),
        (INST_BOOL_RAISE, (), (INST_BOOL_RAISE, INST_BOOL_RAISE, False)),
    ]
)
def test__get_result_s(source, args, _EXPECTED):
    pytest_func_tester__no_kwargs(Lambda(source, *args).get_result_or_raise, args, _EXPECTED[0])
    pytest_func_tester__no_kwargs(Lambda(source, *args).get_result_or_exx, args, _EXPECTED[1])
    pytest_func_tester__no_kwargs(Lambda(source, *args).get_result_bool, args, _EXPECTED[2])


def test__get_result_or_raise__raise():
    try:
        Lambda(LAMBDA_RAISE).get_result_or_raise()
    except:
        assert True
    else:
        assert False

    assert Lambda(Exception).get_result_or_raise() == Exception()
    assert Lambda().get_result_or_raise() == Exception()

# =====================================================================================================================
# DERIVATIVES
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
