import pytest
import time

from base_aux.base_argskwargs import *
from base_aux.classes.lambdas import *
from base_aux.funcs import *
from base_aux.objects.primitives import *
from base_aux.files import *


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="kwargs",
    argvalues=[
        Kwargs(name="name"),
    ]
)
def test__1(kwargs):
    victim = FilePath(**kwargs.KWARGS)
    # assert victim
    #
    # assert


# =====================================================================================================================
