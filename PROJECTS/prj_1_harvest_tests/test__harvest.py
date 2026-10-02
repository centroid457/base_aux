import json

from base_aux.clients.m2_manager_1__serial import ClientManager_Serial
from base_aux.aux_eq.m4_eq_valid2_derivatives import *


# ======================================================================================================================
manager = ClientManager_Serial()


# ======================================================================================================================
@pytest.mark.skipif(True, reason="used for exploring executions/methods")
class Test_000__Explore:
    # WARN!!! DONT FORGET TURN OFF IT!!! else more of tests would failed!

    @pytest.mark.skip
    def test_1__devices_all__usb(self, harvest):
        harvest.get_info__usb_all(EqValid_Regexp(r"ttyS\d"))

    @pytest.mark.skip
    def test_2__rfid_script(self, harvest):
        scriptname = "scr__rfid_scan.py"
        assert harvest.file_name__push(scriptname)

        command_line = f"python3 {scriptname}"
        output = harvest.cmd_timeout__write_read__payload(
            command_line,
            # stop_line=EqValid_Regexp(rb'found=\d+epc'),
            timeout_continue=10,
        )
        print(f"FINISH")

    @pytest.mark.skip
    def test_3__btus(self, harvest):
        bt_scaned = harvest.bt__scan()
        print(f"{bt_scaned=}")

        info = harvest.bt__get_dev_info("D4:81:ED:BB:AA:6B")
        print(json.dumps(info, indent=2))


        # for mac in [list(bt_get_known_devices)[0], "E5:C6:EB:4E:F3:05", "F6:D4:61:D3:B7:55"]:
        #     result = harvest.bt__get_dev_info(mac)
        #     print(result)


# ======================================================================================================================
@pytest.mark.DET
class Test_01__Detection:
    def test_det_1__transport_1__serial(self, transport):
        # 0=serial
        if transport.lower() != "serial":
            pytest.skip()

        # 1=exist_ports ------------------------------------
        result = manager.ADDRESSES_CASHED
        print(f"\nPORTS_EXISTED[{result}]")
        assert result != [], "Не обнаружено ни одного последовательного порта."

        # 2=exist_can_open ------------------------------------
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

    def test_det_2__dev_0__detection(self, harvest):
        """
        Тест проверяет, что устройство успешно обнаружено,
        и выводит его уникальный идентификатор.
        """
        assert harvest, "Устройство Harvest не обнаружено."

    @pytest.mark.skipif(True, reason="bad work!!!")
    def test_det_2__dev_1__info(self, harvest_info):
        print(json.dumps(harvest_info, indent=2, ensure_ascii=False))
        assert harvest_info, "Устройство Harvest не обнаружено."

    def test_det_2__dev_2__sql_settings(self, sql_settings):
        assert sql_settings, "настройки устройства из SQL не получены"


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

    def test_pre_2__sqlite3(self, harvest, internet_access):
        self.pkg__check_installed_or_install(harvest, internet_access, "sqlite3")

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

    def test_pre_4__python_bleak(self, harvest, internet_access):
        if not harvest.cmd_timeout__check_executed_success(f'python3 -c "import bleak"'):
            assert internet_access, "нет интернета для установки пакетов"
            assert harvest.apt_install("python3-bleak")

    def test_pre_5__wifi1__iw(self, harvest, internet_access):
        self.pkg__check_installed_or_install(harvest, internet_access, "iw")

    def test_pre_5__wifi2__bluez(self, harvest, internet_access):
        self.pkg__check_installed_or_install(harvest, internet_access, "bluetoothctl", "bluez")

    def test_pre_5__wifi3__usbutils(self, harvest, internet_access):
        self.pkg__check_installed_or_install(harvest, internet_access, "lsusb", "usbutils")

    # ------------------------------------------------------------------------------------------------------------------
    def test_pre_6__push1__ubx(self, harvest):
        assert harvest.file_name__push("scr__gnss_info_ubx.py"), "скрипт не отправился"

    def test_pre_6__push2__at_client(self, harvest):
        assert harvest.file_name__push("scr__gsm_at_client.py"), "скрипт не отправился"

    def test_pre_6__push3__rfid_scan(self, harvest):
        assert harvest.file_name__push("scr__rfid_scan.py"), "скрипт не отправился"

    def test_pre_6__push4__bt(self, harvest):
        assert harvest.file_name__push("scr__bt_find.py"), "скрипт не отправился"

    def test_pre_6__push5__btus(self, harvest):
        assert harvest.file_name__push("scr__btus_read.py"), "скрипт не отправился"


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

        IF IT STOPS STREAMING - REBOOT!!!
        ==================================
        ---- Opened the serial port COM16 ----
        ---- Sent utf8 encoded message: "cat /dev/ttyUSB0\r\n" ----
        cat /dev/ttyUSB0
        6,,,N*6C
        $GNVTG,,,,,,,,,N*2E
        $GNGGA,114456.00,,,,,0,00,99.99,,root@harvest05:~#
        root@harvest05:~#
        ---- Sent utf8 encoded message: "cat /dev/ttyUSB0\r\n" ----
        cat /dev/ttyUSB0
        $GNRMC,114740.00,V,,,,,,,110826,,,N*68
        $GNVTG,,,,,,,,,N*2E
        $GNroot@harvest05:~#
        root@harvest05:~#
        ---- Sent utf8 encoded message: "cat /dev/ttyUSB0\r\n" ----
        cat /dev/ttyUSB0
        $GNRMC,114743.00,V,,,,,,,110826,,,N*6B
        $GNVTG,,,,,,,,,N*2E
        $GNroot@harvest05:~#
        root@harvest05:~#
        ---- Sent utf8 encoded message: "cat /dev/ttyUSB0\r\n" ----
        cat /dev/ttyUSB0
        $GNRMC,114746.00,V,,,,,,,110826,,,N*6E
        $GNVTG,,,,,,,,,N*2E
        $GNroot@harvest05:~#
        root@harvest05:~#

[15:39:03.948819]COM16.write[OK]= b'timeout 3 cat /dev/ttyUSB0\r\n'
[15:39:03.974066]COM16.readEOL[OK]= b'timeout 3 cat /dev/ttyUSB0'
[15:39:03.977072]COM16.readEOL[OK]= b'\x1b[?2004l'
[15:39:04.015178]COM16.readEOL[OK]= b'$GNRMC,123527.00,V,,,,,,,110826,,,N*6F'
[15:39:04.023177]COM16.readEOL[OK]= b'$GNVTG,,,,,,,,,N*2E'
[15:39:04.035514]COM16.readEOL[OK]= b'$GN\x1b[?2004hroot@harvest05:~# '
[15:39:04.035514]COM16.stop_line[OK]= b'' [extra=EqValid_Regexp(v_args=(b'.*root@.+:.+#.*',)/v_kwargs={}/_cumulate_mode=<EnumAdj_BoolCumulate.ALL_TRUE: <built-in function all>>/_other_resolve=True)]
[15:39:04.035514]COM16.readNoEOL[OK]= b'$GN\x1b[?2004hroot@harvest05:~# '
[15:39:04.136724]COM16.reset_input[OK]= b'in_waiting__bytes_count=36'
[15:39:04.136724]COM16.in_waiting__bytes_data[OK]= b'\n\x1b[?2004l\r\x1b[?2004hroot@harvest05:~# '
[15:39:04.136724]COM16.reset_input[OK]= b''
[15:39:04.136724]COM16.write[OK]= b'\x03'
[COM16.WRITEREAD]
	write=[timeout 3 cat /dev/ttyUSB0]
	read=[$GNRMC,123527.00,V,,,,,,,110826,,,N*6F
$GNVTG,,,,,,,,,N*2E]


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

        2=BLOCK STAY LONG TIME on window - ower 2 houers
        ==================================
        read=[,,,,,,,,,,,99.99,99.99,99.99*2E
        $GPGSV,5,1,19,01,12,180,26,03,6GSV,3,1,10,65,21,275,,71,45,073,,72,71,307,,73,40,083,*69
        $GLGSV,3,2,10,74,20,136,,80,21,021,,81,05,352,,86,03,198,*6D
        $GLGSV,3,3,10,87,30,225,,88,38,308,*6D
        $GNGLL,,,,,091636.00,V,N*5F
        $GNRMC,091637.00,V,,,,,,,010926,,,N*65
        $GNVTG,,,,,,,,,N*2E
        $GNGGA,091637.00,,,,,0,00,99.99,,,,,,*72
        $GNGSA,A,1,,,,,,,,,,,,,99.99,99.99,99.99*2E
        $GNGSA,A,1,,,,,,,,,,,,,99.99,99.99,99.99*2E
        $GPGSV,5,1,17,01,11,180,31,03,63,136,30,04,70,244,30,06,36,304,26*72
        $GPGSV,5,2,17,07,,,29,09,34,253,27,11,,,34,14,,,36*4C
        $GPGSV,5,3,17,21,,,34,22,,,22,23,,,33,24,,,36*7F
        $GPGSV,5,4,17,25,,,37,31,43,064,27,36,26,187,34,40,24,159,30*4B
        $GPGSV,5,5,17,49,20,217,36*41
        $GLGSV,3,1,10,65,21,275,,71,45,073,,72,71,307,,73,40,083,*69
        $GLGSV,3,2,10,74,20,136,,80,21,021,,81,05,352,,86,03,198,*6D
        $GLGSV,3,3,10,87,30,225,,88,38,308,*6D
        $GNGLL,,,,,091637.00,V,N*5E
        $GNRMC,091638.00,V,,,,,,,010926,,,N*6A
        $GNVTG,,,,,,,,,N*2E
        $GNGGA,091638.00,,,,,0,00,99.99,,,,,,*7D
        $GNGSA,A,1,,,,,,,,,,,,,99.99,99.99,99.99*2E
        $GNGSA,A,1,,,,,,,,,,,,,99.99,99.99,99.99*2E
        $GPGSV,4,1,16,01,11,180,24,03,63,136,30,04,70,244,30,06,36,304,23*73
        $GPGSV,4,2,16,07,,,34,09,34,253,27,11,,,34,14,,,37*41
        $GPGSV,4,3,16,21,,,35,23,,,34,24,,,37,25,,,38*74
        $GPGSV,4,4,16,31,43,064,27,36,26,187,34,40,24,159,32,49,20,217,36*74
        $GLGSV,3,1,10,65,21,275,,71,45,073,,72,71,307,,73,40,083,*69
        $GLGSV,3,2,10,74,20,136,,80,21,021,,81,05,352,,86,03,198,*6D
        $GLGSV,3,3,10,87,30,225,,88,38,308,*6D
        $GNGLL,,,,,091638.00,V,N*51
        $GNRMC,091639.00,V,,,,,,,010926,,,N*6B
        $GNVTG,,,,,,,,,N*2E
        $GNGGA,091639.00,,,,,0,00,99.99,,,,,,*7C
        $GNGSA,A,1,,,,,,,,,,,,,99.99,99.99,99.99*2E
        $GNGSA,A,1,,,,,,,,,,,,,99.99,99.99,99.99*2E
        $GPGSV,5,1,17,01,11,180,22,03,63,136,29,04,70,244,32,06,36,303,20*7B
        $GPGSV,5,2,17,07,,,34,09,34,253,24,11,,,31,14,,,34*44
        $GPGSV,5,3,17,21,,,32,22,,,33,23,,,33,24,,,35*7A
        $GPGSV,5,4,17,25,,,36,31,43,064,29,36,26,187,31,40,24,159,31*40]
        """
        gnss_collected: dict[str, set[str]] = dict.fromkeys(self.MNEA_VALIDATE)

        output_collected = list()
        for step in range(3):
            output = harvest.cmd_timeout__write_read__payload("cat /dev/ttyUSB0", timeout=3, timeout_continue=3)
            output = output.splitlines()
            output_collected.extend(output)
            if len(output_collected) > 10:
                break

        for msg_type, data in gnss_collected.items():
            lines = set(filter(lambda line: line.startswith(msg_type), output_collected))
            gnss_collected[msg_type] = lines
            if lines:
                return

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
            result = harvest.gnss_get_info_ubx()
            if result:
                return True
            else:
                time.sleep(1)

        # FINAL --------------------------
        assert False, "После нескольких попыток UBX_RESPONSE так и не был получен"


# ======================================================================================================================
@pytest.mark.BT
class Test_21__BT:
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
        bt_scaned = harvest.bt__scan(5)
        assert bt_scaned, f"Не обнаружено ни одного Bluetooth-устройства {bt_scaned=}"

    @pytest.mark.dependency(depends=["bt_present", ])
    def test_bt_4__deep__c1_hciconfig_a(self, harvest):
        """
        "hciconfig hci0 -a",           # полная информация об интерфейсе

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

        ПРИМЕР ОСТАНОВЛЕНОГО КОНТРОЛЛЕРА BT!!!
        ---- Sent utf8 encoded message: "hciconfig hci0 -a\r\n" ----
        hciconfig hci0 -a
        hci0:   Type: Primary  Bus: UART
                BD Address: A6:20:96:B6:A9:5E  ACL MTU: 1021:8  SCO MTU: 64:1
                DOWN
                RX bytes:53561 acl:79 sco:0 events:1511 errors:0
                TX bytes:3006 acl:33 sco:0 commands:113 errors:0
                Features: 0xbf 0xfe 0xcf 0xfe 0xdb 0xff 0x7b 0x87
                Packet type: DM1 DM3 DM5 DH1 DH3 DH5 HV1 HV2 HV3
                Link policy: RSWITCH SNIFF
                Link mode: PERIPHERAL ACCEPT

        root@harvest05:~#
        """
        cmd = "hciconfig hci0 -a"
        output = harvest.cmd_timeout__write_read__payload(
            cmd,
            timeout_continue=1.5,
        )
        assert f"UP RUNNING" in output, "не поднят!"

    @pytest.mark.dependency(depends=["bt_present", ])
    def test_bt_4__deep__c2_hciconfig_version(self, harvest):
        """
        [COM16.WRITEREAD]
	write=[hciconfig hci0 version]
	read=[hci0:	Type: Primary  Bus: UART
	BD Address: A6:20:96:B6:A9:5E  ACL MTU: 1021:8  SCO MTU: 64:1
	HCI Version: 4.0 (0x6)  Revision: 0x6a
	LMP Version: 4.0 (0x6)  Subversion: 0x2209
	Manufacturer: Broadcom Corporation (15)]
        """
        cmd = "hciconfig hci0 version"      # версия прошивки/стека

        # Минимальная валидация: в hciconfig version должен быть Manufacturer
        output = harvest.cmd_timeout__write_read__payload(
            cmd,
            timeout_continue=1.5,
        )
        assert "Manufacturer" in output, \
            "Не удалось получить производителя Bluetooth (возможно, модуль не инициализирован)"

    @pytest.mark.dependency(depends=["bt_present", ])
    def test_bt_4__deep__c3_rfkill_list_bt(self, harvest):
        """
        [COM16.WRITEREAD]
	write=[rfkill list bluetooth]
        read=[0: sunxi-bt: Bluetooth
        Soft blocked: no
        Hard blocked: no
    2: hci0: Bluetooth
        Soft blocked: no
        Hard blocked: no]
        """
        cmd = "rfkill list bluetooth"       # состояние блокировок
        # Проверяем, что rfkill не показывает Hard blocked
        output = harvest.cmd_timeout__write_read__payload(
            cmd,
            timeout_continue=1.5,
        )
        assert "Soft blocked: no" in output, "Bluetooth заблокирован (Soft blocked)"
        assert "Hard blocked: no" in output, "Bluetooth заблокирован (Hard blocked)"

    @pytest.mark.dependency(depends=["bt_present", ])
    def test_bt_4__deep__c4(self, harvest):
        """
        [COM16.WRITEREAD]
            write=[btmgmt info]
            read=[Index list with 1 item
        hci0:	Primary controller
            addr A6:20:96:B6:A9:5E version 6 manufacturer 15 class 0x000000
            supported settings: powered connectable fast-connectable discoverable bondable link-security ssp br/edr hs le advertising secure-conn debug-keys privacy static-addr
            current settings: powered ssp br/edr le secure-conn
            name harvest05
            short name ]
        """
        cmd = "btmgmt info"         # настройки контроллера (поддерживаемые/текущие)
        output = harvest.cmd_timeout__write_read__payload(
            cmd,
            timeout_continue=1.5,
        )

    @pytest.mark.dependency(depends=["bt_present", ])
    def test_bt_4__deep__c5(self, harvest):
        """
[COM16.WRITEREAD]
	write=[bluetoothctl list]
	read=[Controller A6:20:96:B6:A9:5E harvest05 [default]]
        """
        cmd = "bluetoothctl list"   # список контроллеров
        output = harvest.cmd_timeout__write_read__payload(
            cmd,
            timeout_continue=1.5,
        )

    @pytest.mark.dependency(depends=["bt_present", ])
    def test_bt_4__deep__c6(self, harvest):
        """
        [COM16.WRITEREAD]
            write=[bluetoothctl show]
            read=[Controller A6:20:96:B6:A9:5E (public)
            Name: harvest05
            Alias: harvest05
            Class: 0x00000000
            Powered: yes
            Discoverable: no
            DiscoverableTimeout: 0x00001388
            Pairable: no
            UUID: Generic Attribute Profile (00001801-0000-1000-8000-00805f9b34fb)
            UUID: Generic Access Profile    (00001800-0000-1000-8000-00805f9b34fb)
            UUID: PnP Information           (00001200-0000-1000-8000-00805f9b34fb)
            UUID: A/V Remote Control Target (0000110c-0000-1000-8000-00805f9b34fb)
            UUID: A/V Remote Control        (0000110e-0000-1000-8000-00805f9b34fb)
            UUID: Device Information        (0000180a-0000-1000-8000-00805f9b34fb)
            Modalias: usb:v1D6Bp0246d0542
            Discovering: no
            Roles: central
            Roles: peripheral
        Advertising Features:
            ActiveInstances: 0x00 (0)
            SupportedInstances: 0x05 (5)
            SupportedIncludes: tx-power
            SupportedIncludes: appearance
            SupportedIncludes: local-name]
        """
        cmd = "bluetoothctl show"   # детали контроллера (UUID, режимы)
        output = harvest.cmd_timeout__write_read__payload(
            cmd,
            timeout_continue=1.5,
        )

    @pytest.mark.dependency(depends=["bt_present", ])
    def test_bt_4__deep__c7(self, harvest):
        """
        [COM16.WRITEREAD]
        write=[hciconfig hci0 features]
        read=[hci0:	Type: Primary  Bus: UART
        BD Address: A6:20:96:B6:A9:5E  ACL MTU: 1021:8  SCO MTU: 64:1
        Features page 0: 0xbf 0xfe 0xcf 0xfe 0xdb 0xff 0x7b 0x87
            <3-slot packets> <5-slot packets> <encryption> <slot offset>
            <timing accuracy> <role switch> <sniff mode> <RSSI>
            <channel quality> <SCO link> <HV2 packets> <HV3 packets>
            <u-law log> <A-law log> <CVSD> <paging scheme> <power control>
            <transparent SCO> <broadcast encrypt> <EDR ACL 2 Mbps>
            <EDR ACL 3 Mbps> <enhanced iscan> <interlaced iscan>
            <interlaced pscan> <inquiry with RSSI> <extended SCO>
            <EV4 packets> <EV5 packets> <AFH cap. perip.>
            <AFH cls. perip.> <LE support> <3-slot EDR ACL>
            <5-slot EDR ACL> <sniff subrating> <pause encryption>
            <AFH cap. central> <AFH cls. central> <EDR eSCO 2 Mbps>
            <EDR eSCO 3 Mbps> <3-slot EDR eSCO> <extended inquiry>
            <LE and BR/EDR> <simple pairing> <encapsulated PDU>
            <err. data report> <non-flush flag> <LSTO> <inquiry TX power>
            <EPC> <extended features>
        Features page 1: 0x03 0x00 0x00 0x00 0x00 0x00 0x00 0x00]
        """
        cmd = "hciconfig hci0 features"     # поддерживаемые функции
        output = harvest.cmd_timeout__write_read__payload(
            cmd,
            timeout_continue=1.5,
        )


# ----------------------------------------------------------------------------------------------------------------------
@pytest.mark.BT
class Test_22__BTUS:
    """Тесты УЗ датчика передача данных"""
    @pytest.mark.dependency(name="btus_present")
    def test_btus_1__present(self, harvest, sql_settings):
        assert harvest.cmd_timeout__check_executed_success("hciconfig hci0"), "Bluetooth интерфейс hci0 не обнаружен"

        # PREPARE
        assert harvest.file_name__push("scr__btus_read.py"), "скрипт не отправился"
        assert harvest.bt__connections__clear_all()

    # @pytest.mark.skip
    @pytest.mark.dependency(depends=["btus_present"])
    def test_btus_1__present2__ultrasonic_mac__any(self, ultrasonic_mac__any):
        assert ultrasonic_mac__any, "EP (UltraSonic) датчики вообще не обнаружены в радиусе действия"

    # ------------------------------------------------------------------------------------------------------------------
    def _msg_validate__us(self, harvest, mac: str | None = None) -> bool | NoReturn:
        packets = []
        for step in range(3):
            packets = harvest.btus__read(mac=mac, max_pkgs=1, timeout=30.0)
            print(f"2={step=}={packets=}")
            if packets:
                break
        print(f"2=FINAL={packets=}")
        assert packets, f"не получено пакетов от {mac=} {packets=}"

        for packet in packets:
            print(f"3={packet=}")
            assert harvest.btus__validate_pkg(packet), f"пакет не валидирован! {packet}"

        return True

    # @pytest.mark.skip
    @pytest.mark.dependency(depends=["btus_present"])
    def test_btus_3__msg_validate__any(self, harvest):
        assert self._msg_validate__us(harvest)

    @pytest.mark.dependency(depends=["btus_present"])
    def test_btus_3__msg_validate__us1(self, harvest, sql_settings):
        print(f"1={sql_settings=}")
        assert sql_settings
        mac = sql_settings["macUz1"]
        assert self._msg_validate__us(harvest, mac)

    @pytest.mark.dependency(depends=["btus_present"])
    def test_btus_3__msg_validate__us2(self, harvest, sql_settings):
        print(f"1={sql_settings=}")
        assert sql_settings
        if sql_settings["uzTwo"] == "0":
            pytest.skip(f"US setup only for one!")
        mac = sql_settings["macUz2"]
        assert self._msg_validate__us(harvest, mac)


# ======================================================================================================================
@pytest.mark.WIFI
class Test_3__WiFi:
    # Пороговые значения для оценки качества (можно вынести в конфиг)
    RSSI_MIN_OK = -75        # dBm – ниже этого уже внимание
    RSSI_MIN_CRITICAL = -85  # dBm – ниже этого ошибка
    BEACON_LOSS_MAX = 5      # за время сессии (если накопилось больше – проблема)
    TX_RETRIES_MAX_RATIO = 0.15  # 15% повторных передач от общего числа – подозрительно
    MIN_SCAN_NETWORKS = 3    # минимальное количество видимых сетей (если меньше – возможно антенна)

    # ------------------------------------------------------------------------------------------------------------------
    def test_wf_1__present(self, wf__present):
        assert wf__present, "нет устройства"

    # ------------------------------------------------------------------------------------------------------------------
    def test_wf_3__connected1__link(self, wf__link_connected):
        assert wf__link_connected, "Нет Wi-Fi соединения с сетью!"

    def test_wf_3__connected2__station_dump(self, harvest, wf__link_connected):
        """
        1=DISCONNECTED ------------------------------
        ---- Sent utf8 encoded message: "iw dev wlan0 station dump\r\n" ----
        iw dev wlan0 station dump
        root@harvest05:~#

        2=CONNECTED ---------------------------------
        ---- Sent utf8 encoded message: "iw dev wlan0 station dump\r\n" ----
iw dev wlan0 station dump
Station ea:4f:a4:27:39:98 (on wlan0)
        inactive time:  0 ms
        rx bytes:       5479
        rx packets:     34
        tx bytes:       1873
        tx packets:     20
        tx failed:      0
        signal:         -51 [-51] dBm
        tx bitrate:     24.0 MBit/s
        rx bitrate:     6.0 MBit/s
        authorized:     yes
        authenticated:  yes
        associated:     yes
        WMM/WME:        yes
        TDLS peer:      no
        DTIM period:    1
        beacon interval:100
        short preamble: yes
        short slot time:yes
        connected time: 1429 seconds
        current time:   1786619989041 ms
root@harvest05:~#
        """
        # 0=DEPENDANCY ------------------------
        if not wf__link_connected:
            pytest.skip()

        # 1=TEST ------------------------------
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

    def test_wf_3__connected3__ifconfig(self, harvest, wf__link_connected):
        """
        1=DISCONNECTED ------------------------------
        ---- Sent utf8 encoded message: "ifconfig wlan0\r\n" ----
        ifconfig wlan0
        wlan0: flags=4099<UP,BROADCAST,MULTICAST>  mtu 1500
                ether 2e:07:94:ea:0e:b0  txqueuelen 1000  (Ethernet)
                RX packets 613  bytes 193957 (189.4 KiB)
                RX errors 0  dropped 0  overruns 0  frame 0
                TX packets 1560  bytes 318656 (311.1 KiB)
                TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

        root@harvest05:~#

        2=CONNECTED ---------------------------------
        ---- Sent utf8 encoded message: "ifconfig wlan0\r\n" ----
        ifconfig wlan0
        wlan0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
                inet 192.168.137.57  netmask 255.255.255.0  broadcast 192.168.137.255
                inet6 fe80::eeca:37c1:3b57:2a47  prefixlen 64  scopeid 0x20<link>
                ether 54:78:c9:02:22:b0  txqueuelen 1000  (Ethernet)
                RX packets 296  bytes 70435 (68.7 KiB)
                RX errors 0  dropped 0  overruns 0  frame 0
                TX packets 329  bytes 77552 (75.7 KiB)
                TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

        root@harvest05:~#
        """
        # 0=DEPENDANCY ------------------------
        if not wf__link_connected:
            pytest.skip()

        # 1=TEST ------------------------------
        ifconfig = harvest.cmd_timeout__write_read__payload("ifconfig wlan0")
        print(f"{ifconfig=}")

    def test_wf_3__connected4__rout_def(self, harvest, wf__link_connected):
        """
        1=DISCONNECTED ------------------------------
        ---- Sent utf8 encoded message: "ip route show default\r\n" ----
        ip route show default
        default via 192.168.0.1 dev usb0 proto dhcp src 192.168.0.100 metric 100
        root@harvest05:~#

        2=CONNECTED ---------------------------------
        ---- Sent utf8 encoded message: "ip route show default\r\n" ----
        ip route show default
        default via 192.168.0.1 dev usb0 proto dhcp src 192.168.0.100 metric 100
        default via 192.168.137.1 dev wlan0 proto dhcp src 192.168.137.57 metric 600
        root@harvest05:~#
        """
        # 0=DEPENDANCY ------------------------
        if not wf__link_connected:
            pytest.skip()

        # 1=TEST ------------------------------
        output = harvest.cmd_timeout__write_read__payload("ip route show default")
        print(f"{output=}")

    def test_wf_3__connected5__dns(self, harvest, wf__link_connected):
        """
        1=DISCONNECTED ------------------------------
        ---- Sent utf8 encoded message: "cat /etc/resolv.conf\r\n" ----
        cat /etc/resolv.conf
        # Dynamic resolv.conf(5) file for glibc resolver(3) generated by resolvconf(8)
        #     DO NOT EDIT THIS FILE BY HAND -- YOUR CHANGES WILL BE OVERWRITTEN
        # 127.0.0.53 is the systemd-resolved stub resolver.
        # run "resolvectl status" to see details about the actual nameservers.

        nameserver 192.168.0.1
        root@harvest05:~#

        2=CONNECTED ---------------------------------
        ---- Sent utf8 encoded message: "cat /etc/resolv.conf\r\n" ----
        cat /etc/resolv.conf
        # Dynamic resolv.conf(5) file for glibc resolver(3) generated by resolvconf(8)
        #     DO NOT EDIT THIS FILE BY HAND -- YOUR CHANGES WILL BE OVERWRITTEN
        # 127.0.0.53 is the systemd-resolved stub resolver.
        # run "resolvectl status" to see details about the actual nameservers.

        nameserver 192.168.0.1
        nameserver 192.168.137.1
        search lan
        root@harvest05:~#
        """
        # 0=DEPENDANCY ------------------------
        if not wf__link_connected:
            pytest.skip()

        # 1=TEST ------------------------------
        output = harvest.cmd_timeout__write_read__payload("cat /etc/resolv.conf")
        print(f"{output=}")

    def test_wf_3__connected6__wpa_cli(self, harvest, wf__link_connected):
        """
        1=DISCONNECTED ------------------------------
        ---- Sent utf8 encoded message: "wpa_cli status\r\n" ----
        wpa_cli status
        Selected interface 'wlan0'
        wpa_state=DISCONNECTED
        p2p_device_address=ea:24:2a:24:ab:ed
        address=2e:07:94:ea:0e:b0
        uuid=d83b1bcc-0d53-50f9-8229-9e981e5cabeb
        root@harvest05:~#

        2=CONNECTED ---------------------------------
        ---- Sent utf8 encoded message: "wpa_cli status\r\n" ----
        wpa_cli status
        Selected interface 'wlan0'
        bssid=80:af:ca:f0:9d:8d
        freq=2462
        ssid=Vest
        id=0
        mode=station
        pairwise_cipher=CCMP
        group_cipher=CCMP
        key_mgmt=WPA2-PSK
        wpa_state=COMPLETED
        ip_address=192.168.137.57
        p2p_device_address=26:12:e1:8b:b4:0f
        address=54:78:c9:02:22:b0
        uuid=150fbe1b-957e-56d5-b1d9-c1c892424155
        root@harvest05:~#

        [COM3.WRITEREAD]
            write=[wpa_cli status]
            read=[Selected interface 'wlan0'
        wpa_state=ASSOCIATING
        p2p_device_address=ea:24:2a:24:ab:ed
        address=54:78:c9:02:22:b0
        uuid=d83b1bcc-0d53-50f9-8229-9e981e5cabeb]
        output="Selected interface 'wlan0'\nwpa_state=ASSOCIATING\np2p_device_address=ea:24:2a:24:ab:ed\naddress=54:78:c9:02:22:b0\nuuid=d83b1bcc-0d53-50f9-8229-9e981e5cabeb"
        """
        # 0=DEPENDANCY ------------------------
        if not wf__link_connected:
            pytest.skip()

        # 1=TEST ------------------------------
        output = harvest.cmd_timeout__write_read__payload("wpa_cli status")
        print(f"{output=}")

    # ------------------------------------------------------------------------------------------------------------------
    def test_wf_4__deep__info(self, harvest, wf__present):
        """
        Собирает максимальную информацию об адаптере:
        - версия прошивки/драйвера
        - MAC-адрес
        - поддерживаемые стандарты (из iw phy)
        - статистика ошибок (из ip -s link)
        """
        # 0=DEPENDANCY ------------------------
        if not wf__present:
            pytest.skip()

        # 1=TEST ------------------------------
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

        # 2. Информация о беспроводном интерфейсе
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

    # ------------------------------------------------------------------------------------------------------------------
    def test_wf_4__deep__scan_ssids(self, harvest, wf__present, wf__link_connected):
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
        # 0=DEPENDANCY ------------------------
        if not wf__present:
            pytest.skip()

        # 1=TEST ------------------------------
        if wf__link_connected:
            pytest.skip("невозможно сканировать сеть при подключении к любому SSID")

        ssids = harvest.wf__scan()
        assert ssids, "сети не обнаружены"
        assert len(ssids) >= self.MIN_SCAN_NETWORKS, \
            f"Обнаружено мало сетей ({len(ssids)}), минимально ожидается {self.MIN_SCAN_NETWORKS}."

    def test_wf_4__deep__scan_signal(self, harvest, wf__present, wf__link_connected):
        """
        Собираем BSSID и уровни сигнала
        """
        # 0=DEPENDANCY ------------------------
        if not wf__present:
            pytest.skip()

        if wf__link_connected:
            pytest.skip("невозможно сканировать сеть при подключении к любому SSID")

        # 1=TEST ------------------------------
        scan_output = harvest.cmd_timeout__write_read__payload(
            "iw dev wlan0 scan",
            timeout=10,
            timeout_continue=2
        )
        signal_bds = re.findall(r'\s*signal:\s(.+)\sdBm\s*\n*', scan_output)
        signal_bds = [*map(float, signal_bds)]
        print(f"Wi-Fi quality {signal_bds=}")
        max_db = max(*signal_bds)
        print(f"Wi-Fi quality {max_db=}")
        assert max_db > self.RSSI_MIN_OK, "уровень сигнала слишком мал! проверьте антенну!"


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

    @pytest.mark.flaky(reruns=3, reruns_delay=1)
    @pytest.mark.dependency(depends=["gsm_present"])
    def test_gsm_3__deep__ping3_dns(self, harvest):
        """Разрешение DNS и доступность внешнего ресурса (ya.ru)."""
        ping_ok = harvest.cmd_timeout__check_executed_success(
            f"ping -I {self.INTERFACE_NAME} -c 1 -W 2 ya.ru",
            timeout=2
        )
        assert ping_ok, f"ya.ru недоступен через {self.INTERFACE_NAME} (проверьте DNS/интернет)"


# ----------------------------------------------------------------------------------------------------------------------
@pytest.mark.GSM
class Test_42__GSMAT:
    """
    Тесты GSM-модема через AT команды
    (Qualcomm/SIMcom 7682, - требуется ручная инициализация драйвера option)
    """

    # ------------------------------------------------------------------------------------------------------------------
    # @pytest.mark.skip
    # def test_gsmat_0__explore1_one(self, harvest, gsm_at__port):
    #     print()
    #     print()
    #     print()
    #     result = harvest.at_cmd__explore(
    #         cmd="CREG",
    #         port=gsm_at__port,
    #     )
    #     # print(f"{result=}")
    #     assert result, "не удалось получить данные"
    #     # result = list(filter(lambda x: x[0].endswith("?"), result))
    #     # print(json.dumps(result, indent=2, ensure_ascii=False))

    # @pytest.mark.skip
    # def test_gsmat_0__explore2_several(self, harvest, gsm_at__port):
    #     print()
    #     print()
    #     print()
    #     result = harvest.at_cmds__explore(
    #         cmds=harvest.AT_CMDS__GROUPED,
    #         port=gsm_at__port,
    #     )
    #     # print(f"{result=}")
    #     assert result, "не удалось получить данные"
    #     # result = list(filter(lambda x: x[0].endswith("?"), result))
    #     # print(json.dumps(result, indent=2, ensure_ascii=False))

    # @pytest.mark.skip
    # def test_gsmat_0__explore3_groups(self, harvest, gsm_at__port):
    #     result_full = dict()
    #
    #     for group_name, group_values in harvest.AT_GROUPS.items():
    #         print()
    #         print()
    #         print()
    #         print(f"=========={group_name=}==========")
    #         result = harvest.at_cmds__explore(
    #             cmds=group_values,
    #             port=gsm_at__port,
    #         )
    #         # print(f"{result=}")
    #         result_full[group_name] = result

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
    def test_gsmat_3__deep__dump(self, gsm_at__dump_dict):
        assert gsm_at__dump_dict, "dump не получен"

    # ------------------------------------------------------------------------------------------------------------------
    @pytest.mark.dependency(depends=["gsmat_present"])
    def test_gsmat_4__sim_ready(self, gsm_at__dump_dict):
        """AT+CPIN? -> READY."""
        assert "+CPIN: READY" in gsm_at__dump_dict.get("AT+CPIN?"), f"SIM не готова"

    @pytest.mark.dependency(depends=["gsmat_present"])
    def test_gsmat_4__signal_quality(self, gsm_at__dump_dict):
        """AT+CSQ, RSSI >= 5 (из 31)."""
        at_cmd = "AT+CSQ"
        out = gsm_at__dump_dict.get(at_cmd)
        for line in out.splitlines():
            if "+CSQ:" in line:
                parts = line.split(":")[1].strip().split(",")
                rssi = int(parts[0])
                assert rssi >= 5, f"Низкий уровень сигнала GSM: {rssi}/31"
                return
        pytest.fail(f"CSQ не найден: {out}")

    @pytest.mark.dependency(depends=["gsmat_present"])
    def test_gsmat_4__network_registration(self, gsm_at__dump_dict):
        """AT+CREG? – статус 1 (зарегистрирован) или 5 (роуминг).

        AT+CREG? – статус 1 или 5.
        [at_output='+CREG: 0,1\nOK']
        """
        at_cmd = "AT+CREG?"
        out = gsm_at__dump_dict.get(at_cmd)
        registered = any(
            "+CREG:" in l and (",1" in l or ",5" in l)
            for l in out.splitlines()
        )
        assert registered, f"Не зарегистрирован в сети: {out}"

    @pytest.mark.dependency(depends=["gsmat_present"])
    def test_gsmat_4__operator(self, gsm_at__dump_dict):
        """AT+COPS? – имя оператора.
        [at_output='+COPS: 0,2,"25020",7\nOK']
        """
        at_cmd = "AT+COPS?"
        out = gsm_at__dump_dict.get(at_cmd)
        assert "COPS" in out, f"Оператор не получен: {out}"
        print(f"GSM operator: {out}")


# ======================================================================================================================
@pytest.mark.RFID
class Test_5__RFID:
    @pytest.mark.dependency(name="rfid_present")
    def test_rfid_1__present(self, harvest):
        assert harvest.cmd_timeout__check_executed_success("ls /dev/ttyS2"), \
            "Порт RFID (/dev/ttyS2) не обнаружен!"
        assert harvest.file_name__push("scr__rfid_scan.py"), "скрипт не отправился"
        assert harvest.rfid__check_working(), "устройство не отвечает на порту!!! вероятно отключено!"

    @pytest.mark.dependency(depends=["rfid_present"])
    def test_rfid_2__scan(self, harvest):
        epcs = harvest.rfid__scan(3)
        assert epcs, f"rfid метки не найдены {epcs=}"


# ======================================================================================================================
