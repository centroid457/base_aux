import pytest
from serial_utils import *


# =====================================================================================================================
class Test__HarvestDetection:
    harvest: SerialClient2 = None

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

    def test_3__harvest_detection(self):
        """
        Тест проверяет, что устройство успешно обнаружено,
        и выводит его уникальный идентификатор.
        """
        found: list[SerialClient2] = []
        for conn in manager.make__not_occupied(can_open=True, baudrate=115200):
            with conn:
                if manager.harvest__validate(conn):
                    dev_id = manager.harvest__take_name(conn)
                    conn.occupy(dev_id)
                    print(f"\n[HARVEST_FOUND]{conn}/{dev_id=}")
                    found.append(conn)

        assert found, "Устройств не обнаружено."

        self.harvest = found[0]
        assert self.harvest.device_name, "Не удалось получить идентификатор устройства."


# =====================================================================================================================
