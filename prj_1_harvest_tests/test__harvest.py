import re
import time

import pytest

from .utils import *

from base_aux.buses.d1_serial2_new.m2_manager import SerialManager
from base_aux.buses.d1_serial2_new.m1_serial_client import SerialClient2
from base_aux.aux_eq.m3_eq_valid3_derivatives import *


# ======================================================================================================================
manager = SerialManager()


def _rules__raws_hex__understanding():
    data_raw: bytes = b'\x00EXT CORE 3.01 (107900)'
    print("data_raw=", data_raw)
    # data_raw= b'\x00EXT CORE 3.01 (107900)'

    data_hex_from_raw: str = data_raw.hex()
    print("data_hex_from_raw=", data_hex_from_raw)
    # data_hex_from_raw= 0045585420434f524520332e3031202831303739303029

    data_raw_from_hex: bytes = bytes.fromhex(data_hex_from_raw)
    print("data_raw_from_hex=", data_raw_from_hex)
    # data_raw_from_hex= b'\x00EXT CORE 3.01 (107900)'


    # 2=если мы в начале имеем байтстроку самого hex --------------------
    output_hex_bytes = b'312c3331302c32342c30372c37392c3039362c2c30382c31352c3039392c32342a37380d0a2447504753562c342c322c31332c30392c34342c3132372c32342c31312c30332c3234392c2c31342c31332c3139302c2c31362c31332c3033372c2a37340d0a2447504753562c342c332c31332c31382c30352c3335382c2c32302c30392c3239362c32322c32312c35302c3236382c32312c32372c31382c3036342c2a37460d0a2447504753562c342c342c31332c33302c35352c3234322c2a34430d0a24474c4753562c312c312c30302a36350d0a24474e474c4c2c2c2c2c2c3135323833332e30302c562c4e2a35410d0ab5620a04fa0045585420434f52'
    print(output_hex_bytes)
    # b'312c3331302c32342c30372c37392c3039362c2c30382c31352c3039392c32342a37380d0a2447504753562c342c322c31332c30392c34342c3132372c32342c31312c30332c3234392c2c31342c31332c3139302c2c31362c31332c3033372c2a37340d0a2447504753562c342c332c31332c31382c30352c3335382c2c32302c30392c3239362c32322c32312c35302c3236382c32312c32372c31382c3036342c2a37460d0a2447504753562c342c342c31332c33302c35352c3234322c2a34430d0a24474c4753562c312c312c30302a36350d0a24474e474c4c2c2c2c2c2c3135323833332e30302c562c4e2a35410d0ab5620a04fa0045585420434f52'

    # КОРРЕКТНАЯ СТРОКА
    # output_hex_str = str(output_hex_bytes)[1:]    # НЕКОРРЕКТНО! кавычки остаются!
    output_hex_str = output_hex_bytes.decode('ascii')  # получаем чистую HEX-строку
    print(output_hex_str)
    # 312c3331302c32342c30372c37392c3039362c2c30382c31352c3039392c32342a37380d0a2447504753562c342c322c31332c30392c34342c3132372c32342c31312c30332c3234392c2c31342c31332c3139302c2c31362c31332c3033372c2a37340d0a2447504753562c342c332c31332c31382c30352c3335382c2c32302c30392c3239362c32322c32312c35302c3236382c32312c32372c31382c3036342c2a37460d0a2447504753562c342c342c31332c33302c35352c3234322c2a34430d0a24474c4753562c312c312c30302a36350d0a24474e474c4c2c2c2c2c2c3135323833332e30302c562c4e2a35410d0ab5620a04fa0045585420434f52

    output_raw = bytes.fromhex(output_hex_str)  # преобразуем в бинарные данные
    print(output_raw)
    # b'1,310,24,07,79,096,,08,15,099,24*78\r\n$GPGSV,4,2,13,09,44,127,24,11,03,249,,14,13,190,,16,13,037,*74\r\n$GPGSV,4,3,13,18,05,358,,20,09,296,22,21,50,268,21,27,18,064,*7F\r\n$GPGSV,4,4,13,30,55,242,*4C\r\n$GLGSV,1,1,00*65\r\n$GNGLL,,,,,152833.00,V,N*5A\r\n\xb5b\n\x04\xfa\x00EXT COR'


# ======================================================================================================================
@pytest.mark.skipif(True, reason="used for exploring executions/methods")
class Test_000__Explore:
    # WARN!!! DONT FORGET TURN OFF IT!!! else more of tests would failed!

    def test_1__devices_all__usb(self, harvest):
        harvest.get_info__usb_all(EqValid_Regexp(r"ttyS\d"))

    def test_2__rfid_script(self, harvest):
        scriptname = "/tmp/rfid_scan.py"
        assert harvest.file_name__push(scriptname)

        command_line = f"python3 {scriptname}"
        output = harvest.cmd_timeout__write_read__payload(
            command_line,
            # stop_line=EqValid_Regexp(rb'found=\d+epc'),
            timeout_continue=10,
        )
        print(f"FINISH")


# ======================================================================================================================
@pytest.mark.DET
class Test_01__Detection:
    def test_serial_1__exist_ports(self):
        result = manager.ADDRESSES_CASHED
        print(f"\nPORTS_EXISTED[{result}]")
        assert result != [], "Не обнаружено ни одного последовательного порта."

    def test_serial_2__exist_can_open(self):
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

    def test_serial_3__harvest_detection(self, harvest):
        """
        Тест проверяет, что устройство успешно обнаружено,
        и выводит его уникальный идентификатор.
        """
        assert harvest, "Устройство Harvest не обнаружено."

    @pytest.mark.skipif(True, reason="bad work!!!")
    def test_serial_4__harvest_info(self, harvest_info):
        print(json.dumps(harvest_info, indent=2, ensure_ascii=False))
        assert harvest_info, "Устройство Harvest не обнаружено."


# ======================================================================================================================
@pytest.mark.PRE
class Test_02__PreInstall:
    # ------------------------------------------------------------------------------------------------------------------
    def pkg__check_installed_or_install(self, harvest, internet_access, name_check: str, name_install: str | None = None) -> None | NoReturn:
        name_install = name_install or name_check
        if not harvest.cmd_timeout__check_executed_success(f"which {name_check}"):
            assert internet_access, f"Нет интернета для установки пакетов {name_check}"
            assert harvest.apt_install(name_install)

    # ------------------------------------------------------------------------------------------------------------------
    def test_pre_0__internet(self, internet_access):
        assert internet_access, "НЕТ ИНТЕРНЕТА"

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
        if not harvest.cmd_timeout__check_executed_success(f'python3 -c "import serial"'):
            assert internet_access, "нет интернета для установки пакетов"
            assert harvest.apt_install("python3-serial")

    # @pytest.mark.skip("just for now")
    def test_pre_5__wifi1__iw(self, harvest, internet_access):
        self.pkg__check_installed_or_install(harvest, internet_access, "iw")

    def test_pre_5__wifi2__bluez(self, harvest, internet_access):
        self.pkg__check_installed_or_install(harvest, internet_access, "bluetoothctl", "bluez")

    def test_pre_5__wifi3__usbutils(self, harvest, internet_access):
        self.pkg__check_installed_or_install(harvest, internet_access, "lsusb", "usbutils")

    # ------------------------------------------------------------------------------------------------------------------
    def test_pre_6__push1__ubx(self, harvest):
        assert harvest.file_name__push("/tmp/get__gnss_info__ubx.py"), "скрипт не отправился"

    def test_pre_6__push2__at_client(self, harvest):
        assert harvest.file_name__push("/tmp/at_client.py"), "скрипт не отправился"

    def test_pre_6__push3__rfid_scan(self, harvest):
        assert harvest.file_name__push("/tmp/rfid_scan.py"), "скрипт не отправился"


# ======================================================================================================================
@pytest.mark.GNSS
class Test_1__GNSS:
    MNEA_VALIDATE: dict[str, Base_EqValid | None] = {
        "$GPGSV": EqValid_Regexp(),
        "$GLGSV": None,

        "$GNGSA": None,
        "$GNGGA": None,

        "$GNRMC": None,
        "$GNGLL": None,
    }

    @pytest.mark.dependency(name="gnss_present")
    def test_gnss_1__present(self, harvest):
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
        assert harvest.cmd_timeout__check_executed_success("ls /dev/ttyUSB0"), "GNSS не найден"

    @pytest.mark.dependency(depends=["gnss_present", ])
    def test_gnss_2__quick__nmea_flow(self, harvest):
        """
        1=BLOCK STAY LONG TIME on table
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
        gnss_collected: dict[str, set[str]] = dict.fromkeys(self.MNEA_VALIDATE)

        output = harvest.cmd_timeout__write_read_lines("cat /dev/ttyUSB0", timeout=1, timeout_continue=1, return_str=False)

        for msg_type, data in gnss_collected.items():
            gnss_collected[msg_type] = set(filter(lambda line: line.startswith(msg_type), output))

        for msg_type, data in gnss_collected.items():
            assert data, f"NMEA-предложения {msg_type=} не получены {data=}"
            print(f"NMEA-{msg_type} получены {data=}")

    @pytest.mark.dependency(depends=["gnss_present", ])
    def test_gnss_3__deep1__pids(self, harvest):
        props = harvest.get_info__usb("/dev/ttyUSB0")
        assert props, "данные устройства не получены"

    @pytest.mark.dependency(depends=["gnss_present", ])
    def test_gnss_3__deep2__ubx(self, harvest):
        """

        UBX_RESPONSE:b5620a04fa0045585420434f524520332e3031202831303739303029000000000000000030303038303030300000524f4d204241534520332e3031202831303738383829000000000000000046575645523d53504720332e30310000000000000000000000000000000050524f545645523d31382e303000000000000000000000000000000000004d4f443d4e454f2d4d384e2d3000000000000000000000000000000000004649533d30784546343031352028313030313131290000000000000000004750533b474c4f3b47414c3b424453000000000000000000000000000000534241533b494d45533b515a535300000000000000000000000000000000
        root@harvest05:~#

        FULL: b'python3 /tmp/get__gnss_info__ubx.py\r\n\r\n/dev/ttyUSB0:          682\r\n\x1b[?2004hroot@harvest05:~# \r\n\x1b[?2004l\r\x1b[?2004hroot@harvest05:~# python3 /tmp/get__gnss_info__ubx.py\r\n\x1b[?2004l\rUBX_RESPONSE:[b5620a04fa0045585420434f524520332e3031202831303739303029000000000000000030303038303030300000524f4d204241534520332e3031202831303738383829000000000000000046575645523d53504720332e30310000000000000000000000000000000050524f545645523d31382e303000000000000000000000000000000000004d4f443d4e454f2d4d384e2d3000000000000000000000000000000000004649533d30784546343031352028313030313131290000000000000000004750533b474c4f3b47414c3b424453000000000000000000000000000000534241533b494d45533b515a5353000000000000000000000000000000005800]\r\n\x1b[?2004hroot@harvest05:~# \r\n\x1b[?2004l\r\x1b[?2004hroot@harvest05:~# '
            output_hex_bytes=b'b5620a04fa0045585420434f524520332e3031202831303739303029000000000000000030303038303030300000524f4d204241534520332e3031202831303738383829000000000000000046575645523d53504720332e30310000000000000000000000000000000050524f545645523d31382e303000000000000000000000000000000000004d4f443d4e454f2d4d384e2d3000000000000000000000000000000000004649533d30784546343031352028313030313131290000000000000000004750533b474c4f3b47414c3b424453000000000000000000000000000000534241533b494d45533b515a5353000000000000000000000000000000005800'
            output_hex_str='b5620a04fa0045585420434f524520332e3031202831303739303029000000000000000030303038303030300000524f4d204241534520332e3031202831303738383829000000000000000046575645523d53504720332e30310000000000000000000000000000000050524f545645523d31382e303000000000000000000000000000000000004d4f443d4e454f2d4d384e2d3000000000000000000000000000000000004649533d30784546343031352028313030313131290000000000000000004750533b474c4f3b47414c3b424453000000000000000000000000000000534241533b494d45533b515a5353000000000000000000000000000000005800'
            raw_data=b'\xb5b\n\x04\xfa\x00EXT CORE 3.01 (107900)\x00\x00\x00\x00\x00\x00\x00\x0000080000\x00\x00ROM BASE 3.01 (107888)\x00\x00\x00\x00\x00\x00\x00\x00FWVER=SPG 3.01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00PROTVER=18.00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00MOD=NEO-M8N-0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00FIS=0xEF4015 (100111)\x00\x00\x00\x00\x00\x00\x00\x00\x00GPS;GLO;GAL;BDS\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00SBAS;IMES;QZSS\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00X\x00'
        {
          "sw_version": "EXT CORE 3.01 (107900)",
          "hw_version": "00080000",
          "extensions": [
            "ROM BASE 3.01 (107888)",
            "FWVER=SPG 3.01",
            "PROTVER=18.00",
            "MOD=NEO-M8N-0",
            "FIS=0xEF4015 (100111)",
            "GPS;GLO;GAL;BDS",
            "SBAS;IMES;QZSS"
          ]
        }
        """
        for attempt in range(3):
            print(f"Попытка {attempt=}: UBX_RESPONSE поиск...")

            # Убиваем предыдущие экземпляры скрипта и освобождаем порт
            harvest.conn.write_read_bytes('pkill -9 -f get__gnss_info__ubx.py; fuser -k /dev/ttyUSB0; sleep 0.5')

            output = harvest.conn.write_read_bytes('python3 /tmp/get__gnss_info__ubx.py', timeout_continue=5)
            assert output, "данные от устройства не получены вообще"

            if b'UBX_RESPONSE:[' in output:
                # Извлекаем HEX-строку --------------------
                print(f"FULL: {output}")

                match = re.search(rb'UBX_RESPONSE:\[([0-9a-fA-F]*)\]', output)
                assert match, "Не найден корректный UBX_RESPONSE в выводе"
                output_hex_bytes = match.group(1)
                print(f"\t{output_hex_bytes=}")

                output_hex_str: str = output_hex_bytes.decode('ascii')  # получаем чистую HEX-строку
                print(f"\t{output_hex_str=}")

                # Декодируем HEX-строку в настоящие байты
                try:
                    raw_data: bytes = bytes.fromhex(output_hex_str)
                    print(f"\t{raw_data=}")
                except ValueError:
                    assert False, f"Невалидная HEX-строка: {output_hex_str!r}"

                result = harvest.parse__gnss_info__UBX(raw_data)
                print(json.dumps(result, indent=2))

                if result:
                    return True
            else:
                time.sleep(1)

        # FINAL --------------------------
        assert False, "После нескольких попыток UBX_RESPONSE так и не был получен"


# ======================================================================================================================
@pytest.mark.BT
class Test_2__Bluetooth:
    """Тесты Bluetooth (тот же чип что и WiFi)"""
    @pytest.mark.dependency(name="bt_present")
    def test_bt_1__present(self, harvest):
        """
        ---- Sent utf8 encoded message: "hciconfig\r\n" ----
        hciconfig
        hci0:   Type: Primary  Bus: UART
                BD Address: A6:20:96:B6:A9:5E  ACL MTU: 1021:8  SCO MTU: 64:1
                UP RUNNING
                RX bytes:71478 acl:1555 sco:0 events:879 errors:0
                TX bytes:2897 acl:33 sco:0 commands:102 errors:0

        root@harvest05:~#
        """
        assert harvest.cmd_timeout__check_executed_success("hciconfig hci0"), "Bluetooth интерфейс hci0 не обнаружен"

    @pytest.mark.dependency(depends=["bt_present", ])
    def test_bt_2__quick__scan(self, harvest):
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
        output = harvest.cmd_timeout__write_read__payload("bluetoothctl -- scan on", timeout=1, timeout_continue=1)
        assert "Discovery started" in output, "Bluetooth поиск не запустился"

        # пример строки: [NEW] Device 68:4E:05:DA:46:2C 403
        bt_scaned = re.findall(r'\s*Device\s\S+\s(.+)\s*\n*', output)
        assert bt_scaned, f"Не обнаружено ни одного Bluetooth-устройства {bt_scaned=}"

    @pytest.mark.dependency(depends=["bt_present", ])
    def test_bt_3__deep__info(self, harvest):
        """
        Полный дамп всей доступной информации о Bluetooth-модуле.
        Выполняется несколько команд, их вывод объединяется.
        """
        # Список команд для сбора информации
        commands = [
            "hciconfig hci0 -a",           # полная информация об интерфейсе
            "hciconfig hci0 version",      # версия прошивки/стека
            "hciconfig hci0 features",     # поддерживаемые функции
            "btmgmt info",                 # настройки контроллера (поддерживаемые/текущие)
            "bluetoothctl show",            # детали контроллера (UUID, режимы)
            "bluetoothctl list",            # список контроллеров
            "rfkill list bluetooth",        # состояние блокировок
        ]

        full_output: list[str] = []
        for cmd in commands:
            lines = harvest.cmd_timeout__write_read__payload(
                cmd,
                timeout_continue=1.5,
                return_str=False,
            )
            # добавляем заголовок и сам вывод
            full_output.append(f"--- {cmd} ---")
            if isinstance(lines, str):
                full_output.append(lines)
            else:
                full_output.extend(lines)
            full_output.append("")  # пустая строка-разделитель

        # Выводим в лог pytest (будет видно в отчёте)
        print("\n".join(full_output))

        # Минимальная валидация: в hciconfig version должен быть Manufacturer
        version_output = harvest.cmd_timeout__write_read__payload(
            "hciconfig hci0 version",
            timeout_continue=1.5,
        )
        assert "Manufacturer" in version_output, \
            "Не удалось получить производителя Bluetooth (возможно, модуль не инициализирован)"

        # Проверяем, что rfkill не показывает Hard blocked
        rfkill_output = harvest.cmd_timeout__write_read__payload(
            "rfkill list bluetooth",
            timeout_continue=1.5,
        )
        assert "Hard blocked: yes" not in rfkill_output, "Bluetooth аппаратно заблокирован (Hard blocked)"

    @pytest.mark.dependency(depends=["bt_present", ])
    def test_bt_4__deep__(self, harvest):
        pytest.skip("not realised")
        # TODO: check errors
        """
        2004hroot@harvest05:~# "
            printable=hciconfig hci0 -a
        
        hci0:	Type: Primary  Bus: UART
            BD Address: A6:20:96:B6:A9:5E  ACL MTU: 1021:8  SCO MTU: 64:1
            UP RUNNING 
            RX bytes:936753 acl:29093 sco:0 events:3626 errors:0
            TX bytes:5144 acl:117 sco:0 commands:216 errors:0
            Features: 0xbf 0xfe 0xcf 0xfe 0xdb 0xff 0x7b 0x87
            Packet type: DM1 DM3 DM5 DH1 DH3 DH5 HV1 HV2 HV3 
            Link policy: RSWITCH SNIFF 
            Link mode: PERIPHERAL ACCEPT 
            Name: 'harvest05'
            Class: 0x000000
            Service Classes: Unspecified
            Device Class: Miscellaneous, 
            HCI Version: 4.0 (0x6)  Revision: 0x6a
            LMP Version: 4.0 (0x6)  Subversion: 0x2209
            Manufacturer: Broadcom Corporation (15)
        
        root@harvest05:~#      
        """


# ----------------------------------------------------------------------------------------------------------------------
@pytest.mark.WIFI
class Test_3__WiFi:
    # Пороговые значения для оценки качества (можно вынести в конфиг)
    RSSI_MIN_OK = -75        # dBm – ниже этого уже внимание
    RSSI_MIN_CRITICAL = -85  # dBm – ниже этого ошибка
    BEACON_LOSS_MAX = 5      # за время сессии (если накопилось больше – проблема)
    TX_RETRIES_MAX_RATIO = 0.15  # 15% повторных передач от общего числа – подозрительно
    MIN_SCAN_NETWORKS = 3    # минимальное количество видимых сетей (если меньше – возможно антенна)

    @pytest.mark.dependency(name="wifi_present")
    def test_wf_1__present(self, harvest):
        """
        Проверяет наличие Wi-Fi интерфейса wlan0 и его тип.

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
        # Проверка существования
        assert harvest.cmd_timeout__check_executed_success(
            "ip link show wlan0"
        ), "Wi-Fi интерфейс wlan0 не обнаружен"

        # Дополнительная проверка, что это именно беспроводной интерфейс
        output = harvest.cmd_timeout__write_read__payload("iw dev wlan0 info")
        assert "wlan0" in output, "iw dev не видит wlan0"
        assert "type managed" in output.lower() or "type ap" in output.lower(), \
            f"wlan0 не является беспроводным интерфейсом: {output}"

    @pytest.mark.dependency(depends=["wifi_present"])
    def test_wf_3_deep__connected(self, harvest):
        """
        Проверяет текущее подключение к точке доступа:
        - уровень сигнала (RSSI)
        - частота/канал
        - скорости TX/RX битрейт
        - количество повторных передач и ошибок
        - beacon loss
        """
        # Убедимся, что есть соединение
        link_output = harvest.cmd_timeout__write_read__payload("iw dev wlan0 link")
        assert "Not connected." not in link_output, "Нет Wi-Fi соединения с сетью! НО МОЖЕТ ЭТО И НЕ НУЖНО??)))"

        # Извлекаем основные параметры через station dump (более информативно)
        station_output = harvest.cmd_timeout__write_read__payload("iw dev wlan0 station dump")
        print(f"Station dump:\n{station_output}")

        # Парсим station dump в словарь
        station_data = {}
        for line in station_output.splitlines():
            if ':' in line:
                k, v = line.split(':', 1)
                station_data[k.strip()] = v.strip()

        # Проверки
        rssi_str = station_data.get('signal', '-100')  # dBm
        rssi = int(rssi_str.split()[0]) if rssi_str else -100

        tx_bitrate = station_data.get('tx bitrate', 'unknown')
        rx_bitrate = station_data.get('rx bitrate', 'unknown')
        beacon_loss = int(station_data.get('beacon loss', '0'))
        tx_retries = int(station_data.get('tx retries', '0'))
        tx_packets = int(station_data.get('tx packets', '1'))  # чтобы делить
        retry_ratio = tx_retries / tx_packets if tx_packets else 0

        # assert'ы с пояснениями
        assert rssi >= self.RSSI_MIN_CRITICAL, \
            f"Критически низкий уровень сигнала Wi-Fi: {rssi} dBm (порог {self.RSSI_MIN_CRITICAL})"
        if rssi < self.RSSI_MIN_OK:
            print(f"ВНИМАНИЕ: пониженный уровень сигнала {rssi} dBm (желательно > {self.RSSI_MIN_OK})")

        assert beacon_loss <= self.BEACON_LOSS_MAX, \
            f"Слишком много потерянных beacon-ов: {beacon_loss} (допустимо {self.BEACON_LOSS_MAX})"

        if retry_ratio > self.TX_RETRIES_MAX_RATIO:
            print(f"ВНИМАНИЕ: высокая доля повторных передач {retry_ratio:.2%} (>{self.TX_RETRIES_MAX_RATIO:.0%})")

        # Выводим скорости для информации
        print(f"Скорость TX: {tx_bitrate}, RX: {rx_bitrate}")

    @pytest.mark.dependency(depends=["wifi_present"])
    def test_wf_3__deep__scan(self, harvest):
        """
        Выполняет сканирование и оценивает количество видимых сетей,
        уровни сигнала от ближайших точек доступа.
        Это необходимо для диагностики проблем с антенной:
        если не видно почти ничего, или все уровни аномально низкие,
        вероятен обрыв антенного тракта.

        ---- Sent utf8 encoded message: "iw dev wlan0 scan | grep -E 'on wlan0|SSID|signal|freq'\r\n" ----
        iw dev wlan0 scan | grep -E 'on wlan0|SSID|signal|freq'
        BSS 80:af:ca:f0:9d:8d(on wlan0) -- associated
                freq: 2417
                signal: -55.00 dBm
                SSID: Vest
        BSS 78:45:58:3a:38:db(on wlan0)
                freq: 2437
                signal: -77.00 dBm
                SSID: Element-T
                         * SSID List
        BSS 7e:45:58:3a:38:db(on wlan0)
                freq: 2437
                signal: -77.00 dBm
                SSID: Element_Guest
                         * SSID List
        BSS 82:45:58:3a:38:db(on wlan0)
                freq: 2437
                signal: -77.00 dBm
                SSID: Element-t_2Gz
                         * SSID List
        BSS 9c:9d:7e:75:00:5b(on wlan0)
                freq: 2437
                signal: -63.00 dBm
                SSID: Element-T_lab
                         * SSID List
                         * center freq segment 1: 8
                         * center freq segment 2: 0
        BSS cc:2d:e0:c2:7d:42(on wlan0)
                freq: 2452
                signal: -68.00 dBm
                SSID: MikroTik-C27D42
        BSS 50:ff:20:f5:08:cf(on wlan0)
                freq: 2452
                signal: -82.00 dBm
                SSID: Prometei-PG
        BSS c4:9a:31:fb:d2:2b(on wlan0)
                freq: 2462
                signal: -93.00 dBm
                SSID: SSR_WORK
                         * SSID List
                         * center freq segment 1: 11
                         * center freq segment 2: 0
        BSS c4:0a:cb:5c:d6:93(on wlan0)
                freq: 2412
                signal: -70.00 dBm
                SSID: Advanta_Messages
        BSS c4:0a:cb:5c:d6:94(on wlan0)
                freq: 2412
                signal: -74.00 dBm
                SSID: Advanta_Work
        BSS c4:0a:cb:5c:d6:95(on wlan0)
                freq: 2412
                signal: -71.00 dBm
                SSID: Advanta
        BSS d2:a4:6f:e6:fa:d2(on wlan0)
                freq: 2427
                signal: -74.00 dBm
                SSID: DIRECT-bQ-Pantum BM5100 Series
        BSS 86:45:58:3a:38:db(on wlan0)
                freq: 2437
                signal: -82.00 dBm
                SSID:
                         * SSID List
        BSS c6:2b:31:fb:d2:2f(on wlan0)
                freq: 2462
                signal: -92.00 dBm
                SSID:
                         * SSID List
                         * center freq segment 1: 11
                         * center freq segment 2: 0
        BSS c6:2b:31:fb:d2:20(on wlan0)
                freq: 2462
                signal: -91.00 dBm
                SSID: IKS_WORK
                         * SSID List
                         * center freq segment 1: 11
                         * center freq segment 2: 0
        root@harvest05:~#
        root@harvest05:~#
        """
        scan_output = harvest.cmd_timeout__write_read__payload(
            "iw dev wlan0 scan | grep SSID",
            timeout=10,
            timeout_continue=2
        )
        ssids = re.findall(r'\s*SSID:\s(.+)\s*\n*', scan_output)
        print(f"Wi-Fi scan {ssids=}")
        assert ssids, "сети не обнаружены"

        assert len(ssids) >= self.MIN_SCAN_NETWORKS, \
            f"Обнаружено мало сетей ({len(ssids)}), минимально ожидается {self.MIN_SCAN_NETWORKS}."

        # Собираем BSSID и уровни сигнала -----------------------------
        scan_output = harvest.cmd_timeout__write_read__payload(
            "iw dev wlan0 scan | grep signal",
            timeout=10,
            timeout_continue=2
        )
        signal_bds = re.findall(r'\s*signal:\s(.+)\sdBm\s*\n*', scan_output)
        signal_bds = [*map(float, signal_bds)]
        print(f"Wi-Fi quality {signal_bds=}")
        max_db = max(*signal_bds)
        print(f"Wi-Fi quality {max_db=}")
        assert max_db > self.RSSI_MIN_OK, "уровень сигнала слишком мал! проверьте антенну!"

    @pytest.mark.dependency(depends=["wifi_present"])
    def test_wf_3__deep__info(self, harvest):
        """
        Собирает максимальную информацию об адаптере:
        - версия прошивки/драйвера
        - MAC-адрес
        - поддерживаемые стандарты (из iw phy)
        - статистика ошибок (из ip -s link)
        """
        info = {}

        # 1. Версия драйвера и прошивки (ethtool)
        ethtool_output = harvest.cmd_timeout__write_read__payload(
            "ethtool -i wlan0 2>/dev/null"
        )
        for line in ethtool_output.splitlines():
            if ':' in line:
                k, v = line.split(':', 1)
                info[k.strip()] = v.strip()
        print(f"Driver info: {info}")

        # Проверка, что драйвер загружен и прошивка указана
        assert info.get('driver', ''), "Не удалось определить драйвер Wi-Fi (ethtool -i)"
        assert info.get('firmware-version', ''), "Не удалось получить версию прошивки Wi-Fi"

        # 2. Информация о беспроводном интерфейсе (iw dev wlan0 info)
        iw_info = harvest.cmd_timeout__write_read__payload("iw dev wlan0 info")
        print(f"iw info:\n{iw_info}")

        # 3. MAC-адрес и состояние
        ip_output = harvest.cmd_timeout__write_read__payload("ip link show wlan0")
        mac_match = re.search(r'link/ether ([\da-fA-F:]+)', ip_output)
        if mac_match:
            info['mac'] = mac_match.group(1)
        assert 'mac' in info, "Не удалось извлечь MAC-адрес wlan0"

        # 4. Поддерживаемые частоты и режимы (iw phy)
        phy_output = harvest.cmd_timeout__write_read__payload("iw phy phy0 info 2>/dev/null")
        print(f"iw phy summary (первые 500 символов): {phy_output[:500]}...")

        # 5. Счетчики ошибок интерфейса (для последующего анализа трендов)
        stats_raw = harvest.cmd_timeout__write_read__payload("ip -s link show wlan0")
        print(f"Interface statistics:\n{stats_raw}")

        # Сохраняем всё в отчёт (можно вернуть словарь, но pytest сохранит вывод в лог)
        # Для простоты – пусть информация просто печатается, она попадёт в HTML-отчёт.


# ======================================================================================================================
@pytest.mark.GSM
class Test_41__GSM:
    """Тесты GSM-модема"""
    INTERFACE_NAME: str = "usb0"

    # ------------------------------------------------------------------------------------------------------------------
    @pytest.mark.dependency(name="gsm_present")
    def test_gsm_1__present(self, harvest):
        """
        ---- Sent utf8 encoded message: "ip link show\r\n" ----
        ip link show
        1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT group default qlen 1000
            link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
        2: wlan0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc pfifo_fast state DOWN mode DORMANT group default qlen 1000
            link/ether c6:94:13:d4:50:d5 brd ff:ff:ff:ff:ff:ff
        3: usb0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UNKNOWN mode DEFAULT group default qlen 1000
            link/ether 46:d1:74:50:fa:0f brd ff:ff:ff:ff:ff:ff
        root@harvest05:~#
        """
        assert harvest.cmd_timeout__check_executed_success(f"ip link show {self.INTERFACE_NAME}"), f"GSM-интерфейс {self.INTERFACE_NAME} не обнаружен"

    # ------------------------------------------------------------------------------------------------------------------
    @pytest.mark.dependency(depends=["gsm_present"])
    def test_gsm_2__quick(self, harvest):
        """
        Быстрая проверка: наличие IP-адреса и доступность 8.8.8.8 через этот интерфейс.

        ---- Sent utf8 encoded message: "ip link show usb0\r\n" ----
        ip link show usb0
        3: usb0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UNKNOWN mode DEFAULT group default qlen 1000
            link/ether 46:d1:74:50:fa:0f brd ff:ff:ff:ff:ff:ff
        root@harvest05:~#
        """
        out = harvest.cmd_timeout__write_read__payload(
            f"ip link show {self.INTERFACE_NAME}",
            timeout=2
        )
        assert ",UP," in out, "GSM-интерфейс {self.INTERFACE_NAME} не поднят"

        # 1. Проверяем IP
        """
        ---- Sent utf8 encoded message: "ip -4 addr show usb0\r\n" ----
        ip -4 addr show usb0
        3: usb0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UNKNOWN group default qlen 1000
            inet 192.168.0.100/24 brd 192.168.0.255 scope global dynamic noprefixroute usb0
               valid_lft 59186sec preferred_lft 59186sec
        root@harvest05:~#
        
        ---- Sent utf8 encoded message: "ip -4 addr show wlan0\r\n" ----
        ip -4 addr show wlan0
        root@harvest05:~# 
        root@harvest05:~# 
        """
        ip_ok = harvest.cmd_timeout__write_read__payload(
            f"ip -4 addr show {self.INTERFACE_NAME} | grep inet",
            timeout=2
        )
        assert ip_ok, f"Нет IPv4 адреса на {self.INTERFACE_NAME}"

        ping_ok = harvest.cmd_timeout__check_executed_success(
            f"ping -I {self.INTERFACE_NAME} -c 1 -W 2 8.8.8.8",
            timeout=3
        )
        assert ping_ok, f"Пинг 8.8.8.8 через {self.INTERFACE_NAME} не прошёл (проверьте SIM/покрытие)"

    # ------------------------------------------------------------------------------------------------------------------
    @pytest.mark.dependency(depends=["gsm_present"])
    def test_gsm_3__deep__default_route(self, harvest):
        """
        Информация: является ли usb0 маршрутом по умолчанию.
        Не падает, если нет – просто сообщает в лог.

        ---- Sent utf8 encoded message: "ip route show\r\n" ----
        ip route show
        default via 192.168.0.1 dev usb0 proto dhcp src 192.168.0.100 metric 100
        169.254.0.0/16 dev usb0 scope link metric 1000
        192.168.0.0/24 dev usb0 proto kernel scope link src 192.168.0.100 metric 100
        root@harvest05:~#
        """
        default_route = harvest.cmd_timeout__write_read__payload(
            "ip route show default", timeout=2
        )
        result = "usb0" in default_route
        if result:
            print("GSM (usb0) является основным шлюзом (default route)")
        else:
            print("GSM (usb0) НЕ является основным шлюзом (WiFi или другой интерфейс активен)")

        assert result, "GSM (usb0) НЕ является основным шлюзом (WiFi или другой интерфейс активен)"

    @pytest.mark.dependency(depends=["gsm_present"])
    def test_gsm_3__deep__ping1_gw(self, harvest):
        """Пинг шлюза (из default via ... dev usb0).

        ---- Sent utf8 encoded message: "ip route show default | grep usb0\r\n" ----
        ip route show default | grep usb0
        default via 192.168.0.1 dev usb0 proto dhcp src 192.168.0.100 metric 100
        root@harvest05:~#
        """
        gw_out = harvest.cmd_timeout__write_read__payload(
            "ip route show default | grep usb0",
            timeout=2
        ).strip()
        assert gw_out, "нет данных"

        gw = gw_out.split()[2]
        assert gw, "Не удалось извлечь IP шлюза для usb0"
        print(f"[{gw=}]")

        ping_ok = harvest.cmd_timeout__check_executed_success(
            f"ping -I {self.INTERFACE_NAME} -c 1 -W 1 {gw}",
            timeout=2
        )
        assert ping_ok, f"Шлюз {gw} не отвечает через {self.INTERFACE_NAME}"

    @pytest.mark.dependency(depends=["gsm_present"])
    def test_gsm_3__deep__ping2_8888(self, harvest):
        """Разрешение DNS и доступность внешнего ресурса (ya.ru)."""
        ping_ok = harvest.cmd_timeout__check_executed_success(
            f"ping -I {self.INTERFACE_NAME} -c 1 -W 2 8.8.8.8",
            timeout=2
        )
        assert ping_ok, f"[8.8.8.8] недоступен через {self.INTERFACE_NAME}"

    @pytest.mark.dependency(depends=["gsm_present"])
    def test_gsm_3__deep__ping3_dns(self, harvest):
        """Разрешение DNS и доступность внешнего ресурса (ya.ru)."""
        ping_ok = harvest.cmd_timeout__check_executed_success(
            f"ping -I {self.INTERFACE_NAME} -c 1 -W 2 ya.ru",
            timeout=2
        )
        assert ping_ok, f"ya.ru недоступен через {self.INTERFACE_NAME} (проверьте DNS/интернет)"


# ======================================================================================================================
@pytest.mark.GSM
class Test_42__GSMAT:
    """Тесты GSM-модема через AT команды (Qualcomm/SIMcom 7682, требуется ручная инициализация драйвера option)"""

    # ------------------------------------------------------------------------------------------------------------------
    @pytest.mark.dependency(name="gsmat_present")
    def test_gsmat_1__detect(self, gsm_at__port):
        assert gsm_at__port, "порт не обнаружен!"

    # ------------------------------------------------------------------------------------------------------------------
    @pytest.mark.dependency(depends=["gsmat_present"])
    def test_gsmat_2__quick__check(self, harvest, gsm_at__port):
        """Базовая проверка: AT -> OK."""
        out = harvest.at_cmd__simple(cmd="AT", port=gsm_at__port)
        assert "OK" in out, f"Модем не отвечает на AT: {out}"

    # ------------------------------------------------------------------------------------------------------------------
    @pytest.mark.dependency(depends=["gsmat_present"])
    def test_gsmat_3__deep__dump(self, gsm_at__dump):
        assert gsm_at__dump, "dump не получен"

    # ------------------------------------------------------------------------------------------------------------------
    @pytest.mark.dependency(depends=["gsmat_present"])
    def test_gsmat_4__sim_ready(self, gsm_at__dump):
        """AT+CPIN? -> READY."""
        assert "+CPIN: READY" in gsm_at__dump.get("AT+CPIN?"), f"SIM не готова"

    @pytest.mark.dependency(depends=["gsmat_present"])
    def test_gsmat_4__signal_quality(self, gsm_at__dump):
        """AT+CSQ, RSSI >= 5 (из 31)."""
        at_cmd = "AT+CSQ"
        out = gsm_at__dump.get(at_cmd)
        for line in out.splitlines():
            if "+CSQ:" in line:
                parts = line.split(":")[1].strip().split(",")
                rssi = int(parts[0])
                assert rssi >= 5, f"Низкий уровень сигнала GSM: {rssi}/31"
                return
        pytest.fail(f"CSQ не найден: {out}")

    @pytest.mark.dependency(depends=["gsmat_present"])
    def test_gsmat_4__network_registration(self, gsm_at__dump):
        """AT+CREG? – статус 1 (зарегистрирован) или 5 (роуминг).

        AT+CREG? – статус 1 или 5.
        [at_output='+CREG: 0,1\nOK']
        """
        at_cmd = "AT+CREG?"
        out = gsm_at__dump.get(at_cmd)
        registered = any(
            "+CREG:" in l and (",1" in l or ",5" in l)
            for l in out.splitlines()
        )
        assert registered, f"Не зарегистрирован в сети: {out}"

    @pytest.mark.dependency(depends=["gsmat_present"])
    def test_gsmat_4__operator(self, gsm_at__dump):
        """AT+COPS? – имя оператора.
        [at_output='+COPS: 0,2,"25020",7\nOK']
        """
        at_cmd = "AT+COPS?"
        out = gsm_at__dump.get(at_cmd)
        assert "COPS" in out, f"Оператор не получен: {out}"
        print(f"GSM operator: {out}")


# ======================================================================================================================
@pytest.mark.RFID
class Test_5__RFID:
    @pytest.mark.dependency(name="rfid_present")
    def test_rfid_1__present(self, harvest):
        assert harvest.cmd_timeout__check_executed_success("ls /dev/ttyS2"), \
            "Порт RFID (/dev/ttyS2) не обнаружен!"
        # assert harvest.file_name__push("/tmp/rfid_scan.py"), "скрипт не отправился"
        pass

    @pytest.mark.dependency(depends=["rfid_present"])
    def test_rfid_2__scan(self, harvest):
        epcs = harvest.rfid_scan(3)
        assert epcs, "rfid метки не найдены"


# ======================================================================================================================
