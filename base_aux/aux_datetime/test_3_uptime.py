import time
import pytest
from base_aux.base_lambdas.m1_lambda import *
from base_aux.aux_datetime.m3_uptime import *


# =====================================================================================================================
START_AMENDMENT = 0.0000001


@pytest.mark.parametrize(
    argnames="pause",
    argvalues=[
        0.1, 0.2, 0.3,
    ]
)
def test__uptime(pause: float):
    ethalon = time.time()
    victim = Uptime(cmp_accuracy_value=START_AMENDMENT)
    assert victim.time_started - ethalon <= START_AMENDMENT
    assert victim <= START_AMENDMENT

    time.sleep(pause)
    assert victim.get() > pause - START_AMENDMENT
    assert victim > pause


# =====================================================================================================================
