import pytest

from .utils import HarvestDevice

from base_aux.buses.d1_serial2_new.m2_manager import SerialManager
from base_aux.buses.d1_serial2_new.m1_serial_client import SerialClient2
from base_aux.aux_eq.m3_eq_valid3_derivatives import *


# ======================================================================================================================
manager = SerialManager()


# ======================================================================================================================
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


# ======================================================================================================================
class Test_02__PreInstall:
    # ------------------------------------------------------------------------------------------------------------------
    def pkg__check_installed_or_install(self, harvest, internet_access, name_check: str, name_install: str | None = None):
        name_install = name_install or name_check
        if not harvest.cmd__check_executed_success(f"which {name_check}"):
            assert internet_access, f"Нет интернета для установки пакетов {name_check}"
            assert harvest.apt_install(name_install)

    # ------------------------------------------------------------------------------------------------------------------
    def test_pre_0__internet(self, internet_access):
        assert internet_access

    def test_pre_1__coreutils_timeout(self, harvest, internet_access):
        self.pkg__check_installed_or_install(harvest, internet_access, "timeout")

    def test_pre_2__picocom(self, harvest, internet_access):
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
        self.pkg__check_installed_or_install(harvest, internet_access, "picocom")

    def test_pre_3__python(self, harvest, internet_access):
        self.pkg__check_installed_or_install(harvest, internet_access, "python3")

    def test_pre_4__python_serial(self, harvest, internet_access):
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
        if not harvest.cmd__check_executed_success(f'python3 -c "import serial"'):
            assert internet_access, "нет интернета для установки пакетов"
            assert harvest.apt_install("python3-serial")

    # @pytest.mark.skip("just for now")
    def test_pre_5__wifi_1__iw(self, harvest, internet_access):
        self.pkg__check_installed_or_install(harvest, internet_access, "iw")

    def test_pre_5__wifi_2__bluez(self, harvest, internet_access):
        self.pkg__check_installed_or_install(harvest, internet_access, "bluetoothctl", "bluez")

    def test_pre_5__wifi_3__usbutils(self, harvest, internet_access):
        self.pkg__check_installed_or_install(harvest, internet_access, "lsusb", "usbutils")


# ======================================================================================================================
class Test_1__GNSS:
    MNEA_VALIDATE: dict[str, Base_EqValid | None] = {
        "$GPGSV": EqValid_Regexp(),
        "$GLGSV": None,

        "$GNGSA": None,
        "$GNGGA": None,

        "$GNRMC": None,
        "$GNGLL": None,
    }

    @pytest.mark.dependency(name="present__gnss")
    def test_gnss_1__device_present(self, harvest):
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
        assert harvest.cmd__check_executed_success("ls /dev/ttyUSB0"), "GNSS не найден"

    @pytest.mark.dependency(depends=["present__gnss", ])
    def test_gnss_2__device_responds(self, harvest):
        """
        1=BLOCK STAY LONG TIMУ on table
        ==================================
        ---- Sent utf8 encoded message: "cat /dev/ttyUSB0 & sleep 1.0; kill %1\r\n" ----
        cat /dev/ttyUSB0 & sleep 1.0; kill %1
        [1] 2008

        $GPGSV,4,1,13,01,16,181,11,03,65,133,,04,66,243,31,06,35,306,*77
        $GPGSV,4,2,13,09,31,251,,11,06,330,,16,01,125,27,17,02,253,*73
        $GPGSV,4,3,13,19,12,281,27,25,06,013,28,26,19,103,,28,23,046,23*76
        $GPGSV,4,4,13,31,46,069,*44
        $GLGSV,1,1,00*65

        ///

        $GNGLL,,,,,114728.00,V,N*5D
        $GNRMC,114729.00,V,,,,,,,240726,,,N*6E
        $GNVTG,,,,,,,,,N*2E
        $GNGGA,114729.00,,,,,0,00,99.99,,,,,,*70
        $GNGSA,A,1,,,,,,,,,,,,,99.99,99.99,99.99*2E
        $GNGSA,A,1,,,,,,,,,,,,,99.99,99.99,99.99*2E
        $GPGSV,4,1,13,01,16,181,,03,65,133,,04,66,243,30,06,35,306,15*72
        $GPGSV,4,2,13,09,31,251,21,11,06,330,17,16,01,125,,17,02,253,26*77
        $GPGSV,4,3,13,19,12,281,,25,06,013,26,26,19,103,,28,23,046,21*7F
        $GPGSV,4,4,13,31,45,069,25*40
        $GLGSV,1,1,00*65
        $GNGLL,,,,,114729.00,V,N*5C
        $GNRMC,114730.00,V,,,,,,,240726,,,N*66
        $GNVTG,,,,,,,,,N*2E
        $GNGGA,114730.00,,,,,0,00,99.99,,,,,,*78
        $GNGSA,A,1,,,,,,,,,,,,,99.99,99.99,99.99*2E
        $GNGSA,A,1,,,,,,,,,,,,,99.99,99.99,99.99*2E
        $GPGSV,4,1,13,01,16,181,,03,65,133,21,04,66,243,30,06,35,306,14*70
        $GPGSV,4,2,13,09,31,251,18,11,06,330,17,16,01,125,,17,02,253,25*7E
        $GPGSV,4,3,13,19,12,281,24,25,06,013,26,26,19,103,,28,23,046,21*79
        $GPGSV,4,4,13,31,45,069,25*40
        $GLGSV,1,1,00*65
        $GNGLL,,,,,114730.00,V,N*54
        $GNRMC,114731.00,V,,,,,,,240726,,,N*67
        $GNVTG,,,,,,,,,N*2E
        $GNGGA,114731.00,,,,,0,00,99.99,,,,,,*79
        $GNGSA,A,1,,,,,,,,,,,,,99.99,99.99,99.99*2E
        $GNGSA,A,1,,,,,,,,,,,,,99.99,99.99,99.99*2E
        $GPGSV,4,1,13,01,16,181,,03,65,133,21,04,66,243,30,06,35,306,*75
        $GPGSV,4,2,13,09,31,251,16,11,06,330,15,16,01,125,,17,02,253,26*71
        $GPGSV,4,3,13,19,12,281,22,25,06,013,26,26,19,103,,28,23,046,21*7F
        $GPGSV,4,4,13,31,45,069,25*40
        $GLGSV,1,1,00*65
        $GNGLL,,,,,114731.00,V,N*55
        $GNRMC,114732.00,V,,,,,,,240726,,,N*64
        $GNVTG,,,,,,,,,N*2E
        $GNGGA,114732.00,,,,,0,00,99.99,,,,,,*7A
        $GNGSA,A,1,,,,,,,,,,,,,99.99,99.99,99.99*2E
        $GNGSA,A,1,,,,,,,,,,,,,99.99,99.99,99.99*2E
        $GPGSV,4,1,13,01,16,181,,03,65,133,18,04,66,243,30,06,35,306,*7Froot@harvest05:~#
        [1]+  Terminated              cat /dev/ttyUSB0
        root@harvest05:~#
        """
        gnss_data: dict[str, set[str]] = dict.fromkeys(self.MNEA_VALIDATE)

        harvest.cmd_timeout__write_bytes("cat /dev/ttyUSB0")
        output = harvest.conn.read_lines(timeout_continue=1)

        for msg_type, data in gnss_data.items():
            gnss_data[msg_type] = set(filter(lambda line: line.startswith(msg_type), output))

        for msg_type, data in gnss_data.items():
            assert data, f"NMEA-предложения {msg_type=} не получены {data=}"
            print(f"NMEA-предложения {msg_type=} получены {data=}")

    @pytest.mark.dependency(depends=["present__gnss", ])
    def test_gnss_3__nmea_output_correct(self, harvest):
        # FIXME: explore values without correct data!
        pass


# ======================================================================================================================
class Test_21__Bluetooth:
    """Тесты Bluetooth (тот же чип что и WiFi)"""
    @pytest.mark.dependency(name="present__bt")
    def test_bt_1__device_present(self, harvest):
        """Проверяет, виден ли Bluetooth интерфейс."""
        assert harvest.cmd__check_executed_success("hciconfig hci0"), "Bluetooth интерфейс hci0 не обнаружен"

    @pytest.mark.dependency(depends=["present__bt", ])
    def test_bt_2__device_responds(self, harvest):
        """
        ---- Sent utf8 encoded message: "bluetoothctl -- scan on & sleep 2; bluetoothctl -- scan off\r\n" ----
        bluetoothctl -- scan on & sleep 2; bluetoothctl -- scan off
        [7] 3968
        Discovery started
        [CHG] Controller A6:20:96:B6:A9:5E Discovering: yes
        [NEW] Device 68:4E:05:DA:46:2C 403
        [NEW] Device 68:4E:05:DA:37:2E 405
        [NEW] Device E3:77:12:64:59:DE UltraSonic
        [NEW] Device C8:69:CD:28:12:BA C8-69-CD-28-12-BA
        [NEW] Device 47:CD:B2:66:05:A7 47-CD-B2-66-05-A7
        [NEW] Device FC:82:20:D6:82:CF COROS NOMAD BD4407
        [NEW] Device EB:1C:93:49:2D:D2 UltraSonic
        [NEW] Device 78:84:C0:B5:89:AA 78-84-C0-B5-89-AA
        [NEW] Device 54:F2:9F:0E:1E:D1 404
        [NEW] Device 43:05:75:66:62:C5 43-05-75-66-62-C5
        [NEW] Device CE:4A:2C:2D:67:47 UltraSonic
        [NEW] Device E5:C6:EB:4E:F3:05 UltraSonic
        [NEW] Device F6:D4:61:D3:B7:55 UltraSonic
        [NEW] Device CE:60:07:4B:72:02 UltraSonic
        [NEW] Device E9:B6:5B:44:1D:AC MTBO-NB
        [NEW] Device C7:22:DB:64:DC:AE MTBO-01-2G
        [NEW] Device 8C:26:AA:E8:88:13 8C-26-AA-E8-88-13
        [2]   Done                    bluetoothctl -- scan on
        [3]   Done                    bluetoothctl -- scan on
        [4]   Done                    bluetoothctl -- scan on
        [5]   Done                    bluetoothctl -- scan on
        [6]   Done                    bluetoothctl -- scan on
        Failed to stop discovery: org.bluez.Error.Failed
        root@harvest05:~#
        root@harvest05:~# [NEW] Device F8:5E:A0:93:C9:A1 d5420
        [CHG] Device EB:1C:93:49:2D:D2 RSSI: -75
        [CHG] Device 78:84:C0:B5:89:AA RSSI: -80
        [CHG] Device CE:4A:2C:2D:67:47 RSSI: -81
        [CHG] Device CE:60:07:4B:72:02 RSSI: -69
        [CHG] Device C7:22:DB:64:DC:AE RSSI: -103
        [NEW] Device 66:4E:D7:D9:93:3C 66-4E-D7-D9-93-3C
        [CHG] Device F8:5E:A0:93:C9:A1 RSSI: -75
        [CHG] Device FC:82:20:D6:82:CF RSSI: -84
        [CHG] Device CE:4A:2C:2D:67:47 RSSI: -71
        [CHG] Device E3:77:12:64:59:DE RSSI: -72
        [CHG] Device C7:22:DB:64:DC:AE RSSI: -94
        ---- Sent utf8 encoded message: "pkill bluetoothctl\r\n" ----
        pkill bluetoothctl
        root@harvest05:~#
        root@harvest05:~#
        """
        # запускаем короткое сканирование (bluetoothctl или hcitool)
        output = harvest.cmd_timeout__write_read_lines("bluetoothctl -- scan on", timeout=1, timeout_continue=2)

        # Ищем строки с "Device" (новый BLE/BR) в выводе
        result = False
        for line in output:
            print(f"{line=}")
            for expected in ["] Device", ]:
                if expected in line:
                    result = True
                    break

        assert result, "Не обнаружено ни одного Bluetooth-устройства"

    @pytest.mark.dependency(depends=["present__bt", ])
    def test_bt_3__scan_devices_count(self, harvest):
        """Валидация: должно быть хотя бы 2 устройства (если окружение не пустое)."""
        output = harvest.cmd_timeout__write_read_lines("bluetoothctl -- scan on", timeout=1, timeout_continue=2)

        # Считаем уникальные адреса
        addrs = set()
        for line in output:
            if "] Device" in line:
                # формат: [NEW] Device XX:XX:XX:XX:XX:XX ...
                parts = line.split()
                if len(parts) >= 3:
                    dev_id = parts[2]
                    addrs.add(dev_id)
                    print(f"{dev_id=}")

        assert len(addrs) >= 2, f"Найдено только {len(addrs)} Bluetooth-устройств, ожидалось >= 2"


# ----------------------------------------------------------------------------------------------------------------------
class Test_22__WiFi:
    @pytest.mark.dependency(name="present__wifi")
    def test_wf_1__device_present(self, harvest):
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
        assert harvest.cmd__check_executed_success("ip link show wlan0"), "Wi-Fi интерфейс wlan0 не обнаружен"

    @pytest.mark.dependency(depends=["present__wifi", ])
    def test_wf_2__device_responds(self, harvest):
        # assert harvest.cmd__check_success("iw dev wlan0 link"), "Команда iw dev wlan0 link вернула ошибку"
        stdout_connected = harvest.conn.write_read_lines("iw dev wlan0 link")
        assert "Not connected." not in stdout_connected, "нет соединения по WiFi"

    @pytest.mark.dependency(depends=["present__wifi", ])
    def test_wf_3__signal_quality(self, harvest):
        """Валидация: уровень сигнала не хуже порога."""
        # ожидаемый формат: "signal: -XX dBm"
        lines = harvest.conn.write_read_lines("iw dev wlan0 link | grep signal", timeout_continue=1)
        signal_line = [line for line in lines if 'signal:' in line]
        if not signal_line:
            pytest.fail("Не найдена строка signal")
        rssi_str = signal_line[0].split("signal:")[1].split()[0]
        rssi = int(rssi_str)
        assert rssi > -85
        pytest.fail(f"Не удалось извлечь уровень сигнала Wi-Fi/{lines=}")


# ======================================================================================================================
class Test_3__GSM:
    """Тесты GSM-модема (интерфейс usb0)"""

    @pytest.mark.dependency(name="present__gsm")
    def test_gsm_1__device_present(self, harvest):
        """Физическое наличие модема."""
        assert harvest.cmd__check_executed_success("ip link show usb0"), "GSM-интерфейс usb0 не обнаружен"

    @pytest.mark.dependency(depends=["present__gsm", ])
    def test_gsm_2__device_responds(self, harvest):
        raise NotImplementedError()

    @pytest.mark.dependency(depends=["present__gsm", ])
    def test_gsm_3__sim_detected(self, harvest):
        """Получение данных: проверка SIM-карты через AT."""
        # Ищем порт AT-команд (обычно /dev/ttyUSB2)
        # Проверяем, что порт существует и отвечает
        harvest.conn.write_bytes('echo -e "AT+CPIN?\\r\\n" > /dev/ttyUSB2 && cat /dev/ttyUSB2 & sleep 0.5; kill %1')
        output = harvest.conn.read_lines(timeout_continue=1.5)
        # Ищем строку с +CPIN: READY или SIM PIN
        ready = any("+CPIN: READY" in line for line in output)
        assert ready, "SIM-карта не готова или модем не отвечает"

    @pytest.mark.dependency(depends=["present__gsm", ])
    def test_gsm_4__network_registration(self, harvest):
        """Валидация: регистрация в сети."""
        harvest.conn.write_bytes('echo -e "AT+CREG?\\r\\n" > /dev/ttyUSB2 && cat /dev/ttyUSB2 & sleep 0.5; kill %1')
        output = harvest.conn.read_lines(timeout_continue=1.5)
        # Ищем +CREG: 0,1 или 0,5 (зарегистрирован)
        registered = any("+CREG: " in line and (line.endswith("1") or line.endswith("5")) for line in output)
        assert registered, "Модем не зарегистрирован в сотовой сети"

    @pytest.mark.dependency(depends=["present__gsm", ])
    def test_gsm_5__signal_quality(self, harvest):
        """Валидация уровня сигнала (RSSI > 5)."""
        harvest.conn.write_bytes('echo -e "AT+CSQ\\r\\n" > /dev/ttyUSB2 && cat /dev/ttyUSB2 & sleep 0.5; kill %1')
        output = harvest.conn.read_lines(timeout_continue=1.5)
        for line in output:
            if "+CSQ:" in line:
                try:
                    # формат +CSQ: <rssi>,<ber>
                    parts = line.replace("+CSQ:", "").strip().split(",")
                    rssi = int(parts[0])
                    assert rssi >= 5, f"Низкий уровень сигнала GSM: {rssi} (из 31)"
                    return
                except Exception:
                    pass
        pytest.fail("Не удалось извлечь уровень сигнала GSM")


# ======================================================================================================================
class Test_4__RFID:
    """Тесты RFID-считывателя (скрипт e710.py)"""
    def test_rfid_01__script_send(self, harvest):
        """Физическое наличие скрипта."""
        assert False, "не получилось отправить скрипт"

    def test_rfid_02__script_present(self, harvest):
        """Физическое наличие скрипта."""
        assert False, "Скрипт /root/e710.py не найден"

    def test_rfid_1__device_present(self, harvest):
        raise NotImplementedError()

    def test_rfid_2__device_responds(self, harvest):
        raise NotImplementedError()

    def test_rfid_2__execution_no_error(self, harvest):
        """Получение данных: скрипт запускается и завершается без ошибок."""
        harvest.conn.write_bytes("timeout 2 python3 /root/e710.py")  # используем timeout для завершения
        output = harvest.conn.read_lines(timeout_continue=3)
        # Ищем признаки ошибок
        has_traceback = any("Traceback" in line for line in output)
        assert not has_traceback, "Скрипт RFID завершился с ошибкой"

    def test_rfid_3__valid_response_present(self, harvest):
        """Валидация: при наличии меток скрипт должен выдавать данные."""
        harvest.conn.write_bytes("timeout 3 python3 /root/e710.py")
        output = harvest.conn.read_lines(timeout_continue=4)
        # В работающем состоянии вывод содержит шестнадцатеричные данные (например, b'...')
        # или сообщение 'tmout'. Главное — не пустой и не только ошибки.
        # Проверяем, что есть хотя бы одна строка с данными или 'tmout'.
        has_data = any("tmout" in line or "b'" in line or "b\"" in line for line in output)
        assert has_data, "RFID-скрипт не вернул ни данных, ни таймаутов"


# ======================================================================================================================
