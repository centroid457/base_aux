import pytest

from utils import HarvestDevice

from base_aux.buses.d1_serial2_new.m2_manager import SerialManager
from base_aux.buses.d1_serial2_new.m1_serial_client import SerialClient2


# =====================================================================================================================
@pytest.fixture(scope="session")
def harvest() -> HarvestDevice:
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
        yield found[0]


# =====================================================================================================================
@pytest.fixture(scope="session")
def internet_access(harvest) -> bool:
    return harvest.check__has_internet()


# =====================================================================================================================
@pytest.fixture(scope="session")
def present__gnss(harvest):
    """
    ---- Sent utf8 encoded message: "ls /dev/ttyUSB0\r\n" ----
    ls /dev/ttyUSB0
    /dev/ttyUSB0
    root@harvest05:~#
    root@harvest05:~#
    ---- Sent utf8 encoded message: "ls /dev/ttyUSB1\r\n" ----
    ls /dev/ttyUSB1
    ls: cannot access '/dev/ttyUSB1': No such file or directory
    root@harvest05:~#
    root@harvest05:~#
    """
    return harvest.cmd__check_executed_success("ls /dev/ttyUSB0")


@pytest.fixture(scope="session")
def present__wifi(harvest):
    """

    ---- Sent utf8 encoded message: "ip link show wlan0 2>/dev/null || echo ERROR_MSG\r\n" ----
    ip link show wlan0 2>/dev/null || echo ERROR_MSG
    2: wlan0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc pfifo_fast state DOWN mode DORMANT group default qlen 1000
        link/ether ca:f0:e5:d6:0c:79 brd ff:ff:ff:ff:ff:ff
    root@harvest05:~#
    root@harvest05:~#
    ---- Sent utf8 encoded message: "ip link show wlan1 2>/dev/null || echo ERROR_MSG\r\n" ----
    ip link show wlan1 2>/dev/null || echo ERROR_MSG
    ERROR_MSG
    root@harvest05:~#
    root@harvest05:~#


    ---- Sent utf8 encoded message: "ip link show wlan0\r\n" ----
    ip link show wlan0
    2: wlan0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc pfifo_fast state DOWN mode DORMANT group default qlen 1000
        link/ether ca:f0:e5:d6:0c:79 brd ff:ff:ff:ff:ff:ff
    root@harvest05:~#
    root@harvest05:~#
    ---- Sent utf8 encoded message: "ip link show wlan1\r\n" ----
    ip link show wlan1
    Device "wlan1" does not exist.
    root@harvest05:~#
    root@harvest05:~#
    """
    return harvest.cmd__check_executed_success("ip link show wlan0")


@pytest.fixture(scope="session")
def present__bt(harvest):
    """Проверяет, виден ли Bluetooth интерфейс."""
    return harvest.cmd__check_executed_success("hciconfig hci0")


@pytest.fixture(scope="session")
def present__gsm(harvest):
    """Проверяет, виден ли интерфейс GSM (usb0)."""
    return harvest.cmd__check_executed_success("ip link show usb0")


@pytest.fixture(scope="session")
def present__rfid_script(harvest):
    """Проверяет наличие RFID-скрипта."""
    return harvest.cmd__check_executed_success("ls /root/e710.py")


# =====================================================================================================================
