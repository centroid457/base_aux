import pytest

from utils import HarvestDevice

from base_aux.buses.d1_serial2_new.m2_manager import SerialManager
from base_aux.buses.d1_serial2_new.m1_serial_client import SerialClient2


# =====================================================================================================================
manager = SerialManager()


# =====================================================================================================================
class Test_01__Detection:
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

    def test_3__harvest_detection(self, harvest):
        """
        Тест проверяет, что устройство успешно обнаружено,
        и выводит его уникальный идентификатор.
        """
        assert harvest, "Устройство Harvest не обнаружено."


# =====================================================================================================================
class Test_02__PreInstall:
    def test_0__internet(self, has_internet):
        assert has_internet

    # ---------------------------------------------------------------------------------------
    def test_1__picocom(self, harvest, has_internet):
        """
        Проверяет, доступна ли команда в системе linux

        ---- Sent utf8 encoded message: "which picocom\r\n" ----
        which picocom
        /usr/bin/picocom
        root@harvest05:~#
        root@harvest05:~#
        ---- Sent utf8 encoded message: "which picocom22\r\n" ----
        which picocom22
        root@harvest05:~#
        root@harvest05:~#

        ---- Sent utf8 encoded message: "which picocom 2>/dev/null || echo NOT_FOUND\r\n" ----
        which picocom 2>/dev/null || echo NOT_FOUND
        /usr/bin/picocom
        root@harvest05:~#
        root@harvest05:~# [17686.556981] IPv6: ADDRCONF(NETDEV_UP): wlan0: link is not ready
        ---- Sent utf8 encoded message: "which picocom1111 2>/dev/null || echo NOT_FOUND\r\n" ----
        which picocom1111 2>/dev/null || echo NOT_FOUND
        NOT_FOUND
        root@harvest05:~#
        root@harvest05:~#
        """
        if not harvest._cmd__check_success(f"which picocom"):
            assert has_internet, "нет интернета для установки пакетов"
            assert harvest.apt_install("picocom")

    def test_2__python(self, harvest, has_internet):
        if not harvest._cmd__check_success(f"which python3"):
            assert has_internet, "нет интернета для установки пакетов"
            assert harvest.apt_install("python3")

    def test_3__python_serial(self, harvest, has_internet):
        """
        ---- Sent utf8 encoded message: "python3 -c \"import serial\" || echo ERROR_MSG\r\n" ----
        python3 -c "import serial" || echo ERROR_MSG
        root@harvest05:~#
        root@harvest05:~#

        --- Sent utf8 encoded message: "python3 -c \"import serial123\" || echo ERROR_MSG\r\n" ----
        python3 -c "import serial123" || echo ERROR_MSG
        Traceback (most recent call last):
          File "<string>", line 1, in <module>
        ModuleNotFoundError: No module named 'serial123'
        ERROR_MSG
        root@harvest05:~#
        root@harvest05:~#
        """
        if not harvest._cmd__check_success(f'python3 -c "import serial"'):
            assert has_internet, "нет интернета для установки пакетов"
            assert harvest.apt_install("python3-serial")


# =====================================================================================================================
class Test_1__GNSS:
    def test__gnss_exists(self, harvest):
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
        assert harvest._cmd__check_success("ls /dev/ttyUSB0"), "Порт GNSS не найден"

    def test__nmea_output(self, harvest):
        # Настраиваем порт и читаем несколько строк
        harvest.conn.write_bytes("stty -F /dev/ttyUSB0 9600 raw -echo")
        harvest.conn.write_bytes("timeout 5 cat /dev/ttyUSB0")
        out = harvest.conn.read_lines(timeout_start=0.5, timeout_continue=5)
        assert "$GNGGA" in out or "$GNRMC" in out, "NMEA-предложения не получены"


# =====================================================================================================================
