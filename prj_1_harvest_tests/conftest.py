import pytest
import os
import time
import re
import json
from datetime import datetime

from .utils import *

from base_aux.buses.d1_serial2_new.m2_manager import SerialManager
from base_aux.buses.d1_serial2_new.m1_serial_client import SerialClient2
from base_aux.aux_eq.m3_eq_valid3_derivatives import *


# ======================================================================================================================
@pytest.fixture(scope="session")
def harvest(request) -> HarvestDevice:
    """Находит устройство Harvest и возвращает авторизованный клиент."""
    found: list[HarvestDevice] = []
    for conn in SerialManager().make__not_occupied(can_open=True, baudrate=115200):
        print(f"try {conn=}")
        with conn:
            if HarvestDevice(conn).validate_conn():
                dev_id = HarvestDevice(conn).get_hostname_and_occupy()
                print(f"\n[HARVEST_FOUND]{conn}/{dev_id=}")
                found.append(HarvestDevice(conn))

    if len(found) == 0:
        pytest.exit("Устройств Harvest не обнаружено.")
    if len(found) > 1:
        pytest.exit("Устройств Harvest более чем 1!")

    device = found[0]
    with device.conn:
        device.prepare__stop__kernel_terminal_logs()
        device.prepare__stop__services()
        request.config.stash["device_id"] = dev_id
        yield device


@pytest.fixture(scope="session")
def harvest_info(harvest, request):
    info = harvest.get_info__system()
    request.config.stash["device_info"] = info
    print(json.dumps(info, indent=2, ensure_ascii=False))
    return info


# ======================================================================================================================
@pytest.fixture(scope="session")
def gsm_at__port(harvest):
    """Возвращает первый порт, ответивший OK на AT, или None.

            Для SIMcom 7682 требуется предварительная инициализация драйвера option.

            ищем само устройство - чип 7682
            ---- Sent utf8 encoded message: "lsusb\r\n" ----
    lsusb
    Bus 008 Device 002: ID 1a86:7523 QinHeng Electronics CH340 serial converter
    Bus 008 Device 001: ID 1d6b:0001 Linux Foundation 1.1 root hub
    Bus 005 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
    Bus 007 Device 001: ID 1d6b:0001 Linux Foundation 1.1 root hub
    Bus 004 Device 002: ID 1e0e:9011 Qualcomm / Option A76XX Series LTE Module
    Bus 004 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
    Bus 006 Device 001: ID 1d6b:0001 Linux Foundation 1.1 root hub
    Bus 003 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
    Bus 002 Device 001: ID 1d6b:0001 Linux Foundation 1.1 root hub
    Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
    Bus 009 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
    root@harvest05:~#
    root@harvest05:~#

    ---- Sent utf8 encoded message: "lsusb | grep -i qualcomm || echo ERR\r\n" ----
    lsusb | grep -i qualcomm || echo ERR
    Bus 004 Device 011: ID 1e0e:9011 Qualcomm / Option A76XX Series LTE Module
    root@harvest05:~#

    ---- Sent utf8 encoded message: "dmesg | grep -i '1e0e\\|9011\\|option\\|qmi\\|wwan\\|ttyUSB'\r\n" ----
    dmesg | grep -i '1e0e\|9011\|option\|qmi\|wwan\|ttyUSB'
    [    1.967031] usbcore: registered new interface driver qmi_wwan
    [    2.253212] usbcore: registered new interface driver option
    [    3.700857] usb 4-1: New USB device found, idVendor=1e0e, idProduct=9011
    [    5.504550] cgroup: cgroup2: unknown option "memory_recursiveprot"
    [    6.557039] systemd[1]: /etc/systemd/system/rc-local.service:11: Support for option SysVStartPriority= has been removed and it is ignored
    [   11.818187] usb 8-1: ch341-uart converter now attached to ttyUSB0
    root@harvest05:~#


            ---- Sent utf8 encoded message: "ls /dev/ttyUSB2 || echo ERROR_MS\r\n" ----
            ls /dev/ttyUSB2 || echo ERROR_MS
            /dev/ttyUSB2
            root@harvest05:~#
            root@harvest05:~#
            ---- Sent utf8 encoded message: "ls /dev/ttyUSB2\r\n" ----
            ls /dev/ttyUSB2
            /dev/ttyUSB2
            root@harvest05:~#
            root@harvest05:~#
            ---- Sent utf8 encoded message: "ls /dev/ttyUSB222\r\n" ----
            ls /dev/ttyUSB222
            ls: cannot access '/dev/ttyUSB222': No such file or directory
            root@harvest05:~#
            root@harvest05:~#
            ---- Sent utf8 encoded message: "ls /dev/ttyUSB2222 || echo ERROR_MS\r\n" ----
            ls /dev/ttyUSB2222 || echo ERROR_MS
            ls: cannot access '/dev/ttyUSB2222': No such file or directory
            ERROR_MS
            root@harvest05:~#
            root@harvest05:~#


            ДАННЫЕ ВСЕ УСТРОЙСТВ
            ОТЛИЧИЯ ГРУППЫ
            Ключ	/dev/ttyUSB1	/dev/ttyUSB2	/dev/ttyUSB3
            DEVPATH	.../usb4/4-1/4-1:1.2/ttyUSB1...	.../usb4/4-1/4-1:1.4/ttyUSB2...	.../usb4/4-1/4-1:1.5/ttyUSB3...
            DEVNAME	/dev/ttyUSB1	/dev/ttyUSB2	/dev/ttyUSB3
            MINOR	1	2	3
            USEC_INITIALIZED	6102352040	6102359538	6102362425
            ID_USB_INTERFACE_NUM	02	04	05
            ID_PATH	...-usb-0:1:1.2	...-usb-0:1:1.4	...-usb-0:1:1.5
            ID_PATH_TAG	...-usb-0_1_1_2	...-usb-0_1_1_4	...-usb-0_1_1_5
            DEVLINKS	...-if02-port0 / ...1.2-port0	...-if04-port0 / ...1.4-port0	...-if05-port0 / ...1.5-port0

            {
              "/dev/ttyUSB0": {
                "DEVPATH": "/devices/platform/soc/1c1d400.usb/usb8/8-1/8-1:1.0/ttyUSB0/tty/ttyUSB0",
                "DEVNAME": "/dev/ttyUSB0",
                "MAJOR": "188",
                "MINOR": "0",
                "SUBSYSTEM": "tty",
                "USEC_INITIALIZED": "11918469",
                "ID_BUS": "usb",
                "ID_MODEL": "USB_Serial",
                "ID_MODEL_ENC": "USB\\x20Serial",
                "ID_MODEL_ID": "7523",
                "ID_SERIAL": "1a86_USB_Serial",
                "ID_VENDOR": "1a86",
                "ID_VENDOR_ENC": "1a86",
                "ID_VENDOR_ID": "1a86",
                "ID_REVISION": "0264",
                "ID_TYPE": "generic",
                "ID_USB_MODEL": "USB_Serial",
                "ID_USB_MODEL_ENC": "USB\\x20Serial",
                "ID_USB_MODEL_ID": "7523",
                "ID_USB_SERIAL": "1a86_USB_Serial",
                "ID_USB_VENDOR": "1a86",
                "ID_USB_VENDOR_ENC": "1a86",
                "ID_USB_VENDOR_ID": "1a86",
                "ID_USB_REVISION": "0264",
                "ID_USB_TYPE": "generic",
                "ID_USB_INTERFACES": ":ff0102:",
                "ID_USB_INTERFACE_NUM": "00",
                "ID_USB_DRIVER": "ch341",
                "ID_USB_CLASS_FROM_DATABASE": "Vendor Specific Class",
                "ID_VENDOR_FROM_DATABASE": "QinHeng Electronics",
                "ID_MODEL_FROM_DATABASE": "CH340 serial converter",
                "ID_PATH": "platform-1c1d400.usb-usb-0:1:1.0",
                "ID_PATH_TAG": "platform-1c1d400_usb-usb-0_1_1_0",
                "ID_MM_CANDIDATE": "1",
                "DEVLINKS": "/dev/serial/by-path/platform-1c1d400.usb-usb-0:1:1.0-port0 /dev/serial/by-id/usb-1a86_USB_Serial-if00-port0",
                "TAGS": ":systemd:",
                "CURRENT_TAGS": ":systemd:"
              },
             "/dev/ttyUSB1": {
                "DEVPATH": "/devices/platform/soc/1c1c000.usb/usb4/4-1/4-1:1.2/ttyUSB1/tty/ttyUSB1",
                "DEVNAME": "/dev/ttyUSB1",
                "MAJOR": "188",
                "MINOR": "1",
                "SUBSYSTEM": "tty",
                "USEC_INITIALIZED": "6102352040",
                "ID_BUS": "usb",
                "ID_MODEL": "A76XX_Series_LTE_Module",
                "ID_MODEL_ENC": "A76XX\\x20Series\\x20LTE\\x20Module",
                "ID_MODEL_ID": "9011",
                "ID_SERIAL": "SIMCom_Wireless_Solution_A76XX_Series_LTE_Module_200806006809080000",
                "ID_SERIAL_SHORT": "200806006809080000",
                "ID_VENDOR": "SIMCom_Wireless_Solution",
                "ID_VENDOR_ENC": "SIMCom\\x20Wireless\\x20Solution",
                "ID_VENDOR_ID": "1e0e",
                "ID_REVISION": "0100",
                "ID_TYPE": "generic",
                "ID_USB_MODEL": "A76XX_Series_LTE_Module",
                "ID_USB_MODEL_ENC": "A76XX\\x20Series\\x20LTE\\x20Module",
                "ID_USB_MODEL_ID": "9011",
                "ID_USB_SERIAL": "SIMCom_Wireless_Solution_A76XX_Series_LTE_Module_200806006809080000",
                "ID_USB_SERIAL_SHORT": "200806006809080000",
                "ID_USB_VENDOR": "SIMCom_Wireless_Solution",
                "ID_USB_VENDOR_ENC": "SIMCom\\x20Wireless\\x20Solution",
                "ID_USB_VENDOR_ID": "1e0e",
                "ID_USB_REVISION": "0100",
                "ID_USB_TYPE": "generic",
                "ID_USB_INTERFACES": ":e00103:0a0000:ff0000:",
                "ID_USB_INTERFACE_NUM": "02",
                "ID_USB_DRIVER": "option",
                "ID_USB_CLASS_FROM_DATABASE": "Miscellaneous Device",
                "ID_USB_PROTOCOL_FROM_DATABASE": "Interface Association",
                "ID_VENDOR_FROM_DATABASE": "Qualcomm / Option",
                "ID_PATH": "platform-1c1c000.usb-usb-0:1:1.2",
                "ID_PATH_TAG": "platform-1c1c000_usb-usb-0_1_1_2",
                "ID_MM_CANDIDATE": "1",
                "DEVLINKS": "/dev/serial/by-path/platform-1c1c000.usb-usb-0:1:1.2-port0 /dev/serial/by-id/usb-SIMCom_Wireless_Solution_A76XX_Series_LTE_Module_200806006809080000-if02-port0",
                "TAGS": ":systemd:",
                "CURRENT_TAGS": ":systemd:"
              },
              !!!!!НАШ КАНДИТАТ!!!
              "/dev/ttyUSB2": {
                "DEVPATH": "/devices/platform/soc/1c1c000.usb/usb4/4-1/4-1:1.4/ttyUSB2/tty/ttyUSB2",
                "DEVNAME": "/dev/ttyUSB2",
                "MAJOR": "188",
                "MINOR": "2",
                "SUBSYSTEM": "tty",
                "USEC_INITIALIZED": "6102359538",
                "ID_BUS": "usb",
                "ID_MODEL": "A76XX_Series_LTE_Module",
                "ID_MODEL_ENC": "A76XX\\x20Series\\x20LTE\\x20Module",
                "ID_MODEL_ID": "9011",
                "ID_SERIAL": "SIMCom_Wireless_Solution_A76XX_Series_LTE_Module_200806006809080000",
                "ID_SERIAL_SHORT": "200806006809080000",
                "ID_VENDOR": "SIMCom_Wireless_Solution",
                "ID_VENDOR_ENC": "SIMCom\\x20Wireless\\x20Solution",
                "ID_VENDOR_ID": "1e0e",
                "ID_REVISION": "0100",
                "ID_TYPE": "generic",
                "ID_USB_MODEL": "A76XX_Series_LTE_Module",
                "ID_USB_MODEL_ENC": "A76XX\\x20Series\\x20LTE\\x20Module",
                "ID_USB_MODEL_ID": "9011",
                "ID_USB_SERIAL": "SIMCom_Wireless_Solution_A76XX_Series_LTE_Module_200806006809080000",
                "ID_USB_SERIAL_SHORT": "200806006809080000",
                "ID_USB_VENDOR": "SIMCom_Wireless_Solution",
                "ID_USB_VENDOR_ENC": "SIMCom\\x20Wireless\\x20Solution",
                "ID_USB_VENDOR_ID": "1e0e",
                "ID_USB_REVISION": "0100",
                "ID_USB_TYPE": "generic",
                "ID_USB_INTERFACES": ":e00103:0a0000:ff0000:",
                "ID_USB_INTERFACE_NUM": "04",
                "ID_USB_DRIVER": "option",
                "ID_USB_CLASS_FROM_DATABASE": "Miscellaneous Device",
                "ID_USB_PROTOCOL_FROM_DATABASE": "Interface Association",
                "ID_VENDOR_FROM_DATABASE": "Qualcomm / Option",
                "ID_PATH": "platform-1c1c000.usb-usb-0:1:1.4",
                "ID_PATH_TAG": "platform-1c1c000_usb-usb-0_1_1_4",
                "ID_MM_CANDIDATE": "1",
                "DEVLINKS": "/dev/serial/by-id/usb-SIMCom_Wireless_Solution_A76XX_Series_LTE_Module_200806006809080000-if04-port0 /dev/serial/by-path/platform-1c1c000.usb-usb-0:1:1.4-port0",
                "TAGS": ":systemd:",
                "CURRENT_TAGS": ":systemd:"
              },
              "/dev/ttyUSB3": {
                "DEVPATH": "/devices/platform/soc/1c1c000.usb/usb4/4-1/4-1:1.5/ttyUSB3/tty/ttyUSB3",
                "DEVNAME": "/dev/ttyUSB3",
                "MAJOR": "188",
                "MINOR": "3",
                "SUBSYSTEM": "tty",
                "USEC_INITIALIZED": "6102362425",
                "ID_BUS": "usb",
                "ID_MODEL": "A76XX_Series_LTE_Module",
                "ID_MODEL_ENC": "A76XX\\x20Series\\x20LTE\\x20Module",
                "ID_MODEL_ID": "9011",
                "ID_SERIAL": "SIMCom_Wireless_Solution_A76XX_Series_LTE_Module_200806006809080000",
                "ID_SERIAL_SHORT": "200806006809080000",
                "ID_VENDOR": "SIMCom_Wireless_Solution",
                "ID_VENDOR_ENC": "SIMCom\\x20Wireless\\x20Solution",
                "ID_VENDOR_ID": "1e0e",
                "ID_REVISION": "0100",
                "ID_TYPE": "generic",
                "ID_USB_MODEL": "A76XX_Series_LTE_Module",
                "ID_USB_MODEL_ENC": "A76XX\\x20Series\\x20LTE\\x20Module",
                "ID_USB_MODEL_ID": "9011",
                "ID_USB_SERIAL": "SIMCom_Wireless_Solution_A76XX_Series_LTE_Module_200806006809080000",
                "ID_USB_SERIAL_SHORT": "200806006809080000",
                "ID_USB_VENDOR": "SIMCom_Wireless_Solution",
                "ID_USB_VENDOR_ENC": "SIMCom\\x20Wireless\\x20Solution",
                "ID_USB_VENDOR_ID": "1e0e",
                "ID_USB_REVISION": "0100",
                "ID_USB_TYPE": "generic",
                "ID_USB_INTERFACES": ":e00103:0a0000:ff0000:",
                "ID_USB_INTERFACE_NUM": "05",
                "ID_USB_DRIVER": "option",
                "ID_USB_CLASS_FROM_DATABASE": "Miscellaneous Device",
                "ID_USB_PROTOCOL_FROM_DATABASE": "Interface Association",
                "ID_VENDOR_FROM_DATABASE": "Qualcomm / Option",
                "ID_PATH": "platform-1c1c000.usb-usb-0:1:1.5",
                "ID_PATH_TAG": "platform-1c1c000_usb-usb-0_1_1_5",
                "ID_MM_CANDIDATE": "1",
                "DEVLINKS": "/dev/serial/by-id/usb-SIMCom_Wireless_Solution_A76XX_Series_LTE_Module_200806006809080000-if05-port0 /dev/serial/by-path/platform-1c1c000.usb-usb-0:1:1.5-port0",
                "TAGS": ":systemd:",
                "CURRENT_TAGS": ":systemd:"
              }

            ПРЕЗАПУСК!!!
            ВЫВОДЫ
            Устройство	Ключ	Первичная группа	Новая группа
            /dev/ttyUSB0	USEC_INITIALIZED	11866470	12067303
            /dev/ttyUSB1	USEC_INITIALIZED	6102352040	544886628
            /dev/ttyUSB2	USEC_INITIALIZED	6102359538	544877723
            /dev/ttyUSB3	USEC_INITIALIZED	6102362425	544889337
            Вывод: Все идентификаторы устройств (ID_MODEL, ID_VENDOR, ID_SERIAL, DEVLINKS и т.д.) полностью совпадают.
            Это подтверждает, что после перезагрузки определились те же самые физические устройства,
            просто процесс инициализации занял другое время (USEC_INITIALIZED).
            Никаких перестановок или изменений в составе оборудования не произошло.
            {
              "/dev/ttyUSB0": {
                "DEVPATH": "/devices/platform/soc/1c1d400.usb/usb8/8-1/8-1:1.0/ttyUSB0/tty/ttyUSB0",
                "DEVNAME": "/dev/ttyUSB0",
                "MAJOR": "188",
                "MINOR": "0",
                "SUBSYSTEM": "tty",
                "USEC_INITIALIZED": "12067303",
                "ID_BUS": "usb",
                "ID_MODEL": "USB_Serial",
                "ID_MODEL_ENC": "USB\\x20Serial",
                "ID_MODEL_ID": "7523",
                "ID_SERIAL": "1a86_USB_Serial",
                "ID_VENDOR": "1a86",
                "ID_VENDOR_ENC": "1a86",
                "ID_VENDOR_ID": "1a86",
                "ID_REVISION": "0264",
                "ID_TYPE": "generic",
                "ID_USB_MODEL": "USB_Serial",
                "ID_USB_MODEL_ENC": "USB\\x20Serial",
                "ID_USB_MODEL_ID": "7523",
                "ID_USB_SERIAL": "1a86_USB_Serial",
                "ID_USB_VENDOR": "1a86",
                "ID_USB_VENDOR_ENC": "1a86",
                "ID_USB_VENDOR_ID": "1a86",
                "ID_USB_REVISION": "0264",
                "ID_USB_TYPE": "generic",
                "ID_USB_INTERFACES": ":ff0102:",
                "ID_USB_INTERFACE_NUM": "00",
                "ID_USB_DRIVER": "ch341",
                "ID_USB_CLASS_FROM_DATABASE": "Vendor Specific Class",
                "ID_VENDOR_FROM_DATABASE": "QinHeng Electronics",
                "ID_MODEL_FROM_DATABASE": "CH340 serial converter",
                "ID_PATH": "platform-1c1d400.usb-usb-0:1:1.0",
                "ID_PATH_TAG": "platform-1c1d400_usb-usb-0_1_1_0",
                "ID_MM_CANDIDATE": "1",
                "DEVLINKS": "/dev/serial/by-path/platform-1c1d400.usb-usb-0:1:1.0-port0 /dev/serial/by-id/usb-1a86_USB_Serial-if00-port0",
                "TAGS": ":systemd:",
                "CURRENT_TAGS": ":systemd:"
              },
              "/dev/ttyUSB1": {
                "DEVPATH": "/devices/platform/soc/1c1c000.usb/usb4/4-1/4-1:1.2/ttyUSB1/tty/ttyUSB1",
                "DEVNAME": "/dev/ttyUSB1",
                "MAJOR": "188",
                "MINOR": "1",
                "SUBSYSTEM": "tty",
                "USEC_INITIALIZED": "544886628",
                "ID_BUS": "usb",
                "ID_MODEL": "A76XX_Series_LTE_Module",
                "ID_MODEL_ENC": "A76XX\\x20Series\\x20LTE\\x20Module",
                "ID_MODEL_ID": "9011",
                "ID_SERIAL": "SIMCom_Wireless_Solution_A76XX_Series_LTE_Module_200806006809080000",
                "ID_SERIAL_SHORT": "200806006809080000",
                "ID_VENDOR": "SIMCom_Wireless_Solution",
                "ID_VENDOR_ENC": "SIMCom\\x20Wireless\\x20Solution",
                "ID_VENDOR_ID": "1e0e",
                "ID_REVISION": "0100",
                "ID_TYPE": "generic",
                "ID_USB_MODEL": "A76XX_Series_LTE_Module",
                "ID_USB_MODEL_ENC": "A76XX\\x20Series\\x20LTE\\x20Module",
                "ID_USB_MODEL_ID": "9011",
                "ID_USB_SERIAL": "SIMCom_Wireless_Solution_A76XX_Series_LTE_Module_200806006809080000",
                "ID_USB_SERIAL_SHORT": "200806006809080000",
                "ID_USB_VENDOR": "SIMCom_Wireless_Solution",
                "ID_USB_VENDOR_ENC": "SIMCom\\x20Wireless\\x20Solution",
                "ID_USB_VENDOR_ID": "1e0e",
                "ID_USB_REVISION": "0100",
                "ID_USB_TYPE": "generic",
                "ID_USB_INTERFACES": ":e00103:0a0000:ff0000:",
                "ID_USB_INTERFACE_NUM": "02",
                "ID_USB_DRIVER": "option",
                "ID_USB_CLASS_FROM_DATABASE": "Miscellaneous Device",
                "ID_USB_PROTOCOL_FROM_DATABASE": "Interface Association",
                "ID_VENDOR_FROM_DATABASE": "Qualcomm / Option",
                "ID_PATH": "platform-1c1c000.usb-usb-0:1:1.2",
                "ID_PATH_TAG": "platform-1c1c000_usb-usb-0_1_1_2",
                "ID_MM_CANDIDATE": "1",
                "DEVLINKS": "/dev/serial/by-path/platform-1c1c000.usb-usb-0:1:1.2-port0 /dev/serial/by-id/usb-SIMCom_Wireless_Solution_A76XX_Series_LTE_Module_200806006809080000-if02-port0",
                "TAGS": ":systemd:",
                "CURRENT_TAGS": ":systemd:"
              },
              "/dev/ttyUSB2": {
                "DEVPATH": "/devices/platform/soc/1c1c000.usb/usb4/4-1/4-1:1.4/ttyUSB2/tty/ttyUSB2",
                "DEVNAME": "/dev/ttyUSB2",
                "MAJOR": "188",
                "MINOR": "2",
                "SUBSYSTEM": "tty",
                "USEC_INITIALIZED": "544877723",
                "ID_BUS": "usb",
                "ID_MODEL": "A76XX_Series_LTE_Module",
                "ID_MODEL_ENC": "A76XX\\x20Series\\x20LTE\\x20Module",
                "ID_MODEL_ID": "9011",
                "ID_SERIAL": "SIMCom_Wireless_Solution_A76XX_Series_LTE_Module_200806006809080000",
                "ID_SERIAL_SHORT": "200806006809080000",
                "ID_VENDOR": "SIMCom_Wireless_Solution",
                "ID_VENDOR_ENC": "SIMCom\\x20Wireless\\x20Solution",
                "ID_VENDOR_ID": "1e0e",
                "ID_REVISION": "0100",
                "ID_TYPE": "generic",
                "ID_USB_MODEL": "A76XX_Series_LTE_Module",
                "ID_USB_MODEL_ENC": "A76XX\\x20Series\\x20LTE\\x20Module",
                "ID_USB_MODEL_ID": "9011",
                "ID_USB_SERIAL": "SIMCom_Wireless_Solution_A76XX_Series_LTE_Module_200806006809080000",
                "ID_USB_SERIAL_SHORT": "200806006809080000",
                "ID_USB_VENDOR": "SIMCom_Wireless_Solution",
                "ID_USB_VENDOR_ENC": "SIMCom\\x20Wireless\\x20Solution",
                "ID_USB_VENDOR_ID": "1e0e",
                "ID_USB_REVISION": "0100",
                "ID_USB_TYPE": "generic",
                "ID_USB_INTERFACES": ":e00103:0a0000:ff0000:",
                "ID_USB_INTERFACE_NUM": "04",
                "ID_USB_DRIVER": "option",
                "ID_USB_CLASS_FROM_DATABASE": "Miscellaneous Device",
                "ID_USB_PROTOCOL_FROM_DATABASE": "Interface Association",
                "ID_VENDOR_FROM_DATABASE": "Qualcomm / Option",
                "ID_PATH": "platform-1c1c000.usb-usb-0:1:1.4",
                "ID_PATH_TAG": "platform-1c1c000_usb-usb-0_1_1_4",
                "ID_MM_CANDIDATE": "1",
                "DEVLINKS": "/dev/serial/by-id/usb-SIMCom_Wireless_Solution_A76XX_Series_LTE_Module_200806006809080000-if04-port0 /dev/serial/by-path/platform-1c1c000.usb-usb-0:1:1.4-port0",
                "TAGS": ":systemd:",
                "CURRENT_TAGS": ":systemd:"
              },
              "/dev/ttyUSB3": {
                "DEVPATH": "/devices/platform/soc/1c1c000.usb/usb4/4-1/4-1:1.5/ttyUSB3/tty/ttyUSB3",
                "DEVNAME": "/dev/ttyUSB3",
                "MAJOR": "188",
                "MINOR": "3",
                "SUBSYSTEM": "tty",
                "USEC_INITIALIZED": "544889337",
                "ID_BUS": "usb",
                "ID_MODEL": "A76XX_Series_LTE_Module",
                "ID_MODEL_ENC": "A76XX\\x20Series\\x20LTE\\x20Module",
                "ID_MODEL_ID": "9011",
                "ID_SERIAL": "SIMCom_Wireless_Solution_A76XX_Series_LTE_Module_200806006809080000",
                "ID_SERIAL_SHORT": "200806006809080000",
                "ID_VENDOR": "SIMCom_Wireless_Solution",
                "ID_VENDOR_ENC": "SIMCom\\x20Wireless\\x20Solution",
                "ID_VENDOR_ID": "1e0e",
                "ID_REVISION": "0100",
                "ID_TYPE": "generic",
                "ID_USB_MODEL": "A76XX_Series_LTE_Module",
                "ID_USB_MODEL_ENC": "A76XX\\x20Series\\x20LTE\\x20Module",
                "ID_USB_MODEL_ID": "9011",
                "ID_USB_SERIAL": "SIMCom_Wireless_Solution_A76XX_Series_LTE_Module_200806006809080000",
                "ID_USB_SERIAL_SHORT": "200806006809080000",
                "ID_USB_VENDOR": "SIMCom_Wireless_Solution",
                "ID_USB_VENDOR_ENC": "SIMCom\\x20Wireless\\x20Solution",
                "ID_USB_VENDOR_ID": "1e0e",
                "ID_USB_REVISION": "0100",
                "ID_USB_TYPE": "generic",
                "ID_USB_INTERFACES": ":e00103:0a0000:ff0000:",
                "ID_USB_INTERFACE_NUM": "05",
                "ID_USB_DRIVER": "option",
                "ID_USB_CLASS_FROM_DATABASE": "Miscellaneous Device",
                "ID_USB_PROTOCOL_FROM_DATABASE": "Interface Association",
                "ID_VENDOR_FROM_DATABASE": "Qualcomm / Option",
                "ID_PATH": "platform-1c1c000.usb-usb-0:1:1.5",
                "ID_PATH_TAG": "platform-1c1c000_usb-usb-0_1_1_5",
                "ID_MM_CANDIDATE": "1",
                "DEVLINKS": "/dev/serial/by-id/usb-SIMCom_Wireless_Solution_A76XX_Series_LTE_Module_200806006809080000-if05-port0 /dev/serial/by-path/platform-1c1c000.usb-usb-0:1:1.5-port0",
                "TAGS": ":systemd:",
                "CURRENT_TAGS": ":systemd:"
              }
            }
            }
            """
    # return "/dev/ttyUSB2"
    result: str | None = None
    # 1=------------------------------------------------------------
    assert harvest.cmd_timeout__check_executed_success(
        "lsusb | grep -i qualcomm"), "устройствоне обнружено [9011 Qualcomm]"

    # ------------------------------------------------------------
    # 2=Пробуем активировать драйвер (безопасно, даже если уже загружен)
    assert harvest.cmd_timeout__check_executed_success(
        "modprobe option"), "драйвер не установлен ID 1e0e:9011 Qualcomm / Option A76XX Series LTE Module"

    # 3=------------------------------------------------------------
    # можно запускать сколько угодно! ошибки не будет!
    """
    сама команда дает результат того куда что подключено - НО если DMSG включен!!! 

    ---- Sent utf8 encoded message: "echo "1e0e 9011" > /sys/bus/usb-serial/drivers/option1/new_id 2>/dev/null\r\n" ----
echo "1e0e 9011" > /sys/bus/usb-serial/drivers/option1/new_id 2>/dev/null
[ 6102.041184] option 4-1:1.2: GSM modem (1-port) converter detected
[ 6102.048043] usb 4-1: GSM modem (1-port) converter now attached to ttyUSB1
[ 6102.057099] option 4-1:1.4: GSM modem (1-port) converter detected
[ 6102.064194] usb 4-1: GSM modem (1-port) converter now attached to ttyUSB2
[ 6102.073013] option 4-1:1.5: GSM modem (1-port) converter detected
[ 6102.079925] usb 4-1: GSM modem (1-port) converter now attached to ttyUSB3
root@harvest05:~# 
    """
    assert harvest.cmd_timeout__check_executed_success(
        'echo "1e0e 9011" > /sys/bus/usb-serial/drivers/option1/new_id 2>/dev/null'
    ), "активация шины связи для AT команд не состоялось"
    time.sleep(1)  # даём время на создание портов

    port_candidates = harvest.cmd_parsed__ls(path="/dev/", filters=EqValid_Regexp(r"ttyUSB\d+"))
    assert port_candidates, f"не обнаружены варианты портов для перебора {port_candidates=}"

    for port in port_candidates:
        props = harvest.get_info__usb(port)

        # 4=Проверяем props ---------------
        if any([
            not props,
            props.get("ID_VENDOR_ID") != "1e0e",
            props.get("ID_MODEL_ID") != "9011",
            "A76XX" not in props.get("ID_MODEL", ""),
            props.get("ID_USB_DRIVER") != "option",
        ]):
            print(f"[SKIPPED] {port=}")
            continue

        # 5=Проверяем AT-ответ
        out = harvest.cmd_timeout__write_read__payload(
            f"stty -F {port} 115200 raw -echo 2>/dev/null; "
            f"cat {port} & sleep 0.1; "
            f"printf 'AT\\r\\n' > {port}; "
            f"sleep 0.3; "
            f"kill %1 2>/dev/null",
            timeout=3,
        )
        if "OK" not in out:
            continue

        result = port

        # 6=Настраиваем порт на постоянку (raw mode + отключаем эхо)
        assert harvest.cmd_timeout__check_executed_success(
            f"stty -F {port} 115200 raw -echo -echoe -echok -echoctl 2>/dev/null; "
            f"cat {port} & sleep 0.1; "
            f"printf 'ATE0\\r\\n' > {port}; "
            f"sleep 0.2; "
            f"kill %1 2>/dev/null",
            timeout=3,
        ), f"не удалось натсроить порт"

        if result:
            break

    assert result, f"порт устройства для отправки AT команд не найден! {port_candidates=}"

    # # убиваем ВСЕ процессы, которые могли остаться на порту
    # harvest.conn.write_bytes(f"fuser -k {result} 2>/dev/null")
    # time.sleep(0.5)

    print(f"[DETECTED] {result=}")
    return result


# ----------------------------------------------------------------------------------------------------------------------
@pytest.fixture(scope="session")
def gsm_at__dump(harvest, gsm_at__port):
    dump = harvest.at_cmd__dump(port=gsm_at__port, method_simple=True)
    print(json.dumps(dump, indent=2, ensure_ascii=False))
    return dump


# ======================================================================================================================
@pytest.fixture(scope="session")
def internet_access(harvest) -> bool:
    return harvest.check__has_internet()


# ======================================================================================================================
@pytest.fixture(scope="module")
def ultrasonic_mac__any(harvest) -> str | None:
    """Находит MAC-адрес UltraSonic датчика."""
    bt_devs = harvest.bt__scan()
    for mac, name in bt_devs.items():
        if str(name).lower() == "UltraSonic".lower():
            return mac


# ======================================================================================================================
# HTML REPORT
def patch_html__title(filepath, new_title, **kwargs):
    """Заменяет содержимое тега <h1 id="title"> в HTML-отчёте."""
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    new_html = re.sub(
        r'<h1 id="title">.*?</h1>',
        f'<h1 id="title">{new_title}</h1>',
        html
    )
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_html)
    print(f"Заголовок отчёта изменён на '{new_title}'")


@pytest.hookimpl(trylast=True)
def pytest_unconfigure(config):
    """
    GOAL
    finalise all processes
    """
    # 1=HTML ----------------------------------------------------------------------------
    # Переименовывает HTML-отчёт, добавляя dev_id и текущую дату-время
    html_path = config.getoption('--html', default=None)
    if not html_path:
        print("HTML-отчёт не задан – переименование не требуется.")
        return

    # Даём время на завершение записи файла
    for _ in range(10):
        if os.path.isfile(html_path):
            break
        time.sleep(0.5)
    else:
        print(f"HTML-отчёт не появился: {html_path}")
        return

    # Получаем DEVICE_ID из stash – больше никакой глобальной переменной
    DEVICE_ID = config.stash.get("device_id", None)
    if DEVICE_ID is None:
        print("DEVICE_ID не определён")

    mark_expr = config.getoption('markexpr', default='')
    safe_mark = mark_expr.replace(' ', '_').replace('(', '').replace(')', '')

    dir_name, file_name = os.path.split(html_path)
    print(dir_name, file_name)
    date_str = datetime.now().strftime('%Y.%m.%d_%H-%M-%S')

    new_name = f"{DEVICE_ID}_{date_str}_m[{safe_mark}].html"
    new_path = os.path.join(dir_name, new_name)

    try:
        os.rename(html_path, new_path)
        print(f"Отчёт переименован в: {new_path}")
        # Меняем заголовок
        title = f"{DEVICE_ID} – {date_str}"
        if safe_mark:
            title += f" (markers: {safe_mark})"
        patch_html__title(filepath=new_path, new_title=new_name)
    except OSError as exc:
        print(f"Ошибка переименования отчёта: {exc!r}")


# ======================================================================================================================
