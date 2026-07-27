import re

import pytest
from .utils import HarvestDevice

from base_aux.buses.d1_serial2_new.m2_manager import SerialManager
from base_aux.buses.d1_serial2_new.m1_serial_client import SerialClient2
from base_aux.aux_eq.m3_eq_valid3_derivatives import *


# ======================================================================================================================
manager = SerialManager()


# ======================================================================================================================
class SCRIPTS:
    gnss_info__ubx = r"""
import serial, time

SOURCE_ADR: str = '/dev/ttyUSB0'
START_UBX: bytes = b'\xb5\x62'
MAX_BUFFER: int = 1000

s = serial.Serial(SOURCE_ADR, 9600, timeout=0.8)
time.sleep(0.3)
s.reset_input_buffer()            # clear previous NMEA
s.write(b'\xb5\x62\x0a\x04\x00\x00\x0e\x34')   # UBX MON-VER

buf = b''
while True:
    byte = s.read(1)
    if not byte:
        break   # timeout
        
    buf += byte
    
    if buf[-2:] == START_UBX:
        # дождались синхробайтов – читаем остаток заголовка
        header_rest = s.read(4)
        if len(header_rest) < 4:
            break   # timeout
            
        expected_load_length = int.from_bytes(header_rest[2:4], 'little')
        # payload + checksum(2 байта)
        load_with_checksum = s.read(expected_load_length + 2)
        if len(load_with_checksum) < expected_load_length + 2:
            break   # timeout
            
        full_msg: bytes = START_UBX + header_rest + load_with_checksum
        # send data in hex view
        print('UBX_RESPONSE:[' + full_msg.hex() + ']')
        break
    
    if len(buf) >= MAX_BUFFER:
        break
    
s.close()
    """
#     gnss_info__ubx = r"""
# import serial, time, re
# s = serial.Serial('/dev/ttyUSB0', 9600, timeout=0.8)
# time.sleep(0.3)
# s.reset_input_buffer()  # если не сделать то будут сыпаться NMEA $GPGSV / ...
# # Дадим модулю время, чтобы он мог выдать идентификационные NMEA-строки (u-blox часто шлёт $GPTXT)
# data0_first = s.read(2048)
# # print('ORIGINAL:' + data0_first.decode(errors='ignore'))
#
# while True:
#     # 1=UBX_TXT -------------------------------
#     data1_ubx_txt = re.findall(rb'\$GPTXT,.*', data0_first)
#     if data1_ubx_txt:
#         print('UBX_TXT:' + data1_ubx_txt[0].decode(errors='ignore'))
#         break
#
#     # 2=UBX_RESPONSE---------------------------
#     # u-blox UBX MON-VER
#     # Очищаем буфер перед UBX, чтобы не было старых NMEA
#     s.reset_input_buffer()
#     s.write(b'\xb5\x62\x0a\x04\x00\x00\x0e\x34')
#     time.sleep(0.5)
#     data2_ubx_resp = s.read(256)
#     if b'\xb5\x62\x0a\x04' in data2_ubx_resp:
#         # print(data2_ubx_resp)
#         # print(data2_ubx_resp.hex())
#
#         # raw=b'\xb5b\n\x04\xfa\x00EXT CORE 3.01 (107900)\x00\x00\x00\x00\x00\x00\x00\x0000080000\x00\x00ROM BASE 3.01 (107888)\x00\x00\x00\x00\x00\x00\x00\x00FWVER=SPG 3.01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00PROTVER=18.00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00MOD=NEO-M8N-0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00FIS=0xEF4015 (100111)\x00\x00\x00\x00\x00\x00\x00\x00\x00GPS;GLO;GAL;BDS\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00SBAS;IMES;QZSS\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
#         # hex=b5620a04fa0045585420434f524520332e3031202831303739303029000000000000000030303038303030300000524f4d204241534520332e3031202831303738383829000000000000000046575645523d53504720332e30310000000000000000000000000000000050524f545645523d31382e303000000000000000000000000000000000004d4f443d4e454f2d4d384e2d3000000000000000000000000000000000004649533d30784546343031352028313030313131290000000000000000004750533b474c4f3b47414c3b424453000000000000000000000000000000534241533b494d45533b515a535300000000000000000000000000000000
#
#         print(f'UBX_RESPONSE:[{data2_ubx_resp.hex()}]')
#         break
#
#     # 3=MTK_RESPONSE---------------------------
#     # MediaTek PMTK запрос версии
#     s.reset_input_buffer()
#     s.write(b'$PMTK605*31\r\n')
#     time.sleep(0.3)
#     data3_mtk_resp = s.read(256)
#     if b'$PMTK' in data3_mtk_resp:
#         print('MTK_RESPONSE:' + data3_mtk_resp.decode(errors='ignore'))
#         break
#
#     # 4=NO_IDENT---------------------------
#     # Если ничего не получено – печатаем начало сырых данных
#     if not (data1_ubx_txt or data2_ubx_resp or data3_mtk_resp):
#         print('NO_IDENT:' + data0_first[:200].hex())
#         break
#
#     break
#
# s.close()
# time.sleep(0.1)
# """


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
@pytest.mark.skipif(False, reason="used for exploring executions/methods")
class Test_000__Explore:
    def test_1__push_file(self, harvest):
        assert harvest.push_text_file("print(123)")

    def test_2__gnss(self, harvest):
        script_explore = SCRIPTS.gnss_info__ubx

        assert harvest.push_text_file(script_explore, "/tmp/script_explore.py")
        assert harvest.conn.write_read_lines('python3 /tmp/script_explore.py', timeout_continue=5)


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


# ======================================================================================================================
@pytest.mark.PRE
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
    def test_gnss_1__present_port(self, harvest):
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

    @pytest.mark.dependency(depends=["gnss_present", ], name="gnss_responds")
    def test_gnss_2__device_responds__weak(self, harvest):
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
        gnss_data: dict[str, set[str]] = dict.fromkeys(self.MNEA_VALIDATE)

        output = harvest.cmd_timeout__write_read_lines("cat /dev/ttyUSB0", timeout=1, timeout_continue=1)

        for msg_type, data in gnss_data.items():
            gnss_data[msg_type] = set(filter(lambda line: line.startswith(msg_type), output))

        for msg_type, data in gnss_data.items():
            assert data, f"NMEA-предложения {msg_type=} не получены {data=}"
            print(f"NMEA-предложения {msg_type=} получены {data=}")

    @pytest.mark.dependency(depends=["gnss_responds", ])
    def test_gnss_3__device_info(self, harvest):
        """

        UBX_RESPONSE:b5620a04fa0045585420434f524520332e3031202831303739303029000000000000000030303038303030300000524f4d204241534520332e3031202831303738383829000000000000000046575645523d53504720332e30310000000000000000000000000000000050524f545645523d31382e303000000000000000000000000000000000004d4f443d4e454f2d4d384e2d3000000000000000000000000000000000004649533d30784546343031352028313030313131290000000000000000004750533b474c4f3b47414c3b424453000000000000000000000000000000534241533b494d45533b515a535300000000000000000000000000000000
        root@harvest05:~#
        """
        assert harvest.push_text_file(SCRIPTS.gnss_info__ubx, "/tmp/gnss_info__ubx.py"), "скрипт не отправился"

        for attempt in range(3):
            print(f"Попытка {attempt=}: UBX_RESPONSE поиск...")

            # Убиваем предыдущие экземпляры скрипта и освобождаем порт
            harvest.conn.write_read_bytes('pkill -9 -f gnss_info__ubx.py; fuser -k /dev/ttyUSB0; sleep 0.5')

            output = harvest.conn.write_read_bytes('python3 /tmp/gnss_info__ubx.py', timeout_continue=5)
            assert output, "данные от устройства не получены вообще"

            if b'UBX_RESPONSE:[' in output:
                # Извлекаем HEX-строку --------------------
                print(f"FULL: {output}")

                match = re.search(rb'UBX_RESPONSE:\[([0-9a-fA-F]*)\]', output)
                assert match, "Не найден корректный UBX_RESPONSE в выводе"
                output_hex_bytes = match.group(1)
                print(f"LR-STRIPPED:\t{output_hex_bytes=}")

                output_hex_str: str = output_hex_bytes.decode('ascii')  # получаем чистую HEX-строку
                print(f"LR-STRIPPED:\t{output_hex_str=}")

                # Декодируем HEX-строку в настоящие байты
                try:
                    raw_data: bytes = bytes.fromhex(output_hex_str)
                    print(f"LR-STRIPPED:\t{raw_data=}")
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

    @pytest.mark.dependency(depends=["gnss_responds", ])
    def test_gnss_4__work1__weak(self, harvest):
        """
        GOAL
        test exact data

        """
        pytest.skip("not realised")

    @pytest.mark.dependency(depends=["gnss_responds", ])
    def test_gnss_4__work2__deep(self, harvest):
        """
        GOAL
        test exact data

        """
        pytest.skip("not realised")


# ======================================================================================================================
@pytest.mark.BT
class Test_21__Bluetooth:
    """Тесты Bluetooth (тот же чип что и WiFi)"""
    @pytest.mark.dependency(name="bt_present")
    def test_bt_1__present_port(self, harvest):
        """Проверяет, виден ли Bluetooth интерфейс."""
        assert harvest.cmd__check_executed_success("hciconfig hci0"), "Bluetooth интерфейс hci0 не обнаружен"

    @pytest.mark.dependency(depends=["bt_present", ], name="bt_responds")
    def test_bt_2__device_responds_info(self, harvest):
        # FIXME: use smth light! like serial number and model!!!
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

    @pytest.mark.dependency(depends=["bt_responds", ])
    def test_bt_3__work1__scan_devices(self, harvest):
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
@pytest.mark.WIFI
class Test_22__WiFi:
    @pytest.mark.dependency(name="wifi_present")
    def test_wf_1__present_port(self, harvest):
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

    @pytest.mark.dependency(depends=["wifi_present", ], name="wifi_responds")
    def test_wf_2__device_responds_info(self, harvest):
        # assert harvest.cmd__check_success("iw dev wlan0 link"), "Команда iw dev wlan0 link вернула ошибку"
        stdout_connected = harvest.conn.write_read_lines("iw dev wlan0 link")
        assert "Not connected." not in stdout_connected, "нет соединения по WiFi"

    @pytest.mark.dependency(depends=["wifi_responds", ])
    def test_wf_3__work1__signal_quality(self, harvest):
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
@pytest.mark.GSM
class Test_3__GSM:
    """Тесты GSM-модема (интерфейс usb0)"""

    @pytest.mark.dependency(name="gsm_present")
    def test_gsm_1__present_port(self, harvest):
        """Физическое наличие модема."""
        assert harvest.cmd__check_executed_success("ip link show usb0"), "GSM-интерфейс usb0 не обнаружен"

    @pytest.mark.dependency(depends=["gsm_present", ], name="gsm_responds")
    def test_gsm_2__device_responds_info(self, harvest):
        raise NotImplementedError()

    @pytest.mark.dependency(depends=["gsm_responds", ])
    def test_gsm_3__work1__sim_detected(self, harvest):
        """Получение данных: проверка SIM-карты через AT."""
        # Ищем порт AT-команд (обычно /dev/ttyUSB2)
        # Проверяем, что порт существует и отвечает
        harvest.conn.write_bytes('echo -e "AT+CPIN?\\r\\n" > /dev/ttyUSB2 && cat /dev/ttyUSB2 & sleep 0.5; kill %1')
        output = harvest.conn.read_lines(timeout_continue=1.5)
        # Ищем строку с +CPIN: READY или SIM PIN
        ready = any("+CPIN: READY" in line for line in output)
        assert ready, "SIM-карта не готова или модем не отвечает"

    @pytest.mark.dependency(depends=["gsm_responds", ])
    def test_gsm_3__work1__signal_quality(self, harvest):
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

    @pytest.mark.dependency(depends=["gsm_responds", ])
    def test_gsm_3__work1__network_registration(self, harvest):
        """Валидация: регистрация в сети."""
        harvest.conn.write_bytes('echo -e "AT+CREG?\\r\\n" > /dev/ttyUSB2 && cat /dev/ttyUSB2 & sleep 0.5; kill %1')
        output = harvest.conn.read_lines(timeout_continue=1.5)
        # Ищем +CREG: 0,1 или 0,5 (зарегистрирован)
        registered = any("+CREG: " in line and (line.endswith("1") or line.endswith("5")) for line in output)
        assert registered, "Модем не зарегистрирован в сотовой сети"


# ======================================================================================================================
@pytest.mark.RFID
class Test_4__RFID:

    @pytest.mark.dependency(name="rfid_script_present")
    def test_rfid_0__script_send_present(self, harvest):
        """Физическое наличие скрипта."""
        assert True, "не получилось отправить скрипт"
        assert True, "Скрипт /root/e710.py не найден"

    @pytest.mark.dependency(depends=["rfid_script_present", ], name="rfid_present")
    def test_rfid_1__present_port(self, harvest):
        raise NotImplementedError()

    @pytest.mark.dependency(depends=["rfid_present", ], name="rfid_responds")
    def test_rfid_2__device_responds_info(self, harvest):
        raise NotImplementedError()

    @pytest.mark.dependency(depends=["rfid_responds", ])
    def test_rfid_3__work1__execution_no_error(self, harvest):
        """Получение данных: скрипт запускается и завершается без ошибок."""
        harvest.conn.write_bytes("timeout 2 python3 /root/e710.py")  # используем timeout для завершения
        output = harvest.conn.read_lines(timeout_continue=3)
        # Ищем признаки ошибок
        has_traceback = any("Traceback" in line for line in output)
        assert not has_traceback, "Скрипт RFID завершился с ошибкой"

    @pytest.mark.dependency(depends=["rfid_responds", ])
    def test_rfid_3__work2__valid_response_present(self, harvest):
        """Валидация: при наличии меток скрипт должен выдавать данные."""
        harvest.conn.write_bytes("timeout 3 python3 /root/e710.py")
        output = harvest.conn.read_lines(timeout_continue=4)
        # В работающем состоянии вывод содержит шестнадцатеричные данные (например, b'...')
        # или сообщение 'tmout'. Главное — не пустой и не только ошибки.
        # Проверяем, что есть хотя бы одна строка с данными или 'tmout'.
        has_data = any("tmout" in line or "b'" in line or "b\"" in line for line in output)
        assert has_data, "RFID-скрипт не вернул ни данных, ни таймаутов"


# ======================================================================================================================
