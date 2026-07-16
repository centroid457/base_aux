import pytest
import serial.tools.list_ports

from serial_utils import *


# =====================================================================================================================
@pytest.fixture(scope="session")
def PORTS_EXISTED(request) -> list[str]:
    result = [port.device for port in serial.tools.list_ports.comports()]
    print(f"\nPORTS_EXISTED[{result}]")
    yield result


# =====================================================================================================================
@pytest.fixture(scope="session")
def device(request) -> DeviceConsole:
    console, port = find_device_port()
    print(f"\nУстройство найдено на порту: {port}, ID: {console.device_id}")
    yield console
    console.close()


# =====================================================================================================================
