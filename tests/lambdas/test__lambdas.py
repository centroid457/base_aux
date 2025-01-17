import pytest

from base_aux.aux_pytester.m1_pytest_aux import *
from base_aux.base_objects.m0_primitives import *

from base_aux.lambdas.m1_lambdas import *


# =====================================================================================================================
def test__raise():
    try:
        Lambda(LAMBDA_RAISE)()
        assert False
    except:
        assert True

    assert Lambda(INST_EXCEPTION)() == INST_EXCEPTION
    assert isinstance(Lambda(Exception)(), Exception)


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
def test__derivatives(source, args, _EXPECTED):
    # for Cls, Expected in zip(, _EXPECTED):    # tis good idea but we cant see directly exact line!

    PytestAux(Lambda(source, *args)).assert_check(_EXPECTED[0])
    PytestAux(LambdaBool(source, *args)).assert_check(_EXPECTED[1])
    PytestAux(LambdaBoolReversed(source, *args)).assert_check(_EXPECTED[2])
    PytestAux(LambdaTrySuccess(source, *args)).assert_check(_EXPECTED[3])
    PytestAux(LambdaTryFail(source, *args)).assert_check(_EXPECTED[4])


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
        assert False
    except:
        assert True
    assert time.time() - start_time > pause * 0.9


# =====================================================================================================================
