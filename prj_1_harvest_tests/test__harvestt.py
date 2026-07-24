import pytest

from utils import HarvestDevice

from base_aux.buses.d1_serial2_new.m2_manager import SerialManager
from base_aux.buses.d1_serial2_new.m1_serial_client import SerialClient2
from base_aux.aux_eq.m3_eq_valid3_derivatives import *


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
    def pkg__check_installed_or_install(self, harvest, internet_access, pkg_name: str):
        if not harvest.cmd__check_success(f"which {pkg_name}"):
            assert internet_access, f"Нет интернета для установки пакетов {pkg_name}"
            assert harvest.apt_install(pkg_name)

    # ---------------------------------------------------------------------------------------
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
        if not harvest.cmd__check_success(f'python3 -c "import serial"'):
            assert internet_access, "нет интернета для установки пакетов"
            assert harvest.apt_install("python3-serial")

    # @pytest.mark.skip("just for now")
    def test_pre_5__wifi_1__iw(self, harvest, internet_access):
        self.pkg__check_installed_or_install(harvest, internet_access, "iw")

    def test_pre_5__wifi_2__bluez(self, harvest, internet_access):
        self.pkg__check_installed_or_install(harvest, internet_access, "bluez")

    def test_pre_5__wifi_3__usbutils(self, harvest, internet_access):
        self.pkg__check_installed_or_install(harvest, internet_access, "usbutils")


# =====================================================================================================================
class Test_1__GNSS:
    MNEA_VALIDATE: dict[str, Base_EqValid | None] = {
        "$GPGSV": EqValid_Regexp(),
        "$GLGSV": None,

        "$GNGSA": None,
        "$GNGGA": None,

        "$GNRMC": None,

        "$GNGLL": None,
    }

    def test_gnss_1__gnss_exists(self, present__gnss):
        assert present__gnss, "GNSS не найден"

    def test_gnss_2__nmea_output_exists(self, harvest):
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

        harvest.cmd__send_with_timeout("cat /dev/ttyUSB0")
        output = harvest.conn.read_lines(timeout_continue=1)

        for msg_type, data in gnss_data.items():
            gnss_data[msg_type] = set(filter(lambda line: line.startswith(msg_type), output))

        for msg_type, data in gnss_data.items():
            assert data, f"NMEA-предложения {msg_type=} не получены {data=}"
            print(f"NMEA-предложения {msg_type=} получены {data=}")

    @pytest.mark.skip("Not realised yet")
    def test_gnss_3__nmea_output_correct(self, harvest):
        # FIXME: explore values without correct data!
        pass


# =====================================================================================================================
class Test_21__WiFi:
    def test_wf_1__interface_exists(self, harvest, present__wifi):
        assert present__wifi, "Wi-Fi интерфейс wlan0 не обнаружен"

    def test_wf_2__link_connected(self, harvest, present__wifi):
        """Получение данных о текущем подключении."""
        if not present__wifi:
            pytest.skip("Wi-Fi отсутствует")

        # assert harvest.cmd__check_success("iw dev wlan0 link"), "Команда iw dev wlan0 link вернула ошибку"
        stdout_connected = harvest.conn.write_read_lines("iw dev wlan0 link")
        assert "Not connected." not in stdout_connected, "нет соединения по WiFi"

    def test_wf_3__signal_quality(self, harvest, present__wifi):
        """Валидация: уровень сигнала не хуже порога."""
        if not present__wifi:
            pytest.skip("Wi-Fi отсутствует")

        # получаем строку с signal
        harvest.conn.write_bytes("iw dev wlan0 link | grep signal")
        lines = harvest.conn.read_lines(timeout_continue=1)
        # ожидаемый формат: "signal: -XX dBm"
        for line in lines:
            if "signal:" in line:
                try:
                    value_str = line.split("signal:")[1].strip().split()[0]
                    rssi = int(value_str)
                    assert rssi > -85, f"Слишком слабый сигнал Wi-Fi: {rssi} dBm"
                    return
                except Exception:
                    pass
        pytest.fail(f"Не удалось извлечь уровень сигнала Wi-Fi/{lines=}")


# ----------------------------------------------------------------------------------------------------------------------
class Test_22__Bluetooth:
    """Тесты Bluetooth (тот же чип что и WiFi)"""
    def test_bt_1__interface_exists(self, harvest, present__bt):
        """Физическое наличие адаптера."""
        assert present__bt, "Bluetooth интерфейс hci0 не обнаружен"

    def test_bt_2__scan_devices(self, harvest, present__bt):
        """Получение данных: сканирование устройств."""
        if not present__bt:
            pytest.skip("Bluetooth отсутствует")

        # запускаем короткое сканирование (bluetoothctl или hcitool)
        # используем bluetoothctl, так как он обычно есть
        harvest.conn.write_bytes("bluetoothctl -- scan on & sleep 2; bluetoothctl -- scan off")
        output = harvest.conn.read_lines(timeout_continue=3)
        # Ищем строки с "Device" (новый BLE/BR) в выводе
        devices_found = [line for line in output if "Device" in line]
        assert len(devices_found) > 0, "Не обнаружено ни одного Bluetooth-устройства"

    def test_bt_3__scan_devices_count(self, harvest, present__bt):
        """Валидация: должно быть хотя бы 2 устройства (если окружение не пустое)."""
        if not present__bt:
            pytest.skip("Bluetooth отсутствует")

        harvest.conn.write_bytes("bluetoothctl -- scan on & sleep 3; bluetoothctl -- scan off")
        output = harvest.conn.read_lines(timeout_continue=4)
        devices = [line for line in output if "Device" in line and "RSSI" in line]  # bluetoothctl обычно выводит RSSI
        # Если окружение заведомо насыщенное, порог можно поднять
        assert len(devices) >= 2, f"Найдено только {len(devices)} устройств, ожидалось >= 2"


# =====================================================================================================================
class Test_3__GSM:
    """Тесты GSM-модема (интерфейс usb0)"""

    def test_gsm_1__interface_exists(self, harvest, present__gsm):
        """Физическое наличие модема."""
        assert present__gsm, "GSM-интерфейс usb0 не обнаружен"

    def test_gsm_2__sim_detected(self, harvest, present__gsm):
        """Получение данных: проверка SIM-карты через AT."""
        if not present__gsm:
            pytest.skip("GSM отсутствует")

        # Ищем порт AT-команд (обычно /dev/ttyUSB2)
        # Проверяем, что порт существует и отвечает
        harvest.conn.write_bytes('echo -e "AT+CPIN?\\r\\n" > /dev/ttyUSB2 && cat /dev/ttyUSB2 & sleep 0.5; kill %1')
        output = harvest.conn.read_lines(timeout_continue=1.5)
        # Ищем строку с +CPIN: READY или SIM PIN
        ready = any("+CPIN: READY" in line for line in output)
        assert ready, "SIM-карта не готова или модем не отвечает"

    def test_gsm_3__network_registration(self, harvest, present__gsm):
        """Валидация: регистрация в сети."""
        if not present__gsm:
            pytest.skip("GSM отсутствует")

        harvest.conn.write_bytes('echo -e "AT+CREG?\\r\\n" > /dev/ttyUSB2 && cat /dev/ttyUSB2 & sleep 0.5; kill %1')
        output = harvest.conn.read_lines(timeout_continue=1.5)
        # Ищем +CREG: 0,1 или 0,5 (зарегистрирован)
        registered = any("+CREG: " in line and (line.endswith("1") or line.endswith("5")) for line in output)
        assert registered, "Модем не зарегистрирован в сотовой сети"

    def test_gsm_4__signal_quality(self, harvest, present__gsm):
        """Валидация уровня сигнала (RSSI > 5)."""
        if not present__gsm:
            pytest.skip("GSM отсутствует")

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


# =====================================================================================================================
class Test_4__RFID:
    """Тесты RFID-считывателя (скрипт e710.py)"""
    def test_rfid_1__script_exists(self, harvest, present__rfid_script):
        """Физическое наличие скрипта."""
        assert present__rfid_script, "Скрипт /root/e710.py не найден"

    def test_rfid_2__execution_no_error(self, harvest, present__rfid_script):
        """Получение данных: скрипт запускается и завершается без ошибок."""
        if not present__rfid_script:
            pytest.skip("Скрипт RFID отсутствует")
        harvest.conn.write_bytes("timeout 2 python3 /root/e710.py")  # используем timeout для завершения
        output = harvest.conn.read_lines(timeout_continue=3)
        # Ищем признаки ошибок
        has_traceback = any("Traceback" in line for line in output)
        assert not has_traceback, "Скрипт RFID завершился с ошибкой"

    def test_rfid_3__valid_response_present(self, harvest, present__rfid_script):
        """Валидация: при наличии меток скрипт должен выдавать данные."""
        if not present__rfid_script:
            pytest.skip("Скрипт RFID отсутствует")
        harvest.conn.write_bytes("timeout 3 python3 /root/e710.py")
        output = harvest.conn.read_lines(timeout_continue=4)
        # В работающем состоянии вывод содержит шестнадцатеричные данные (например, b'...')
        # или сообщение 'tmout'. Главное — не пустой и не только ошибки.
        # Проверяем, что есть хотя бы одна строка с данными или 'tmout'.
        has_data = any("tmout" in line or "b'" in line or "b\"" in line for line in output)
        assert has_data, "RFID-скрипт не вернул ни данных, ни таймаутов"


# =====================================================================================================================
