import pytest
from base_aux.base_lambdas.m1_lambda import *

from base_aux.chains.m1_chains import *


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="source, chains, _EXPECTED",
    argvalues=[
        (1, (lambda x: x+1, ), 2),
        (1, (lambda x: x+1, lambda x: x+1), 3),
        (1, (lambda x: x+1, lambda x: x+1, lambda x: x-2), 1),
    ]
)
def test__chains(source, chains, _EXPECTED):
    Lambda(ChainResolve(*chains, source=source).resolve).check_expected__assert(_EXPECTED)


# =====================================================================================================================
