import pytest
import os
import time
import re
import json
from datetime import datetime

from .utils import HarvestDevice

from base_aux.buses.d1_serial2_new.m2_manager import SerialManager
from base_aux.buses.d1_serial2_new.m1_serial_client import SerialClient2


# =====================================================================================================================
@pytest.fixture(scope="session")
def harvest(request) -> HarvestDevice:
    """Находит устройство Harvest и возвращает авторизованный клиент."""
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
        request.config.stash["device_id"] = dev_id
        yield found[0]


@pytest.fixture(scope="session")
def harvest_info(harvest, request):
    info = harvest.get_info__system()
    request.config.stash["device_info"] = info
    print(json.dumps(info, indent=2, ensure_ascii=False))
    return info


# =====================================================================================================================
@pytest.fixture(scope="session")
def internet_access(harvest) -> bool:
    return harvest.check__has_internet()


# =====================================================================================================================
# HTML REPORT
def patch_html__title(filepath, new_title, **kwargs):
    """Заменяет содержимое тега <h1 id="title"> в HTML-отчёте."""
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    new_html = re.sub(
        r'<h1 id="title">.*?</h1>',
        f'<h1 id="title">{new_title}</h1>',
        html
    )
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_html)
    print(f"Заголовок отчёта изменён на '{new_title}'")


@pytest.hookimpl(trylast=True)
def pytest_unconfigure(config):
    """
    GOAL
    finalise all processes
    """
    # 1=HTML ----------------------------------------------------------------------------
    # Переименовывает HTML-отчёт, добавляя dev_id и текущую дату-время
    html_path = config.getoption('--html', default=None)
    if not html_path:
        print("HTML-отчёт не задан – переименование не требуется.")
        return

    # Даём время на завершение записи файла
    for _ in range(10):
        if os.path.isfile(html_path):
            break
        time.sleep(0.5)
    else:
        print(f"HTML-отчёт не появился: {html_path}")
        return

    # Получаем DEVICE_ID из stash – больше никакой глобальной переменной
    DEVICE_ID = config.stash.get("device_id", None)
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
        # Меняем заголовок
        title = f"{DEVICE_ID} – {date_str}"
        if safe_mark:
            title += f" (markers: {safe_mark})"
        patch_html__title(filepath=new_path, new_title=new_name)
    except OSError as exc:
        print(f"Ошибка переименования отчёта: {exc!r}")


# =====================================================================================================================
