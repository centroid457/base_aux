import pytest
import os
import time
import re
import json
from datetime import datetime

from .utils import HarvestDevice

from base_aux.buses.d1_serial2_new.m2_manager import SerialManager
from base_aux.buses.d1_serial2_new.m1_serial_client import SerialClient2
from base_aux.aux_eq.m3_eq_valid3_derivatives import *


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

    device = found[0]
    with device.conn:
        device.prepare__stop__kernel_terminal_logs()
        device.prepare__stop__services()
        request.config.stash["device_id"] = dev_id
        yield device


@pytest.fixture(scope="session")
def harvest_info(harvest, request):
    info = harvest.get_info__system()
    request.config.stash["device_info"] = info
    print(json.dumps(info, indent=2, ensure_ascii=False))
    return info


# =====================================================================================================================
@pytest.fixture(scope="session")
def gsm_at_port(harvest):
    # return "/dev/ttyUSB2"
    result: str | None = None
    # 1=------------------------------------------------------------
    assert harvest.cmd_timeout__check_executed_success(
        "lsusb | grep -i qualcomm"), "устройствоне обнружено [9011 Qualcomm]"

    # ------------------------------------------------------------
    # 2=Пробуем активировать драйвер (безопасно, даже если уже загружен)
    assert harvest.cmd_timeout__check_executed_success(
        "modprobe option"), "драйвер не установлен ID 1e0e:9011 Qualcomm / Option A76XX Series LTE Module"

    # 3=------------------------------------------------------------
    # можно запускать сколько угодно! ошибки не будет!
    """
    сама команда дает результат того куда что подключено - НО если DMSG включен!!! 

    ---- Sent utf8 encoded message: "echo "1e0e 9011" > /sys/bus/usb-serial/drivers/option1/new_id 2>/dev/null\r\n" ----
echo "1e0e 9011" > /sys/bus/usb-serial/drivers/option1/new_id 2>/dev/null
[ 6102.041184] option 4-1:1.2: GSM modem (1-port) converter detected
[ 6102.048043] usb 4-1: GSM modem (1-port) converter now attached to ttyUSB1
[ 6102.057099] option 4-1:1.4: GSM modem (1-port) converter detected
[ 6102.064194] usb 4-1: GSM modem (1-port) converter now attached to ttyUSB2
[ 6102.073013] option 4-1:1.5: GSM modem (1-port) converter detected
[ 6102.079925] usb 4-1: GSM modem (1-port) converter now attached to ttyUSB3
root@harvest05:~# 
    """
    assert harvest.cmd_timeout__check_executed_success(
        'echo "1e0e 9011" > /sys/bus/usb-serial/drivers/option1/new_id 2>/dev/null'
    ), "активация шины связи для AT команд не состоялось"
    time.sleep(1)  # даём время на создание портов

    port_candidates = harvest.cmd_parsed__ls(path="/dev/", filters=EqValid_Regexp(r"ttyUSB\d+"))
    assert port_candidates, f"не обнаружены варианты портов для перебора {port_candidates=}"

    for port in port_candidates:
        props = harvest.get_info__usb(port)

        # 4=Проверяем props ---------------
        if any([
            not props,
            props.get("ID_VENDOR_ID") != "1e0e",
            props.get("ID_MODEL_ID") != "9011",
            "A76XX" not in props.get("ID_MODEL", ""),
            props.get("ID_USB_DRIVER") != "option",
        ]):
            print(f"[SKIPPED] {port=}")
            continue

        # 5=Проверяем AT-ответ
        out = harvest.cmd_timeout__write_read__payload(
            f"stty -F {port} 115200 raw -echo 2>/dev/null; "
            f"cat {port} & sleep 0.1; "
            f"printf 'AT\\r\\n' > {port}; "
            f"sleep 0.3; "
            f"kill %1 2>/dev/null",
            timeout=3,
        )
        if "OK" not in out:
            continue

        result = port

        # 6=Настраиваем порт на постоянку (raw mode + отключаем эхо)
        assert harvest.cmd_timeout__check_executed_success(
            f"stty -F {port} 115200 raw -echo -echoe -echok -echoctl 2>/dev/null; "
            f"cat {port} & sleep 0.1; "
            f"printf 'ATE0\\r\\n' > {port}; "
            f"sleep 0.2; "
            f"kill %1 2>/dev/null",
            timeout=3,
        ), f"не удалось натсроить порт"

        if result:
            break

    assert result, f"порт устройства для отправки AT команд не найден! {port_candidates=}"

    # # убиваем ВСЕ процессы, которые могли остаться на порту
    # harvest.conn.write_bytes(f"fuser -k {result} 2>/dev/null")
    # time.sleep(0.5)

    print(f"[DETECTED] {result=}")
    return result


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
