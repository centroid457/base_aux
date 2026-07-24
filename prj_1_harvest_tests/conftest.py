import pytest

from utils import HarvestDevice

from base_aux.buses.d1_serial2_new.m2_manager import SerialManager
from base_aux.buses.d1_serial2_new.m1_serial_client import SerialClient2


# =====================================================================================================================
@pytest.fixture(scope="session")
def harvest() -> HarvestDevice:
    """Находит первое устройство Harvest и возвращает авторизованный клиент."""
    found: list[HarvestDevice] = []
    for conn in SerialManager().make__not_occupied(can_open=True, baudrate=115200):
        with conn:
            if HarvestDevice(conn).validate_conn():
                dev_id = HarvestDevice(conn).get_name_and_occupy()
                print(f"\n[HARVEST_FOUND]{conn}/{dev_id=}")
                found.append(HarvestDevice(conn))

    if len(found) == 0:
        pytest.exit("Устройств Harvest не обнаружено.")
    if len(found) > 1:
        pytest.exit("Устройств Harvest более чем 1!")

    with found[0].conn:
        yield found[0]


# =====================================================================================================================
