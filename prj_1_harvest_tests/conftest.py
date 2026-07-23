import pytest
from serial_utils import manager, SerialClient2


# =====================================================================================================================
@pytest.fixture(scope="session")
def harvest() -> SerialClient2:
    """Находит первое устройство Harvest и возвращает авторизованный клиент."""
    found: list[SerialClient2] = []
    for conn in manager.make__not_occupied(can_open=True, baudrate=115200):
        with conn:
            if manager.harvest__validate(conn):
                dev_id = manager.harvest__get_name_and_occupy(conn)
                print(f"\n[HARVEST_FOUND]{conn}/{dev_id=}")
                found.append(conn)

    if len(found) == 0:
        pytest.exit("Устройств Harvest не обнаружено.")
    if len(found) > 1:
        pytest.exit("Устройств Harvest более чем 1!")

    with found[0] as conn:
        yield conn


# =====================================================================================================================
