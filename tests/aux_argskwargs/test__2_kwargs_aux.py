import pytest

from base_aux.aux_pytester.m1_pytest_aux import PytestAux
from base_aux.aux_argskwargs.m2_argskwargs_aux import ArgsKwargsAux


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="source, _EXPECTED",
    argvalues=[
        (None, (None, )),
    ]
)
def test__args(source, _EXPECTED):
    func_link = ArgsKwargsAux(source).resolve_args
    PytestAux(func_link).assert_check(_EXPECTED)


# =====================================================================================================================
