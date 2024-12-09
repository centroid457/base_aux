import pytest
import time

from base_aux.base_argskwargs import *
from base_aux.classes.lambdas import *
from base_aux.funcs import *
from base_aux.objects.primitives import *
from base_aux.files import *


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="source, args, _EXPECTED",
    argvalues=[
        (INST_BOOL_RAISE, Kwargs(name="name"), INST_BOOL_RAISE),
    ]
)
def test__1(source, args, _EXPECTED):
    func_link = FilePath
    pytest_func_tester__no_args_kwargs(Lambda(source, *args), _EXPECTED[0])


# =====================================================================================================================
