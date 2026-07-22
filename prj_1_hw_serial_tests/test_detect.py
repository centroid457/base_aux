import pytest
from serial_utils import *


# =====================================================================================================================
class Test__HarvestDetection:
    def test_1__exist_ports(self):
        result = manager.ADDRESSES_CASHED
        print(f"\nPORTS_EXISTED[{result}]")
        assert result != [], "Не обнаружено ни одного последовательного порта."

    def test_2__exist_can_open(self):
        exist_opening__ok = []
        exist_opening__fail = []

        for port in manager.ADDRESSES_CASHED:
            if manager.check__address_could_open(port):
                exist_opening__ok.append(port)
            else:
                exist_opening__fail.append(port)

        print(f"{exist_opening__ok=}")
        print(f"{exist_opening__fail=}")
        assert exist_opening__ok != [], "Ни один порт не удалось открыть."

    def test_3__dut_detection(self, device):
        """
        Тест проверяет, что устройство успешно обнаружено,
        и выводит его уникальный идентификатор.
        """

        assert device is not None, "Устройство не подключено."
        assert device.device_name, "Не удалось получить идентификатор устройства."
        print(f"\n=== Устройство идентифицировано: {device.device_name} ===")


# =====================================================================================================================
