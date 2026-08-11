from typing import *

import time
import re
import threading
import json
import logging
import base64
import pathlib

from base_aux.buses.d1_serial2_new.m1_serial_client import SerialClient2
from base_aux.aux_eq.m3_eq_valid3_derivatives import *


# ======================================================================================================================
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ======================================================================================================================
class Harvest:
    AT_CMD__DUMP: list[str] = [
        # =========================================================================
        "AT",  # ответ эхо - проверка функционирования модема на канал

        # =========================================================================
        # попытка определить номер телефона
        "AT+CNUM",                # Основной запрос номера - НЕДОСТУПЕН НА M2M SIM!!!
        # "AT+CPBS=\"ON\"; +CPBR=1",  # Чтение своего номера из книги
        # "AT+CPBS=\'ON\'; +CPBR=1",  # Чтение своего номера из книги
        # "AT+CIMI",                # IMSI (для идентификации)
        # "AT+CRSM=176,28589,0,0,12",  # Чтение EF_MSISDN с SIM (прямой доступ)
        #
        # "+CNUM",  #
        # "+CNUM?",  #
        # "AT+CNUM?",  #
        # "AT+CNUM",  #

        # =========================================================================
        # ИДЕНТИФИКАЦИЯ И ВЕРСИИ
        "ATI",  # Общая информация о производителе/модели
        "AT+CGMI",  # Запрос производителя (Manufacturer ID)
        "AT+CGMM",  # Запрос модели (Model ID)
        "AT+CGMR",  # Запрос ревизии прошивки (Revision)
        "AT+CGSN",  # Запрос IMEI (Serial Number)
        "AT+CIMI",  # Запрос IMSI (International Mobile Subscriber ID)
        "AT+GSN",  # Аналог CGSN — IMEI

        # =========================================================================
        # СОСТОЯНИЕ SIM-КАРТЫ И PIN
        "AT+CPIN?",  # Статус SIM: READY, SIM PIN, SIM PUK, SIM PIN2...
        # "AT+CPINR=\"SIM PIN\"",  # Остаток попыток ввода PIN
        # "AT+CPINR=\"SIM PUK\"",  # Остаток попыток ввода PUK
        "AT+CCID",      # ICCID (серийный номер SIM-карты)
        "AT+ICCID",  # ICCID (серийный номер SIM-карты)

        # =========================================================================
        # СЕТЬ И РЕГИСТРАЦИЯ
        "AT+COPS?",  # Текущий оператор (режим, формат, MCC/MNC)
        # "AT+COPS=3,2; +COPS?",  # Принудительно числовой формат + получить оператора
        "AT+CREG?",  # Статус регистрации в сети (0=нет, 1=домашняя, 5=роуминг)
        "AT+CGREG?",  # Статус GPRS/PS регистрации
        "AT+CEREG?",  # Статус EPS (LTE) регистрации

        # =========================================================================
        # УРОВЕНЬ СИГНАЛА И КАЧЕСТВО
        "AT+CSQ",  # RSSI (0-31) и BER (качество канала)
        "AT+CESQ",  # Расширенный запрос качества (RSSI, RSCP, ECN0, RSRP, RSRQ)

        # =========================================================================
        # ТЕКУЩАЯ СОТА И ЧАСТОТА
        "AT*CNTI=0",  # Информация о текущей соте (MCC, MNC, LAC, CellID, band, ARFCN)

        # =========================================================================
        # ТЕХНОЛОГИЯ РАДИОДОСТУПА (RAT)
        "AT+WS46?",  # Выбор технологии: 12=LTE, 2=3G, 0=2G/GERAN
        # "AT+COPS=3,2; +COPS?",  # (повтор для получения RAT в числовом виде)

        # =========================================================================
        # PDP / APN / ДАННЫЕ
        "AT+CGDCONT?",  # Список APN-профилей (apn, type, ip...)
        "AT+CGCONTRDP",  # Параметры активного PDP-контекста (IP, шлюз, DNS1, DNS2)
        "AT+CGPADDR",  # Список назначенных PDP-адресов (IP)
        "AT+CGACT?",  # Статус активации PDP-контекстов (0/1)
        "AT+CGATT?",  # Статус GPRS-присоединения (attached/detached)
        # "AT+CGDATA=\"PPP\"",  # Состояние data-вызова (idle/active)

        # =========================================================================
        # IMS (VoLTE / VoWiFi)
        "AT+CIMS?",  # Статус IMS-регистрации (0=не зарегистрирован, 1=зарегистрирован)
        "AT+CIREG?",  # IMS регистрация (более детально)

        # =========================================================================
        # РЕЖИМЫ ЭНЕРГОСБЕРЕЖЕНИЯ И ФУНКЦИОНАЛЬНОСТЬ
        "AT+CFUN?",  # Уровень функциональности (0=min, 1=full, 4=flight mode)
        "AT+CSCLK?",  # Режим сна (1=разрешён sleep mode)

        # =========================================================================
        # ТЕМПЕРАТУРА И ПИТАНИЕ
        "AT+CPMUTEMP?",  # Температура модуля (если поддерживается)
        "AT+CBC",  # Заряд батареи/питание (charge level, voltage)

        # =========================================================================
        # СОСЕДНИЕ СОТЫ (опционально, зависит от модуля)
        "AT+CCED?",  # Соседние соты (GSM/GPRS)
        "AT*CELLINFO?",  # Расширенная информация о сотах (vendor-specific)

        # =========================================================================
        # ОШИБКИ И СБРОСЫ (диагностика)
        "AT+CEER",  # Extended Error Report — причина последнего сбоя/разъединения
    ]

    COMPILE_EOF__STR = re.compile(r".+@.+:.*#\s*")

    def __init__(self, conn: SerialClient2):
        self.conn = conn
        self.hostname = None

    # ------------------------------------------------------------------------------------------------------------------
    def validate_conn(self) -> bool:
        """
        ============LOGIN
        harvest05 login:
        ---- Sent utf8 encoded message: "root\r\n" ----
        root
        Password:
        ---- Sent utf8 encoded message: "1\r\n" ----

        Linux harvest05 4.14.111 #193 SMP Thu Jun 10 18:20:47 CST 2021 armv7l

        The programs included with the Debian GNU/Linux system are free software;
        the exact distribution terms for each program are described in the
        individual files in /usr/share/doc/*/copyright.

        Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
        permitted by applicable law.
        Last login: Wed Jul 22 18:37:34 MSK 2026 on ttyS0
        root@harvest05:

        ===============secondary LOGGED_IN
        root@harvest05:~#
        ---- Sent utf8 encoded message: "root\r\n" ----
        root
        -bash: root: command not found
        root@harvest05:~#
        root@harvest05:~#
        """
        return (
                self.login_try()
                and
                self.login_check()
        )

    def login_try(self) -> bool:
        """
        harvest05 login:
        ---- Sent utf8 encoded message: "root\r\n" ----
        root
        Password:
        ---- Sent utf8 encoded message: "1\r\n" ----

        Linux harvest05 4.14.111 #193 SMP Thu Jun 10 18:20:47 CST 2021 armv7l

        The programs included with the Debian GNU/Linux system are free software;
        the exact distribution terms for each program are described in the
        individual files in /usr/share/doc/*/copyright.

        Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
        permitted by applicable law.
        Last login: Tue Aug  4 14:39:52 MSK 2026 on ttyS0
        root@harvest05:~#
        """
        # stop all previous
        self.conn.send__ctrl_c()

        data = self.conn.write_read_bytes(data="root", timeout_start=3, timeout_continue=0.9)
        if b"command not found" in data:
            # already logged in!
            return True

        elif b"Password:" in data:
            data = self.conn.write_read_bytes(data="1", timeout_start=6, timeout_continue=1.9)
            if b"root@harvest" in data:
                return True

        return False

    def login_check(self) -> bool:
        data = self.cmd_timeout__write_read_text(cmd="hostname")
        result = bool(self.COMPILE_EOF__STR.search(data))
        return result

    def get_hostname_and_occupy(self) -> str:
        device_name = self.cmd_timeout__write_read__payload(cmd="hostname")
        self.hostname = device_name
        self.conn.occupy(device_name)
        return device_name

    # WR ===============================================================================================================
    def _cmd_cover_timeout(self, cmd: str, timeout: float | None = None) -> str:
        """
        work with SYSTEMD_PAGER

---- Sent utf8 encoded message: "SYSTEMD_PAGER=cat udevadm info -q property -n /dev/ttyUSB0  2>/dev/null\r\n" ----
SYSTEMD_PAGER=cat udevadm info -q property -n /dev/ttyUSB0  2>/dev/null
DEVPATH=/devices/platform/soc/1c1d400.usb/usb8/8-1/8-1:1.0/ttyUSB0/tty/ttyUSB0
DEVNAME=/dev/ttyUSB0
MAJOR=188
MINOR=0
SUBSYSTEM=tty
USEC_INITIALIZED=13287546
ID_BUS=usb
ID_MODEL=USB_Serial
ID_MODEL_ENC=USB\x20Serial
ID_MODEL_ID=7523
ID_SERIAL=1a86_USB_Serial
ID_VENDOR=1a86
ID_VENDOR_ENC=1a86
ID_VENDOR_ID=1a86
ID_REVISION=0264
ID_TYPE=generic
ID_USB_MODEL=USB_Serial
ID_USB_MODEL_ENC=USB\x20Serial
ID_USB_MODEL_ID=7523
ID_USB_SERIAL=1a86_USB_Serial
ID_USB_VENDOR=1a86
ID_USB_VENDOR_ENC=1a86
ID_USB_VENDOR_ID=1a86
ID_USB_REVISION=0264
ID_USB_TYPE=generic
ID_USB_INTERFACES=:ff0102:
ID_USB_INTERFACE_NUM=00
ID_USB_DRIVER=ch341
ID_USB_CLASS_FROM_DATABASE=Vendor Specific Class
ID_VENDOR_FROM_DATABASE=QinHeng Electronics
ID_MODEL_FROM_DATABASE=CH340 serial converter
ID_PATH=platform-1c1d400.usb-usb-0:1:1.0
ID_PATH_TAG=platform-1c1d400_usb-usb-0_1_1_0
ID_MM_CANDIDATE=1
DEVLINKS=/dev/serial/by-path/platform-1c1d400.usb-usb-0:1:1.0-port0 /dev/serial/by-id/usb-1a86_USB_Serial-if00-port0
TAGS=:systemd:
CURRENT_TAGS=:systemd:
root@harvest05:~#
root@harvest05:~#

---- Sent utf8 encoded message: "timeout 4 SYSTEMD_PAGER=cat udevadm info -q property -n /dev/ttyUSB0  2>/dev/null\r\n" ----
timeout 4 SYSTEMD_PAGER=cat udevadm info -q property -n /dev/ttyUSB0  2>/dev/null
root@harvest05:~#
root@harvest05:~#

---- Sent utf8 encoded message: "timeout 4 sh -c 'SYSTEMD_PAGER=cat udevadm info -q property -n /dev/ttyUSB0  2>/dev/null'\r\n" ----
timeout 4 sh -c 'SYSTEMD_PAGER=cat udevadm info -q property -n /dev/ttyUSB0  2>/dev/null'
DEVPATH=/devices/platform/soc/1c1d400.usb/usb8/8-1/8-1:1.0/ttyUSB0/tty/ttyUSB0
DEVNAME=/dev/ttyUSB0
MAJOR=188
MINOR=0
SUBSYSTEM=tty
USEC_INITIALIZED=13287546
ID_BUS=usb
ID_MODEL=USB_Serial
ID_MODEL_ENC=USB\x20Serial
ID_MODEL_ID=7523
ID_SERIAL=1a86_USB_Serial
ID_VENDOR=1a86
ID_VENDOR_ENC=1a86
ID_VENDOR_ID=1a86
ID_REVISION=0264
ID_TYPE=generic
ID_USB_MODEL=USB_Serial
ID_USB_MODEL_ENC=USB\x20Serial
ID_USB_MODEL_ID=7523
ID_USB_SERIAL=1a86_USB_Serial
ID_USB_VENDOR=1a86
ID_USB_VENDOR_ENC=1a86
ID_USB_VENDOR_ID=1a86
ID_USB_REVISION=0264
ID_USB_TYPE=generic
ID_USB_INTERFACES=:ff0102:
ID_USB_INTERFACE_NUM=00
ID_USB_DRIVER=ch341
ID_USB_CLASS_FROM_DATABASE=Vendor Specific Class
ID_VENDOR_FROM_DATABASE=QinHeng Electronics
ID_MODEL_FROM_DATABASE=CH340 serial converter
ID_PATH=platform-1c1d400.usb-usb-0:1:1.0
ID_PATH_TAG=platform-1c1d400_usb-usb-0_1_1_0
ID_MM_CANDIDATE=1
DEVLINKS=/dev/serial/by-id/usb-1a86_USB_Serial-if00-port0 /dev/serial/by-path/platform-1c1d400.usb-usb-0:1:1.0-port0
TAGS=:systemd:
CURRENT_TAGS=:systemd:
root@harvest05:~#
root@harvest05:~#
        """
        result = ""
        if timeout:
            result += f"timeout {timeout} "

        if cmd.startswith("SYSTEMD_PAGER"):
            cmd = f"sh -c '{cmd}'"

        result += cmd
        return result

    def cmd_timeout__write_bytes(self, cmd: str, timeout: float | None = None) -> bool:
        """
        запуск команды в среде linux с таймаутом в самой система

        2=VARIANT
        --------------------
        ---- Sent utf8 encoded message: "timeout 2 ping ya.ru\r\n" ----
        timeout 2 ping ya.ru
        PING ya.ru (77.88.44.242) 56(84) bytes of data.
        64 bytes from ya.ru (77.88.44.242): icmp_seq=1 ttl=57 time=41.1 ms
        64 bytes from ya.ru (77.88.44.242): icmp_seq=2 ttl=57 time=38.0 ms
        root@harvest05:~#
        root@harvest05:~#
        """
        # return self.conn.write_bytes(f"{cmd} & sleep {timeout}; kill %1")  # OLD-incorrect!
        return self.conn.write_bytes(self._cmd_cover_timeout(cmd, timeout))

    def cmd_timeout__write_read_bytes(self, cmd: str, timeout: float | None = None, **wr_kwargs) -> bytes:
        cmd = self._cmd_cover_timeout(cmd, timeout)
        return self.conn.write_read_bytes(cmd, **wr_kwargs)

    @property
    def stopline_prompt__eq(self) -> Base_EqValid:
        if self.hostname:
            stopline_prompt__eq = rb".*root@" + self.hostname.encode() + rb":~#.*"
        else:
            stopline_prompt__eq = rb".*root@.+:.+#.*"
        stop_line = EqValid_Regexp(stopline_prompt__eq)
        return stop_line

    def cmd_timeout__write_read_text(
            self,
            cmd: str,
            timeout: float | None = None,
            payload_only: bool | None = None,
            **wr_kwargs,
    ) -> str:
        cmd = self._cmd_cover_timeout(cmd, timeout)

        # ---------------------------------------
        if wr_kwargs.get("stop_line") is None:
            wr_kwargs["stop_line"] = self.stopline_prompt__eq

        output = self.conn.write_read_text(cmd, **wr_kwargs)
        if output.splitlines()[-1] != self.stopline_prompt__eq:
            self.conn.send__ctrl_c()
            time.sleep(0.2)

        if payload_only:
            output = self._stdout__parce_payload(cmd=cmd, data=output)

        print(f"[{self.conn.ADDRESS}.WRITEREAD]")
        print(f"\twrite=[", cmd, "]", sep="")
        print("\tread=[", output, "]", sep="")

        return output

    def _stdout__parce_payload(self, cmd: str, data: str) -> str:
        """

        пример когда появился еще вариант странный уникальный!!!

        [COM16.WRITEREAD]
	write=[ls /dev/ttyS2 2>/dev/null || echo ERROR_MSG]
	read=[/dev/ttyS2]
output='/dev/ttyS2'
[15:32:10.248577]COM16.reset_input[OK]= b'in_waiting=36'
[15:32:10.823471]COM16.write[OK]= b"printf '%s' 'IyA9PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09CiMgc2NyX19yZmlkX3NjYW4ucHkgLSDQktCV0KDQodCY0K8g0KEg0J/QoNCv0JzQq9CcINCY0JfQktCb0JXQp9CV0J3QmNCV0JwgRVBDCiMgPT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PQppbXBvcnQgc2VyaWFsLCB0aW1lLCBzeXMsIHJlCgpQT1JUID0gJy9kZXYvdHR5UzInCkJBVUQgPSAxMTUyMDAKVElNRU9VVCA9IDAuNQoKIyBSRUFEIEJBTksKQ01EID0gYnl0ZXMoWzB4QTAsIDB4MEEsIDB4MDEsIDB4ODEsIDB4MDEsIDB4MDAsIDB4MDgsIDB4MDAsIDB4MDAsIDB4MDAsIDB4MDAsIDB4Q0JdKQoKCmRlZiByZWFkX3Jlc3BvbnNlKCkgLT4gYnl0ZXM6CiAgICBzZXIgPSBzZXJpYWwuU2VyaWFsKFBPUlQsIEJBVUQsIHRpbWVvdXQ9VElNRU9VVCkKICAgIHNlci5yZXNldF9pbnB1dF9idWZmZXIoKQogICAgc2VyLndyaXRlKENNRCkKCiAgICByZXNwb25zZSA9IGIiIgogICAgc3RhcnQgPSB0aW1lLnRpbWUoKQogICAgd2hpbGUgdGltZS50aW1lKCkgLSBzdGFydCA8IDEuMDoKICAgICAgICBjaHVuayA9IHNlci5yZWFkKHNlci5pbl93YWl0aW5nIG9yIDEpCiAgICAgICAgaWYgY2h1bms6CiAgICAgICAgICAgIHJlc3BvbnNlICs9IGNodW5rCiAgICAgICAgZWxzZToKICAgICAgICAgICAgdGltZS5zbGVlcCgwLjA1KQogICAgc2VyLmNsb3NlKCkKICAgIHJldHVybiByZXNwb25zZQoKCmRlZiBwYXJzZV9lcGMoZGF0YSk6CiAgICBlcGNfbGlzdCA9IFtdCiAgICBpID0gMAoKICAgIHdoaWxlIGkgPCBsZW4oZGF0YSk6CiAgICAgICAgIyDQmNGJ0LXQvCDQvdCw0YfQsNC70L4g0L/QsNC60LXRgtCwIDB4QTAKICAgICAgICBpZiBkYXRhW2ldICE9IDB4QTA6CiAgICAgICAgICAgIGkgKz0gMQogICAgICAgICAgICBjb250aW51ZQoKICAgICAgICBpZiBpICsgMSA+PSBsZW4oZGF0YSk6CiAgICAgICAgICAgIGJyZWFrCgogICAgICAgIGxlbmd0aCA9IGRhdGFbaSArIDFdCiAgICAgICAgaWYgaSArIGxlbmd0aCArIDEgPiBsZW4oZGF0YSk6CiAgICAgICAgICAgIGkgKz0gMQogICAgICAgICAgICBjb250aW51ZQoKICAgICAgICBwYWNrZXQgPSBkYXRhW2k6aSArIGxlbmd0aCArIDFdCiAgICAgICAgaSArPSBsZW5ndGggKyAxCgogICAgICAgICMg0J/RgNC+0LLQtdGA0Y/QtdC8INGC0LjQvyDQv9Cw0LrQtdGC0LAgKDB4MDEgMHg4MSAtINC40L3QstC10L3RgtCw0YDQuNC30LDRhtC40Y8pCiAgICAgICAgaWYgbGVuKHBhY2tldCkgPCA2IG9yIHBhY2tldFsyXSAhPSAweDAxIG9yIHBhY2tldFszXSAhPSAweDgxOgogICAgICAgICAgICBjb250aW51ZQoKICAgICAgICAjINCY0YnQtdC8IEVQQyDQtNCw0L3QvdGL0LUKICAgICAgICAjINCe0LHRi9GH0L3QviBFUEMg0L3QsNGH0LjQvdCw0LXRgtGB0Y8g0L/QvtGB0LvQtSDQt9Cw0LPQvtC70L7QstC60LAgKNC/0YDQuNC80LXRgNC90L4g0YEgNy3Qs9C+INCx0LDQudGC0LApCiAgICAgICAgIyDQmNGJ0LXQvCDQv9C+0YHQu9C10LTQvtCy0LDRgtC10LvRjNC90L7RgdGC0LgsINC60L7RgtC+0YDRi9C1INC90LDRh9C40L3QsNGO0YLRgdGPINGBIDB4MzAg0LjQu9C4IDB4MzQgKNGF0LDRgNCw0LrRgtC10YDQvdC+INC00LvRjyBFUEMpCiAgICAgICAgZm9yIGogaW4gcmFuZ2UoNSwgbGVuKHBhY2tldCkpOgogICAgICAgICAgICAjINCf0YDQvtC/0YPRgdC60LDQtdC8INC+0LTQuNC90L7Rh9C90YvQtSDQsdCw0LnRgtGLINC4INC40YnQtdC8INC90LDRh9Cw0LvQviBFUEMKICAgICAgICAgICAgaWYgcGFja2V0W2pdIGluICgweDMwLCAweDM0KTogICMg0KXQsNGA0LDQutGC0LXRgNC90L7QtSDQvdCw0YfQsNC70L4gRVBDCiAgICAgICAgICAgICAgICAjINCf0YDQvtCy0LXRgNGP0LXQvCwg0YfRgtC+INC00LDQu9GM0YjQtSDQuNC00YPRgiDQtNCw0L3QvdGL0LUKICAgICAgICAgICAgICAgIHJlbWFpbmluZyA9IGxlbihwYWNrZXQpIC0gagogICAgICAgICAgICAgICAgaWYgcmVtYWluaW5nID49IDE0OiAgIyDQnNC40L3QuNC80YPQvCAxNCDQsdCw0LnRgiDQtNC70Y8g0L/QvtC70L3QvtCz0L4gRVBDCiAgICAgICAgICAgICAgICAgICAgIyDQmNC30LLQu9C10LrQsNC10Lwg0LTQviAyMCDQsdCw0LnRgiAoNDAgaGV4INGB0LjQvNCy0L7Qu9C+0LIpCiAgICAgICAgICAgICAgICAgICAgZXBjX2J5dGVzID0gcGFja2V0W2o6aiArIG1pbigyMCwgcmVtYWluaW5nKV0KCiAgICAgICAgICAgICAgICAgICAgIyDQpNC40LvRjNGC0YDRg9C10LwgLSDQvtGB0YLQsNCy0LvRj9C10Lwg0YLQvtC70YzQutC+IGhleC3RgdC40LzQstC+0LvRiwogICAgICAgICAgICAgICAgICAgIGhleF9zdHIgPSAnJwogICAgICAgICAgICAgICAgICAgIGZvciBiIGluIGVwY19ieXRlczoKICAgICAgICAgICAgICAgICAgICAgICAgaGV4X3N0ciArPSBmJ3tiOjAyWH0nCgogICAgICAgICAgICAgICAgICAgICMg0J/RgNC+0LLQtdGA0Y/QtdC8LCDRh9GC0L4g0YHRgtGA0L7QutCwINC/0L7RhdC+0LbQsCDQvdCwIEVQQyAo0L3QsNGH0LjQvdCw0LXRgtGB0Y8g0YEgMzAvMzQg0Lgg0LTQvtGB0YLQsNGC0L7Rh9C90L7QuSDQtNC70LjQvdGLKQogICAgICAgICAgICAgICAgICAgIGlmIGxlbihoZXhfc3RyKSA+PSAyMDogICMg0JzQuNC90LjQvNGD0LwgMTAg0LHQsNC50YIgPSAyMCDRgdC40LzQstC+0LvQvtCyCiAgICAgICAgICAgICAgICAgICAgICAgICMg0J7QsdGA0LXQt9Cw0LXQvCDQtNC+INGA0LDQt9GD0LzQvdC+0Lkg0LTQu9C40L3RiyAoMjAtMjgg0YHQuNC80LLQvtC70L7QsikKICAgICAgICAgICAgICAgICAgICAgICAgZm9yIGN1dF9sZW4gaW4gWzI4LCAyNiwgMjQsIDIyLCAyMF06CiAgICAgICAgICAgICAgICAgICAgICAgICAgICBjYW5kaWRhdGUgPSBoZXhfc3RyWzpjdXRfbGVuXQogICAgICAgICAgICAgICAgICAgICAgICAgICAgaWYgY2FuZGlkYXRlLnN0YXJ0c3dpdGgoKCczMCcsICczNCcpKSBhbmQgY2FuZGlkYXRlIG5vdCBpbiBlcGNfbGlzdDoKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBlcGNfbGlzdC5hcHBlbmQoY2FuZGlkYXRlKQogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIGJyZWFrCiAgICAgICAgICAgICAgICAgICAgYnJlYWsKCiAgICByZXR1cm4gZXBjX2xpc3QKCgpkZWYgcGFyc2VfZXBjX2FkdmFuY2VkKGRhdGEpOgogICAgIyDQo9C70YPRh9GI0LXQvdC90YvQuSDQv9Cw0YDRgdC10YAgRVBDCiAgICBlcGNfbGlzdCA9IFtdCiAgICBoZXhfZGF0YSA9IGRhdGEuaGV4KCkudXBwZXIoKQoKICAgICMg0JjRidC10LwgRVBDINC/0L4g0YXQsNGA0LDQutGC0LXRgNC90YvQvCDQv9GA0LjQt9C90LDQutCw0Lw6CiAgICAjIDEuINCd0LDRh9C40L3QsNGO0YLRgdGPINGBIDMwMDAsIDMwMEUsIDM0MDAKICAgICMgMi4g0JjQvNC10Y7RgiDQtNC70LjQvdGDIDIwLTI4INGB0LjQvNCy0L7Qu9C+0LIKICAgIHBhdHRlcm5zID0gWwogICAgICAgIHInKDMwMDBbMC05QS1GXXsxNiwyNH0pJywgICMgMzAwMCArIDE2LTI0IGhleCDRgdC40LzQstC+0LvQvtCyCiAgICAgICAgcicoMzAwRVswLTlBLUZdezE2LDI0fSknLCAgIyAzMDBFICsgMTYtMjQgaGV4INGB0LjQvNCy0L7Qu9C+0LIKICAgICAgICByJygzNDAwWzAtOUEtRl17MTYsMjR9KScsICAjIDM0MDAgKyAxNi0yNCBoZXgg0YHQuNC80LLQvtC70L7QsgogICAgXQoKICAgIGZvciBwYXR0ZXJuIGluIHBhdHRlcm5zOgogICAgICAgIG1hdGNoZXMgPSByZS5maW5kYWxsKHBhdHRlcm4sIGhleF9kYXRhKQogICAgICAgIGZvciBtYXRjaCBpbiBtYXRjaGVzOgogICAgICAgICAgICAjINCe0YHRgtCw0LLQu9GP0LXQvCDRgtC+0LvRjNC60L4g0L/QvtC70L3Ri9C1IEVQQyAo0L7QsdGL0YfQvdC+IDI0LTI4INGB0LjQvNCy0L7Qu9C+0LIpCiAgICAgICAgICAgIGlmIGxlbihtYXRjaCkgPj0gMjQ6CiAgICAgICAgICAgICAgICAjINCe0LHRgNC10LfQsNC10Lwg0LTQviDRgdGC0LDQvdC00LDRgNGC0L3QvtC5INC00LvQuNC90Ysg0LXRgdC70Lgg0L3Rg9C20L3QvgogICAgICAgICAgICAgICAgaWYgbGVuKG1hdGNoKSA+IDI4OgogICAgICAgICAgICAgICAgICAgIG1hdGNoID0gbWF0Y2hbOjI4XQogICAgICAgICAgICAgICAgaWYgbWF0Y2ggbm90IGluIGVwY19saXN0OgogICAgICAgICAgICAgICAgICAgIGVwY19saXN0LmFwcGVuZChtYXRjaCkKCiAgICAjINCV0YHQu9C4INC90LUg0L3QsNGI0LvQuCAtINC/0YDQvtCx0YPQtdC8INC90LDQudGC0Lgg0LvRjtCx0YvQtSDQtNC70LjQvdC90YvQtSBoZXgt0YHRgtGA0L7QutC4CiAgICBpZiBub3QgZXBjX2xpc3Q6CiAgICAgICAgbG9uZ19oZXggPSByZS5maW5kYWxsKHInKFswLTlBLUZdezI0LDI4fSknLCBoZXhfZGF0YSkKICAgICAgICBmb3IgY2FuZGlkYXRlIGluIGxvbmdfaGV4OgogICAgICAgICAgICBpZiBjYW5kaWRhdGUuc3RhcnRzd2l0aCgoJzMwJywgJzM0JykpIGFuZCBjYW5kaWRhdGUgbm90IGluIGVwY19saXN0OgogICAgICAgICAgICAgICAgZXBjX2xpc3QuYXBwZW5kKGNhbmRpZGF0ZSkKCiAgICByZXR1cm4gZXBjX2xpc3QKCgojID09PSBNQUlOID09PQppZiBfX25hbWVfXyA9PSAiX19tYWluX18iOgogICAgZGF0YSA9IHJlYWRfcmVzcG9uc2UoKQoKICAgICMg0J7RgtC70LDQtNC60LA6INC/0L7QutCw0LbQtdC8INGB0YvRgNGL0LUg0LTQsNC90L3Ri9C1CiAgICBwcmludChmIlJhd0RhdGEoe2xlbihkYXRhKX1ieXRlcyk6W3tkYXRhLmhleCgpLnVwcGVyKCl9XSIsIGZpbGU9c3lzLnN0ZGVycikKCiAgICB0YWdzID0gcGFyc2VfZXBjX2FkdmFuY2VkKGRhdGEpCgogICAgZm9yIGVwYyBpbiB0YWdzOgogICAgICAgIHByaW50KGVwYykKCiAgICBwcmludChmImZvdW5kPXtsZW4odGFncyl9ZXBjIikKICAgIHN5cy5leGl0KDAgaWYgdGFncyBlbHNlIDEpCgo=' | base64 -d > scr__rfid_scan.py 2>/dev/null || echo ERROR_MSG\r\n"
[15:32:13.292665]COM16.readEOL[OK]= b"printf '%s' 'IyA9PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09CiMgc2NyX19yZmlkX3NjYW4ucHkgLSDQktCV0KDQodCY0K8g0KEg0J/QoNCv0JzQq9CcINCY0JfQktCb0JXQp9CV0J3QmNCV0JwgRVBDCiMgPT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PQppbXBvcnQgc2VyaWFsLCB0aW1lLCBzeXMsIHJlCgpQT1JUID0gJy9kZXYvdHR5UzInCkJBVUQgPSAxMTUyMDAKVElNRU9VVCA9IDAuNQoKIyBSRUFEIEJBTksKQ01EID0gYnl0ZXMoWzB4QTAsIDB4MEEsIDB4MDEsIDB4ODEsIDB4MDEsIDB4MDAsIDB4MDgsIDB4MDAsIDB4MDAsIDB4MDAsIDB4MDAsIDB4Q0JdKQoKCmRlZiByZWFkX3Jlc3BvbnNlKCkgLT4gYnl0ZXM6CiAgICBzZXIgPSBzZXJpYWwuU2VyaWFsKFBPUlQsIEJBVUQsIHRpbWVvdXQ9VElNRU9VVCkKICAgIHNlci5yZXNldF9pbnB1dF9idWZmZXIoKQogICAgc2VyLndyaXRlKENNRCkKCiAgICByZXNwb25zZSA9IGIiIgogICAgc3RhcnQgPSB0aW1lLnRpbWUoKQogICAgd2hpbGUgdGltZS50aW1lKCkgLSBzdGFydCA8IDEuMDoKICAgICAgICBjaHVuayA9IHNlci5yZWFkKHNlci5pbl93YWl0aW5nIG9yIDEpCiAgICAgICAgaWYgY2h1bms6CiAgICAgICAgICAgIHJlc3BvbnNlICs9IGNodW5rCiAgICAgICAgZWxzZToKICAgICAgICAgICAgdGltZS5zbGVlcCgwLjA1KQogICAgc2VyLmNsb3NlKCkKICAgIHJldHVybiByZXNwb25zZQoKCmRlZiBwYXJzZV9lcGMoZGF0YSk6CiAgICBlcGNfbGlzdCA9IFtdCiAgICBpID0gMAoKICAgIHdoaWxlIGkgPCBsZW4oZGF0YSk6CiAgICAgICAgIyDQmNGJ0LXQvCDQvdCw0YfQsNC70L4g0L/QsNC60LXRgtCwIDB4QTAKICAgICAgICBpZiBkYXRhW2ldICE9IDB4QTA6CiAgICAgICAgICAgIGkgKz0gMQogICAgICAgICAgICBjb250aW51ZQoKICAgICAgICBpZiBpICsgMSA+PSBsZW4oZGF0YSk6CiAgICAgICAgICAgIGJyZWFrCgogICAgICAgIGxlbmd0aCA9IGRhdGFbaSArIDFdCiAgICAgICAgaWYgaSArIGxlbmd0aCArIDEgPiBsZW4oZGF0YSk6CiAgICAgICAgICAgIGkgKz0gMQogICAgICAgICAgICBjb250aW51ZQoKICAgICAgICBwYWNrZXQgPSBkYXRhW2k6aSArIGxlbmd0aCArIDFdCiAgICAgICAgaSArPSBsZW5ndGggKyAxCgogICAgICAgICMg0J/RgNC+0LLQtdGA0Y/QtdC8INGC0LjQvyDQv9Cw0LrQtdGC0LAgKDB4MDEgMHg4MSAtINC40L3QstC10L3RgtCw0YDQuNC30LDRhtC40Y8pCiAgICAgICAgaWYgbGVuKHBhY2tldCkgPCA2IG9yIHBhY2tldFsyXSAhPSAweDAxIG9yIHBhY2tldFszXSAhPSAweDgxOgogICAgICAgICAgICBjb250aW51ZQoKICAgICAgICAjINCY0YnQtdC8IEVQQyDQtNCw0L3QvdGL0LUKICAgICAgICAjINCe0LHRi9GH0L3QviBFUEMg0L3QsNGH0LjQvdCw0LXRgtGB0Y8g0L/QvtGB0LvQtSDQt9Cw0LPQvtC70L7QstC60LAgKNC/0YDQuNC80LXRgNC90L4g0YEgNy3Qs9C+INCx0LDQudGC0LApCiAgICAgICAgIyDQmNGJ0LXQvCDQv9C+0YHQu9C10LTQvtCy0LDRgtC10LvRjNC90L7RgdGC0LgsINC60L7RgtC+0YDRi9C1INC90LDRh9C40L3QsNGO0YLRgdGPINGBIDB4MzAg0LjQu9C4IDB4MzQgKNGF0LDRgNCw0LrRgtC10YDQvdC+INC00LvRjyBFUEMpCiAgICAgICAgZm9yIGogaW4gcmFuZ2UoNSwgbGVuKHBhY2tldCkpOgogICAgICAgICAgICAjINCf0YDQvtC/0YPRgdC60LDQtdC8INC+0LTQuNC90L7Rh9C90YvQtSDQsdCw0LnRgtGLINC4INC40YnQtdC8INC90LDRh9Cw0LvQviBFUEMKICAgICAgICAgICAgaWYgcGFja2V0W2pdIGluICgweDMwLCAweDM0KTogICMg0KXQsNGA0LDQutGC0LXRgNC90L7QtSDQvdCw0YfQsNC70L4gRVBDCiAgICAgICAgICAgICAgICAjINCf0YDQvtCy0LXRgNGP0LXQvCwg0YfRgtC+INC00LDQu9GM0YjQtSDQuNC00YPRgiDQtNCw0L3QvdGL0LUKICAgICAgICAgICAgICAgIHJlbWFpbmluZyA9IGxlbihwYWNrZXQpIC0gagogICAgICAgICAgICAgICAgaWYgcmVtYWluaW5nID49IDE0OiAgIyDQnNC40L3QuNC80YPQvCAxNCDQsdCw0LnRgiDQtNC70Y8g0L/QvtC70L3QvtCz0L4gRVBDCiAgICAgICAgICAgICAgICAgICAgIyDQmNC30LLQu9C10LrQsNC10Lwg0LTQviAyMCDQsdCw0LnRgiAoNDAgaGV4INGB0LjQvNCy0L7Qu9C+0LIpCiAgICAgICAgICAgICAgICAgICAgZXBjX2J5dGVzID0gcGFja2V0W2o6aiArIG1pbigyMCwgcmVtYWluaW5nKV0KCiAgICAgICAgICAgICAgICAgICAgIyDQpNC40LvRjNGC0YDRg9C10LwgLSDQvtGB0YLQsNCy0LvRj9C10Lwg0YLQvtC70YzQutC+IGhleC3RgdC40LzQstC+0LvRiwogICAgICAgICAgICAgICAgICAgIGhleF9zdHIgPSAnJwogICAgICAgICAgICAgICAgICAgIGZvciBiIGluIGVwY19ieXRlczoKICAgICAgICAgICAgICAgICAgICAgICAgaGV4X3N0ciArPSBmJ3tiOjAyWH0nCgogICAgICAgICAgICAgICAgICAgICMg0J/RgNC+0LLQtdGA0Y/QtdC8LCDRh9GC0L4g0YHRgtGA0L7QutCwINC/0L7RhdC+0LbQsCDQvdCwIEVQQyAo0L3QsNGH0LjQvdCw0LXRgtGB0Y8g0YEgMzAvMzQg0Lgg0LTQvtGB0YLQsNGC0L7Rh9C90L7QuSDQtNC70LjQvdGLKQogICAgICAgICAgICAgICAgICAgIGlmIGxlbihoZXhfc3RyKSA+PSAyMDogICMg0JzQuNC90LjQvNGD0LwgMTAg0LHQsNC50YIgPSAyMCDRgdC40LzQstC+0LvQvtCyCiAgICAgICAgICAgICAgICAgICAgICAgICMg0J7QsdGA0LXQt9Cw0LXQvCDQtNC+INGA0LDQt9GD0LzQvdC+0Lkg0LTQu9C40L3RiyAoMjAtMjgg0YHQuNC80LLQvtC70L7QsikKICAgICAgICAgICAgICAgICAgICAgICAgZm9yIGN1dF9sZW4gaW4gWzI4LCAyNiwgMjQsIDIyLCAyMF06CiAgICAgICAgICAgICAgICAgICAgICAgICAgICBjYW5kaWRhdGUgPSBoZXhfc3RyWzpjdXRfbGVuXQogICAgICAgICAgICAgICAgICAgICAgICAgICAgaWYgY2FuZGlkYXRlLnN0YXJ0c3dpdGgoKCczMCcsICczNCcpKSBhbmQgY2FuZGlkYXRlIG5vdCBpbiBlcGNfbGlzdDoKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBlcGNfbGlzdC5hcHBlbmQoY2FuZGlkYXRlKQogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIGJyZWFrCiAgICAgICAgICAgICAgICAgICAgYnJlYWsKCiAgICByZXR1cm4gZXBjX2xpc3QKCgpkZWYgcGFyc2VfZXBjX2FkdmFuY2VkKGRhdGEpOgogICAgIyDQo9C70YPRh9GI0LXQvdC90YvQuSDQv9Cw0YDRgdC10YAgRVBDCiAgICBlcGNfbGlzdCA9IFtdCiAgICBoZXhfZGF0YSA9IGRhdGEuaGV4KCkudXBwZXIoKQoKICAgICMg0JjRidC10LwgRVBDINC/0L4g0YXQsNGA0LDQutGC0LXRgNC90YvQvCDQv9GA0LjQt9C90LDQutCw0Lw6CiAgICAjIDEuINCd0LDRh9C40L3QsNGO0YLRgdGPINGBIDMwMDAsIDMwMEUsIDM0MDAKICAgICMgMi4g0JjQvNC10Y7RgiDQtNC70LjQvdGDIDIwLTI4INGB0LjQvNCy0L7Qu9C+0LIKICAgIHBhdHRlcm5zID0gWwogICAgICAgIHInKDMwMDBbMC05QS1GXXsxNiwyNH0pJywgICMgMzAwMCArIDE2LTI0IGhleCDRgdC40LzQstC+0LvQvtCyCiAgICAgICAgcicoMzAwRVswLTlBLUZdezE2LDI0fSknLCAgIyAzMDBFICsgMTYtMjQgaGV4INGB0LjQvNCy0L7Qu9C+0LIKICAgICAgICByJygzNDAwWzAtOUEtRl17MTYsMjR9KScsICAjIDM0MDAgKyAxNi0yNCBoZXgg0YHQuNC80LLQvtC70L7QsgogICAgXQoKICAgIGZvciBwYXR0ZXJuIGluIHBhdHRlcm5zOgogICAgICAgIG1hdGNoZXMgPSByZS5maW5kYWxsKHBhdHRlcm4sIGhleF9kYXRhKQogICAgICAgIGZvciBtYXRjaCBpbiBtYXRjaGVzOgogICAgICAgICAgICAjINCe0YHRgtCw0LLQu9GP0LXQvCDRgtC+0LvRjNC60L4g0L/QvtC70L3Ri9C1IEVQQyAo0L7QsdGL0YfQvdC+IDI0LTI4INGB0LjQvNCy0L7Qu9C+0LIpCiAgICAgICAgICAgIGlmIGxlbihtYXRjaCkgPj0gMjQ6CiAgICAgICAgICAgICAgICAjINCe0LHRgNC10LfQsNC10Lwg0LTQviDRgdGC0LDQvdC00LDRgNGC0L3QvtC5INC00LvQuNC90Ysg0LXRgdC70Lgg0L3Rg9C20L3QvgogICAgICAgICAgICAgICAgaWYgbGVuKG1hdGNoKSA+IDI4OgogICAgICAgICAgICAgICAgICAgIG1hdGNoID0gbWF0Y2hbOjI4XQogICAgICAgICAgICAgICAgaWYgbWF0Y2ggbm90IGluIGVwY19saXN0OgogICAgICAgICAgICAgICAgICAgIGVwY19saXN0LmFwcGVuZChtYXRjaCkKCiAgICAjINCV0YHQu9C4INC90LUg0L3QsNGI0LvQuCAtINC/0YDQvtCx0YPQtdC8INC90LDQudGC0Lgg0LvRjtCx0YvQtSDQtNC70LjQvdC90YvQtSBoZXgt0YHRgtGA0L7QutC4CiAgICBpZiBub3QgZXBjX2xpc3Q6CiAgICAgICAgbG9uZ19oZXggPSByZS5maW5kYWxsKHInKFswLTlBLUZdezI0LDI4fSknLCBoZXhfZGF0YSkKICAgICAgICBmb3IgY2FuZGlkYXRlIGluIGxvbmdfaGV4OgogICAgICAgICAgICBpZiBjYW5kaWRhdGUuc3RhcnRzd2l0aCgoJzMwJywgJzM0JykpIGFuZCBjYW5kaWRhdGUgbm90IGluIGVwY19saXN0OgogICAgICAgICAgICAgICAgZXBjX2xpc3QuYXBwZW5kKGNhbmRpZGF0ZSkKCiAgICByZXR1cm4gZXBjX2xpc3QKCgojID09PSBNQUlOID09PQppZiBfX25hbWVfXyA9PSAiX19tYWluX18iOgogICAgZGF0YSA9IHJlYWRfcmVzcG9uc2UoKQoKICAgICMg0J7RgtC70LDQtNC60LA6INC/0L7QutCw0LbQtdC8INGB0YvRgNGL0LUg0LTQsNC90L3Ri9C1CiAgICBwcmludChmIlJhd0RhdGEoe2xlbihkYXRhKX1ieXRlcyk6W3tkYXRhLmhleCgpLnVwcGVyKCl9XSIsIGZpbGU9c3lzLnN0ZGVycikKCiAgICB0YWdzID0gcGFyc2VfZXBjX2FkdmFuY2VkKGRhdGEpCgogICAgZm9yIGVwYyBpbiB0YWdzOgogICAgICAgIHByaW50KGVwYykKCiAgICBwcmludChmImZvdW5kPXtsZW4odGFncyl9ZXBjIikKICAgIHN5cy5leGl0KDAgaWYgdGFncyBlbHNlIDEpCgo=' | base64 -d > scr__rfid_scan.py 2>/dev/null || echo ERROR_MSG"
[15:32:13.300800]COM16.readEOL[OK]= b'\x1b[?2004l'
[15:32:13.322988]COM16.readEOL[OK]= b'[33]-  Exit 124                timeout 2.0 cat /dev/ttyUSB2'
[15:32:13.332989]COM16.readEOL[OK]= b'\x1b[?2004hroot@harvest05:~# '
[15:32:13.332989]COM16.stop_line[OK]= b'' [extra=EqValid_Regexp(v_args=(b'.*root@.+:.+#.*',)/v_kwargs={}/_iresult_reverse=None/_iresult_cumulate=<EnumAdj_BoolCumulate.ALL_TRUE: <built-in function all>>/_other_final__resolve=True)]
[15:32:13.332989]COM16.readNoEOL[OK]= b'\x1b[?2004hroot@harvest05:~# '
[COM16.WRITEREAD]
	write=[printf '%s' 'IyA9PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09CiMgc2NyX19yZmlkX3NjYW4ucHkgLSDQktCV0KDQodCY0K8g0KEg0J/QoNCv0JzQq9CcINCY0JfQktCb0JXQp9CV0J3QmNCV0JwgRVBDCiMgPT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PQppbXBvcnQgc2VyaWFsLCB0aW1lLCBzeXMsIHJlCgpQT1JUID0gJy9kZXYvdHR5UzInCkJBVUQgPSAxMTUyMDAKVElNRU9VVCA9IDAuNQoKIyBSRUFEIEJBTksKQ01EID0gYnl0ZXMoWzB4QTAsIDB4MEEsIDB4MDEsIDB4ODEsIDB4MDEsIDB4MDAsIDB4MDgsIDB4MDAsIDB4MDAsIDB4MDAsIDB4MDAsIDB4Q0JdKQoKCmRlZiByZWFkX3Jlc3BvbnNlKCkgLT4gYnl0ZXM6CiAgICBzZXIgPSBzZXJpYWwuU2VyaWFsKFBPUlQsIEJBVUQsIHRpbWVvdXQ9VElNRU9VVCkKICAgIHNlci5yZXNldF9pbnB1dF9idWZmZXIoKQogICAgc2VyLndyaXRlKENNRCkKCiAgICByZXNwb25zZSA9IGIiIgogICAgc3RhcnQgPSB0aW1lLnRpbWUoKQogICAgd2hpbGUgdGltZS50aW1lKCkgLSBzdGFydCA8IDEuMDoKICAgICAgICBjaHVuayA9IHNlci5yZWFkKHNlci5pbl93YWl0aW5nIG9yIDEpCiAgICAgICAgaWYgY2h1bms6CiAgICAgICAgICAgIHJlc3BvbnNlICs9IGNodW5rCiAgICAgICAgZWxzZToKICAgICAgICAgICAgdGltZS5zbGVlcCgwLjA1KQogICAgc2VyLmNsb3NlKCkKICAgIHJldHVybiByZXNwb25zZQoKCmRlZiBwYXJzZV9lcGMoZGF0YSk6CiAgICBlcGNfbGlzdCA9IFtdCiAgICBpID0gMAoKICAgIHdoaWxlIGkgPCBsZW4oZGF0YSk6CiAgICAgICAgIyDQmNGJ0LXQvCDQvdCw0YfQsNC70L4g0L/QsNC60LXRgtCwIDB4QTAKICAgICAgICBpZiBkYXRhW2ldICE9IDB4QTA6CiAgICAgICAgICAgIGkgKz0gMQogICAgICAgICAgICBjb250aW51ZQoKICAgICAgICBpZiBpICsgMSA+PSBsZW4oZGF0YSk6CiAgICAgICAgICAgIGJyZWFrCgogICAgICAgIGxlbmd0aCA9IGRhdGFbaSArIDFdCiAgICAgICAgaWYgaSArIGxlbmd0aCArIDEgPiBsZW4oZGF0YSk6CiAgICAgICAgICAgIGkgKz0gMQogICAgICAgICAgICBjb250aW51ZQoKICAgICAgICBwYWNrZXQgPSBkYXRhW2k6aSArIGxlbmd0aCArIDFdCiAgICAgICAgaSArPSBsZW5ndGggKyAxCgogICAgICAgICMg0J/RgNC+0LLQtdGA0Y/QtdC8INGC0LjQvyDQv9Cw0LrQtdGC0LAgKDB4MDEgMHg4MSAtINC40L3QstC10L3RgtCw0YDQuNC30LDRhtC40Y8pCiAgICAgICAgaWYgbGVuKHBhY2tldCkgPCA2IG9yIHBhY2tldFsyXSAhPSAweDAxIG9yIHBhY2tldFszXSAhPSAweDgxOgogICAgICAgICAgICBjb250aW51ZQoKICAgICAgICAjINCY0YnQtdC8IEVQQyDQtNCw0L3QvdGL0LUKICAgICAgICAjINCe0LHRi9GH0L3QviBFUEMg0L3QsNGH0LjQvdCw0LXRgtGB0Y8g0L/QvtGB0LvQtSDQt9Cw0LPQvtC70L7QstC60LAgKNC/0YDQuNC80LXRgNC90L4g0YEgNy3Qs9C+INCx0LDQudGC0LApCiAgICAgICAgIyDQmNGJ0LXQvCDQv9C+0YHQu9C10LTQvtCy0LDRgtC10LvRjNC90L7RgdGC0LgsINC60L7RgtC+0YDRi9C1INC90LDRh9C40L3QsNGO0YLRgdGPINGBIDB4MzAg0LjQu9C4IDB4MzQgKNGF0LDRgNCw0LrRgtC10YDQvdC+INC00LvRjyBFUEMpCiAgICAgICAgZm9yIGogaW4gcmFuZ2UoNSwgbGVuKHBhY2tldCkpOgogICAgICAgICAgICAjINCf0YDQvtC/0YPRgdC60LDQtdC8INC+0LTQuNC90L7Rh9C90YvQtSDQsdCw0LnRgtGLINC4INC40YnQtdC8INC90LDRh9Cw0LvQviBFUEMKICAgICAgICAgICAgaWYgcGFja2V0W2pdIGluICgweDMwLCAweDM0KTogICMg0KXQsNGA0LDQutGC0LXRgNC90L7QtSDQvdCw0YfQsNC70L4gRVBDCiAgICAgICAgICAgICAgICAjINCf0YDQvtCy0LXRgNGP0LXQvCwg0YfRgtC+INC00LDQu9GM0YjQtSDQuNC00YPRgiDQtNCw0L3QvdGL0LUKICAgICAgICAgICAgICAgIHJlbWFpbmluZyA9IGxlbihwYWNrZXQpIC0gagogICAgICAgICAgICAgICAgaWYgcmVtYWluaW5nID49IDE0OiAgIyDQnNC40L3QuNC80YPQvCAxNCDQsdCw0LnRgiDQtNC70Y8g0L/QvtC70L3QvtCz0L4gRVBDCiAgICAgICAgICAgICAgICAgICAgIyDQmNC30LLQu9C10LrQsNC10Lwg0LTQviAyMCDQsdCw0LnRgiAoNDAgaGV4INGB0LjQvNCy0L7Qu9C+0LIpCiAgICAgICAgICAgICAgICAgICAgZXBjX2J5dGVzID0gcGFja2V0W2o6aiArIG1pbigyMCwgcmVtYWluaW5nKV0KCiAgICAgICAgICAgICAgICAgICAgIyDQpNC40LvRjNGC0YDRg9C10LwgLSDQvtGB0YLQsNCy0LvRj9C10Lwg0YLQvtC70YzQutC+IGhleC3RgdC40LzQstC+0LvRiwogICAgICAgICAgICAgICAgICAgIGhleF9zdHIgPSAnJwogICAgICAgICAgICAgICAgICAgIGZvciBiIGluIGVwY19ieXRlczoKICAgICAgICAgICAgICAgICAgICAgICAgaGV4X3N0ciArPSBmJ3tiOjAyWH0nCgogICAgICAgICAgICAgICAgICAgICMg0J/RgNC+0LLQtdGA0Y/QtdC8LCDRh9GC0L4g0YHRgtGA0L7QutCwINC/0L7RhdC+0LbQsCDQvdCwIEVQQyAo0L3QsNGH0LjQvdCw0LXRgtGB0Y8g0YEgMzAvMzQg0Lgg0LTQvtGB0YLQsNGC0L7Rh9C90L7QuSDQtNC70LjQvdGLKQogICAgICAgICAgICAgICAgICAgIGlmIGxlbihoZXhfc3RyKSA+PSAyMDogICMg0JzQuNC90LjQvNGD0LwgMTAg0LHQsNC50YIgPSAyMCDRgdC40LzQstC+0LvQvtCyCiAgICAgICAgICAgICAgICAgICAgICAgICMg0J7QsdGA0LXQt9Cw0LXQvCDQtNC+INGA0LDQt9GD0LzQvdC+0Lkg0LTQu9C40L3RiyAoMjAtMjgg0YHQuNC80LLQvtC70L7QsikKICAgICAgICAgICAgICAgICAgICAgICAgZm9yIGN1dF9sZW4gaW4gWzI4LCAyNiwgMjQsIDIyLCAyMF06CiAgICAgICAgICAgICAgICAgICAgICAgICAgICBjYW5kaWRhdGUgPSBoZXhfc3RyWzpjdXRfbGVuXQogICAgICAgICAgICAgICAgICAgICAgICAgICAgaWYgY2FuZGlkYXRlLnN0YXJ0c3dpdGgoKCczMCcsICczNCcpKSBhbmQgY2FuZGlkYXRlIG5vdCBpbiBlcGNfbGlzdDoKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBlcGNfbGlzdC5hcHBlbmQoY2FuZGlkYXRlKQogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIGJyZWFrCiAgICAgICAgICAgICAgICAgICAgYnJlYWsKCiAgICByZXR1cm4gZXBjX2xpc3QKCgpkZWYgcGFyc2VfZXBjX2FkdmFuY2VkKGRhdGEpOgogICAgIyDQo9C70YPRh9GI0LXQvdC90YvQuSDQv9Cw0YDRgdC10YAgRVBDCiAgICBlcGNfbGlzdCA9IFtdCiAgICBoZXhfZGF0YSA9IGRhdGEuaGV4KCkudXBwZXIoKQoKICAgICMg0JjRidC10LwgRVBDINC/0L4g0YXQsNGA0LDQutGC0LXRgNC90YvQvCDQv9GA0LjQt9C90LDQutCw0Lw6CiAgICAjIDEuINCd0LDRh9C40L3QsNGO0YLRgdGPINGBIDMwMDAsIDMwMEUsIDM0MDAKICAgICMgMi4g0JjQvNC10Y7RgiDQtNC70LjQvdGDIDIwLTI4INGB0LjQvNCy0L7Qu9C+0LIKICAgIHBhdHRlcm5zID0gWwogICAgICAgIHInKDMwMDBbMC05QS1GXXsxNiwyNH0pJywgICMgMzAwMCArIDE2LTI0IGhleCDRgdC40LzQstC+0LvQvtCyCiAgICAgICAgcicoMzAwRVswLTlBLUZdezE2LDI0fSknLCAgIyAzMDBFICsgMTYtMjQgaGV4INGB0LjQvNCy0L7Qu9C+0LIKICAgICAgICByJygzNDAwWzAtOUEtRl17MTYsMjR9KScsICAjIDM0MDAgKyAxNi0yNCBoZXgg0YHQuNC80LLQvtC70L7QsgogICAgXQoKICAgIGZvciBwYXR0ZXJuIGluIHBhdHRlcm5zOgogICAgICAgIG1hdGNoZXMgPSByZS5maW5kYWxsKHBhdHRlcm4sIGhleF9kYXRhKQogICAgICAgIGZvciBtYXRjaCBpbiBtYXRjaGVzOgogICAgICAgICAgICAjINCe0YHRgtCw0LLQu9GP0LXQvCDRgtC+0LvRjNC60L4g0L/QvtC70L3Ri9C1IEVQQyAo0L7QsdGL0YfQvdC+IDI0LTI4INGB0LjQvNCy0L7Qu9C+0LIpCiAgICAgICAgICAgIGlmIGxlbihtYXRjaCkgPj0gMjQ6CiAgICAgICAgICAgICAgICAjINCe0LHRgNC10LfQsNC10Lwg0LTQviDRgdGC0LDQvdC00LDRgNGC0L3QvtC5INC00LvQuNC90Ysg0LXRgdC70Lgg0L3Rg9C20L3QvgogICAgICAgICAgICAgICAgaWYgbGVuKG1hdGNoKSA+IDI4OgogICAgICAgICAgICAgICAgICAgIG1hdGNoID0gbWF0Y2hbOjI4XQogICAgICAgICAgICAgICAgaWYgbWF0Y2ggbm90IGluIGVwY19saXN0OgogICAgICAgICAgICAgICAgICAgIGVwY19saXN0LmFwcGVuZChtYXRjaCkKCiAgICAjINCV0YHQu9C4INC90LUg0L3QsNGI0LvQuCAtINC/0YDQvtCx0YPQtdC8INC90LDQudGC0Lgg0LvRjtCx0YvQtSDQtNC70LjQvdC90YvQtSBoZXgt0YHRgtGA0L7QutC4CiAgICBpZiBub3QgZXBjX2xpc3Q6CiAgICAgICAgbG9uZ19oZXggPSByZS5maW5kYWxsKHInKFswLTlBLUZdezI0LDI4fSknLCBoZXhfZGF0YSkKICAgICAgICBmb3IgY2FuZGlkYXRlIGluIGxvbmdfaGV4OgogICAgICAgICAgICBpZiBjYW5kaWRhdGUuc3RhcnRzd2l0aCgoJzMwJywgJzM0JykpIGFuZCBjYW5kaWRhdGUgbm90IGluIGVwY19saXN0OgogICAgICAgICAgICAgICAgZXBjX2xpc3QuYXBwZW5kKGNhbmRpZGF0ZSkKCiAgICByZXR1cm4gZXBjX2xpc3QKCgojID09PSBNQUlOID09PQppZiBfX25hbWVfXyA9PSAiX19tYWluX18iOgogICAgZGF0YSA9IHJlYWRfcmVzcG9uc2UoKQoKICAgICMg0J7RgtC70LDQtNC60LA6INC/0L7QutCw0LbQtdC8INGB0YvRgNGL0LUg0LTQsNC90L3Ri9C1CiAgICBwcmludChmIlJhd0RhdGEoe2xlbihkYXRhKX1ieXRlcyk6W3tkYXRhLmhleCgpLnVwcGVyKCl9XSIsIGZpbGU9c3lzLnN0ZGVycikKCiAgICB0YWdzID0gcGFyc2VfZXBjX2FkdmFuY2VkKGRhdGEpCgogICAgZm9yIGVwYyBpbiB0YWdzOgogICAgICAgIHByaW50KGVwYykKCiAgICBwcmludChmImZvdW5kPXtsZW4odGFncyl9ZXBjIikKICAgIHN5cy5leGl0KDAgaWYgdGFncyBlbHNlIDEpCgo=' | base64 -d > scr__rfid_scan.py 2>/dev/null || echo ERROR_MSG]
	read=[[33]-  Exit 124                timeout 2.0 cat /dev/ttyUSB2]
output='[33]-  Exit 124                timeout 2.0 cat /dev/ttyUSB2'
PASSED
        """
        # === ЗАЩИТА ОТ ПУСТОГО ОТВЕТА ===
        if not data:
            return ""

        # 0=split -----------------------
        result = data.splitlines()

        # 1=CMD ECHO --------------------
        if result[0].strip() == cmd.strip():
            result = result[1:]

        # 2=EOF -------------------------
        while result and (self.COMPILE_EOF__STR.match(result[-1]) or result[-1].strip() == ''):
            result = result[:-1]

        # 3=SERVICE LOGS ----------------
        # AT": "[1]   Terminated              timeout 2.0 cat /dev/ttyUSB2\nOK"
        # [AT] AT+CSQ ---> at_output='[4] 1836\n[3]   Exit 124                timeout 2.0 cat /dev/ttyUSB2\n+CSQ: 20,99\nOK'
        # Удаляем служебные строки bash о статусе фоновых процессов
        result_clear_service = [
            line for line in result
            if not (
                re.match(r'\s*\[\d+\]\s+(?:Exit|Terminated|Done)?\s*\d*\s*', line)
                or
                re.match(r'\s*\[\d+\]-?\s+(?:Exit|Terminated|Done)?\s*\d*\s*.*', line)
            )
        ]
        result = result_clear_service

        # 4=EXIT ------------------------
        return "\n".join(result)

    # ------------------------------------------------------------------------------------------------------------------
    def cmd_timeout__write_read__payload(
            self,
            cmd: str,
            timeout_continue: float = 2.0,  # ОБЯЗАТЕЛЬНО!!!
            **wr_kwargs,
    ) -> str:
        """
        Выполняет команду на устройстве и возвращает stdout в виде строки.
        При ошибке возвращает пустую строку.
        """
        return self.cmd_timeout__write_read_text(
            cmd,
            payload_only=True,
            timeout_continue=timeout_continue,
            **wr_kwargs)

    # ------------------------------------------------------------------------------------------------------------------
    def cmd_timeout__check_executed_success(self, cmd: str, **wr_kwargs) -> bool:
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
        output = self.cmd_timeout__write_read__payload(f"{cmd} 2>/dev/null || echo {ERROR_MSG}", **wr_kwargs)
        print(f"{output=}")
        return ERROR_MSG not in output

    # ------------------------------------------------------------------------------------------------------------------
    def cmd_parsed__ls(
            self,
            path: str | None = None,
            filters: Base_EqValid | list | None = None,
            **wr_kwargs,
    ) -> list[str]:
        """

        ---- Sent utf8 encoded message: "ls /dev/\r\n" ----
        ls /dev/
        adsp1            kmem              nbd13               stdout  tty36  tty8
        audio            kmsg              nbd14               tty     tty37  tty9
        audio1           kvm               nbd15               tty0    tty38  ttyS0
        audio2           log               nbd2                tty1    tty39  ttyS1
        audio3           loop-control      nbd3                tty10   tty4   ttyS2
        autofs           loop0             nbd4                tty11   tty40  ttyS3
        block            loop1             nbd5                tty12   tty41  ttyS4
        btrfs-control    loop2             nbd6                tty13   tty42  ttyS5
        bus              loop3             nbd7                tty14   tty43  ttyS6
        cec0             loop4             nbd8                tty15   tty44  ttyS7
        char             loop5             nbd9                tty16   tty45  ttyUSB0
        console          loop6             net                 tty17   tty46  urandom
        cpu_dma_latency  loop7             network_latency     tty18   tty47  v4l
        cuse             mapper            network_throughput  tty19   tty48  vcs
        disk             mem               null                tty2    tty49  vcs1
        dri              memory_bandwidth  ppp                 tty20   tty5   vcs2
        dsp              mixer             psaux               tty21   tty50  vcs3
        dsp1             mixer1            ptmx                tty22   tty51  vcs4
        dsp2             mixer2            pts                 tty23   tty52  vcs5
        dsp3             mixer3            random              tty24   tty53  vcs6
        fb0              mmcblk0           rfkill              tty25   tty54  vcsa
        fd               mmcblk0boot0      rtc                 tty26   tty55  vcsa1
        full             mmcblk0boot1      rtc0                tty27   tty56  vcsa2
        fuse             mmcblk0p1         rtc1                tty28   tty57  vcsa3
        gpiochip0        mmcblk0p2         sequencer           tty29   tty58  vcsa4
        gpiochip1        mmcblk0p3         sequencer2          tty3    tty59  vcsa5
        i2c-0            mqueue            serial              tty30   tty6   vcsa6
        i2c-1            nbd0              shm                 tty31   tty60  vhci
        i2c-2            nbd1              snd                 tty32   tty61  video0
        i2c-3            nbd10             spidev0.0           tty33   tty62  watchdog
        initctl          nbd11             stderr              tty34   tty63  watchdog0
        input            nbd12             stdin               tty35   tty7   zero
        root@harvest05:~#
        """
        result = []

        # PATH
        path = path or ""
        if path and not path.endswith("/"):
            path += "/"

        # PAYLOAD
        output = self.cmd_timeout__write_read__payload(
            f"ls {path}",
            timeout=3,
            timeout_continue=1.0,
            **wr_kwargs,
        )

        # SPLIT
        parsed = output.split()

        # FILTER
        for item in parsed:
            item = item.strip()
            if not item:
                continue
            if filters and item not in filters:
                continue

            result.append(f"{path}{item}")
        return result

    # FILES ============================================================================================================
    def file_name__push(self, name: str) -> bool:
        DIRNAME = "scripts"
        dirpath = pathlib.Path(__file__).parent.joinpath(DIRNAME)
        filepath = dirpath.joinpath(name)

        text = filepath.read_text(encoding="utf8")
        return self._file_text__push(filepath=name, text=text)

    def _file_text__push(self, filepath: str = f"script.py", text: str = "") -> bool:
        """
        GOAL
        transfer file scripts into device,
        """
        # 1=MKDIR --------------------
        splited = filepath.rsplit('/', 1)
        if "/" in filepath:
            if splited[0] == "":
                dirpath = "/"
            else:
                dirpath = splited[0]
        else:
            dirpath = ""

        # mkdir -p создаст путь, если его нет.
        if dirpath not in ["", "/", None]:
            cmd = f"mkdir -p {dirpath}"
            if not self.cmd_timeout__check_executed_success(cmd):
                return False

        # 2=PUSH --------------------
        text_b64 = base64.b64encode(text.encode()).decode()
        # printf не добавляет '\n', в отличие от echo; одинарные кавычки защищают от пробелов.
        cmd = f"printf '%s' '{text_b64}' | base64 -d > {filepath}"
        return self.cmd_timeout__check_executed_success(cmd)

    def file__check_exist(self, filepath: str) -> bool:
        """
        GOAL
        Проверяет наличие скрипта на устройстве
        НЕ ПРОВЕРЯЕТ КОРРЕКТНОСТЬ!
        """
        return self.cmd_timeout__check_executed_success(f"test -f {filepath}")

    # AT ===============================================================================================================
    pass

    # def send__at_command__simple(self, cmd: str, port="/dev/ttyUSB2", timeout=1.0) -> str:
    # НЕ РАБОТАЕТ!!!
    #
    #     full_cmd = (
    #         f"timeout {timeout} bash -c 'echo -e \"{cmd}\\r\\n\" > {port}; "
    #         f"timeout {timeout} cat {port}'"
    #     )
    #     at_output = self.cmd_timeout__write_read__payload_str(full_cmd, timeout=timeout * 2)
    #     # Убираем возможное эхо команды
    #     at_output = at_output.replace(cmd + "\n", "")
    #     print(f"[{at_output=}]")
    #     return at_output
    #
    # def send__at_command__simple(self, cmd: str, port="/dev/ttyUSB2", timeout=1.0) -> str:
    #     """
    #     Отправляет AT-команду через прямой ввод-вывод в порт.
    #     Работает после того, как порт настроен (raw mode + echo off).
    #     """
    #     # Отправить команду, прочитать ответ с таймаутом через утилиту timeout
    #     # - ВАЖНО: bash -c нужен, чтобы пайп обрабатывался целиком
    #     full_cmd = (
    #         f"timeout {timeout} bash -c '"
    #         f"printf \"{cmd}\\r\\n\" > {port}; "
    #         f"timeout {timeout} cat {port}'"
    #     )
    #     at_output = self.cmd_timeout__write_read__payload_str(
    #         full_cmd,
    #         timeout=None,
    #         timeout_continue=timeout * 1.5
    #     )
    #     # Убираем пустые строки и возможное эхо (если echo не выключено)
    #     lines = [line.strip() for line in at_output.split('\n') if line.strip()]
    #     # Отфильтровываем саму команду, если echo ещё активно
    #     lines = [line for line in lines if line != cmd]
    #     at_output = '\n'.join(lines)
    #     print(f"[SIMPLE_AT] {at_output=}")
    #     return at_output

    def at_cmd__simple(self, cmd: str, port="/dev/ttyUSB2", timeout=2.0, timeout_continue=None) -> str:
        """
        Отправить AT-команду на уже настроенный порт (stty raw + echo off).

        SerialClient2(COM16.115200,occupied=o,isopen=True){'write': b"timeout 2 cat /dev/ttyUSB2 & sleep 0.1; printf 'AT+COPS?\\r\\n' > /dev/ttyUSB2; sleep 0.4; kill %1 2>/dev/null\r\n"}
        SerialClient2(COM16.115200,occupied=o,isopen=True)READ(
            bytes=b'timeout 2 cat /dev/ttyUSB2 & sleep 0.1; printf \'AT+COPS?\\r\\n\' > /dev/ttyUSB2; sleep 0.4; kill %1 2>/dev/null\r\n\x1b[?2004l\r[6] 5353\r\n[5]   Exit 124                timeout 2 cat /dev/ttyUSB2\r\n\r\r\n+COPS: 0,2,"25020",7\r\r\n\r\r\nOK\r\r\n\x1b[?2004hroot@harvest05:~# \r\n\x1b[?2004l\r\x1b[?2004hroot@harvest05:~# '
            printable=timeout 2 cat /dev/ttyUSB2 & sleep 0.1; printf 'AT+COPS?\r\n' > /dev/ttyUSB2; sleep 0.4; kill %1 2>/dev/null
        [6] 5353
        [5]   Exit 124                timeout 2 cat /dev/ttyUSB2

        root@harvest05:~#
        root@harvest05:~# )
        [AT] AT+COPS? -> at_output='+COPS: 0,2,"25020",7\nOK'
        GSM operator: +COPS: 0,2,"25020",7
        OK

        НЕЛЬЗЯ ПРОСТО ДВА ПЕРВЫХ УДАЛЯТЬ!!!
        [15:19:47.271369]COM16.writeline[OK]= b"timeout 2.0 cat /dev/ttyUSB2 & sleep 0.1; printf 'AT\\r\\n' > /dev/ttyUSB2; sleep 0.4\r\n"
        [15:19:47.306637]COM16.readline[OK]= b"timeout 2.0 cat /dev/ttyUSB2 & sleep 0.1; printf 'AT\\r\\n' > /dev/ttyUSB2; sleep 0.4"
        [15:19:47.310637]COM16.readline[OK]= b'\x1b[?2004l'
        [15:19:47.313637]COM16.readline[OK]= b'[1] 3964'
        [15:19:47.410022]COM16.readline[OK]= b'OK'
        [15:19:47.836296]COM16.readline[OK]= b'\x1b[?2004hroot@harvest05:~# '
        [15:19:47.841624]COM16.readline[OK]= b'\x1b[?2004l'
        [COM16.WRITEREAD]
            write=[timeout 2.0 cat /dev/ttyUSB2 & sleep 0.1; printf 'AT\r\n' > /dev/ttyUSB2; sleep 0.4]
            read=[[1] 3964
        OK]
        [AT] AT ---> at_output=''
        FAILED
        """
        cmd_full = (
            f"cat {port} & sleep 0.1; "
            f"printf '{cmd}\\r\\n' > {port}; "
            f"sleep 0.4; "
            f"kill %1 2>/dev/null"
        )
        at_output = self.cmd_timeout__write_read__payload(
            cmd=cmd_full,
            timeout=timeout,
            timeout_continue=timeout_continue or timeout * 0.8,
        )
        print(f"[AT]{cmd}--->{at_output}")
        return at_output

    def at_cmd__raw(
            self,
            cmd: str,
            bridge: str = "scr__gsm_at_client.py",
            port: str = "/dev/ttyUSB2",
            baudrate: int = 115200,
            stop_line=b"OK",

            timeout: float = 2.0,
            timeout_continue: float | None = None,
            **read_kwargs
    ) -> str | NoReturn:
        """
        !USE SIMPLE! - works quicker!
        Отправляет AT-команду через скрипт на устройстве и возвращает строку ответа.

        SerialClient2(COM16.115200,occupied=harvest05,isopen=True){'write': b"timeout 2 python3 /tmp/at_client.py 'AT+CSQ' /dev/ttyUSB2 115200\r\n"}
        SerialClient2(COM16.115200,occupied=harvest05,isopen=True)READ(
            bytes=b"timeout 2 python3 /tmp/at_client.py 'AT+CSQ' /dev/ttyUSB2 115200\r\n\x1b[?2004l\r\r\r\n+CSQ: 23,99\r\r\n\r\r\nOK\r\r\n\r\n\x1b[?2004hroot@harvest05:~# \r\n\x1b[?2004l\r\x1b[?2004hroot@harvest05:~# "
            printable=timeout 2 python3 /tmp/at_client.py 'AT+CSQ' /dev/ttyUSB2 115200
        root@harvest05:~#
        root@harvest05:~# )
        [at_output='+CSQ: 23,99\nOK']
        """
        command_line = f"python3 {bridge} '{cmd}' {port} {baudrate}"
        at_output = ""
        for _ in range(2):

            at_output = self.cmd_timeout__write_read__payload(
                command_line,
                stop_line=stop_line,
                timeout=timeout,
                timeout_continue=timeout_continue,
                **read_kwargs
            )
            # Убираем возможное эхо команды
            if at_output.startswith(cmd + "\n"):
                at_output = at_output.replace(cmd + "\n", "", 1)

            if "No such file or directory" in at_output:
                if not self.file_name__push(bridge):
                    break

        print(f"[AT]{cmd}--->{at_output}")
        return at_output

    def at_cmd__dump(self, port: str, method_simple: bool = True, timeout: float = 2.0) -> dict[str, str]:
        """
        Опрашивает AT-команды из AT_CMD__DUMP

        ----------------------------
        M2M SIM
        я запустил симку на телефоне
        вызовы
        *201#
        *105#
        дают ответ Неполадки подключения или неверный код MMI
        при попытке позвонить комуто - идет переадресация вызова и завершение вызова сразу

        Действие	Результат	Причина
        *201#, *105#	"Неверный код MMI"	USSD-сервис отключен на уровне HLR оператора
        Звонок	Переадресация → сброс	Голос заблокирован, включена безусловная переадресация (CFU) на "заглушку"
        SMS	Не отправляются/не доходят	SMS-центр не настроен или услуга отключена

        ----------------------------
        HARVEST=M2M
        {
          "AT": "OK",
          "AT+CNUM": "OK",
          "ATI": "Manufacturer: INCORPORATED\nModel: A7682E-R\nRevision: A7682M6_V1.11.1\nIMEI1: 865286077380516\nIMEI2: 865286076965218\n+GCAP: +CGSM,+FCLASS,+DS\nOK",
          "AT+CGMI": "INCORPORATED\nOK",
          "AT+CGMM": "A7682E-R\nOK",
          "AT+CGMR": "+CGMR: A011B02A7682M6_DS_FOTA\nOK",
          "AT+CGSN": "865286077380516\nOK",
          "AT+CIMI": "250470002905372\nOK",
          "AT+GSN": "865286077380516\nOK",
          "AT+CPIN?": "+CPIN: READY\nOK",
          "AT+CCID": "ERROR",
          "AT+ICCID": "ERROR",
          "AT+COPS?": "+COPS: 0,2,\"25020\",7\nOK",
          "AT+CREG?": "+CREG: 0,1\nOK",
          "AT+CGREG?": "+CGREG: 0,1\nOK",
          "AT+CEREG?": "+CEREG: 0,1\nOK",
          "AT+CSQ": "+CSQ: 25,99\nOK",
          "AT+CESQ": "+CESQ: 49,99,255,255,24,55\nOK",
          "AT*CNTI=0": "ERROR",
          "AT+WS46?": "+WS46:30\nOK",
          "AT+CGDCONT?": "+CGDCONT: 1,\"IP\",\"simsim.MNC047.MCC250.GPRS\",\"10.0.206.58\",0,0,,,,\nOK",
          "AT+CGCONTRDP": "+CGCONTRDP: 1,5,\"simsim.MNC047.MCC250.GPRS\",\"10.0.206.58\",\"\",\"100.77.8.8\",\"100.77.4.4\",\"\",\"\",0,01400\nOK",
          "AT+CGPADDR": "+CGPADDR: 1,10.0.206.58\nOK",
          "AT+CGACT?": "+CGACT: 1,1\nOK",
          "AT+CGATT?": "+CGATT: 1\nOK",
          "AT+CIMS?": "ERROR",
          "AT+CIREG?": "+CME ERROR: Operation not supported",
          "AT+CFUN?": "+CFUN: 1\nOK",
          "AT+CSCLK?": "+CSCLK: 0\nOK",
          "AT+CPMUTEMP?": "ERROR",
          "AT+CBC": "+CBC: 3.830V\nOK",
          "AT+CCED?": "ERROR",
          "AT*CELLINFO?": "ERROR",
          "AT+CEER": "+CEER: \"0 Unknown\"\nOK"
        }
        SIM Tinkoff!!!
        {
          "AT": "OK",
          "AT+CNUM": "OK",
          "ATI": "Manufacturer: INCORPORATED\nModel: A7682E-R\nRevision: A7682M6_V1.11.1\nIMEI1: 865286077380516\nIMEI2: 865286076965218\n+GCAP: +CGSM,+FCLASS,+DS\nOK",
          "AT+CGMI": "INCORPORATED\nOK",
          "AT+CGMM": "A7682E-R\nOK",
          "AT+CGMR": "+CGMR: A011B02A7682M6_DS_FOTA\nOK",
          "AT+CGSN": "865286077380516\nOK",
          "AT+CIMI": "250621002917518\nOK",
          "AT+GSN": "865286077380516\nOK",
          "AT+CPIN?": "+CPIN: READY\nOK",
          "AT+CCID": "ERROR",
          "AT+ICCID": "ERROR",
          "AT+COPS?": "+COPS: 0,2,\"25020\",7\nOK",
          "AT+CREG?": "+CREG: 0,1\nOK",
          "AT+CGREG?": "+CGREG: 0,1\nOK",
          "AT+CEREG?": "+CEREG: 0,1\nOK",
          "AT+CSQ": "+CSQ: 19,99\nOK",
          "AT+CESQ": "+CESQ: 36,99,255,255,24,40\nOK",
          "AT*CNTI=0": "ERROR",
          "AT+WS46?": "+WS46:30\nOK",
          "AT+CGDCONT?": "+CGDCONT: 1,\"IP\",\"tt.MNC062.MCC250.GPRS\",\"10.74.253.15\",0,0,,,,\nOK",
          "AT+CGCONTRDP": "+CGCONTRDP: 1,5,\"tt.MNC062.MCC250.GPRS\",\"10.74.253.15\",\"\",\"10.219.250.1\",\"10.219.250.2\",\"\",\"\",0,0\nOK",
          "AT+CGPADDR": "+CGPADDR: 1,10.74.253.15\nOK",
          "AT+CGACT?": "+CGACT: 1,1\nOK",
          "AT+CGATT?": "+CGATT: 1\nOK",
          "AT+CIMS?": "ERROR",
          "AT+CIREG?": "+CME ERROR: Operation not supported",
          "AT+CFUN?": "+CFUN: 1\nOK",
          "AT+CSCLK?": "+CSCLK: 0\nOK",
          "AT+CPMUTEMP?": "ERROR",
          "AT+CBC": "+CBC: 3.810V\nOK",
          "AT+CCED?": "ERROR",
          "AT*CELLINFO?": "ERROR",
          "AT+CEER": "+CEER: \"0 Unknown\"\nOK"
        }

        Параметр	Значение
        Модель	SIMCom A7682E-R
        Прошивка	A7682M6_V1.11.1 / A011B02A7682M6_DS_FOTA
        IMEI1	865286077380516
        IMEI2	865286076965218 (две SIM)
        IMSI	250470002905372
        Оператор	25020 (Tele2 Russia)
        RAT	7 (LTE)
        WS46	30 (LTE + GSM)
        RSSI	20/31 (хороший)
        CESQ	RSRP=30, RSRQ=40 (отличный LTE)
        Регистрация	CREG/CGREG/CEREG = 0,1 (домашняя)
        PDP IP	10.0.188.251
        DNS	100.77.8.8, 100.77.4.4
        Питание	3.840V
        CFUN	1 (полный)
        CSCLK	0 (сон выключен)

        ERROR (ожидаемо для этого модуля):
        AT+CPINR — не поддерживает доп. информацию по PIN/PUK
        AT+CCID — видимо не реализован (можно попробовать AT+ICCID)
        AT*CNTI=0 — vendor-specific, не поддерживается
        AT+CGDATA="PPP" — режим не активен
        AT+CIMS?, AT+CIREG? — IMS не поддерживается
        AT+CPMUTEMP? — нет датчика температуры
        AT+CCED?, AT*CELLINFO? — нет расширенной инфы по сотам
        """
        results = {}
        method_send = self.at_cmd__simple if method_simple else self.at_cmd__raw
        for cmd in self.AT_CMD__DUMP:
            try:
                resp = method_send(cmd, port=port, timeout=timeout)
                results[cmd] = resp.strip()
            except Exception as exc:
                results[cmd] = f"PYERROR:{exc!r}"   # нет таких!
        return results

    # CMDS =============================================================================================================
    def prepare__stop__kernel_terminal_logs(self) -> bool:
        """
        GOAL
        deactivate logging kernel errors into terminal
        leave only errors (KERN_ERR and above) no warns!

        root@harvest05:~#
        root@harvest05:~# [ 2817.555181] IPv6: ADDRCONF(NETDEV_UP): wlan0: link is not ready
        [ 3230.554402] IPv6: ADDRCONF(NETDEV_UP): wlan0: link is not ready
        [ 3643.553379] IPv6: ADDRCONF(NETDEV_UP): wlan0: link is not ready
        [ 4056.552119] IPv6: ADDRCONF(NETDEV_UP): wlan0: link is not ready
        [ 4469.553782] IPv6: ADDRCONF(NETDEV_UP): wlan0: link is not ready
        [ 4882.553558] IPv6: ADDRCONF(NETDEV_UP): wlan0: link is not ready
        [ 5295.554909] IPv6: ADDRCONF(NETDEV_UP): wlan0: link is not ready
        [ 5708.553030] IPv6: ADDRCONF(NETDEV_UP): wlan0: link is not ready
        [ 6121.554739] IPv6: ADDRCONF(NETDEV_UP): wlan0: link is not ready
        """
        print("не удалось изменить режим логгирования сообщений ядра Linux в консоль")
        return self.cmd_timeout__check_executed_success(f'dmesg -n 3')

    def prepare__stop__services(self) -> bool:
        """
        GOAL
        stop all services which could interfere with tests

        systemctl stop только останавливает текущий запущенный процесс, но не меняет флаги автозагрузки (enable/disable).
После перезагрузки systemd снова запустит сервис
        """
        result: bool = True
        # Останавливаем ModemManager, если он может мешать порту - обычно занимает порты с устройствами ttyUSB*!!!
        # mm_active = self.cmd_timeout__check_executed_success("systemctl is-active ModemManager")
        for service in [
            "ModemManager",         #
            "harvester.service",    # не будет работать BTUS! не соединится
            "urozhai",              # вроде без него все работает! но просто так за компанию! потому что был в инструкции!
        ]:
            result &= self.cmd_timeout__check_executed_success(f"systemctl stop {service}")
        return result

    # ------------------------------------------------------------------------------------------------------------------
    def apt_install(self, module: str, timeout_continue: float = 5, **wr_kwargs) -> bool:
        """
        if need DELETE
            sudo apt remove picocom
        """
        result = self.cmd_timeout__check_executed_success(f"apt install -y {module}", timeout_continue=timeout_continue, **wr_kwargs)
        return result

    def check__has_internet(self) -> bool:
        """
        root@harvest05:~#
        ---- Sent utf8 encoded message: "ping -c 1 -W 2 8.8.8.8\r\n" ----
        ping -c 1 -W 2 8.8.8.8
        PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.

        --- 8.8.8.8 ping statistics ---
        1 packets transmitted, 0 received, 100% packet loss, time 0ms

        root@harvest05:~#
        """
        return self.cmd_timeout__check_executed_success(
                "ping -c 1 -W 1 8.8.8.8",
                timeout_continue=2,
                timeout=3,
            )

    # INFO =============================================================================================================
    def get_info__system(self) -> dict[str, Any]:
        result = {}

        # ----- Идентификация и версия ОС -----
        result['hostname'] = self.cmd_timeout__write_read__payload("hostname", timeout=1).strip()

        raw_os = self.cmd_timeout__write_read__payload("cat /etc/os-release 2>/dev/null", timeout=3)
        os_dict = {}
        for line in raw_os.split('\n'):
            if '=' in line:
                k, v = line.split('=', 1)
                os_dict[k.strip()] = v.strip().strip('"')
        result['os'] = os_dict

        result['kernel'] = self.cmd_timeout__write_read__payload("uname -r", timeout=1).strip()
        result['architecture'] = self.cmd_timeout__write_read__payload("uname -m", timeout=1).strip()

        # ----- Модель платы -----
        # Попытка через device-tree, иначе через dmesg
        model = self.cmd_timeout__write_read__payload(
            "cat /proc/device-tree/model 2>/dev/null || cat /sys/firmware/devicetree/base/model 2>/dev/null"
            , timeout=5
        ).strip()
        if not model:
            dmesg_model = self.cmd_timeout__write_read__payload(
                "dmesg | grep 'Machine model' | head -1 | cut -d: -f2-",
                timeout=3
            ).strip()
            model = dmesg_model if dmesg_model else "N/A"
        result['board_model'] = model

        # ----- CPU -----
        cpu_lines = self.cmd_timeout__write_read__payload("cat /proc/cpuinfo 2>/dev/null", timeout=3)
        cores = 0
        model_name = ""
        for line in cpu_lines.split('\n'):
            if line.startswith("processor"):
                cores += 1
            if line.startswith("model name") and not model_name:
                model_name = line.split(":")[1].strip()
            if line.startswith("Hardware") and not model_name:
                model_name = line.split(":")[1].strip()
        result['cpu'] = {
            'model': model_name or 'ARM',
            'cores': cores
        }

        # ----- Память -----
        mem_lines = self.cmd_timeout__write_read__payload("free -m 2>/dev/null || cat /proc/meminfo", timeout=3)
        if 'Mem:' in mem_lines:
            mem_parts = mem_lines.split('\n')[1].split()
            total = mem_parts[1]
            used = mem_parts[2]
            free = mem_parts[3]
            result['memory'] = {'total_mb': int(total), 'used_mb': int(used), 'free_mb': int(free)}
        else:
            mem = {}
            for line in mem_lines.split('\n'):
                parts = line.split()
                if len(parts) >= 2:
                    mem[parts[0].rstrip(':')] = parts[1]
            result['memory'] = mem

        # ----- Накопители -----
        disk_lines = self.cmd_timeout__write_read__payload("df -h / 2>/dev/null || echo NA", timeout=3)
        if disk_lines and disk_lines != 'N/A':
            parts = disk_lines.split('\n')[1].split()
            result['disk'] = {'total': parts[1], 'used': parts[2], 'available': parts[3], 'use%': parts[4]}
        else:
            result['disk'] = 'N/A'

        # ----- Uptime -----
        uptime_raw = self.cmd_timeout__write_read__payload("cat /proc/uptime", timeout=1)
        result['uptime'] = uptime_raw.split()[0] if uptime_raw else 'N/A'

        # ----- Сетевые интерфейсы -----
        net = {}
        iface_list = self.cmd_timeout__write_read__payload("ls /sys/class/net/", timeout=3).split()
        for iface in iface_list:
            iface = iface.strip()
            if not iface or iface == 'lo':
                continue
            mac = self.cmd_timeout__write_read__payload(f"cat /sys/class/net/{iface}/address 2>/dev/null", timeout=3).strip()
            ip_addr = self.cmd_timeout__write_read__payload(
                f"ip -4 addr show {iface} 2>/dev/null | grep inet | head -1")
            net[iface] = {
                'mac': mac if mac else 'N/A',
                'ip': ip_addr.split()[1].split('/')[0] if 'inet' in ip_addr else 'N/A'
            }
        result['network'] = net

        # ----- USB‑устройства (исправляем таймаут и убираем лишний stderr) -----
        # Используем timeout_continue=2 для гарантированного чтения вывода
        usb_raw = self.cmd_timeout__write_read__payload(
            "lsusb",
            timeout = 3,
            timeout_continue=2.0  # ждём до 2 секунд после эхо
        )
        result['usb_devices'] = [line.strip() for line in usb_raw.split('\n') if line.strip() and 'lsusb' not in line]

        # ----- I2C‑шины -----
        i2c_list = self.cmd_timeout__write_read__payload("i2cdetect -l 2>/dev/null", timeout=2).split('\n')
        result['i2c_buses'] = {}
        for bus_line in i2c_list:
            if 'i2c-' in bus_line:
                bus_num = bus_line.split()[0].split('-')[1]
                scan = self.cmd_timeout__write_read__payload(
                    f"i2cdetect -y {bus_num} 2>/dev/null",
                    timeout_continue=1.5,
                    timeout=2,
                )
                # Оставляем только строки с данными
                result['i2c_buses'][f'i2c-{bus_num}'] = [x.strip() for x in scan.split('\n')[1:] if x.strip()]

        # ----- Версия U‑Boot (ищем через grep) -----
        uboot_raw = self.cmd_timeout__write_read__payload(
            "dmesg | grep -i 'u-boot\|uboot' | head -1",
            timeout=2
        ).strip()
        result['uboot'] = uboot_raw if uboot_raw else 'N/A'

        return result

    # ==================================================================================================================
    def get_info__usb(self, port: str) -> dict[str, Any]:
        """
        available both variants:
            full path   - /dev/ttyUSB0
            devName     - ttyUSB0

        {
          "DEVPATH": "/devices/platform/soc/1c1d400.usb/usb8/8-1/8-1:1.0/ttyUSB0/tty/ttyUSB0",
          "DEVNAME": "/dev/ttyUSB0",
          "MAJOR": "188",
          "MINOR": "0",
          "SUBSYSTEM": "tty",
          "USEC_INITIALIZED": "12701625",
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
        }
        """
        # Отключаем пейджер, чтобы получить полный вывод без интерактива
        output = self.cmd_timeout__write_read__payload(
            f"SYSTEMD_PAGER=cat udevadm info -q property -n {port} 2>/dev/null",
            timeout_continue=0.5,
            timeout=4,
        ).split("\n")

        result = {}
        for line in output:
            if "SYSTEMD_PAGER=" in line:
                continue
            if '=' in line:
                key, val = line.split('=', 1)
                result[key.strip()] = val.strip()

        print(json.dumps(result, indent=2, ensure_ascii=False))
        return result

    def get_info__usb_all(self, filters: list | Base_EqValid | None = None) -> dict[str, dict[str, str]]:
        """
        Собирает udev-свойства для всех физических USB-устройств в /dev/.
        Фильтрует: только устройства с ID_BUS=usb (не консоли ttyS*, не виртуальные).

        Returns:
            {
                "/dev/ttyUSB0": {"ID_VENDOR": "1a86", "ID_MODEL": "USB_Serial", ...},
                "/dev/video0":  {"ID_VENDOR": "...", "ID_MODEL": "...", ...},
                "/dev/i2c-1":   {"ID_VENDOR": "...", "ID_MODEL": "...", ...},
            }
        """
        result: dict[str, dict[str, str]] = {}

        # Получаем список ВСЕХ устройств в /dev/
        dev_list = self.cmd_parsed__ls("/dev/", filters)
        """        
        WHAT USED
            ttyUSB* — USB-UART адаптеры
            ttyACM* — USB-модемы (если есть)
            video* — веб-камеры
            i2c-* — шины I2C (часто через USB-хаб)
            snd/* — звуковые устройства
            input/* — устройства ввода
            spidev* — SPI устройства
            
            
        
        some other devices no USB 
{
  "/dev/adsp1": {
    "DEVPATH": "/devices/platform/snd_aloop.0/sound/card1/adsp1",
    "DEVNAME": "/dev/adsp1",
    "MAJOR": "14",
    "MINOR": "28",
    "SUBSYSTEM": "sound",
    "USEC_INITIALIZED": "10866555",
    "TAGS": ":uaccess:",
    "CURRENT_TAGS": ":uaccess:"
  },
  "/dev/audio": {
    "DEVPATH": "/devices/platform/snd_dummy.0/sound/card0/audio",
    "DEVNAME": "/dev/audio",
    "MAJOR": "14",
    "MINOR": "4",
    "SUBSYSTEM": "sound",
    "USEC_INITIALIZED": "10846646",
    "TAGS": ":uaccess:",
    "CURRENT_TAGS": ":uaccess:"
  },
  "/dev/audio1": {
    "DEVPATH": "/devices/platform/snd_aloop.0/sound/card1/audio1",
    "DEVNAME": "/dev/audio1",
    "MAJOR": "14",
    "MINOR": "20",
    "SUBSYSTEM": "sound",
    "USEC_INITIALIZED": "10867924",
    "TAGS": ":uaccess:",
    "CURRENT_TAGS": ":uaccess:"
  },
  "/dev/audio2": {
    "DEVPATH": "/devices/platform/soc/1c22c00.codec/sound/card2/audio2",
    "DEVNAME": "/dev/audio2",
    "MAJOR": "14",
    "MINOR": "36",
    "SUBSYSTEM": "sound",
    "USEC_INITIALIZED": "11653994",
    "TAGS": ":uaccess:",
    "CURRENT_TAGS": ":uaccess:"
  },
  "/dev/audio3": {
    "DEVPATH": "/devices/platform/soc/soc:sound/sound/card3/audio3",
    "DEVNAME": "/dev/audio3",
    "MAJOR": "14",
    "MINOR": "52",
    "SUBSYSTEM": "sound",
    "USEC_INITIALIZED": "12165930",
    "TAGS": ":uaccess:",
    "CURRENT_TAGS": ":uaccess:"
  },
  "/dev/cec0": {
    "DEVPATH": "/devices/platform/soc/1ee0000.hdmi/cec0",
    "DEVNAME": "/dev/cec0",
    "MAJOR": "250",
    "MINOR": "0",
    "SUBSYSTEM": "cec"
  },
  "/dev/ttyUSB0": {
    "DEVPATH": "/devices/platform/soc/1c1d400.usb/usb8/8-1/8-1:1.0/ttyUSB0/tty/ttyUSB0",
    "DEVNAME": "/dev/ttyUSB0",
    "MAJOR": "188",
    "MINOR": "0",
    "SUBSYSTEM": "tty",
    "USEC_INITIALIZED": "13287546",
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
    "DEVLINKS": "/dev/serial/by-id/usb-1a86_USB_Serial-if00-port0 /dev/serial/by-path/platform-1c1d400.usb-usb-0:1:1.0-port0",
    "TAGS": ":systemd:",
    "CURRENT_TAGS": ":systemd:"
  },
  "/dev/vcs": {
    "DEVPATH": "/devices/virtual/vc/vcs",
    "DEVNAME": "/dev/vcs",
    "MAJOR": "7",
    "MINOR": "0",
    "SUBSYSTEM": "vc"
  },
  "/dev/dsp": {
    "DEVPATH": "/devices/platform/snd_dummy.0/sound/card0/dsp",
    "DEVNAME": "/dev/dsp",
    "MAJOR": "14",
    "MINOR": "3",
    "SUBSYSTEM": "sound",
    "USEC_INITIALIZED": "10843084",
    "TAGS": ":uaccess:",
    "CURRENT_TAGS": ":uaccess:"
  },
  "/dev/dsp1": {
    "DEVPATH": "/devices/platform/snd_aloop.0/sound/card1/dsp1",
    "DEVNAME": "/dev/dsp1",
    "MAJOR": "14",
    "MINOR": "19",
    "SUBSYSTEM": "sound",
    "USEC_INITIALIZED": "10877809",
    "TAGS": ":uaccess:",
    "CURRENT_TAGS": ":uaccess:"
  },
  "/dev/dsp2": {
    "DEVPATH": "/devices/platform/soc/1c22c00.codec/sound/card2/dsp2",
    "DEVNAME": "/dev/dsp2",
    "MAJOR": "14",
    "MINOR": "35",
    "SUBSYSTEM": "sound",
    "USEC_INITIALIZED": "11801536",
    "TAGS": ":uaccess:",
    "CURRENT_TAGS": ":uaccess:"
  },
  "/dev/dsp3": {
    "DEVPATH": "/devices/platform/soc/soc:sound/sound/card3/dsp3",
    "DEVNAME": "/dev/dsp3",
    "MAJOR": "14",
    "MINOR": "51",
    "SUBSYSTEM": "sound",
    "USEC_INITIALIZED": "12189275",
    "TAGS": ":uaccess:",
    "CURRENT_TAGS": ":uaccess:"
  },
  "/dev/vcsa": {
    "DEVPATH": "/devices/virtual/vc/vcsa",
    "DEVNAME": "/dev/vcsa",
    "MAJOR": "7",
    "MINOR": "128",
    "SUBSYSTEM": "vc"
  },
  "/dev/gpiochip0": {
    "DEVPATH": "/devices/platform/soc/1c20800.pinctrl/gpiochip0",
    "DEVNAME": "/dev/gpiochip0",
    "OF_NAME": "pinctrl",
    "OF_FULLNAME": "/soc/pinctrl@01c20800",
    "OF_COMPATIBLE_0": "allwinner,sun8i-h3-pinctrl",
    "OF_COMPATIBLE_N": "1",
    "MAJOR": "254",
    "MINOR": "0",
    "SUBSYSTEM": "gpio"
  },
  "/dev/sequencer": {
    "DEVPATH": "/devices/virtual/sound/sequencer",
    "DEVNAME": "/dev/sequencer",
    "MAJOR": "14",
    "MINOR": "1",
    "SUBSYSTEM": "sound",
    "USEC_INITIALIZED": "12604561",
    "TAGS": ":uaccess:",
    "CURRENT_TAGS": ":uaccess:"
  },
  "/dev/gpiochip1": {
    "DEVPATH": "/devices/platform/soc/1f02c00.pinctrl/gpiochip1",
    "DEVNAME": "/dev/gpiochip1",
    "OF_NAME": "pinctrl",
    "OF_FULLNAME": "/soc/pinctrl@01f02c00",
    "OF_COMPATIBLE_0": "allwinner,sun8i-h3-r-pinctrl",
    "OF_COMPATIBLE_N": "1",
    "MAJOR": "254",
    "MINOR": "1",
    "SUBSYSTEM": "gpio"
  },
  "/dev/sequencer2": {
    "DEVPATH": "/devices/virtual/sound/sequencer2",
    "DEVNAME": "/dev/sequencer2",
    "MAJOR": "14",
    "MINOR": "8",
    "SUBSYSTEM": "sound",
    "USEC_INITIALIZED": "12701333",
    "TAGS": ":uaccess:",
    "CURRENT_TAGS": ":uaccess:"
  },
  "/dev/i2c-0": {
    "DEVPATH": "/devices/platform/soc/1c2ac00.i2c/i2c-0/i2c-dev/i2c-0",
    "DEVNAME": "/dev/i2c-0",
    "MAJOR": "89",
    "MINOR": "0",
    "SUBSYSTEM": "i2c-dev"
  },
  "/dev/i2c-1": {
    "DEVPATH": "/devices/platform/soc/1c2b000.i2c/i2c-1/i2c-dev/i2c-1",
    "DEVNAME": "/dev/i2c-1",
    "MAJOR": "89",
    "MINOR": "1",
    "SUBSYSTEM": "i2c-dev"
  },
  "/dev/i2c-2": {
    "DEVPATH": "/devices/platform/soc/1c2b400.i2c/i2c-2/i2c-dev/i2c-2",
    "DEVNAME": "/dev/i2c-2",
    "MAJOR": "89",
    "MINOR": "2",
    "SUBSYSTEM": "i2c-dev"
  },
  "/dev/video0": {
    "DEVPATH": "/devices/platform/soc/1cb0000.camera/video4linux/video0",
    "DEVNAME": "/dev/video0",
    "MAJOR": "81",
    "MINOR": "0",
    "SUBSYSTEM": "video4linux",
    "USEC_INITIALIZED": "12019167",
    "ID_V4L_VERSION": "2",
    "ID_V4L_PRODUCT": "sun6i-csi",
    "ID_V4L_CAPABILITIES": ":capture:",
    "ID_PATH": "platform-1cb0000.camera",
    "ID_PATH_TAG": "platform-1cb0000_camera",
    "ID_FOR_SEAT": "video4linux-platform-1cb0000_camera",
    "DEVLINKS": "/dev/v4l/by-path/platform-1cb0000.camera-video-index0",
    "TAGS": ":uaccess:seat:",
    "CURRENT_TAGS": ":uaccess:seat:"
  },
  "/dev/i2c-3": {
    "DEVPATH": "/devices/platform/soc/1ee0000.hdmi/i2c-3/i2c-dev/i2c-3",
    "DEVNAME": "/dev/i2c-3",
    "MAJOR": "89",
    "MINOR": "3",
    "SUBSYSTEM": "i2c-dev"
  },
  "/dev/spidev0.0": {
    "DEVPATH": "/devices/platform/soc/1c68000.spi/spi_master/spi0/spi0.0/spidev/spidev0.0",
    "DEVNAME": "/dev/spidev0.0",
    "MAJOR": "153",
    "MINOR": "0",
    "SUBSYSTEM": "spidev"
  }
}
        """
        # Фильтруем — оставляем только потенциально интересные устройства
        # Исключаем: ttyS* (консоли), tty0-63 (виртуальные консоли),
        if filters:
            SKIP = []
        else:
            SKIP = [
                EqValid_RegexpAnyTrue(
                    r"ttyS\d",  # tty console
                    r"tty\d*",         # virtual tty
                    r"mmcblk.*", r"nbd.*", r"loop.*",   # блочные устройства
                    r"vcs\d+", "vcsa\d+",  # виртуальные консоли
                    r"watchdog\d*",
                    r"rtc\d*",
                    r"mixer\d*",
                ),

                EqValid_EQ(
                    "stdin", "stdout", "stderr",
                    "null", "zero", "full",
                    "bus",
                    "console",
                    "random", "urandom",
                    "mem", "kmsg",
                    "vhci",
                    "rfkill",
                    "ptmx", "pts",

                    "dri", "fb0",
                    "ppp",

                    "ram",
                    "net",
                    "v4l",

                    "watchdog", "cpu_dma_latency",
                    "network_latency", "network_throughput",
                    "memory_bandwidth",
                    "kmsg", "kmem", "mem", "kvm",
                    "fuse", "cuse",
                    "rtc0", "rtc1",
                    "initctl", "autofs", "btrfs-control",
                    "gpiochip",
                    "mqueue", "shm",
                    "fd", "mapper",
                    "psaux",
                ),
            ]

        # Пропускаем заведомо не-USB устройства
        potential_devices: list[str] = [*filter(lambda x: x not in SKIP, dev_list)]

        # Для каждого потенциального устройства пробуем получить udev-свойства
        for dev_path in potential_devices:
            try:
                props = self.get_info__usb(dev_path)

                # Проверяем, что это физическое USB-устройство
                id_bus = props.get("ID_BUS", "")

                # Пропускаем, если это не USB (консоли ttyS*, виртуальные)
                if id_bus != "usb":
                    # Но сохраняем, если есть хоть какие-то полезные ID_*
                    has_useful_ids = any(
                        k.startswith("ID_") and v
                        for k, v in props.items()
                    )
                    if not has_useful_ids:
                        continue
                    # Если есть ID_PATH или DEVPATH с "usb" — оставляем
                    if "usb" not in props.get("DEVPATH", "").lower():
                        if "usb" not in props.get("ID_PATH", "").lower():
                            continue

                if props:  # сохраняем только если есть данные
                    result[dev_path] = props

            except Exception as exc:
                # Устройство может не поддерживать udev — пропускаем
                logger.debug(f"Пропущено {dev_path}: {exc}")
                continue

        print(json.dumps(result, indent=2, ensure_ascii=True))
        return result

    # ==================================================================================================================
    def gnss_get_info_ubx(self) -> dict[str, Any]:
        script = "scr__gnss_info_ubx.py"
        if "/" in script:
            script_name_only = script.rsplit("/", 1)[1]
        else:
            script_name_only = script

        # Убиваем предыдущие экземпляры скрипта и освобождаем порт
        self.cmd_timeout__write_read__payload(f'pkill -9 -f {script_name_only}; fuser -k /dev/ttyUSB0; sleep 0.5')

        output = self.cmd_timeout__write_read__payload(f'python3 {script}', timeout_continue=5)
        assert output, "данные от устройства не получены вообще"

        if 'UBX_RESPONSE:[' in output:
            # Извлекаем HEX-строку --------------------
            print(f"FULL: {output}")

            match = re.search(r'UBX_RESPONSE:\[([0-9A-F]*)\]', output)
            assert match, "Не найден корректный UBX_RESPONSE в выводе"
            output_hex_str = match.group(1)
            print(f"\t{output_hex_str=}")

            # Декодируем HEX-строку в настоящие байты
            try:
                raw_data: bytes = bytes.fromhex(output_hex_str)
                print(f"\t{raw_data=}")
            except ValueError:
                assert False, f"Невалидная HEX-строка: {output_hex_str!r}"

            result = self.parse__gnss_info__UBX(raw_data)
            print(json.dumps(result, indent=2))
            return result

    @staticmethod
    def parse__gnss_info__UBX(raw: bytes) -> dict[str, str | list[str]]:
        """
        Парсит ответ UBX MON-VER (класс 0x0A, ID 0x04) и возвращает словарь:
        {
            'sw_version': str,    # версия расширенного ПО
            'hw_version': str,    # аппаратная версия (строка)
            'extensions': [       # дополнительные поля
                "ROM BASE 3.01 (107888)",
                "FWVER=SPG 3.01",
                "PROTVER=18.00",
                "MOD=NEO-M8N-0",
                "FIS=0xEF4015 (100111)",
                "GPS;GLO;GAL;BDS",
                "SBAS;IMES;QZSS"
            ]
        }
        При ошибке выбрасывает ValueError.

        UBX_RESPONSE:b5620a04fa0045585420434f524520332e3031202831303739303029000000000000000030303038303030300000524f4d204241534520332e3031202831303738383829000000000000000046575645523d53504720332e30310000000000000000000000000000000050524f545645523d31382e303000000000000000000000000000000000004d4f443d4e454f2d4d384e2d3000000000000000000000000000000000004649533d30784546343031352028313030313131290000000000000000004750533b474c4f3b47414c3b424453000000000000000000000000000000534241533b494d45533b515a535300000000000000000000000000000000

        LR-STRIPPED:	output_hex_str='b5620a04fa0045585420434f524520332e3031202831303739303029000000000000000030303038303030300000524f4d204241534520332e3031202831303738383829000000000000000046575645523d53504720332e30310000000000000000000000000000000050524f545645523d31382e303000000000000000000000000000000000004d4f443d4e454f2d4d384e2d3000000000000000000000000000000000004649533d30784546343031352028313030313131290000000000000000004750533b474c4f3b47414c3b424453000000000000000000000000000000534241533b494d45533b515a535300000000000000000000000000000000'
        LR-STRIPPED:	raw_data=b'\xb5b\n\x04\xfa\x00EXT CORE 3.01 (107900)\x00\x00\x00\x00\x00\x00\x00\x0000080000\x00\x00ROM BASE 3.01 (107888)\x00\x00\x00\x00\x00\x00\x00\x00FWVER=SPG 3.01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00PROTVER=18.00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00MOD=NEO-M8N-0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00FIS=0xEF4015 (100111)\x00\x00\x00\x00\x00\x00\x00\x00\x00GPS;GLO;GAL;BDS\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00SBAS;IMES;QZSS\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        """
        # Проверка синхронизации и типа сообщения
        if raw[:2] != b'\xb5\x62':
            raise ValueError("Невалидный UBX заголовок")
        cls, msg_id = raw[2], raw[3]
        if cls != 0x0A or msg_id != 0x04:
            raise ValueError(f"Ожидался MON-VER, получено 0x{cls:02X} 0x{msg_id:02X}")

        length = int.from_bytes(raw[4:6], 'little')
        payload = raw[6:6 + length]

        sw_version: str = payload[:30].split(b'\x00')[0].decode('ascii')
        hw_version: str = payload[30:40].split(b'\x00')[0].decode('ascii')
        extensions_hex: str = payload[40:].decode('ascii')

        # extensions – всё после 40-го байта, разделённые нулями
        extensions = [ext for ext in extensions_hex.split('\x00') if ext]

        return {
            'sw_version': sw_version,
            'hw_version': hw_version,
            'extensions': extensions,
        }

    # ==================================================================================================================
    def rfid__check_working(self) -> bool:
        # Убиваем возможные зависшие процессы на порту
        self.conn.write_read_bytes(f"fuser -k /dev/ttyS2 2>/dev/null", timeout_continue=0.5)
        time.sleep(0.2)

        command_line = f"python3 scr__rfid_scan.py"

        output = self.cmd_timeout__write_read__payload(
            command_line,
            timeout=2,
            timeout_continue=2,
        )
        result = f"RawData(0bytes):" not in output
        return result

    def rfid__scan(self, steps: int | None = None) -> set[str]:
        """
        Ридер получает команду инвентаризации (01).
        Он начинает сканировать. Если меток нет, он сразу формирует и отправляет короткий ответ A0 04 01 81 [CRC].
        Если метки есть, он не тратит время на отправку отдельной квитанции. Он сразу формирует один расширенный пакет, в заголовке которого дублируется статус операции, и следом идут данные о найденных метках.

        ----------------------------------------------------
[15:56:32.073646]COM16.write[OK]= b'python3 scr__rfid_scan.py\r\n'
[15:56:32.093334]COM16.readEOL[OK]= b'python3 scr__rfid_scan.py'
[15:56:32.097352]COM16.readEOL[OK]= b'\x1b[?2004l'
[15:56:33.539228]COM16.readEOL[OK]= b'RawData(0bytes):[]'
[15:56:33.548883]COM16.readEOL[OK]= b'found=0epc'
[15:56:33.600955]COM16.readEOL[OK]= b'\x1b[?2004hroot@harvest05:~# '
[15:56:33.600955]COM16.stop_line[OK]= b'' [extra=EqValid_Regexp(v_args=(b'.*root@.+:.+#.*',)/v_kwargs={}/_iresult_reverse=None/_iresult_cumulate=<EnumAdj_BoolCumulate.ALL_TRUE: <built-in function all>>/_other_final__resolve=True)]
[15:56:33.600955]COM16.readNoEOL[OK]= b'\x1b[?2004hroot@harvest05:~# '
[15:56:33.702284]COM16.reset_input[OK]= b'in_waiting__bytes_count=36'
[15:56:33.702284]COM16.in_waiting__bytes_data[OK]= b'\n\x1b[?2004l\r\x1b[?2004hroot@harvest05:~# '
[15:56:33.702284]COM16.reset_input[OK]= b''
[15:56:33.702284]COM16.write[OK]= b'\x03'
[COM16.WRITEREAD]
	write=[python3 scr__rfid_scan.py]
	read=[RawData(0bytes):[]
found=0epc]
        ----------------------------------------------------
        ТКАНЬ ФАРАДЕЯ
        [COM16.WRITEREAD]
            write=[python3 /tmp/rfid_scan.py]
            read=[RawData(6bytes):[A004018122B8]
        found=0epc]

        Байт	Значение (HEX)	Назначение	Комментарий
        1	A0	Header (Заголовок)	Фиксированный заголовок пакета.
        2	04	Length (Длина)	Длина пакета данных. 0x04 = 4 байта. -ВСЕ ЧТО ПОСЛЕ ЭТОГО БАЙТА!!! тоесть с CRC!!!
        3	01	Command (Команда)	Эхо команды. 0x01 — это команда инвентаризации.
        4	81	Status (Статус)	Самая важная часть! 0x81 — это стандартный код "Operation Succeeded" (Операция успешна). Ошибки были бы другими кодами.
        5-6	22 B8	Checksum (Контрольная сумма)	Это контрольная сумма (обычно CRC-16) для байтов 3 и 4 (01 81).
        ----------------------------------------------------
        1EPC
        [COM16.WRITEREAD]
            write=[python3 /tmp/rfid_scan.py]
            read=[RawData(43bytes):[A02901810001203000E2806894000050035FD77070430A430A3000E2806894000050035FD77070100401F7]
        3000E2806894000050035FD77070
        found=1epc]

A02901810001203000E2806894000050035FD77070430A430A3000E2806894000050035FD77070100401F7 =86символов=43байта=1заголовок+1длина+41тело

        Байт(ы)	HEX-значение	Длина	Назначение	Значение / Расшифровка
        1	A0	1	Заголовок (Header)	Фиксированный маркер начала пакета.
        2	29	1	Длина пакета (Length)	0x29 = 41 байт. Это всё, что после этого байта.
        3	01	1	Код команды (Command)	Эхо вашего запроса 0x01 (команда инвентаризации).
        4	81	1	Статус (Status)	0x81 — операция выполнена успешно.
        5-6	00 01	2	Количество меток	0x0001 = 1 — ридер обнаружил ровно одну метку.
        7	20	1	Длина данных метки	0x20 = 32 байта отведено на данные одной метки.(RSSI + EPC).
        8-39	30 00 E2 ... 10 04	32	Данные метки	Содержат RSSI, EPC и, возможно, другие поля.
        40-41	01 F7	2	Контрольная сумма (CRC)	CRC-16 для проверки целостности пакета.

        ПАКЕТ
        ┌──────┬──────┬──────┬──────┬──────────┬──────┬─────────────────────────────────┬──────┐
        │ A0   │ 29   │ 01   │ 81   │ 00 01    │ 20   │ [32 байта данных метки]          │ 01F7 │
        ├──────┼──────┼──────┼──────┼──────────┼──────┼─────────────────────────────────┼──────┤
        │Head  │ Len  │ Cmd  │ OK   │ 1 метка  │ len  │ RSSI=0x00                        │ CRC  │
        │      │ =41  │ INV  │      │          │ =32  │ EPC=3000E2806894000050035FD77070 │      │
        └──────┴──────┴──────┴──────┴──────────┴──────┴─────────────────────────────────┴──────┘

        ДАННЫЕ МЕТКИ
        ┌──────────┬──────────┬──────────────┬──────────────────────────┐
        │ Заголовок│ Фильтр   │ Идентификатор │ Серийный номер           │
        │  8 бит   │  3 бита  │ компании      │ объекта                  │
        │          │          │ 20-40 бит     │                          │
        ├──────────┼──────────┼──────────────┼──────────────────────────┤
        │   30     │    0     │ 0E2806894    │ 000050035FD77070         │
        └──────────┴──────────┴──────────────┴──────────────────────────┘
        ----------------------------------------------------
        2EPC
        [COM16.WRITEREAD]
            write=[python3 /tmp/rfid_scan.py]
            read=[RawData(86bytes):[A02901810002203000E2806894000040138945853E812981293000E2806894000040138945853E10040146A02901810002203000E2806894000050035FD77070430A430A3000E2806894000050035FD77070100401F6]
        3000E2806894000040138945853E
        3000E2806894000050035FD77070
        found=2epc]
        ----------------------------------------------------
        4epc
        	read=[RawData(172bytes):[A02901810004203000E28068942000502BBD609C95D842D8423000E28068942000502BBD609C951004015AA02901810004203000E2806894000050035FD77070430A430A3000E2806894000050035FD77070100401F4A02901810004203400E77702010000000000000000468446843400E77702010000000000000000100401BEA02901810004203000E2806894000040138945853E812981293000E2806894000040138945853E10040144]
        3000E28068942000502BBD609C95
        3000E2806894000050035FD77070
        3000E2806894000040138945853E
        3400E77702010000000000000000
        found=4epc]
        """
        result = set()
        command_line = f"python3 scr__rfid_scan.py"

        steps = steps or 1
        for step in range(steps):
            # Убиваем возможные зависшие процессы на порту
            self.conn.write_read_bytes(f"fuser -k /dev/ttyS2 2>/dev/null", timeout_continue=0.5)
            time.sleep(0.3)

            output = self.cmd_timeout__write_read__payload(
                command_line,
                timeout_continue=10,
            )
            s_result = output.splitlines()

            # Фильтруем: только строки вида "HEX,ЧИСЛО"
            for line in s_result:
                if re.match(r'^[0-9A-F]{24}', line.strip()):
                    result.add(line.strip())

            if step != steps-1:
                time.sleep(0.3)
        return result

    # ==================================================================================================================
    def bt__scan(
            self,
            timeout: float = 20,
            timeout_continue: float = 4,
            **r_kwargs,
    ) -> dict[str, dict[str, str | int | None]] | NoReturn:   # {mac: {name, rssi}}
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
        output = self.cmd_timeout__write_read__payload(
            "bluetoothctl -- scan on",
            timeout=timeout,
            timeout_continue=timeout_continue or timeout,
            **r_kwargs,
        )
        if "Discovery started" not in output:
            raise Exception("Bluetooth поиск не запустился")

        # пример строки: [NEW] Device 68:4E:05:DA:46:2C 403
        result = dict()
        for mac, name in re.findall(r'\[NEW\]\s+Device\s+([0-9A-F:]{17})\s+(.+)', output):
            if mac not in result:
                result[mac] = dict(name=None, rssi=None, names=list(), rssis=list())

            name_new = name.strip()
            if name_new not in result[mac]["names"]:
                result[mac]["names"].append(name_new)
            result[mac]["name"] = name_new

        for mac, rssi_str in re.findall(r'\[CHG\]\s+Device\s+([0-9A-F:]{17})\s+RSSI:\s+(-\d+)', output):
            if mac not in result:
                result[mac] = dict(name=None, rssi=None, names=list(), rssis=list())

            rssi_str = rssi_str.strip()
            try:
                rssi_new = int(rssi_str)
            except:
                rssi_new = rssi_str

            if not rssi_new:
                continue

            if rssi_new not in result[mac]["rssis"]:
                result[mac]["rssis"].append(rssi_new)
            result[mac]["rssi"] = max(result[mac]["rssis"])

        # Сортируем result по RSSI: чем выше значение (ближе к 0), тем ближе устройство
        sorted_result: dict[str, dict[str, str | int | None]] = dict()

        # Сначала добавляем устройства с известным RSSI, отсортированные по убыванию (ближайшие первыми)
        devices_with_rssi = {mac: data for mac, data in result.items() if data["rssi"] is not None}
        for mac, _ in sorted(devices_with_rssi.items(), key=lambda x: x[1]["rssi"], reverse=True):
            sorted_result[mac] = result[mac]

        # Затем добавляем остальные устройства без данных о RSSI
        for mac, data in result.items():
            if mac not in sorted_result:
                sorted_result[mac] = data

        print(json.dumps(sorted_result, indent=2))
        return sorted_result

    def bt__get_dev_info(self, mac: str) -> dict[str, Any]:
        """
        Получает информацию о конкретном устройстве.
        Важно: mac передается как отдельный аргумент, без кавычек в шелле.

        [COM16.WRITEREAD]
            write=[timeout 5 bluetoothctl info D4:81:ED:BB:AA:6B]
            read=[Device D4:81:ED:BB:AA:6B (random)
            Name: UltraSonic
            Alias: UltraSonic
            Paired: no
            Bonded: no
            Trusted: no
            Blocked: no
            Connected: yes
            LegacyPairing: no
            UUID: Generic Access Profile    (00001800-0000-1000-8000-00805f9b34fb)
            UUID: Generic Attribute Profile (00001801-0000-1000-8000-00805f9b34fb)
            UUID: Vendor specific           (dec01400-ceb1-cec0-dec0-ff0123456789)
            ManufacturerData Key: 0x0059
            ManufacturerData Value:
          54 47 ff ff ff ff 0b 44 01                       TG.....D.       ]

        [COM16.WRITEREAD]
            write=[timeout 5 bluetoothctl info FC:82:20:D6:82:CF]
            read=[Device FC:82:20:D6:82:CF (public)
            Name: COROS NOMAD BD4407
            Alias: COROS NOMAD BD4407
            Appearance: 0x00c0
            Paired: no
            Bonded: no
            Trusted: no
            Blocked: no
            Connected: no
            LegacyPairing: no
            UUID: Battery Service           (0000180f-0000-1000-8000-00805f9b34fb)
            UUID: Device Information        (0000180a-0000-1000-8000-00805f9b34fb)
            UUID: Tencent Holdings Limited. (0000fee7-0000-1000-8000-00805f9b34fb)
            ServiceData Key: 00003802-0000-1000-8000-00805f9b34fb
            ServiceData Value:
          fc 82 20 d6 82 cf                                .. ...          ]

        [COM16.WRITEREAD]
            write=[timeout 5 bluetoothctl info FC:82:20:D6:82:11]
            read=[Device FC:82:20:D6:82:11 not available]

        [COM16.WRITEREAD]
            write=[timeout 5 bluetoothctl info FC:82:20:D6:8]   # bad MAC
            read=[Device FC:82:20:D6:8 not available]

        [COM16.WRITEREAD]
            write=[timeout 5 bluetoothctl info D4:81:ED:BB:AA:6B]
            read=[Device D4:81:ED:BB:AA:6B (random)
            Name: UltraSonic
            Alias: UltraSonic
            Paired: no
            Bonded: no
            Trusted: no
            Blocked: no
            Connected: yes
            LegacyPairing: no
            UUID: Generic Access Profile    (00001800-0000-1000-8000-00805f9b34fb)
            UUID: Generic Attribute Profile (00001801-0000-1000-8000-00805f9b34fb)
            UUID: Vendor specific           (dec01400-ceb1-cec0-dec0-ff0123456789)
            ManufacturerData Key: 0x0059
            ManufacturerData Value:
          54 47 ff ff ff ff 0b 44 01                       TG.....D.       ]
        {
          "mac": "D4:81:ED:BB:AA:6B",
          "random": true,
          "name": "UltraSonic",
          "alias": "UltraSonic",
          "paired": false,
          "bonded": false,
          "trusted": false,
          "blocked": false,
          "connected": true,
          "legacy_pairing": false,
          "uuids": {
            "Generic Access Profile": "00001800-0000-1000-8000-00805f9b34fb",
            "Generic Attribute Profile": "00001801-0000-1000-8000-00805f9b34fb",
            "Vendor specific": "dec01400-ceb1-cec0-dec0-ff0123456789"
          },
          "manufacturer_key": "0x0059",
          "manufacturer_value": "54 47 ff ff ff ff 0b 44 01 TG.....D."
        }
        """
        cmd = f"bluetoothctl info {mac}"
        output = self.cmd_timeout__write_read__payload(
            cmd,
            timeout=5,
            timeout_continue=3,
        )

        result: dict[str, bool | str | Any | None] = {
            "mac": mac,
            "random": None,     # random/public
            "name": None,
            "alias": None,
            "paired": None,
            "bonded": None,
            "trusted": None,
            "blocked": None,
            "connected": None,
            "legacy_pairing": None,
            "uuids": {},
            "manufacturer_key": None,
            "manufacturer_value": None,
        }

        # Флаг для сбора ManufacturerData Value (многострочное поле)
        collecting_manufacturer_value = False
        manufacturer_value_parts = []

        for line in output.splitlines():
            line = line.strip()

            # 1. Первая строка: Device XX:XX:XX:XX:XX:XX (random/public) --------------
            if line.startswith("Device "):
                # "Device D4:81:ED:BB:AA:6B (random)"
                # "Device D4:81:ED:BB:AA:6B not available"
                if "not available" in line:
                    return {"mac": mac, "error": "not available"}

                result["random"] = "(random)" in line

            # 2. Простые поля: Name:...
            elif line.startswith("Name:"):
                result["name"] = line.split(":", 1)[1].strip()

            elif line.startswith("Alias:"):
                result["alias"] = line.split(":", 1)[1].strip()

            elif line.startswith("Paired:"):
                result["paired"] = "yes" in line.lower()

            elif line.startswith("Bonded:"):
                result["bonded"] = "yes" in line.lower()

            elif line.startswith("Trusted:"):
                result["trusted"] = "yes" in line.lower()

            elif line.startswith("Blocked:"):
                result["blocked"] = "yes" in line.lower()

            elif line.startswith("Connected:"):
                result["connected"] = "yes" in line.lower()

            elif line.startswith("LegacyPairing:"):
                result["legacy_pairing"] = "yes" in line.lower()

            # 3. UUID: Name    (hex-uuid)
            elif line.startswith("UUID:"):
                # "UUID: Generic Access Profile    (00001800-0000-1000-8000-00805f9b34fb)"
                match = re.match(r'UUID:\s+(.+?)\s+\(([0-9a-fA-F-]+)\)', line)
                if match:
                    result["uuids"][match.group(1).strip()] = match.group(2).strip()

            # 4. ManufacturerData Key:
            elif line.startswith("ManufacturerData Key:"):
                result["manufacturer_key"] = line.split(":", 1)[1].strip()

            # 5. ManufacturerData Value: (заголовок)
            elif line.startswith("ManufacturerData Value:"):
                collecting_manufacturer_value = True
                manufacturer_value_parts = []

            # 6. Строки ManufacturerData Value (после заголовка)
            elif collecting_manufacturer_value and line:
                # "  54 47 ff ff ff ff 0b 44 01                       TG.....D.       "
                # Берем только HEX-часть (первые несколько слов)
                hex_part = ' '.join(line.split()[:20])  # HEX-байты идут первыми
                manufacturer_value_parts.append(hex_part)

            # 7. Конец ManufacturerData Value (пустая строка или начало нового поля)
            elif collecting_manufacturer_value and not line:
                collecting_manufacturer_value = False
                result["manufacturer_value"] = ' '.join(manufacturer_value_parts)

        # На случай, если ManufacturerData Value был в конце вывода
        if collecting_manufacturer_value and manufacturer_value_parts:
            result["manufacturer_value"] = ' '.join(manufacturer_value_parts)

        return result

    # ==================================================================================================================
    def btus__read(self, mac: str | None = None, max_pkgs: int | None = None, timeout: float = 25.0) -> list[bytes]:
        """
        Собирает данные с UltraSonic датчика.
        D4:81:ED:BB:AA:6B
        """
        mac_s = f"--mac {mac}" if mac else ""
        max_pkgs_s = f"--pockets {max_pkgs}" if max_pkgs else ""
        timeout_s = f"--timeout {timeout}" if timeout else ""
        cmd = f"python3 scr__btus_read.py {mac_s} {max_pkgs_s} {timeout_s}"

        output = self.cmd_timeout__write_read__payload(
            cmd,
            timeout=timeout + 5.0,
            timeout_continue=timeout + 5.0,
        )
        result_hex: list[str] = re.findall(r"PACKET_HEX:\[([0-9A-F]+)\]", output)
        print(f"{result_hex=}")
        result_bytes: list[bytes] = [*map(bytes.fromhex, result_hex)]
        print(f"{result_bytes=}")
        return result_bytes

    @staticmethod
    def btus__validate_pkg(data_bytes: bytes, eq: dict[str, Base_EqValid | Any] | None = None) -> bool:
        """
        b'"UTC":2945843\n"Distance up":000\n"Distance side":000\n"Temperature":023\n"Battery":098\n"Percentage":022'
        """
        data_text = data_bytes.decode(errors="replace")

        eq_default = {
            "UTC": EqValid_GT_NumParsedSingle(0),
            "Distance up": EqValid_LGTE_NumParsedSingle(ge=0, lt=100),
            "Distance side": EqValid_LGTE_NumParsedSingle(ge=0, lt=10),
            "Temperature": EqValid_LGTE_NumParsedSingle(gt=0, lt=40),
            "Battery": EqValid_LGTE_NumParsedSingle(gt=0, lt=100),
            "Percentage": EqValid_LGTE_NumParsedSingle(gt=0, lt=100),
        }

        parced = {
            "UTC": None,
            "Distance up": None,
            "Distance side": None,
            "Temperature": None,
            "Battery": None,
            "Percentage": None,
        }

        for key in parced:
            pattern = rf'"{key}":(\d+)\s*'
            value = re.search(pattern, data_text)
            if value:
                value = value[1]
                print(f"{value=}")
                value = int(value)
                parced[key] = value

        print(json.dumps(parced, indent=2))

        if eq is not None:
            return parced == eq
        else:
            # return None not in parced.values()
            return parced == eq_default

    # ==================================================================================================================
    def sql_settings__get_all(self) -> dict[str, str]:
        """
        ПОЛЯ ---------------------------------
        CREATE TABLE Service_settings (
            identsettings INTEGER    PRIMARY KEY ASC AUTOINCREMENT
                                     NOT NULL
                                     UNIQUE,
            keyname       TEXT (64)  UNIQUE
                                     NOT NULL,
            valuename     TEXT (512) NOT NULL,
            flagactual    INTEGER    DEFAULT (0),
            levelacs      INTEGER    DEFAULT (0)
        );

        ДАМП ---------------------------------
        root@harvest05:~#
        ---- Sent utf8 encoded message: "sqlite3 /srv/publish/Harvester.db \"SELECT * FROM Service_settings\"\r\n" ----
        sqlite3 /srv/publish/Harvester.db "SELECT * FROM Service_settings"
        16|ipComp|127.0.0.1|1|1
        17|timeDelete|300|1|1
        18|minTimeRead|20|1|1
        19|periodDetect|1|1|1
        20|numberTryRead|25|1|1
        21|numberTryWrite|1|1|1
        22|regNum|5|1|1
        23|blockNum|5|1|1
        24|minSpeed|0.5|1|1
        25|portName|/dev/ttyUSB0|1|1
        26|readerSerial|/dev/ttyS2|1|1
        27|urlTimeSend|http://45.90.218.212/api/v1/harvester/telemetry|1|0
        28|urlIncidentessend|http://45.90.218.212/api/v1/harvester/incident|1|0
        29|urlOnlineSend|http://45.90.218.212/api/v1/harvester/online|1|0
        30|urlWorkSend|http://45.90.218.212/api/v1/harvester/discharge|1|0
        31|jwtToken|eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ1cm96aGFpLWNsb3VkIiwic3ViIjoiNSIsInR5cGUiOiJoYXJ2ZXN0ZXIifQ.JNdx5Yhy-fJJ3E4SMQfppF4LbGHzyD1UNgPtmKPBXHY|1|1
        32|macUz1|D4:81:ED:BB:AA:6B|1|1
        33|timeSend|300000|1|0
        35|macUz2|CF:9F:FA:E6:14:3F|1|1
        36|timeGNSS|10000|1|0
        37|timeblue|15000|1|0
        38|timeblueTwo|16000|1|0
        39|timeSendSleep|1800000|1|0
        40|uzTwo|0|1|0
        41|maxHeight|250|1|1
        42|stepMTBO|5|1|0
        43|urlBunker|http://45.90.218.212/api/v1/harvester/discharge/bunker|1|0
        44|incline|0.2|1|0
        45|sendTelemetry|180000|1|0
        46|timeAfterSleepMinutes|20|1|0
        47|maxSputnicHeight|400|1|0
        48|minSputnicHeight|50|1|0
        root@harvest05:~#
        root@harvest05:~#

        {
          "ipComp": "127.0.0.1",
          "timeDelete": "300",
          "minTimeRead": "20",
          "periodDetect": "1",
          "numberTryRead": "25",
          "numberTryWrite": "1",
          "regNum": "5",
          "blockNum": "5",
          "minSpeed": "0.5",
          "portName": "/dev/ttyUSB0",
          "readerSerial": "/dev/ttyS2",
          "urlTimeSend": "http://45.90.218.212/api/v1/harvester/telemetry",
          "urlIncidentessend": "http://45.90.218.212/api/v1/harvester/incident",
          "urlOnlineSend": "http://45.90.218.212/api/v1/harvester/online",
          "urlWorkSend": "http://45.90.218.212/api/v1/harvester/discharge",
          "jwtToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ1cm96aGFpLWNsb3VkIiwic3ViIjoiNSIsInR5cGUiOiJoYXJ2ZXN0ZXIifQ.JNdx5Yhy-fJJ3E4SMQfppF4LbGHzyD1UNgPtmKPBXHY",
          "macUz1": "D4:81:ED:BB:AA:6B",
          "timeSend": "300000",
          "macUz2": "CF:9F:FA:E6:14:3F",
          "timeGNSS": "10000",
          "timeblue": "15000",
          "timeblueTwo": "16000",
          "timeSendSleep": "1800000",
          "uzTwo": "0",
          "maxHeight": "250",
          "stepMTBO": "5",
          "urlBunker": "http://45.90.218.212/api/v1/harvester/discharge/bunker",
          "incline": "0.2",
          "sendTelemetry": "180000",
          "timeAfterSleepMinutes": "20",
          "maxSputnicHeight": "400",
          "minSputnicHeight": "50"
        }
        """
        result = {}
        cmd = f'sqlite3 /srv/publish/Harvester.db "SELECT * FROM Service_settings"'
        output = self.cmd_timeout__write_read__payload(
            cmd,
            timeout=2,
            timeout_continue=1,
        )
        for index, line in enumerate(output.splitlines()):
            print(f"{index=}/{line=}")
            identsettings, keyname, valuename, flagactual, levelacs = line.split("|")
            result[keyname] = valuename

        print("sql_settings__get_all=", json.dumps(result, indent=2))
        return result


# ======================================================================================================================
# def test__():
#     data = b'"UTC":2945843\n"Distance up":000\n"Distance side":000\n"Temperature":023\n"Battery":098\n"Percentage":022'
#     assert Harvest.btus__validate_pkg(data)


# ======================================================================================================================
