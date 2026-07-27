import pytest
import os
import time
from datetime import datetime

from .utils import HarvestDevice

from base_aux.buses.d1_serial2_new.m2_manager import SerialManager
from base_aux.buses.d1_serial2_new.m1_serial_client import SerialClient2


# =====================================================================================================================
# Глобальная переменная для хранения идентификатора устройства
DEVICE_ID: str | None = None


# =====================================================================================================================
@pytest.fixture(scope="session")
def harvest() -> HarvestDevice:
    """Находит устройство Harvest и возвращает авторизованный клиент."""
    global DEVICE_ID

    found: list[HarvestDevice] = []
    for conn in SerialManager().make__not_occupied(can_open=True, baudrate=115200):
        with conn:
            if HarvestDevice(conn).validate_conn():
                dev_id = HarvestDevice(conn).get_hostname_and_occupy()
                print(f"\n[HARVEST_FOUND]{conn}/{dev_id=}")
                found.append(HarvestDevice(conn))

    if len(found) == 0:
        pytest.exit("Устройств Harvest не обнаружено.")
    if len(found) > 1:
        pytest.exit("Устройств Harvest более чем 1!")

    with found[0].conn:
        DEVICE_ID = dev_id   # сохраняем для использования в хуке
        yield found[0]


# =====================================================================================================================
@pytest.fixture(scope="session")
def internet_access(harvest) -> bool:
    return harvest.check__has_internet()


# =====================================================================================================================
@pytest.hookimpl(trylast=True)   # попытка запуска после хука pytest-html - не помогло!!!!
def pytest_sessionfinish(session, exitstatus):
    html_path = session.config.getoption('--html', default=None)
    pass


@pytest.hookimpl(trylast=True)
def pytest_unconfigure(config):
    """Переименовывает HTML-отчёт, добавляя dev_id и текущую дату-время."""
    html_path = config.getoption('--html', default=None)
    if not html_path:
        print("HTML-отчёт не задан – переименование не требуется.")

    # Даём время на завершение записи файла
    for _ in range(10):
        if os.path.isfile(html_path):
            break
        time.sleep(0.5)
    else:
        print(f"HTML-отчёт не появился: {html_path}")
        return

    if DEVICE_ID is None:
        print("DEVICE_ID не определён")

    mark_expr = config.getoption('markexpr', default='')
    safe_mark = mark_expr.replace(' ', '_').replace('(', '').replace(')', '')

    dir_name, file_name = os.path.split(html_path)
    print(dir_name, file_name)
    date_str = datetime.now().strftime('%Y.%m.%d_%H-%M-%S')

    new_name = f"{DEVICE_ID}_{date_str}_m[{safe_mark}].html"
    new_path = os.path.join(dir_name, new_name)

    try:
        os.rename(html_path, new_path)
        print(f"Отчёт переименован в: {new_path}")
    except OSError as exc:
        print(f"Ошибка переименования отчёта: {exc!r}")


# =====================================================================================================================
