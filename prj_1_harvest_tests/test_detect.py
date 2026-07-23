import pytest
from serial_utils import *


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
    __has_internet: bool | None = None

    # ---------------------------------------------------------------------------------------
    def _check_success__stdline(self, harvest, cmd: str, timeout_continue: float = 1.5, **wr_kwargs) -> bool:
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
        ERROR_MSG = "ERROR_MSG"
        out = harvest.write_read_lines(f"{cmd} 2>/dev/null || echo {ERROR_MSG}", timeout_continue=timeout_continue, **wr_kwargs)
        print(f"{out=}")
        return ERROR_MSG not in out[1:]

    def _install_module(self, harvest, module: str, timeout_full_max: float = 30, **wr_kwargs) -> bool:
        """
        if need DELETE
            sudo apt remove picocom
        """

        result = self._check_success__stdline(harvest, f"apt install -y {module}", timeout_full_max=timeout_full_max, **wr_kwargs)
        return result

    def _check__has_internet(self, harvest) -> bool:
        """
        root@harvest05:~#
        ---- Sent utf8 encoded message: "ping -c 1 -W 2 8.8.8.8\r\n" ----
        ping -c 1 -W 2 8.8.8.8
        PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.

        --- 8.8.8.8 ping statistics ---
        1 packets transmitted, 0 received, 100% packet loss, time 0ms

        root@harvest05:~#
        """
        if self.__has_internet is None:
            self.__has_internet = self._check_success__stdline(
                harvest,
                "ping -c 1 -W 2 8.8.8.8",
                timeout_continue=1.5
            )
        return self.__has_internet

    # ---------------------------------------------------------------------------------------
    def test_1__picocom(self, harvest):
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
        if not self._check_success__stdline(harvest, f"which picocom"):
            assert self._check__has_internet(harvest), "нет интернета для установки пакетов"
            assert self._install_module(harvest, "picocom")

    def test_2__python(self, harvest):
        if not self._check_success__stdline(harvest, f"which python3"):
            assert self._check__has_internet(harvest), "нет интернета для установки пакетов"
            assert self._install_module(harvest, "python3")

    def test_3__python_serial(self, harvest):
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
        if not self._check_success__stdline(harvest, f'python3 -c "import serial"'):
            assert self._check__has_internet(harvest), "нет интернета для установки пакетов"
            assert self._install_module(harvest, "python3-serial")


# =====================================================================================================================
class Test_1__GNSS:
    @classmethod
    def setup_class(cls):
        assert True

    def test__device_exists(self, harvest):
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
        out = harvest.write_read_lines("ls /dev/ttyUSB0")
        assert "/dev/ttyUSB0" == out[1], "Порт GNSS не найден"

    def test__nmea_output(self, harvest):
        # Настраиваем порт и читаем несколько строк
        harvest.write_bytes("stty -F /dev/ttyUSB0 9600 raw -echo")
        harvest.write_bytes("timeout 5 cat /dev/ttyUSB0")
        out = harvest.read_lines(timeout_start=0.5, timeout_continue=5)
        assert "$GNGGA" in out or "$GNRMC" in out, "NMEA-предложения не получены"


# =====================================================================================================================
