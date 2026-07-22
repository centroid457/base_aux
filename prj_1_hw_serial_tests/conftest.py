import pytest

from serial_utils import *


# =====================================================================================================================
# @pytest.fixture(scope="session")
# def manager(request) -> SerialManager_Harvest:
#     yield
#

# =====================================================================================================================
@pytest.fixture(scope="session")
def device(request) -> DeviceConsole_Harvest:
    for dev in manager.make__not_occupied(can_open=True):
        with dev:
            if dev.validate__harvest():
                dev_id = dev.exec__take_harvest_name()
                print(f"\n[HARVEST_FOUND]{dev}/{dev_id=}")
                yield dev


# =====================================================================================================================
