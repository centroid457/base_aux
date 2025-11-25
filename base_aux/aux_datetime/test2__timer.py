import time
import pytest
from base_aux.base_lambdas.m1_lambda import *
from base_aux.aux_datetime.m2_timer import *


# =====================================================================================================================
START_AMENDMENT = 0.0000001


@pytest.mark.parametrize(
    argnames="pause",
    argvalues=[
        0.1, 0.2, 0.3,
    ]
)
def test__timer(pause: float):
    ethalon = time.time()
    victim = Timer()
    assert victim.started - ethalon <= START_AMENDMENT

    time.sleep(pause)
    assert victim.check() > pause - START_AMENDMENT


# =====================================================================================================================
