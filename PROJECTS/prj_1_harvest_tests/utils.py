import json
import logging
import base64

from base_aux.aux_eq.m4_eq_valid2_derivatives import *
from base_aux.clients.m1_client_0__base import ClientBase


# ======================================================================================================================
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MAC_HV05 = "D4:81:ED:BB:AA:6B"
PATTERN_MAC = r"[0-9A-F:]{17}"


# ======================================================================================================================
class Harvest:
    AT_CMDS__FLAT: Iterable[str] = [
        # =========================================================================
        "AT",  # ответ эхо - проверка функционирования модема на канал

        # =========================================================================
        # попытка определить номер телефона
        "AT+CNUM",
        "AT+CRSM",
        # "AT+CPBS=\"ON\"; +CPBR=1",  # Чтение своего номера из книги
        # "AT+CPBS=\'ON\'; +CPBR=1",  # Чтение своего номера из книги
        "AT+CIMI",                # IMSI (для идентификации)
        # "AT+CRSM=176,28589,0,0,12",  # Чтение EF_MSISDN с SIM (прямой доступ)

        # =========================================================================
        # ИДЕНТИФИКАЦИЯ И ВЕРСИИ
        "ATI",  # Общая информация о производителе/модели=Основная информация
        "ATI1",  # Расширенная информация
        "ATI2",  # Ещё больше информации
        "ATI3",  # Информация о версии
        "ATI4",  # Дополнительные возможности
        "ATI5",  # Информация о производителе
        "ATI6",  # Информация о модели
        "ATI7",  # Информация о ревизии
        "ATI8",  # Серийный номер
        "ATI9",  # Дополнительная информация

        "AT+CGMI",  # Запрос производителя (Manufacturer ID)
        "AT+CGMM",  # Запрос модели (Model ID)
        "AT+CGMR",  # Запрос ревизии прошивки (Revision)
        "AT+CGSN",  # Запрос IMEI (Serial Number)
        "AT+CIMI",  # Запрос IMSI (International Mobile Subscriber ID)
        "AT+GSN",  # Аналог CGSN — IMEI

        # =========================================================================
        # СОСТОЯНИЕ SIM-КАРТЫ И PIN
        "AT+CPIN?",  # Статус SIM: READY, SIM PIN, SIM PUK, SIM PIN2...
        "AT+CPINR?",  #
        # "AT+CPINR=\"SIM PIN\"",  # Остаток попыток ввода PIN
        # "AT+CPINR=\"SIM PUK\"",  # Остаток попыток ввода PUK
        "AT+CCID",  # ICCID (серийный номер SIM-карты)
        "AT+ICCID",  # ICCID (серийный номер SIM-карты)

        # =========================================================================
        # СЕТЬ И РЕГИСТРАЦИЯ
        "AT+CREG",  # Статус регистрации в сети (0=нет, 1=домашняя, 5=роуминг)
        "AT+CGREG",  # Статус GPRS/PS регистрации
        "AT+CEREG",  # Статус EPS (LTE) регистрации

        # =========================================================================
        # УРОВЕНЬ СИГНАЛА И КАЧЕСТВО
        "AT+CSQ",  # RSSI (0-31) и BER (качество канала)
        "AT+CESQ",  # Расширенный запрос качества (RSSI, RSCP, ECN0, RSRP, RSRQ)

        # =========================================================================
        # ТЕКУЩАЯ СОТА И ЧАСТОТА
        "AT*CNTI",  # Информация о текущей соте (MCC, MNC, LAC, CellID, band, ARFCN)

        # попытка 2
        "AT*CPSI?",     # (часто работает на SIMCom для LTE, возвращает "LTE, TAC, CellID")
        "AT*CNETSCAN", # (может сработать).
        "AT+CRUSET",   # (просмотр текущих настроек сети).
        # "AT+CNETSCAN",   # Это заставит модем поискать другие вышки вокруг
        # "AT+CNETSCAN?",   # Это заставит модем поискать другие вышки вокруг

        # =========================================================================
        # ТЕХНОЛОГИЯ РАДИОДОСТУПА (RAT)
        "AT+WS46",  # Выбор технологии: 12=LTE, 2=3G, 0=2G/GERAN
        # "AT+COPS=3,2; +COPS?",  # (повтор для получения RAT в числовом виде)

        # =========================================================================
        # PDP / APN / ДАННЫЕ
        "AT+CGDCONT",  # Список APN-профилей (apn, type, ip...)
        "AT+CGCONTRDP",  # Параметры активного PDP-контекста (IP, шлюз, DNS1, DNS2)

        "AT+CGPADDR",  # Список назначенных PDP-адресов (IP)            # вероятно блокирует все остальное! все перестает отвечать!
        "AT+CGACT",  # Статус активации PDP-контекстов (0/1)
        "AT+CGATT",  # Статус GPRS-присоединения (attached/detached)
        # "AT+CGDATA=\"PPP\"",  # Состояние data-вызова (idle/active)
        "AT+CGDATA",  #

        # =========================================================================
        # IMS (VoLTE / VoWiFi)
        "AT+CIMS",  # Статус IMS-регистрации (0=не зарегистрирован, 1=зарегистрирован)
        "AT+CIREG",  # IMS регистрация (более детально)

        # =========================================================================
        # РЕЖИМЫ ЭНЕРГОСБЕРЕЖЕНИЯ И ФУНКЦИОНАЛЬНОСТЬ
        "AT+CFUN",  # Уровень функциональности (0=min, 1=full, 4=flight mode)
        "AT+CSCLK",  # Режим сна (1=разрешён sleep mode)

        # =========================================================================
        # ТЕМПЕРАТУРА И ПИТАНИЕ
        "AT+CPMUTEMP",  # Температура модуля (если поддерживается)
        "AT+CBC",  # Заряд батареи/питание (charge level, voltage)

        # =========================================================================
        # СОСЕДНИЕ СОТЫ (опционально, зависит от модуля)
        "AT+CCED",  # Соседние соты (GSM/GPRS)
        "AT*CELLINFO",  # Расширенная информация о сотах (vendor-specific)

        # =========================================================================
        # ОШИБКИ И СБРОСЫ (диагностика)
        "AT+CEER",  # Extended Error Report — причина последнего сбоя/разъединения
        # "AT+CRESET",  # перезагрузка модуля - не использовать!

        # =========================================================================
        # разное
        "AT+GCAP",
    ]

    COMPILE_EOF__STR = re.compile(r".+@.+:.*#\s*")

    def __init__(self, conn: ClientBase):
        """
        REASON (refactor note)
        -----------------------
        Раньше было `conn: ClientSerial` - типизация по конкретному транспорту,
        хотя Harvest использует только протокольные методы (write_read_bytes,
        write_read_text, send__ctrl_c, occupy, ADDRESS, conn как контекстный
        менеджер и т.п.), которые одинаково доступны что через Serial, что
        через SSH. Теперь conn типизирован по интерфейсу ClientBase, поэтому
        Harvest можно передать любой ClientBase независимо от транспорта:

            harvest_over_serial = Harvest(ClientSerial(address="COM16", baudrate=115200))
            harvest_over_ssh    = Harvest(SshClient(address="192.168.0.100", username="root", password="1"))

        Сам класс Harvest при этом не поменялся ни на строчку ниже.
        """
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

        ПОЛНЫЙ ЛОГ ЗАГРУЗКИ

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
        if not output or output.splitlines()[-1] != self.stopline_prompt__eq:
            self.conn.send__ctrl_c()
            # SLEEP
            # 0.2=serial-OK, ssh-NOT GOOD but so-so
            # 0.3=serial-OK, SSH-good!!!
            time.sleep(0.3)

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
[15:32:13.332989]COM16.stop_line[OK]= b'' [extra=EqValid_Regexp(v_args=(b'.*root@.+:.+#.*',)/v_kwargs={}/_cumulate_mode=<EnumAdj_BoolCumulate.ALL_TRUE: <built-in function all>>/_other_resolve=True)]
[15:32:13.332989]COM16.readNoEOL[OK]= b'\x1b[?2004hroot@harvest05:~# '
[COM16.WRITEREAD]
	write=[printf '%s' 'IyA9PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09CiMgc2NyX19yZmlkX3NjYW4ucHkgLSDQktCV0KDQodCY0K8g0KEg0J/QoNCv0JzQq9CcINCY0JfQktCb0JXQp9CV0J3QmNCV0JwgRVBDCiMgPT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PQppbXBvcnQgc2VyaWFsLCB0aW1lLCBzeXMsIHJlCgpQT1JUID0gJy9kZXYvdHR5UzInCkJBVUQgPSAxMTUyMDAKVElNRU9VVCA9IDAuNQoKIyBSRUFEIEJBTksKQ01EID0gYnl0ZXMoWzB4QTAsIDB4MEEsIDB4MDEsIDB4ODEsIDB4MDEsIDB4MDAsIDB4MDgsIDB4MDAsIDB4MDAsIDB4MDAsIDB4MDAsIDB4Q0JdKQoKCmRlZiByZWFkX3Jlc3BvbnNlKCkgLT4gYnl0ZXM6CiAgICBzZXIgPSBzZXJpYWwuU2VyaWFsKFBPUlQsIEJBVUQsIHRpbWVvdXQ9VElNRU9VVCkKICAgIHNlci5yZXNldF9pbnB1dF9idWZmZXIoKQogICAgc2VyLndyaXRlKENNRCkKCiAgICByZXNwb25zZSA9IGIiIgogICAgc3RhcnQgPSB0aW1lLnRpbWUoKQogICAgd2hpbGUgdGltZS50aW1lKCkgLSBzdGFydCA8IDEuMDoKICAgICAgICBjaHVuayA9IHNlci5yZWFkKHNlci5pbl93YWl0aW5nIG9yIDEpCiAgICAgICAgaWYgY2h1bms6CiAgICAgICAgICAgIHJlc3BvbnNlICs9IGNodW5rCiAgICAgICAgZWxzZToKICAgICAgICAgICAgdGltZS5zbGVlcCgwLjA1KQogICAgc2VyLmNsb3NlKCkKICAgIHJldHVybiByZXNwb25zZQoKCmRlZiBwYXJzZV9lcGMoZGF0YSk6CiAgICBlcGNfbGlzdCA9IFtdCiAgICBpID0gMAoKICAgIHdoaWxlIGkgPCBsZW4oZGF0YSk6CiAgICAgICAgIyDQmNGJ0LXQvCDQvdCw0YfQsNC70L4g0L/QsNC60LXRgtCwIDB4QTAKICAgICAgICBpZiBkYXRhW2ldICE9IDB4QTA6CiAgICAgICAgICAgIGkgKz0gMQogICAgICAgICAgICBjb250aW51ZQoKICAgICAgICBpZiBpICsgMSA+PSBsZW4oZGF0YSk6CiAgICAgICAgICAgIGJyZWFrCgogICAgICAgIGxlbmd0aCA9IGRhdGFbaSArIDFdCiAgICAgICAgaWYgaSArIGxlbmd0aCArIDEgPiBsZW4oZGF0YSk6CiAgICAgICAgICAgIGkgKz0gMQogICAgICAgICAgICBjb250aW51ZQoKICAgICAgICBwYWNrZXQgPSBkYXRhW2k6aSArIGxlbmd0aCArIDFdCiAgICAgICAgaSArPSBsZW5ndGggKyAxCgogICAgICAgICMg0J/RgNC+0LLQtdGA0Y/QtdC8INGC0LjQvyDQv9Cw0LrQtdGC0LAgKDB4MDEgMHg4MSAtINC40L3QstC10L3RgtCw0YDQuNC30LDRhtC40Y8pCiAgICAgICAgaWYgbGVuKHBhY2tldCkgPCA2IG9yIHBhY2tldFsyXSAhPSAweDAxIG9yIHBhY2tldFszXSAhPSAweDgxOgogICAgICAgICAgICBjb250aW51ZQoKICAgICAgICAjINCY0YnQtdC8IEVQQyDQtNCw0L3QvdGL0LUKICAgICAgICAjINCe0LHRi9GH0L3QviBFUEMg0L3QsNGH0LjQvdCw0LXRgtGB0Y8g0L/QvtGB0LvQtSDQt9Cw0LPQvtC70L7QstC60LAgKNC/0YDQuNC80LXRgNC90L4g0YEgNy3Qs9C+INCx0LDQudGC0LApCiAgICAgICAgIyDQmNGJ0LXQvCDQv9C+0YHQu9C10LTQvtCy0LDRgtC10LvRjNC90L7RgdGC0LgsINC60L7RgtC+0YDRi9C1INC90LDRh9C40L3QsNGO0YLRgdGPINGBIDB4MzAg0LjQu9C4IDB4MzQgKNGF0LDRgNCw0LrRgtC10YDQvdC+INC00LvRjyBFUEMpCiAgICAgICAgZm9yIGogaW4gcmFuZ2UoNSwgbGVuKHBhY2tldCkpOgogICAgICAgICAgICAjINCf0YDQvtC/0YPRgdC60LDQtdC8INC+0LTQuNC90L7Rh9C90YvQtSDQsdCw0LnRgtGLINC4INC40YnQtdC8INC90LDRh9Cw0LvQviBFUEMKICAgICAgICAgICAgaWYgcGFja2V0W2pdIGluICgweDMwLCAweDM0KTogICMg0KXQsNGA0LDQutGC0LXRgNC90L7QtSDQvdCw0YfQsNC70L4gRVBDCiAgICAgICAgICAgICAgICAjINCf0YDQvtCy0LXRgNGP0LXQvCwg0YfRgtC+INC00LDQu9GM0YjQtSDQuNC00YPRgiDQtNCw0L3QvdGL0LUKICAgICAgICAgICAgICAgIHJlbWFpbmluZyA9IGxlbihwYWNrZXQpIC0gagogICAgICAgICAgICAgICAgaWYgcmVtYWluaW5nID49IDE0OiAgIyDQnNC40L3QuNC80YPQvCAxNCDQsdCw0LnRgiDQtNC70Y8g0L/QvtC70L3QvtCz0L4gRVBDCiAgICAgICAgICAgICAgICAgICAgIyDQmNC30LLQu9C10LrQsNC10Lwg0LTQviAyMCDQsdCw0LnRgiAoNDAgaGV4INGB0LjQvNCy0L7Qu9C+0LIpCiAgICAgICAgICAgICAgICAgICAgZXBjX2J5dGVzID0gcGFja2V0W2o6aiArIG1pbigyMCwgcmVtYWluaW5nKV0KCiAgICAgICAgICAgICAgICAgICAgIyDQpNC40LvRjNGC0YDRg9C10LwgLSDQvtGB0YLQsNCy0LvRj9C10Lwg0YLQvtC70YzQutC+IGhleC3RgdC40LzQstC+0LvRiwogICAgICAgICAgICAgICAgICAgIGhleF9zdHIgPSAnJwogICAgICAgICAgICAgICAgICAgIGZvciBiIGluIGVwY19ieXRlczoKICAgICAgICAgICAgICAgICAgICAgICAgaGV4X3N0ciArPSBmJ3tiOjAyWH0nCgogICAgICAgICAgICAgICAgICAgICMg0J/RgNC+0LLQtdGA0Y/QtdC8LCDRh9GC0L4g0YHRgtGA0L7QutCwINC/0L7RhdC+0LbQsCDQvdCwIEVQQyAo0L3QsNGH0LjQvdCw0LXRgtGB0Y8g0YEgMzAvMzQg0Lgg0LTQvtGB0YLQsNGC0L7Rh9C90L7QuSDQtNC70LjQvdGLKQogICAgICAgICAgICAgICAgICAgIGlmIGxlbihoZXhfc3RyKSA+PSAyMDogICMg0JzQuNC90LjQvNGD0LwgMTAg0LHQsNC50YIgPSAyMCDRgdC40LzQstC+0LvQvtCyCiAgICAgICAgICAgICAgICAgICAgICAgICMg0J7QsdGA0LXQt9Cw0LXQvCDQtNC+INGA0LDQt9GD0LzQvdC+0Lkg0LTQu9C40L3RiyAoMjAtMjgg0YHQuNC80LLQvtC70L7QsikKICAgICAgICAgICAgICAgICAgICAgICAgZm9yIGN1dF9sZW4gaW4gWzI4LCAyNiwgMjQsIDIyLCAyMF06CiAgICAgICAgICAgICAgICAgICAgICAgICAgICBjYW5kaWRhdGUgPSBoZXhfc3RyWzpjdXRfbGVuXQogICAgICAgICAgICAgICAgICAgICAgICAgICAgaWYgY2FuZGlkYXRlLnN0YXJ0c3dpdGgoKCczMCcsICczNCcpKSBhbmQgY2FuZGlkYXRlIG5vdCBpbiBlcGNfbGlzdDoKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBlcGNfbGlzdC5hcHBlbmQoY2FuZGlkYXRlKQogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIGJyZWFrCiAgICAgICAgICAgICAgICAgICAgYnJlYWsKCiAgICByZXR1cm4gZXBjX2xpc3QKCgpkZWYgcGFyc2VfZXBjX2FkdmFuY2VkKGRhdGEpOgogICAgIyDQo9C70YPRh9GI0LXQvdC90YvQuSDQv9Cw0YDRgdC10YAgRVBDCiAgICBlcGNfbGlzdCA9IFtdCiAgICBoZXhfZGF0YSA9IGRhdGEuaGV4KCkudXBwZXIoKQoKICAgICMg0JjRidC10LwgRVBDINC/0L4g0YXQsNGA0LDQutGC0LXRgNC90YvQvCDQv9GA0LjQt9C90LDQutCw0Lw6CiAgICAjIDEuINCd0LDRh9C40L3QsNGO0YLRgdGPINGBIDMwMDAsIDMwMEUsIDM0MDAKICAgICMgMi4g0JjQvNC10Y7RgiDQtNC70LjQvdGDIDIwLTI4INGB0LjQvNCy0L7Qu9C+0LIKICAgIHBhdHRlcm5zID0gWwogICAgICAgIHInKDMwMDBbMC05QS1GXXsxNiwyNH0pJywgICMgMzAwMCArIDE2LTI0IGhleCDRgdC40LzQstC+0LvQvtCyCiAgICAgICAgcicoMzAwRVswLTlBLUZdezE2LDI0fSknLCAgIyAzMDBFICsgMTYtMjQgaGV4INGB0LjQvNCy0L7Qu9C+0LIKICAgICAgICByJygzNDAwWzAtOUEtRl17MTYsMjR9KScsICAjIDM0MDAgKyAxNi0yNCBoZXgg0YHQuNC80LLQvtC70L7QsgogICAgXQoKICAgIGZvciBwYXR0ZXJuIGluIHBhdHRlcm5zOgogICAgICAgIG1hdGNoZXMgPSByZS5maW5kYWxsKHBhdHRlcm4sIGhleF9kYXRhKQogICAgICAgIGZvciBtYXRjaCBpbiBtYXRjaGVzOgogICAgICAgICAgICAjINCe0YHRgtCw0LLQu9GP0LXQvCDRgtC+0LvRjNC60L4g0L/QvtC70L3Ri9C1IEVQQyAo0L7QsdGL0YfQvdC+IDI0LTI4INGB0LjQvNCy0L7Qu9C+0LIpCiAgICAgICAgICAgIGlmIGxlbihtYXRjaCkgPj0gMjQ6CiAgICAgICAgICAgICAgICAjINCe0LHRgNC10LfQsNC10Lwg0LTQviDRgdGC0LDQvdC00LDRgNGC0L3QvtC5INC00LvQuNC90Ysg0LXRgdC70Lgg0L3Rg9C20L3QvgogICAgICAgICAgICAgICAgaWYgbGVuKG1hdGNoKSA+IDI4OgogICAgICAgICAgICAgICAgICAgIG1hdGNoID0gbWF0Y2hbOjI4XQogICAgICAgICAgICAgICAgaWYgbWF0Y2ggbm90IGluIGVwY19saXN0OgogICAgICAgICAgICAgICAgICAgIGVwY19saXN0LmFwcGVuZChtYXRjaCkKCiAgICAjINCV0YHQu9C4INC90LUg0L3QsNGI0LvQuCAtINC/0YDQvtCx0YPQtdC8INC90LDQudGC0Lgg0LvRjtCx0YvQtSDQtNC70LjQvdC90YvQtSBoZXgt0YHRgtGA0L7QutC4CiAgICBpZiBub3QgZXBjX2xpc3Q6CiAgICAgICAgbG9uZ19oZXggPSByZS5maW5kYWxsKHInKFswLTlBLUZdezI0LDI4fSknLCBoZXhfZGF0YSkKICAgICAgICBmb3IgY2FuZGlkYXRlIGluIGxvbmdfaGV4OgogICAgICAgICAgICBpZiBjYW5kaWRhdGUuc3RhcnRzd2l0aCgoJzMwJywgJzM0JykpIGFuZCBjYW5kaWRhdGUgbm90IGluIGVwY19saXN0OgogICAgICAgICAgICAgICAgZXBjX2xpc3QuYXBwZW5kKGNhbmRpZGF0ZSkKCiAgICByZXR1cm4gZXBjX2xpc3QKCgojID09PSBNQUlOID09PQppZiBfX25hbWVfXyA9PSAiX19tYWluX18iOgogICAgZGF0YSA9IHJlYWRfcmVzcG9uc2UoKQoKICAgICMg0J7RgtC70LDQtNC60LA6INC/0L7QutCw0LbQtdC8INGB0YvRgNGL0LUg0LTQsNC90L3Ri9C1CiAgICBwcmludChmIlJhd0RhdGEoe2xlbihkYXRhKX1ieXRlcyk6W3tkYXRhLmhleCgpLnVwcGVyKCl9XSIsIGZpbGU9c3lzLnN0ZGVycikKCiAgICB0YWdzID0gcGFyc2VfZXBjX2FkdmFuY2VkKGRhdGEpCgogICAgZm9yIGVwYyBpbiB0YWdzOgogICAgICAgIHByaW50KGVwYykKCiAgICBwcmludChmImZvdW5kPXtsZW4odGFncyl9ZXBjIikKICAgIHN5cy5leGl0KDAgaWYgdGFncyBlbHNlIDEpCgo=' | base64 -d > scr__rfid_scan.py 2>/dev/null || echo ERROR_MSG]
	read=[[33]-  Exit 124                timeout 2.0 cat /dev/ttyUSB2]
output='[33]-  Exit 124                timeout 2.0 cat /dev/ttyUSB2'
PASSED

[14:02:08.095470]COM3.readEOL[OK]= b'[1]+  Done                    timeout 2.0 cat /dev/ttyUSB2'
        """
        # === ЗАЩИТА ОТ ПУСТОГО ОТВЕТА ===
        if not data:
            return ""

        # 0=split -----------------------
        lines = data.splitlines()

        # 1=CMD ECHO --------------------
        if lines[0].strip() == cmd.strip():
            lines = lines[1:]

        # 2=EOF -------------------------
        while lines and (self.COMPILE_EOF__STR.match(lines[-1]) or lines[-1].strip() == ''):
            lines = lines[:-1]

        # =======FILTERS - OLD
        # 3=SERVICE LOGS ----------------
        # AT": "[1]   Terminated              timeout 2.0 cat /dev/ttyUSB2\nOK"
        # [AT] AT+CSQ ---> output='[4] 1836\n[3]   Exit 124                timeout 2.0 cat /dev/ttyUSB2\n+CSQ: 20,99\nOK'
        # Удаляем служебные строки bash о статусе фоновых процессов
        lines_filtered = [
            line for line in lines
            if not (
                    re.match(r'\s*\[\d+\]\s+(?:Exit|Terminated|Done)?\s*\d*\s*', line)
                    or
                    re.match(r'\s*\[\d+\]-?\s+(?:Exit|Terminated|Done)?\s*\d*\s*.*', line)
                    # re.match(r'\s*\[\d+\][+-]?\s+(?:Exit|Terminated|Done)?\s*\d*\s*.*', line)
            )
        ]

        # =======FILTERS - NEW
        # lines_filtered = []
        # for line in lines:
        #     # 3=SERVICE LOGS ----------------
        #     # AT": "[1]   Terminated              timeout 2.0 cat /dev/ttyUSB2\nOK"
        #     # [AT] AT+CSQ ---> output='[4] 1836\n[3]   Exit 124                timeout 2.0 cat /dev/ttyUSB2\n+CSQ: 20,99\nOK'
        #     # Удаляем служебные строки bash о статусе фоновых процессов
        #     if (
        #             re.match(r'\s*\[\d+\]\s+(?:Exit|Terminated|Done)?\s*\d*\s*', line)
        #             or
        #             re.match(r'\s*\[\d+\]-?\s+(?:Exit|Terminated|Done)?\s*\d*\s*.*', line)
        #             # re.match(r'\s*\[\d+\][+-]?\s+(?:Exit|Terminated|Done)?\s*\d*\s*.*', line)
        #     ):
        #         continue
        #
        #     # 4=prompt ----------------
        #     if self.stopline_prompt__eq == line:
        #         continue
        #
        #     lines_filtered.append(line)

        # 4=EXIT ------------------------
        lines = lines_filtered
        return "\n".join(lines)

    # ------------------------------------------------------------------------------------------------------------------
    def cmd_timeout__write_read__payload(
            self,
            cmd: str,
            timeout_continue: float = 2.0,  # ОБЯЗАТЕЛЬНО!!! лучше больше сделать потому что есть корректный STOPLINE!
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
    #     output = self.cmd_timeout__write_read__payload_str(full_cmd, timeout=timeout * 2)
    #     # Убираем возможное эхо команды
    #     output = output.replace(cmd + "\n", "")
    #     print(f"[{output=}]")
    #     return output
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
    #     output = self.cmd_timeout__write_read__payload_str(
    #         full_cmd,
    #         timeout=None,
    #         timeout_continue=timeout * 1.5
    #     )
    #     # Убираем пустые строки и возможное эхо (если echo не выключено)
    #     lines = [line.strip() for line in output.split('\n') if line.strip()]
    #     # Отфильтровываем саму команду, если echo ещё активно
    #     lines = [line for line in lines if line != cmd]
    #     output = '\n'.join(lines)
    #     print(f"[SIMPLE_AT] {output=}")
    #     return output

    def at_cmd__simple(
            self,
            cmd: str,
            port: str = "/dev/ttyUSB2",
            timeout: float = 5.0,
            timeout_continue: float = 2,
    ) -> str:
        """
        Отправить AT-команду на уже настроенный порт (stty raw + echo off).

        ClientSerial(COM16.115200,occupied=o,isopen=True){'write': b"timeout 2 cat /dev/ttyUSB2 & sleep 0.1; printf 'AT+COPS?\\r\\n' > /dev/ttyUSB2; sleep 0.4; kill %1 2>/dev/null\r\n"}
        ClientSerial(COM16.115200,occupied=o,isopen=True)READ(
            bytes=b'timeout 2 cat /dev/ttyUSB2 & sleep 0.1; printf \'AT+COPS?\\r\\n\' > /dev/ttyUSB2; sleep 0.4; kill %1 2>/dev/null\r\n\x1b[?2004l\r[6] 5353\r\n[5]   Exit 124                timeout 2 cat /dev/ttyUSB2\r\n\r\r\n+COPS: 0,2,"25020",7\r\r\n\r\r\nOK\r\r\n\x1b[?2004hroot@harvest05:~# \r\n\x1b[?2004l\r\x1b[?2004hroot@harvest05:~# '
            printable=timeout 2 cat /dev/ttyUSB2 & sleep 0.1; printf 'AT+COPS?\r\n' > /dev/ttyUSB2; sleep 0.4; kill %1 2>/dev/null
        [6] 5353
        [5]   Exit 124                timeout 2 cat /dev/ttyUSB2

        root@harvest05:~#
        root@harvest05:~# )
        [AT] AT+COPS? -> output='+COPS: 0,2,"25020",7\nOK'
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
        [AT] AT ---> output=''
        FAILED
        """
        # Увеличиваем задержку для медленных команд
        sleep_after_write = 1 if '=' in cmd else 0.6  # для запроса диапазона нужно больше времени 0.6 as first attempt

        cmd_full = (
            f"cat {port} & sleep 0.1; "
            f"printf '{cmd}\\r\\n' > {port}; "
            f"sleep {sleep_after_write}; "
            f"kill %1 2>/dev/null"
        )

        # Добавляем повторную попытку при пустом ответе
        output = None
        for attempt in range(2):
            output = self.cmd_timeout__write_read__payload(
                cmd=cmd_full,
                timeout=timeout,
                timeout_continue=timeout_continue or timeout * 0.8,
            )

            # Если получили ответ - выходим
            if output.strip():
                break

            # Если ответ пустой - ждем и пробуем снова
            if attempt == 0:
                print(f"[AT] Пустой ответ на {cmd}, повторная попытка...")
                time.sleep(0.5)

        print(f"[AT]{cmd}--->[{output!r}]")
        return output

    def at_cmd__raw(    # NOTE: DONT USE!
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

        ClientSerial(COM16.115200,occupied=harvest05,isopen=True){'write': b"timeout 2 python3 /tmp/at_client.py 'AT+CSQ' /dev/ttyUSB2 115200\r\n"}
        ClientSerial(COM16.115200,occupied=harvest05,isopen=True)READ(
            bytes=b"timeout 2 python3 /tmp/at_client.py 'AT+CSQ' /dev/ttyUSB2 115200\r\n\x1b[?2004l\r\r\r\n+CSQ: 23,99\r\r\n\r\r\nOK\r\r\n\r\n\x1b[?2004hroot@harvest05:~# \r\n\x1b[?2004l\r\x1b[?2004hroot@harvest05:~# "
            printable=timeout 2 python3 /tmp/at_client.py 'AT+CSQ' /dev/ttyUSB2 115200
        root@harvest05:~#
        root@harvest05:~# )
        [output='+CSQ: 23,99\nOK']
        """
        cmd = f"python3 {bridge} '{cmd}' {port} {baudrate}"
        output = ""
        for _ in range(2):

            output = self.cmd_timeout__write_read__payload(
                cmd,
                stop_line=stop_line,
                timeout=timeout,
                timeout_continue=timeout_continue,
                **read_kwargs
            )
            # Убираем возможное эхо команды
            if output.startswith(cmd + "\n"):
                output = output.replace(cmd + "\n", "", 1)

            if "No such file or directory" in output:
                if not self.file_name__push(bridge):
                    break

        print(f"[AT]{cmd}--->[{output!r}]")
        return output

    # AT DUMP ==========================================================================================================
    def at_cmd__dump(
            self,
            port: str = '/dev/ttyUSB2',
            method_simple: bool = True,
            timeout: float = 2.0,
            timeout_continue: float | None = None,
            cmds: Iterable[str] | None = None,
            return_sequence: bool | None = None,
    ) -> dict[str, str] | list[tuple[str, str]]:
        """
        Опрашивает AT-команды из AT_CMDS__FLAT
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
        # FIXME: ПЕРЕДЕЛАТЬ на полный дамп!!!
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

        ERROR (ожидаемо для этого модуля - новый модуль со старыми командами):
        Ваш модуль (SIMCom A7682E) — это современный LTE-модуль.
        В сетях 4G (LTE) команды вроде AT+CCED или AT*CELLINFO
        (которые были популярны на старых 2G/3G модемах) практически не работают или отключены прошивкой.

        AT+CPINR — не поддерживает доп. информацию по PIN/PUK
        AT+CCID — видимо не реализован (можно попробовать AT+ICCID)
        AT*CNTI=0 — vendor-specific, не поддерживается
        AT+CGDATA="PPP" — режим не активен
        AT+CIMS?, AT+CIREG? — IMS не поддерживается
        AT+CPMUTEMP? — нет датчика температуры
        AT+CCED?, AT*CELLINFO? — нет расширенной инфы по сотам
        """
        result = []
        method_send = self.at_cmd__simple if method_simple else self.at_cmd__raw

        if cmds is None:
            cmds = self.AT_CMDS__FLAT

        for cmd in cmds:
            try:
                resp = method_send(cmd, port=port, timeout=timeout, timeout_continue=timeout_continue)
                result.append((cmd, resp.strip()))
            except Exception as exc:
                result.append((cmd, f"PYERROR:{exc!r}"))

        if return_sequence:
            return result
        else:
            return dict(result)

    # ------------------------------------------------------------------------------------------------------------------
    def at_cmd__dump_sequence(self, *args, **kwargs) -> list[tuple[str, str]]:
        try:
            kwargs.pop("return_sequence")
        except:
            pass
        return self.at_cmd__dump(*args, return_sequence=True, **kwargs)

    def at_cmd__dump_dict(self, *args, **kwargs) -> dict[str, str]:
        try:
            kwargs.pop("return_sequence")
        except:
            pass
        return self.at_cmd__dump(*args, return_sequence=False, **kwargs)

    # AT 0=EXPLORE =======================================================================================================
    @staticmethod
    def at_param__parse_variants(response: str, max_count: int | None = 10) -> list[str]:
        """
        ВАРИАНТЫ
            1=RANGES
                ('AT+CGATT=?', '+CGATT: (0-1)\nOK')
                ('AT+CGACT=?', '+CGACT: (0,1)\nOK')
                ('AT+CFUN=?', '+CFUN: (0-1,4-8),(0-1)\nOK')

                ('AT+CGDATA=?', '+CGDATA: ("")\nOK')
                ('AT+CIMS=?', 'ERROR')

                [AT]AT+CPBR=?--->+CPBR: (1-100),20,28\nOK
            2=VALUES
            	('AT+CPBS=?', '+CPBS: ("SM","FD","ON","AP")\nOK')
        """
        result: list[str] = []

        # 1=INTS -----------------------------
        int_diaps_final: list[str] = []

        int_diaps_pretend: list[str] = re.findall(r"\(([ 0-9,-]+)\)", response)
        if int_diaps_pretend:
            for diap in int_diaps_pretend:
                int_diaps_final.extend(diap.split(","))

            ints_final: set[int] = set()
            for subdiap in int_diaps_final:
                if "-" in subdiap:
                    nodes = subdiap.split("-")
                    if len(nodes) > 2:
                        nodes = [nodes[0], nodes[-1]]

                    if len(nodes) == 2:
                        try:
                            start, finish = nodes
                            start = int(start.strip())
                            finish = int(finish.strip())
                            for value in range(start, finish+1):
                                ints_final.add(value)
                        except:
                            continue
                else:
                    value = int(subdiap.strip())
                    ints_final.add(value)

            result.extend(map(str, sorted(ints_final)))

        # 2=STR -----------------------------
        str_values: list[str] = re.findall(r'"([^"]+)"', response)
        for value in str_values:
            if value not in result:
                result.append(value)

        # FINAL=slice -------------
        if max_count:
            return result[:max_count]
        else:
            return result

    # ------------------------------------------------------------------------------------------------------------------
    def at_cmd__explore(
            self,
            cmd: str,

            port: str = '/dev/ttyUSB2',
            timeout: float = 5.0,                   # best 2!
            timeout_continue: float | None = 3,     # best 1!
    ) -> list[tuple[str, str]]:
        """
        result = re.search(r"\(0-(\d+)\)", "+CREG: (0-2)\nOK")
        print(result)
        print(result.group(1))
        """
        result = []
        cmds_pretend = []

        cmd_clear = f"{cmd.upper()}".rstrip("=?")

        # 1=EDGES DETECT -----------------
        # "AT+CREG=?" ---> "+CREG: (0-2)\nOK"
        cmd_edges = f"{cmd_clear}=?"
        response = self.at_cmd__simple(cmd=cmd_edges, port=port, timeout=timeout, timeout_continue=timeout_continue)
        result.append((cmd_edges, response))

        # 2=CREATE CMDS LIST-------------
        # direct
        cmds_pretend.append(f"{cmd_clear}")
        cmds_pretend.append(f"{cmd_clear}?")

        # changes
        for value in self.at_param__parse_variants(response) or []:
            cmds_pretend.append(f"{cmd_clear}={value}")
            cmds_pretend.append(f"{cmd_clear}?")

        # 3=FINAL -----------------------
        result.extend(self.at_cmd__dump_sequence(cmds=cmds_pretend, port=port, timeout=timeout, timeout_continue=timeout_continue))
        for line in result or []:
            print(f"\t{line}")
        return result

    def at_cmds__explore(
            self,
            cmds: Iterable[str] | dict,
            **kwargs,
    ) -> dict[str, list[tuple[str, str]]]:
        result = {}

        count = len(cmds)
        # ----------------------------------
        for index, cmd in enumerate(cmds):
            print(f"\n{index=}/{count=}")
            step = self.at_cmd__explore(cmd=cmd, **kwargs)
            result[cmd] = step

        # PRINTOUT -------------------------
        print(f"=========at_cmds__explore===========[")
        print("{")
        for cmd, values in result.items():
            try:
                description = cmds[cmd]      # VALUE is available
                if not isinstance(description, str):
                    description = description[0]
                    if not isinstance(description, str):
                        raise Exception("description is not exists")
                print(f"'{cmd}': ['{description}',")
            except:
                print(f"'{cmd}': [")

            for line in values or []:
                print(f"\t{line},")
            print("],")
        print("}")
        print(f"=========at_cmds__explore===========]")

        # PRINTOUT -------------------------
        return result

    # CMDS =============================================================================================================
    def prepare__echo_off(self) -> bool:
        """
        GOAL
        disable echo for cmdline sent
        """
        result = self.cmd_timeout__check_executed_success(f'stty -echo')
        if not result:
            print("не удалось изменить режим логгирования сообщений ядра Linux в консоль")
        return result

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
        result = self.cmd_timeout__check_executed_success(f'dmesg -n 3')
        if not result:
            print("не удалось изменить режим логгирования сообщений ядра Linux в консоль")
        return result

    def prepare__services(self, start: bool | None = True) -> bool:
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
            "ModemManager",  #
            "harvester.service",  # не будет работать BTUS! не соединится
            "urozhai",  # вроде без него все работает! но просто так за компанию! потому что был в инструкции!
        ]:
            process = "start" if start else "stop"
            result &= self.cmd_timeout__check_executed_success(f"systemctl {process} {service}")
        return result

    # ------------------------------------------------------------------------------------------------------------------
    def apt_install(self, module: str, timeout_continue: float = 5, **wr_kwargs) -> bool:
        """
        if need DELETE
            sudo apt remove picocom
        """
        result = self.cmd_timeout__check_executed_success(f"apt install -y {module}", timeout_continue=timeout_continue,
                                                          **wr_kwargs)
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


        ЧЕРЕЗ ДРУГОЙ ИНТЕРФЕЙС
        ---- Sent utf8 encoded message: "ifconfig\r\n" ----
        ifconfig
        lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
                inet 127.0.0.1  netmask 255.0.0.0
                inet6 ::1  prefixlen 128  scopeid 0x10<host>
                loop  txqueuelen 1000  (Local Loopback)
                RX packets 10110  bytes 5066130 (4.8 MiB)
                RX errors 0  dropped 0  overruns 0  frame 0
                TX packets 10110  bytes 5066130 (4.8 MiB)
                TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

        usb0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
                inet 192.168.0.100  netmask 255.255.255.0  broadcast 192.168.0.255
                inet6 fe80::97a8:216f:d5f4:fd0  prefixlen 64  scopeid 0x20<link>
                ether 46:d1:74:50:fa:0f  txqueuelen 1000  (Ethernet)
                RX packets 237  bytes 11802 (11.5 KiB)
                RX errors 0  dropped 0  overruns 0  frame 0
                TX packets 554  bytes 53510 (52.2 KiB)
                TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

        wlan0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
                inet 192.168.137.57  netmask 255.255.255.0  broadcast 192.168.137.255
                inet6 fe80::eeca:37c1:3b57:2a47  prefixlen 64  scopeid 0x20<link>
                ether 54:78:c9:02:22:b0  txqueuelen 1000  (Ethernet)
                RX packets 8403  bytes 967076 (944.4 KiB)
                RX errors 0  dropped 0  overruns 0  frame 0
                TX packets 8937  bytes 5020645 (4.7 MiB)
                TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

        root@harvest05:~#

        ---- Sent utf8 encoded message: "ping -c 1 -W 1 -I wlan0 8.8.8.8\r\n" ----
ping -c 1 -W 1 -I wlan0 8.8.8.8
PING 8.8.8.8 (8.8.8.8) from 192.168.137.57 wlan0: 56(84) bytes of data.
64 bytes from 8.8.8.8: icmp_seq=1 ttl=101 time=173 ms

--- 8.8.8.8 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 172.762/172.762/172.762/0.000 ms
root@harvest05:~#
root@harvest05:~#
---- Sent utf8 encoded message: "ping -c 1 -W 1 -I usb0 8.8.8.8\r\n" ----
ping -c 1 -W 1 -I usb0 8.8.8.8
PING 8.8.8.8 (8.8.8.8) from 192.168.0.100 usb0: 56(84) bytes of data.

--- 8.8.8.8 ping statistics ---
1 packets transmitted, 0 received, 100% packet loss, time 0ms

root@harvest05:~#
        """
        return self.cmd_timeout__check_executed_success(
            "ping -c 1 -W 1 8.8.8.8",
            timeout=3,
            timeout_continue=2,
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
            mac = self.cmd_timeout__write_read__payload(f"cat /sys/class/net/{iface}/address 2>/dev/null",
                                                        timeout=3).strip()
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
            timeout=3,
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
            timeout=4,
            timeout_continue=0.5,
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
                    r"tty\d*",  # virtual tty
                    r"mmcblk.*", r"nbd.*", r"loop.*",  # блочные устройства
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
    def wf__link_connected(self) -> bool:
        """
        GOAL
        check

        ======================================================================
        2=вариант-2=ПРОВЕРКА через iw dev
        1=DISCONNECTED ------------------------------
        ---- Sent utf8 encoded message: "iw dev wlan0 link\r\n" ----
        iw dev wlan0 link
        Not connected.
        root@harvest05:~#

        2=CONNECTED ---------------------------------
        ---- Sent utf8 encoded message: "iw dev wlan0 link\r\n" ----
        iw dev wlan0 link
        Connected to e2:d0:45:fb:a2:34 (on wlan0)
                SSID: Vest
                freq: 2462
                RX: 342 bytes (2 packets)
                TX: 1506 bytes (10 packets)
                signal: -57 dBm
                rx bitrate: 1.0 MBit/s
                tx bitrate: 65.0 MBit/s

                bss flags:      short-preamble short-slot-time
                dtim period:    3
                beacon int:     100
        root@harvest05:~#

        3=WRONG name ---------------------------------
        ---- Sent utf8 encoded message: "iw dev wlan2 link\r\n" ----
        iw dev wlan2 link
        command failed: No such device (-19)

        ======================================================================
        2=вариант-2=ПРОВЕРКА через ifconfig - ОШИБОЧНО!!! НЕ ПРОВЕРЯТЬ ТАК!!!
        если нет DHCP - то будет некорректно!!!
        НЕТОЧНО!!! показывает inet6 даже при фактическом НЕПОДКЛЮЧЕНИИ!!!

        ---- Sent utf8 encoded message: "iw dev wlan0 link\r\n" ----
        iw dev wlan0 link
        Not connected.
        root@harvest05:~#
        root@harvest05:~#
        ---- Sent utf8 encoded message: "ifconfig wlan0\r\n" ----
        ifconfig wlan0
        wlan0: flags=4099<UP,BROADCAST,MULTICAST>  mtu 1500
                ether 72:d0:0f:2c:1e:2a  txqueuelen 1000  (Ethernet)
                RX packets 37  bytes 11877 (11.5 KiB)
                RX errors 0  dropped 0  overruns 0  frame 0
                TX packets 120  bytes 24512 (23.9 KiB)
                TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

        root@harvest05:~#

        1=DISCONNECTED ------------------------------
        ---- Sent utf8 encoded message: "ifconfig wlan0\r\n" ----
        ifconfig wlan0
        wlan0: flags=4099<UP,BROADCAST,MULTICAST>  mtu 1500
                ether 9a:cc:10:f7:34:46  txqueuelen 1000  (Ethernet)
                RX packets 0  bytes 0 (0.0 B)
                RX errors 0  dropped 0  overruns 0  frame 0
                TX packets 0  bytes 0 (0.0 B)
                TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

        root@harvest05:~#

        2=CONNECTED ---------------------------------
        2.1=БЕЗ DHCP=
        ---- Sent utf8 encoded message: "ifconfig wlan0\r\n" ----
        ifconfig wlan0
        wlan0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
                inet6 fe80::eeca:37c1:3b57:2a47  prefixlen 64  scopeid 0x20<link>
                ether 54:78:c9:02:22:b0  txqueuelen 1000  (Ethernet)
                RX packets 1  bytes 321 (321.0 B)
                RX errors 0  dropped 0  overruns 0  frame 0
                TX packets 10  bytes 1815 (1.7 KiB)
                TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

        root@harvest05:~#

        2.2=С DHCP
        ---- Sent utf8 encoded message: "ifconfig wlan0\r\n" ----
        ifconfig wlan0
        wlan0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
                inet 192.168.137.58  netmask 255.255.255.0  broadcast 192.168.137.255
                inet6 fe80::eeca:37c1:3b57:2a47  prefixlen 64  scopeid 0x20<link>
                ether 54:78:c9:02:22:b0  txqueuelen 1000  (Ethernet)
                RX packets 64  bytes 19652 (19.1 KiB)
                RX errors 0  dropped 0  overruns 0  frame 0
                TX packets 615  bytes 124217 (121.3 KiB)
                TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

        root@harvest05:~#
        """
        output = self.cmd_timeout__write_read__payload("iw dev wlan0 link")
        return "Connected to " in output

    def wf__scan(self, full: bool | None = None) -> list[str] | NoReturn:
        """
        PART
        ===============
        ---- Sent utf8 encoded message: "timeout 2 iw dev wlan0 scan | grep -E 'on wlan0|SSID|signal|freq'\r\n" ----
timeout 2 iw dev wlan0 scan | grep -E 'on wlan0|SSID|signal|freq'
BSS 9c:9d:7e:75:00:5b(on wlan0)
        freq: 2437
        signal: -62.00 dBm
        SSID: Element-T_lab
                 * SSID List
                 * center freq segment 1: 6
                 * center freq segment 2: 0
BSS d2:a4:6f:e6:fa:d2(on wlan0)
        freq: 2427
        signal: -73.00 dBm
        SSID: DIRECT-bQ-Pantum BM5100 Series
BSS d2:2c:4d:3a:5f:e2(on wlan0)
        freq: 2447
        signal: -79.00 dBm
        SSID: Galaxy Z Fold6 5073
                 * SSID List
                 * center freq segment 1: 0
                 * center freq segment 2: 0
BSS 78:45:58:3a:38:db(on wlan0)
        freq: 2412
        signal: -76.00 dBm
        SSID: Element-T
                 * SSID List
BSS 7e:45:58:3a:38:db(on wlan0)
        freq: 2412
        signal: -76.00 dBm
        SSID: Element_Guest
                 * SSID List
BSS 82:45:58:3a:38:db(on wlan0)
        freq: 2412
        signal: -75.00 dBm
        SSID: Element-t_2Gz
                 * SSID List
BSS cc:2d:e0:c2:7d:42(on wlan0)
        freq: 2447
        signal: -69.00 dBm
        SSID: MikroTik-C27D42
BSS c4:0a:cb:5c:d6:94(on wlan0)
        freq: 2412
        signal: -71.00 dBm
        SSID: Advanta_Work
BSS c4:0a:cb:5c:d6:93(on wlan0)
        freq: 2412
        signal: -83.00 dBm
        SSID: Advanta_Messages
BSS c4:0a:cb:5c:d6:95(on wlan0)
        freq: 2412
        signal: -68.00 dBm
        SSID: Advanta
BSS 86:45:58:3a:38:db(on wlan0)
        freq: 2412
        signal: -76.00 dBm
        SSID:
                 * SSID List
BSS 50:ff:20:a5:47:aa(on wlan0)
        freq: 2452
        signal: -80.00 dBm
        SSID: Keenetic-0831
                 * center freq segment 1: 9
                 * center freq segment 2: 0
root@harvest05:~#

        FULL
        ===============
        ---- Sent utf8 encoded message: "timeout 2 iw dev wlan0 scan\r\n" ----
timeout 2 iw dev wlan0 scan
BSS 9c:9d:7e:75:00:5b(on wlan0)
        last seen: 5363.234s [boottime]
        TSF: 0 usec (0d, 00:00:00)
        freq: 2437
        beacon interval: 100 TUs
        capability: ESS Privacy ShortPreamble ShortSlotTime (0x0431)
        signal: -60.00 dBm
        last seen: 5 ms ago
        SSID: Element-T_lab
        Supported rates: 1.0* 2.0* 5.5* 11.0* 6.0 9.0 12.0 18.0
        DS Parameter set: channel 6
        TIM: DTIM Count 0 DTIM Period 1 Bitmap Control 0x0 Bitmap[0] 0x0
        ERP: <no flags>
        Extended supported rates: 24.0 36.0 48.0 54.0
        HT capabilities:
                Capabilities: 0x9ad
                        RX LDPC
                        HT20
                        SM Power Save disabled
                        RX HT20 SGI
                        TX STBC
                        RX STBC 1-stream
                        Max AMSDU length: 7935 bytes
                        No DSSS/CCK HT40
                Maximum RX AMPDU length 65535 bytes (exponent: 0x003)
                Minimum RX AMPDU time spacing: No restriction (0x00)
                HT TX/RX MCS rate indexes supported: 0-15
        HT operation:
                 * primary channel: 6
                 * secondary channel offset: no secondary
                 * STA channel width: 20 MHz
                 * RIFS: 0
                 * HT protection: nonmember
                 * non-GF present: 0
                 * OBSS non-GF present: 0
                 * dual beacon: 0
                 * dual CTS protection: 0
                 * STBC beacon: 0
                 * L-SIG TXOP Prot: 0
                 * PCO active: 0
                 * PCO phase: 0
        Overlapping BSS scan params:
                 * passive dwell: 20 TUs
                 * active dwell: 10 TUs
                 * channel width trigger scan interval: 300 s
                 * scan passive total per channel: 200 TUs
                 * scan active total per channel: 20 TUs
                 * BSS width channel transition delay factor: 5
                 * OBSS Scan Activity Threshold: 0.25 %
        Extended capabilities:
                 * HT Information Exchange Supported
                 * Extended Channel Switching
                 * SSID List
                 * Operating Mode Notification
                 * Max Number Of MSDUs In A-MSDU is unlimited
        VHT capabilities:
                VHT Capabilities (0x33813992):
                        Max MPDU length: 11454
                        Supported Channel Width: neither 160 nor 80+80
                        RX LDPC
                        TX STBC
                        SU Beamformer
                        SU Beamformee
                        RX antenna pattern consistency
                        TX antenna pattern consistency
                VHT RX MCS set:
                        1 streams: MCS 0-9
                        2 streams: MCS 0-9
                        3 streams: not supported
                        4 streams: not supported
                        5 streams: not supported
                        6 streams: not supported
                        7 streams: not supported
                        8 streams: not supported
                VHT RX highest supported: 0 Mbps
                VHT TX MCS set:
                        1 streams: MCS 0-9
                        2 streams: MCS 0-9
                        3 streams: not supported
                        4 streams: not supported
                        5 streams: not supported
                        6 streams: not supported
                        7 streams: not supported
                        8 streams: not supported
                VHT TX highest supported: 0 Mbps
                VHT extended NSS: supported
        VHT operation:
                 * channel width: 0 (20 or 40 MHz)
                 * center freq segment 1: 6
                 * center freq segment 2: 0
                 * VHT basic MCS set: 0xfffc
        HE capabilities:
                HE MAC Capabilities (0x010d1a080040):
                        +HTC HE Supported
                        TWT Responder
                        Dynamic BA Fragementation Level: 1
                        Minimum Payload size of 128 bytes: 1
                        BSR
                        OM Control
                        Maximum A-MPDU Length Exponent: 3
                        A-MSDU in A-MPDU
                HE PHY Capabilities: (0x00600c891dc1831c010800):
                        LDPC Coding in Payload
                        HE SU PPDU with 1x HE-LTF and 0.8us GI
                        STBC Tx <= 80MHz
                        STBC Rx <= 80MHz
                        DCM Max Constellation: 1
                        DCM Max Constellation Rx: 1
                        SU Beamformer
                        SU Beamformee
                        Beamformee STS <= 80Mhz: 7
                        Sounding Dimensions <= 80Mhz: 1
                        Ng = 16 SU Feedback
                        Ng = 16 MU Feedback
                        Codebook Size SU Feedback
                        Codebook Size MU Feedback
                        PPE Threshold Present
                        HE SU PPDU & HE PPDU 4x HE-LTF 0.8us GI
                        Max NC: 3
                        HE ER SU PPDU 4x HE-LTF 0.8us GI
                        RX 1024-QAM
                PPE Threshold 0xfa 0xff 0xfa 0xff 0x19 0x1c 0xc7 0x71
        WMM:     * Parameter version 1
                 * u-APSD
                 * BE: CW 15-1023, AIFSN 3
                 * BK: CW 15-1023, AIFSN 7
                 * VI: CW 7-15, AIFSN 2, TXOP 3008 usec
                 * VO: CW 3-7, AIFSN 2, TXOP 1504 usec
        RSN:     * Version: 1
                 * Group cipher: CCMP
                 * Pairwise ciphers: CCMP
                 * Authentication suites: PSK
                 * Capabilities: 16-PTKSA-RC 1-GTKSA-RC (0x000c)
        WPS:     * Version: 1.0
                 * Wi-Fi Protected Setup State: 2 (Configured)
                 * Model: R3600
                 * Version2: 2.0
BSS d2:a4:6f:e6:fa:d2(on wlan0)
        last seen: 5363.234s [boottime]
        TSF: 0 usec (0d, 00:00:00)
        freq: 2427
        beacon interval: 100 TUs
        capability: ESS Privacy ShortSlotTime (0x0411)
        signal: -70.00 dBm
        last seen: 5 ms ago
        SSID: DIRECT-bQ-Pantum BM5100 Series
        Supported rates: 6.0* 9.0 12.0* 18.0 24.0* 36.0 48.0 54.0
        DS Parameter set: channel 4
        TIM: DTIM Count 0 DTIM Period 1 Bitmap Control 0x0 Bitmap[0] 0x0
        ERP: Barker_Preamble_Mode
        RSN:     * Version: 1
                 * Group cipher: CCMP
                 * Pairwise ciphers: CCMP
                 * Authentication suites: PSK
                 * Capabilities: 16-PTKSA-RC 1-GTKSA-RC (0x000c)
        HT capabilities:
                Capabilities: 0x92c
                        HT20
                        SM Power Save disabled
                        RX HT20 SGI
                        RX STBC 1-stream
                        Max AMSDU length: 7935 bytes
                        No DSSS/CCK HT40
                Maximum RX AMPDU length 65535 bytes (exponent: 0x003)
                Minimum RX AMPDU time spacing: 2 usec (0x04)
                HT Max RX data rate: 300 Mbps
                HT TX/RX MCS rate indexes supported: 0-15
        HT operation:
                 * primary channel: 4
                 * secondary channel offset: no secondary
                 * STA channel width: 20 MHz
                 * RIFS: 0
                 * HT protection: no
                 * non-GF present: 0
                 * OBSS non-GF present: 0
                 * dual beacon: 0
                 * dual CTS protection: 0
                 * STBC beacon: 0
                 * L-SIG TXOP Prot: 0
                 * PCO active: 0
                 * PCO phase: 0
        WMM:     * Parameter version 1
                 * u-APSD
                 * BE: CW 15-1023, AIFSN 3
                 * BK: CW 15-1023, AIFSN 7
                 * VI: CW 7-15, AIFSN 2, TXOP 2976 usec
                 * VO: CW 3-7, AIFSN 2, TXOP 1472 usec
        WPS:     * Version: 1.0
                 * Wi-Fi Protected Setup State: 2 (Configured)
                 * Response Type: 3 (AP)
                 * UUID: e2a12c59-9394-5d0b-90df-113e9b254e10
                 * Manufacturer: Pantum
                 * Model: BM5100ADW
                 * Model Number: BM5100ADW series
                 * Serial Number: CK1A028518
                 * Primary Device Type: 3-0050f204-5
                 * Device name: DIRECT-bQ-Pantum BM5100 Series
                 * Config methods:
                 * Version2: 2.0
        P2P:     * Group capa: 0x21, Device capa: 0x0b
                 * Unknown TLV (0x0d, 51 bytes): d2 a4 6f e6 fa d2 00 80 00 03 00 50 f2 04 00 05 00 10 11 00 1e 44 49 52 45 43 54 2d 62 51 2d 50 61 6e 74 75 6d 20 42 4d 35 31 30 30 20 53 65 72 69 65 73
BSS d2:2c:4d:3a:5f:e2(on wlan0)
        last seen: 5363.234s [boottime]
        TSF: 0 usec (0d, 00:00:00)
        freq: 2447
        beacon interval: 100 TUs
        capability: ESS Privacy ShortPreamble ShortSlotTime RadioMeasure (0x1431)
        signal: -77.00 dBm
        last seen: 5 ms ago
        SSID: Galaxy Z Fold6 5073
        Supported rates: 1.0* 2.0* 5.5* 11.0*
        DS Parameter set: channel 8
        Country: RU     Environment: bogus
                Channels [1 - 13] @ 23 dBm
        ERP: <no flags>
        Extended supported rates: 6.0 9.0 12.0 18.0 24.0 36.0 48.0 54.0
        RSN:     * Version: 1
                 * Group cipher: CCMP
                 * Pairwise ciphers: CCMP
                 * Authentication suites: PSK
                 * Capabilities: 16-PTKSA-RC 1-GTKSA-RC (0x000c)
        Supported operating classes:
                 * current operating class: 81
                 * operating class: 83
                 * operating class: 84
                 * operating class: 125
                 * operating class: 128
                 * operating class: 129
                 * operating class: 134
        HT capabilities:
                Capabilities: 0x9ad
                        RX LDPC
                        HT20
                        SM Power Save disabled
                        RX HT20 SGI
                        TX STBC
                        RX STBC 1-stream
                        Max AMSDU length: 7935 bytes
                        No DSSS/CCK HT40
                Maximum RX AMPDU length 65535 bytes (exponent: 0x003)
                Minimum RX AMPDU time spacing: 4 usec (0x05)
                HT RX MCS rate indexes supported: 0-15
                HT TX MCS rate indexes are undefined
        HT operation:
                 * primary channel: 8
                 * secondary channel offset: no secondary
                 * STA channel width: 20 MHz
                 * RIFS: 0
                 * HT protection: nonmember
                 * non-GF present: 1
                 * OBSS non-GF present: 1
                 * dual beacon: 0
                 * dual CTS protection: 0
                 * STBC beacon: 0
                 * L-SIG TXOP Prot: 0
                 * PCO active: 0
                 * PCO phase: 0
        Extended capabilities:
                 * Extended Channel Switching
                 * SSID List
                 * Operating Mode Notification
                 * Max Number Of MSDUs In A-MSDU is unlimited
        VHT capabilities:
                VHT Capabilities (0x33817992):
                        Max MPDU length: 11454
                        Supported Channel Width: neither 160 nor 80+80
                        RX LDPC
                        TX STBC
                        SU Beamformer
                        SU Beamformee
                        RX antenna pattern consistency
                        TX antenna pattern consistency
                VHT RX MCS set:
                        1 streams: MCS 0-9
                        2 streams: MCS 0-9
                        3 streams: not supported
                        4 streams: not supported
                        5 streams: not supported
                        6 streams: not supported
                        7 streams: not supported
                        8 streams: not supported
                VHT RX highest supported: 780 Mbps
                VHT TX MCS set:
                        1 streams: MCS 0-9
                        2 streams: MCS 0-9
                        3 streams: not supported
                        4 streams: not supported
                        5 streams: not supported
                        6 streams: not supported
                        7 streams: not supported
                        8 streams: not supported
                VHT TX highest supported: 780 Mbps
                VHT extended NSS: supported
        VHT operation:
                 * channel width: 0 (20 or 40 MHz)
                 * center freq segment 1: 0
                 * center freq segment 2: 0
                 * VHT basic MCS set: 0xfffa
        Transmit Power Envelope:
                 * Local Maximum Transmit Power For 20 MHz: 11.5 dBm
        WMM:     * Parameter version 1
                 * u-APSD
                 * BE: CW 15-1023, AIFSN 3
                 * BK: CW 15-1023, AIFSN 7
                 * VI: CW 7-15, AIFSN 2, TXOP 3008 usec
                 * VO: CW 3-7, AIFSN 2, TXOP 1504 usec
BSS 78:45:58:3a:38:db(on wlan0)
        last seen: 5363.234s [boottime]
        TSF: 0 usec (0d, 00:00:00)
        freq: 2412
        beacon interval: 100 TUs
        capability: ESS Privacy ShortPreamble ShortSlotTime RadioMeasure (0x1431)
        signal: -76.00 dBm
        last seen: 5 ms ago
        SSID: Element-T
        Supported rates: 1.0* 2.0* 5.5* 11.0* 6.0 9.0 12.0 18.0
        DS Parameter set: channel 1
        Country: RU     Environment: Indoor/Outdoor
                Channels [1 - 13] @ 20 dBm
        ERP: <no flags>
        RSN:     * Version: 1
                 * Group cipher: CCMP
                 * Pairwise ciphers: CCMP
                 * Authentication suites: PSK
                 * Capabilities: 1-PTKSA-RC 1-GTKSA-RC (0x0000)
        Extended supported rates: 24.0 36.0 48.0 54.0
        BSS Load:
                 * station count: 2
                 * channel utilisation: 112/255
                 * available admission capacity: 31250 [*32us]
        RM enabled capabilities:
                Capabilities: 0x73 0xd0 0x00 0x00 0x0c
                        Link Measurement
                        Neighbor Report
                        Beacon Passive Measurement
                        Beacon Active Measurement
                        Beacon Table Measurement
                        LCI Measurement
                        Transmit Stream/Category Measurement
                        Triggered Transmit Stream/Category
                        FTM Range Report
                        Civic Location Measurement
                Nonoperating Channel Max Measurement Duration: 0
                Measurement Pilot Capability: 4
        HT capabilities:
                Capabilities: 0x1ac
                        HT20
                        SM Power Save disabled
                        RX HT20 SGI
                        TX STBC
                        RX STBC 1-stream
                        Max AMSDU length: 3839 bytes
                        No DSSS/CCK HT40
                Maximum RX AMPDU length 65535 bytes (exponent: 0x003)
                Minimum RX AMPDU time spacing: 8 usec (0x06)
                HT TX/RX MCS rate indexes supported: 0-23
        HT operation:
                 * primary channel: 1
                 * secondary channel offset: no secondary
                 * STA channel width: 20 MHz
                 * RIFS: 1
                 * HT protection: no
                 * non-GF present: 1
                 * OBSS non-GF present: 0
                 * dual beacon: 0
                 * dual CTS protection: 0
                 * STBC beacon: 0
                 * L-SIG TXOP Prot: 0
                 * PCO active: 0
                 * PCO phase: 0
        Extended capabilities:
                 * Extended Channel Switching
                 * TFS
                 * WNM-Sleep Mode
                 * TIM Broadcast
                 * BSS Transition
                 * SSID List
                 * Operating Mode Notification
        WMM:     * Parameter version 1
                 * BE: CW 15-1023, AIFSN 3
                 * BK: CW 15-1023, AIFSN 7
                 * VI: CW 7-15, AIFSN 2, TXOP 3008 usec
                 * VO: CW 3-7, AIFSN 2, TXOP 1504 usec
BSS 7e:45:58:3a:38:db(on wlan0)
        last seen: 5363.234s [boottime]
        TSF: 0 usec (0d, 00:00:00)
        freq: 2412
        beacon interval: 100 TUs
        capability: ESS Privacy ShortPreamble ShortSlotTime RadioMeasure (0x1431)
        signal: -75.00 dBm
        last seen: 5 ms ago
        SSID: Element_Guest
        Supported rates: 1.0* 2.0* 5.5* 11.0* 6.0 9.0 12.0 18.0
        DS Parameter set: channel 1
        Country: RU     Environment: Indoor/Outdoor
                Channels [1 - 13] @ 20 dBm
        ERP: <no flags>
        RSN:     * Version: 1
                 * Group cipher: CCMP
                 * Pairwise ciphers: CCMP
                 * Authentication suites: PSK
                 * Capabilities: 1-PTKSA-RC 1-GTKSA-RC (0x0000)
        Extended supported rates: 24.0 36.0 48.0 54.0
        BSS Load:
                 * station count: 5
                 * channel utilisation: 114/255
                 * available admission capacity: 31250 [*32us]
        RM enabled capabilities:
                Capabilities: 0x73 0xd0 0x00 0x00 0x0c
                        Link Measurement
                        Neighbor Report
                        Beacon Passive Measurement
                        Beacon Active Measurement
                        Beacon Table Measurement
                        LCI Measurement
                        Transmit Stream/Category Measurement
                        Triggered Transmit Stream/Category
                        FTM Range Report
                        Civic Location Measurement
                Nonoperating Channel Max Measurement Duration: 0
                Measurement Pilot Capability: 4
        HT capabilities:
                Capabilities: 0x1ac
                        HT20
                        SM Power Save disabled
                        RX HT20 SGI
                        TX STBC
                        RX STBC 1-stream
                        Max AMSDU length: 3839 bytes
                        No DSSS/CCK HT40
                Maximum RX AMPDU length 65535 bytes (exponent: 0x003)
                Minimum RX AMPDU time spacing: 8 usec (0x06)
                HT TX/RX MCS rate indexes supported: 0-23
        HT operation:
                 * primary channel: 1
                 * secondary channel offset: no secondary
                 * STA channel width: 20 MHz
                 * RIFS: 1
                 * HT protection: no
                 * non-GF present: 1
                 * OBSS non-GF present: 0
                 * dual beacon: 0
                 * dual CTS protection: 0
                 * STBC beacon: 0
                 * L-SIG TXOP Prot: 0
                 * PCO active: 0
                 * PCO phase: 0
        Extended capabilities:
                 * Extended Channel Switching
                 * TFS
                 * WNM-Sleep Mode
                 * TIM Broadcast
                 * BSS Transition
                 * SSID List
                 * Operating Mode Notification
        WMM:     * Parameter version 1
                 * BE: CW 15-1023, AIFSN 3
                 * BK: CW 15-1023, AIFSN 7
                 * VI: CW 7-15, AIFSN 2, TXOP 3008 usec
                 * VO: CW 3-7, AIFSN 2, TXOP 1504 usec
BSS 82:45:58:3a:38:db(on wlan0)
        last seen: 5363.234s [boottime]
        TSF: 0 usec (0d, 00:00:00)
        freq: 2412
        beacon interval: 100 TUs
        capability: ESS Privacy ShortPreamble ShortSlotTime RadioMeasure (0x1431)
        signal: -76.00 dBm
        last seen: 5 ms ago
        SSID: Element-t_2Gz
        Supported rates: 1.0* 2.0* 5.5* 11.0* 6.0 9.0 12.0 18.0
        DS Parameter set: channel 1
        Country: RU     Environment: Indoor/Outdoor
                Channels [1 - 13] @ 20 dBm
        ERP: <no flags>
        RSN:     * Version: 1
                 * Group cipher: CCMP
                 * Pairwise ciphers: CCMP
                 * Authentication suites: PSK
                 * Capabilities: 1-PTKSA-RC 1-GTKSA-RC (0x0000)
        Extended supported rates: 24.0 36.0 48.0 54.0
        BSS Load:
                 * station count: 3
                 * channel utilisation: 114/255
                 * available admission capacity: 31250 [*32us]
        RM enabled capabilities:
                Capabilities: 0x73 0xd0 0x00 0x00 0x0c
                        Link Measurement
                        Neighbor Report
                        Beacon Passive Measurement
                        Beacon Active Measurement
                        Beacon Table Measurement
                        LCI Measurement
                        Transmit Stream/Category Measurement
                        Triggered Transmit Stream/Category
                        FTM Range Report
                        Civic Location Measurement
                Nonoperating Channel Max Measurement Duration: 0
                Measurement Pilot Capability: 4
        HT capabilities:
                Capabilities: 0x1ac
                        HT20
                        SM Power Save disabled
                        RX HT20 SGI
                        TX STBC
                        RX STBC 1-stream
                        Max AMSDU length: 3839 bytes
                        No DSSS/CCK HT40
                Maximum RX AMPDU length 65535 bytes (exponent: 0x003)
                Minimum RX AMPDU time spacing: 8 usec (0x06)
                HT TX/RX MCS rate indexes supported: 0-23
        HT operation:
                 * primary channel: 1
                 * secondary channel offset: no secondary
                 * STA channel width: 20 MHz
                 * RIFS: 1
                 * HT protection: no
                 * non-GF present: 1
                 * OBSS non-GF present: 0
                 * dual beacon: 0
                 * dual CTS protection: 0
                 * STBC beacon: 0
                 * L-SIG TXOP Prot: 0
                 * PCO active: 0
                 * PCO phase: 0
        Extended capabilities:
                 * Extended Channel Switching
                 * TFS
                 * WNM-Sleep Mode
                 * TIM Broadcast
                 * BSS Transition
                 * SSID List
                 * Operating Mode Notification
        WMM:     * Parameter version 1
                 * BE: CW 15-1023, AIFSN 3
                 * BK: CW 15-1023, AIFSN 7
                 * VI: CW 7-15, AIFSN 2, TXOP 3008 usec
                 * VO: CW 3-7, AIFSN 2, TXOP 1504 usec
BSS cc:2d:e0:c2:7d:42(on wlan0)
        last seen: 5363.234s [boottime]
        TSF: 0 usec (0d, 00:00:00)
        freq: 2447
        beacon interval: 100 TUs
        capability: ESS Privacy ShortPreamble ShortSlotTime (0x0431)
        signal: -70.00 dBm
        last seen: 5 ms ago
        SSID: MikroTik-C27D42
        Supported rates: 1.0* 2.0* 5.5* 11.0* 6.0 9.0 12.0 18.0
        DS Parameter set: channel 8
        TIM: DTIM Count 0 DTIM Period 1 Bitmap Control 0x0 Bitmap[0] 0x0
        ERP: <no flags>
        HT capabilities:
                Capabilities: 0x106e
                        HT20/HT40
                        SM Power Save disabled
                        RX HT20 SGI
                        RX HT40 SGI
                        No RX STBC
                        Max AMSDU length: 3839 bytes
                        DSSS/CCK HT40
                Maximum RX AMPDU length 65535 bytes (exponent: 0x003)
                Minimum RX AMPDU time spacing: No restriction (0x00)
                HT RX MCS rate indexes supported: 0-15
                HT TX MCS rate indexes are undefined
        RSN:     * Version: 1
                 * Group cipher: CCMP
                 * Pairwise ciphers: CCMP
                 * Authentication suites: PSK
                 * Capabilities: 1-PTKSA-RC 1-GTKSA-RC (0x0000)
        Extended supported rates: 24.0 36.0 48.0 54.0
        HT operation:
                 * primary channel: 8
                 * secondary channel offset: above
                 * STA channel width: any
                 * RIFS: 0
                 * HT protection: no
                 * non-GF present: 0
                 * OBSS non-GF present: 0
                 * dual beacon: 0
                 * dual CTS protection: 0
                 * STBC beacon: 0
                 * L-SIG TXOP Prot: 0
                 * PCO active: 0
                 * PCO phase: 0
        WMM:     * Parameter version 1
                 * u-APSD
                 * BE: CW 15-1023, AIFSN 3
                 * BK: CW 15-1023, AIFSN 7
                 * VI: CW 7-15, AIFSN 2, TXOP 3008 usec
                 * VO: CW 3-7, AIFSN 2, TXOP 1504 usec
        WPS:     * Version: 1.0
                 * Wi-Fi Protected Setup State: 2 (Configured)
                 * UUID: 00000000-0000-0000-0000-cc2de0c27d3d
                 * RF Bands: 0x1
BSS 50:ff:20:a5:47:98(on wlan0)
        last seen: 5363.234s [boottime]
        TSF: 0 usec (0d, 00:00:00)
        freq: 2442
        beacon interval: 100 TUs
        capability: ESS Privacy ShortSlotTime APSD RadioMeasure (0x1c11)
        signal: -78.00 dBm
        last seen: 5 ms ago
        SSID: Prometei
        Supported rates: 1.0* 2.0* 5.5* 11.0* 9.0 18.0 36.0 54.0
        DS Parameter set: channel 7
        TIM: DTIM Count 0 DTIM Period 1 Bitmap Control 0x1 Bitmap[0] 0x0
        Country: RU     Environment: bogus
                Channels [1 - 13] @ 20 dBm
        Power constraint: 0 dB
        TPC report: TX power: 19 dBm
        RM enabled capabilities:
                Capabilities: 0x02 0x00 0x01 0x00 0x00
                        Neighbor Report
                        AP Channel Report
                Nonoperating Channel Max Measurement Duration: 0
                Measurement Pilot Capability: 0
        AP Channel Report:
                 * operating class: 81
                 * channel(s): 1 2 3 4 5 6 7 8 9 10 11 12 13
        ERP: Use_Protection Barker_Preamble_Mode
        Extended supported rates: 6.0 12.0 24.0 48.0
        RSN:     * Version: 1
                 * Group cipher: CCMP
                 * Pairwise ciphers: CCMP
                 * Authentication suites: PSK
                 * Capabilities: 1-PTKSA-RC 1-GTKSA-RC (0x0000)
        WPS:     * Version: 1.0
                 * Wi-Fi Protected Setup State: 2 (Configured)
                 * AP setup locked: 0x01
                 * UUID: bc329e00-1dd8-11b2-8601-50ff20a54798
                 * RF Bands: 0x1
                 * Version2: 2.0
        BSS Load:
                 * station count: 2
                 * channel utilisation: 15/255
                 * available admission capacity: 31250 [*32us]
        HT capabilities:
                Capabilities: 0x9ad
                        RX LDPC
                        HT20
                        SM Power Save disabled
                        RX HT20 SGI
                        TX STBC
                        RX STBC 1-stream
                        Max AMSDU length: 7935 bytes
                        No DSSS/CCK HT40
                Maximum RX AMPDU length 65535 bytes (exponent: 0x003)
                Minimum RX AMPDU time spacing: 4 usec (0x05)
                HT RX MCS rate indexes supported: 0-15
                HT TX MCS rate indexes are undefined
        HT operation:
                 * primary channel: 7
                 * secondary channel offset: no secondary
                 * STA channel width: 20root@harvest05:~#
root@harvest05:~#
        """
        if full:
            cmd = "iw dev wlan0 scan"
        else:
            cmd = "iw dev wlan0 scan | grep SSID:"

        output = self.cmd_timeout__write_read__payload(
            cmd=cmd,
            timeout=10,
            timeout_continue=2
        )
        """
        если сеть WiFi подключена/соннект установлен - скана не будет!!!
        [COM3.WRITEREAD]
            write=[timeout 10 iw dev wlan0 scan | grep SSID:]
            read=[command failed: Resource temporarily unavailable (-11)]
        """
        if "Resource temporarily unavailable" in output:
            raise Exception("WiFi=NOT AWAILABLE SCAN! cause WiFi is connected!!!")

        ssids = re.findall(r'\s*SSID:\s(.+)\s*\n*', output)
        print(f"Wi-Fi scan {ssids=}")
        return ssids

    # ==================================================================================================================
    def rfid__check_working(self) -> bool:
        # Убиваем возможные зависшие процессы на порту
        self.conn.write_read_bytes(f"fuser -k /dev/ttyS2 2>/dev/null", timeout_continue=0.5)
        time.sleep(0.2)

        cmd = f"python3 scr__rfid_scan.py"

        output = self.cmd_timeout__write_read__payload(
            cmd,
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
[15:56:33.600955]COM16.stop_line[OK]= b'' [extra=EqValid_Regexp(v_args=(b'.*root@.+:.+#.*',)/v_kwargs={}/_cumulate_mode=<EnumAdj_BoolCumulate.ALL_TRUE: <built-in function all>>/_other_resolve=True)]
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
        cmd = f"python3 scr__rfid_scan.py"

        steps = steps or 1
        for step in range(steps):
            # Убиваем возможные зависшие процессы на порту
            self.conn.write_read_bytes(f"fuser -k /dev/ttyS2 2>/dev/null", timeout_continue=0.5)
            time.sleep(0.3)

            output = self.cmd_timeout__write_read__payload(
                cmd,
                timeout_continue=10,
            )
            s_result = output.splitlines()

            # Фильтруем: только строки вида "HEX,ЧИСЛО"
            for line in s_result:
                if re.match(r'^[0-9A-F]{24}', line.strip()):
                    result.add(line.strip())

            if step != steps - 1:
                time.sleep(0.3)
        return result

    # ==================================================================================================================
    def bt__connections__get_active(
            self,
            **r_kwargs,
    ) -> list[str]:
        """
        get MACs for active BT connections
        ==================================
        1=СОЕДИНЕНИЕ УДЕРЖИВАЕТСЯ!!
        ---- Sent utf8 encoded message: "hcitool con\r\n" ----
        hcitool con
        Connections:
                < LE D4:81:ED:BB:AA:6B handle 64 state 1 lm CENTRAL
        root@harvest05:~#

        ==================================
        2=СОЕДИНЕНИЕ РАЗОРВАНО
        ---- Sent utf8 encoded message: "hcitool con\r\n" ----
        hcitool con
        Connections:
        root@harvest05:~#
        """
        cmd = "hcitool con"
        output = self.cmd_timeout__write_read__payload(
            cmd,
            timeout_continue=1,
            **r_kwargs,
        )
        macs = re.findall(PATTERN_MAC, output)
        return macs or []

    def bt__connection__close_mac(
            self,
            mac: str,
            **r_kwargs,
    ) -> bool:
        """
    КОМАНДА РАЗРЫВА
    ==================================

    УСПЕШНАЯ
    ----------------------------------
    root@harvest05:~#
    ---- Sent utf8 encoded message: "bluetoothctl disconnect D4:81:ED:BB:AA:6B\r\n" ----
    bluetoothctl disconnect D4:81:ED:BB:AA:6B
    Attempting to disconnect from D4:81:ED:BB:AA:6B
    Successful disconnected
    root@harvest05:~#

    УЖЕ ОСТАНОВЛЕННОГО - повторный запуск
    ----------------------------------
    ---- Sent utf8 encoded message: "bluetoothctl disconnect D4:81:ED:BB:AA:6B\r\n" ----
    bluetoothctl disconnect D4:81:ED:BB:AA:6B
    Device D4:81:ED:BB:AA:6B not available
    root@harvest05:~#
    root@harvest05:~#

    ОТКЛЮЧЕНИЕ ПРИ РАБОТЕ ОТ HARVESTER сервиса!!!
    ----------------------------------
    bluetoothctl disconnect D4:81:ED:BB:AA:6B 2>/dev/null || echo ERROR_MSG
    Attempting to disconnect from D4:81:ED:BB:AA:6B
    [CHG] Device D4:81:ED:BB:AA:6B ServicesResolved: no
    Successful disconnected
    root@harvest05:~#
        """
        cmd = f"bluetoothctl disconnect {mac}"
        return self.cmd_timeout__check_executed_success(
            cmd,
            timeout_continue=1,
            **r_kwargs,
        )

    def bt__connections__clear_all(self) -> bool:
        """
        SPECIALLY CREATED FOR
        close BTUS fade connection
        """
        active_macs = self.bt__connections__get_active()
        for mac in active_macs:
            if not self.bt__connection__close_mac(mac):
                return False
        return True

    # ------------------------------------------------------------------------------------------------------------------
    def bt__scan(
            self,
            timeout: float = 20,
            timeout_continue: float = 4,
            **r_kwargs,
    ) -> dict[str, dict[str, str | int | None]] | NoReturn:  # {mac: {name, rssi}}
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
            "random": None,  # random/public
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
            "UTC": EqValid_G_E(0),
            "Distance up": EqValid_GL_ET((0, 100)),
            "Distance side": EqValid_GL_ET((0, 10)),
            "Temperature": EqValid_GL_TT((0, 40)),
            "Battery": EqValid_GL_TT((0, 100)),
            "Percentage": EqValid_GL_TT((0, 100)),
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
            timeout=3,
            timeout_continue=2,
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
@pytest.mark.skip
@pytest.mark.parametrize(
    argnames="source, _EXPECTED",
    argvalues=[
        # BLANK ------
        ('ERROR', []),
        ('+CGDATA: ("")\nOK', []),

        # INT=======================
        # SINGLE ------
        ('+CGATT: (0-1)\nOK', ['0', '1']),
        ('+CREG: (0-2)\nOK', ['0', '1', '2']),
        ('+CREG: ( 0 -  2 )\nOK', ['0', '1', '2']),

        ('+CGACT: (0,1)\nOK', ['0', '1']),
        ('+CGACT: ( 0 , 1  )\nOK', ['0', '1']),

        # SOFISTICATED ------
        ('+CFUN: (0-1,4-8),(0-1)\nOK', ['0', '1', '4', '5', '6', '7', '8', ]),
        ('+: (4-8),(0-1)\nOK', ['0', '1', '4', '5', '6', '7', '8', ]),
        ('+: (1,4-8)\nOK', ['1', '4', '5', '6', '7', '8', ]),
        ('+: ( 1 , 4 -  8 )\nOK', ['1', '4', '5', '6', '7', '8', ]),

        ('+: (1-3-4)\nOK', ['1', '2', '3', '4']),
        ('+: (1-3-4,8)\nOK', ['1', '2', '3', '4', '8']),

        ('+CPBR: (1-100),20,28', ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']),
        # ('+CPBR: (1-2),20,28', ['1', '2', '20', '28']),  # is it really important??

        # STR=======================
        ('+CPBS: "SM"\nOK', ["SM",]),
        ('+CPBS: ("SM")\nOK', ["SM",]),
        ('+CPBS: ("SM","FD")\nOK', ["SM","FD"]),
        ('+CPBS: "SM", ("FD")\nOK', ["SM", "FD"]),

        # INT+STR=======================
        ('+CPBS: "SM", (2,0-1)\nOK', ["0", "1", "2", "SM"]),
    ]
)
def test__at_param__parse_variants(source, _EXPECTED):
    func_link = Harvest.at_param__parse_variants
    Lambda(func_link, source).check_expected__assert(_EXPECTED)


# ======================================================================================================================
AT_GROUPS: dict[str, dict[str, str | list[str, tuple[str, str]]]] = {
    # =========================================================================
    # СТРУКТУРА!!!
    # 0=DANGER+USELESS -------------------------------
    # 1=ACCURATE -------------------------------------
    # 2=DOUBT ----------------------------------------
    # 3=UNKNOWN --------------------------------------

    # СИНТАКСИС КОМАНДЫ КОНЕЧНОЕ = та версия что выдает результат напрямую!

    # как определить конечное имя
    # -------------------------------------------------------------------------
    # ВАРИАНТ-0=допустимых может быть несколько
    # 'AT+CGMR': ['revision identification',
    #             ('AT+CGMR=?', 'OK'),
    #             ('AT+CGMR', '+CGMR: A011B02A7682M6_DS_FOTA\nOK'),   # РЕАЛЬНЫЙ ЗАПРОС <<<------- использовать простой!
    #             ('AT+CGMR?', '+CGMR: A011B02A7682M6_DS_FOTA\nOK'),  # РЕАЛЬНЫЙ ЗАПРОС <<<-------

    # ВАРИАНТ-1
    # 'AT+GSN': ['IMEI (алиас)',
    #            ('AT+GSN=?', 'OK'),
    #            ('AT+GSN', '865286077380516\nOK'),     # РЕАЛЬНЫЙ ЗАПРОС <<<-------
    #            ('AT+GSN?', 'ERROR'),                  # НЕКОРРЕКТНЫЙ синтаксис

    # ВАРИАНТ-2
    # 'AT+CIMI': ['IMSI (IMSI SIM-карты)',
    #             ('AT+CIMI=?', 'OK'),                      # всегда может работать НО это запрос доступных вариантов
    #             ('AT+CIMI', '+CME ERROR: SIM failure'),   # РЕАЛЬНЫЙ ЗАПРОС <<<-------
    #             ('AT+CIMI?', '+CME ERROR: Operation not supported'),  # НЕКОРРЕКТНЫЙ синтаксис

    # ВАРИАНТ-3-1=с изменяемыми значениями=правильно запрашивать значение!
    # 'AT+CSQDELTA': ['порог изменения RSSI',
    #                 ('AT+CSQDELTA=?', '+CSQDELTA: (0-5)\nOK'),
    #                 ('AT+CSQDELTA', 'OK'),
    #                 ('AT+CSQDELTA?', '+CSQDELTA: 5\nOK'),     # РЕАЛЬНЫЙ ЗАПРОС <<<-------
    #                 ('AT+CSQDELTA=0', 'OK'),
    #                 ('AT+CSQDELTA?', '+CSQDELTA: 0\nOK'),
    #                 ('AT+CSQDELTA=1', 'OK'),
    #                 ('AT+CSQDELTA?', '+CSQDELTA: 1\nOK'),
    #                 ('AT+CSQDELTA=2', 'OK'),
    #                 ('AT+CSQDELTA?', '+CSQDELTA: 2\nOK'),
    #                 ('AT+CSQDELTA=3', 'OK'),
    #                 ('AT+CSQDELTA?', '+CSQDELTA: 3\nOK'),
    #                 ('AT+CSQDELTA=4', 'OK'),
    #                 ('AT+CSQDELTA?', '+CSQDELTA: 4\nOK'),
    #                 ('AT+CSQDELTA=5', 'OK'),
    #                 ('AT+CSQDELTA?', '+CSQDELTA: 5\nOK'),
    #                 ],

    # ВАРИАНТ-3-2=с изменяемыми значениями=иногда правильно дает по прямому запросу
    # 'AT+CPAS': ['phone activity status',
    #             ('AT+CPAS=?', '+CPAS: (0,3,4)\nOK'),
    #             ('AT+CPAS', '+CPAS: 0\nOK'),                     # РЕАЛЬНЫЙ ЗАПРОС <<<-------
    #             ('AT+CPAS?', '+CME ERROR: Operation not supported'),
    #             ('AT+CPAS=0', 'ERROR'),
    #             ('AT+CPAS?', '+CME ERROR: Operation not supported'),
    #             ('AT+CPAS=3', 'ERROR'),
    #             ('AT+CPAS?', '+CME ERROR: Operation not supported'),
    #             ('AT+CPAS=4', 'ERROR'),
    #             ('AT+CPAS?', '+CME ERROR: Operation not supported'),
    #             ],

    # ==========================================================================
    "1=MODEM": {
        # 0=DANGER+USELESS -------------------------------
        # "AT+CSCS": "[DANGER]выбор TE character set (IRA/GSM/UCS2/HEX)",
        # "AT+SIMEI": "[DANGER]установка IMEI (только для service)",
        # "AT+CUSBPIDSWITCH": "[DANGER]смена USB PID (перезагружает модуль!)",
        # "AT+CLCK": "[DANGER] facility lock (блокировка SIM/сети)",
        # "AT+CPOF": "[DANGER]power off module",
        # "AT+CRESET": "[DANGER]reset module",
        # "AT+CSCLK": "[DANGER]UART sleep control",
        # "AT+CMUX": "[DANGER]мультиплексор UART (4 виртуальных порта) # DANGER",
        # "AT+CUSBPIDSWITCH": "[DANGER]смена USB PID # DANGER (reset)",

        # 'AT+CMEE': ['[USELESS] формат ошибок (+CME ERROR: numeric/verbose)',
        #     ('AT+CMEE=?', '+CMEE: (0-2)\nOK'),
        #     ('AT+CMEE', 'OK'),
        #     ('AT+CMEE?', '+CMEE: 2\nOK'),
        #     ('AT+CMEE=0', 'OK'),
        #     ('AT+CMEE?', '+CMEE: 0\nOK'),
        #     ('AT+CMEE=1', 'OK'),
        #     ('AT+CMEE?', '+CMEE: 1\nOK'),
        #     ('AT+CMEE=2', 'OK'),
        #     ('AT+CMEE?', '+CMEE: 2\nOK'),
        #     ],

        # 1=ACCURATE -------------------------------------
        'AT': ['эхо, проверка связи',
            ('AT=?', 'ERROR'),
            ('AT', 'OK'),
            ('AT?', 'ERROR'),
            ],
        'ATI': ['информация о производителе/модели/ревизии/IMEI',
            ('ATI=?', 'ERROR'),
            ('ATI', 'Manufacturer: INCORPORATED\nModel: A7682E-R\nRevision: A7682M6_V1.11.1\nIMEI1: 865286077380516\nIMEI2: 865286076965218\n+GCAP: +CGSM,+FCLASS,+DS\nOK'),
            ('ATI?', 'ERROR'),
            ],
        # ATI1 - 9 TODO: add???
        'AT+CGMI': ['manufacturer ID',
            ('AT+CGMI=?', 'OK'),
            ('AT+CGMI', 'INCORPORATED\nOK'),
            ('AT+CGMI?', 'INCORPORATED\nOK'),
            ],
        'AT+CGMM': ['model identification',
            ('AT+CGMM=?', 'OK'),
            ('AT+CGMM', 'A7682E-R\nOK'),
            ('AT+CGMM?', 'A7682E-R\nOK'),
            ],
        'AT+CGMR': ['revision identification',
                    ('AT+CGMR=?', 'OK'),
                    ('AT+CGMR', '+CGMR: A011B02A7682M6_DS_FOTA\nOK'),
                    ('AT+CGMR?', '+CGMR: A011B02A7682M6_DS_FOTA\nOK'),
                    ],
        'AT+CGSN': ['IMEI / serial number',
                    ('AT+CGSN=?', 'OK'),
                    ('AT+CGSN', '865286077380516\nOK'),
                    ('AT+CGSN?', 'ERROR'),
                    ],
        'AT+GSN': ['IMEI (алиас)',
                   ('AT+GSN=?', 'OK'),
                   ('AT+GSN', '865286077380516\nOK'),
                   ('AT+GSN?', 'ERROR'),
                   ],
        'AT+CPAS': ['phone activity status',
                    ('AT+CPAS=?', '+CPAS: (0,3,4)\nOK'),
                    ('AT+CPAS', '+CPAS: 0\nOK'),
                    ('AT+CPAS?', '+CME ERROR: Operation not supported'),
                    ('AT+CPAS=0', 'ERROR'),
                    ('AT+CPAS?', '+CME ERROR: Operation not supported'),
                    ('AT+CPAS=3', 'ERROR'),
                    ('AT+CPAS?', '+CME ERROR: Operation not supported'),
                    ('AT+CPAS=4', 'ERROR'),
                    ('AT+CPAS?', '+CME ERROR: Operation not supported'),
                    ],
        'AT+CCLK?': ['real time clock',
                     ('AT+CCLK=?', 'OK'),
                     ('AT+CCLK', 'ERROR'),
                     ('AT+CCLK?', '+CCLK: "70/01/01,00:23:56+00"\nOK'),
                     ],
        'AT+CATR?': ['URC destination interface',
                     ('AT+CATR=?', '+CATR: (0-7)\nOK'),
                     ('AT+CATR', 'ERROR'),
                     ('AT+CATR?', '+CATR: 0\nOK'),
                     ('AT+CATR=0', 'OK'),
                     ('AT+CATR?', '+CATR: 0\nOK'),
                     ('AT+CATR=1', 'OK'),
                     ('AT+CATR?', '+CATR: 1\nOK'),
                     ('AT+CATR=2', 'OK'),
                     ('AT+CATR?', '+CATR: 2\nOK'),
                     ('AT+CATR=3', 'OK'),
                     ('AT+CATR?', '+CATR: 3\nOK'),
                     ('AT+CATR=4', 'OK'),
                     ('AT+CATR?', '+CATR: 4\nOK'),
                     ('AT+CATR=5', 'OK'),
                     ('AT+CATR?', '+CATR: 5\nOK'),
                     ('AT+CATR=6', 'OK'),
                     ('AT+CATR?', '+CATR: 6\nOK'),
                     ('AT+CATR=7', 'OK'),
                     ('AT+CATR?', '+CATR: 7\nOK'),
                     ],

        # 2=DOUBT ----------------------------------------
        'AT+CACM?': ['accumulated call meter',
                     ('AT+CACM=?', 'OK'),
                     ('AT+CACM', '+CME ERROR: Operation not supported'),
                     ('AT+CACM?', '+CME ERROR: unknown error'),
                     ],
        'AT+CAMM?': ['accumulated call meter maximum',
                     ('AT+CAMM=?', 'OK'),
                     ('AT+CAMM', '+CME ERROR: Operation not supported'),
                     ('AT+CAMM?', '+CME ERROR: unknown error'),
                     ],
        'AT+CPUC?': ['price per unit and currency',
                     ('AT+CPUC=?', 'OK'),
                     ('AT+CPUC', 'ERROR'),
                     ('AT+CPUC?', '+CME ERROR: unknown error'),
                     ],

        # 3=UNKNOWN --------------------------------------
        'AT+CGGMM': ['model identification (SIMCom-вариант)',
            ('AT+CGGMM=?', 'ERROR'),
            ('AT+CGGMM', 'ERROR'),
            ('AT+CGGMM?', 'ERROR'),
            ],
        'AT+CGGMR': ['revision identification (SIMCom-вариант)',
            ('AT+CGGMR=?', 'ERROR'),
            ('AT+CGGMR', 'ERROR'),
            ('AT+CGGMR?', 'ERROR'),
            ],
        'AT+GCAP': ['список поддерживаемых возможностей (+CGSM, +FCLASS, +DS)',
            ('AT+GCAP=?', 'OK'),
            ('AT+GCAP', 'ERROR'),
            ('AT+GCAP?', 'ERROR'),
            ],
        'AT+SMEID': ['MEID (CDMA)',
            ('AT+SMEID=?', 'ERROR'),
            ('AT+SMEID', 'ERROR'),
            ('AT+SMEID?', 'ERROR'),
            ],
        'AT+CSPN': ['service provider name',
            ('AT+CSPN=?', 'ERROR'),
            ('AT+CSPN', 'ERROR'),
            ('AT+CSPN?', 'ERROR'),
            ],
    },

    # ==========================================================================
    "2=SIM": {
        # 0=DANGER+USELESS -------------------------------

        # "AT+CPWD": "[DANGER]смена пароля (PIN/PUK)",
        # 'AT+CSVM': ['[USELESS]voice mail subscriber number',
        #     ('AT+CSVM=?', 'ERROR'),
        #     ('AT+CSVM', 'ERROR'),
        #     ('AT+CSVM?', 'ERROR'),
        #     ],

        # 1=ACCURATE -------------------------------------
        'AT+CICCID': ['ICCID SIM-карты',
                      ('AT+CICCID=?', 'OK'),
                      ('AT+CICCID', '+CME ERROR: SIM not inserted'),
                      ('AT+CICCID?', '+CME ERROR: SIM not inserted'),
                      ],
        'AT+CIMI': ['IMSI (IMSI SIM-карты)',
                    ('AT+CIMI=?', 'OK'),
                    ('AT+CIMI', '+CME ERROR: SIM failure'),
                    ('AT+CIMI?', '+CME ERROR: Operation not supported'),
                    ],
        'AT+SPIC': ['остаток попыток ввода PIN/PUK',
                    ('AT+SPIC=?', 'OK'),
                    ('AT+SPIC', '+CME ERROR: SIM not inserted'),
                    ('AT+SPIC?', 'ERROR'),
                    ],
        'AT+CPIN?': ['статус PIN (READY / SIM PIN / SIM PUK)',
                     ('AT+CPIN=?', 'OK'),
                     ('AT+CPIN', 'ERROR'),
                     ('AT+CPIN?', '+CME ERROR: SIM not inserted'),
                     ],

        # 2=DOUBT ----------------------------------------
        'AT+CPINR?': ['остаток попыток PIN (3GPP-вариант)',
                      ('AT+CPINR=?', '+CPINR: (0-3),(0-3),(0-10),(0-10)\nOK'),
                      ('AT+CPINR', '+CME ERROR: Operation not supported'),
                      ('AT+CPINR?', '+CME ERROR: SIM not inserted'),
                      ('AT+CPINR=0', 'ERROR'),
                      ('AT+CPINR?', '+CME ERROR: SIM not inserted'),
                      ('AT+CPINR=1', 'ERROR'),
                      ('AT+CPINR?', '+CME ERROR: SIM not inserted'),
                      ('AT+CPINR=2', 'ERROR'),
                      ('AT+CPINR?', '+CME ERROR: SIM not inserted'),
                      ('AT+CPINR=3', 'ERROR'),
                      ('AT+CPINR?', '+CME ERROR: SIM not inserted'),
                      ('AT+CPINR=4', 'ERROR'),
                      ('AT+CPINR?', '+CME ERROR: SIM not inserted'),
                      ('AT+CPINR=5', 'ERROR'),
                      ('AT+CPINR?', '+CME ERROR: SIM not inserted'),
                      ('AT+CPINR=6', 'ERROR'),
                      ('AT+CPINR?', '+CME ERROR: SIM not inserted'),
                      ('AT+CPINR=7', 'ERROR'),
                      ('AT+CPINR?', '+CME ERROR: SIM not inserted'),
                      ('AT+CPINR=8', 'ERROR'),
                      ('AT+CPINR?', '+CME ERROR: SIM not inserted'),
                      ('AT+CPINR=9', 'ERROR'),
                      ('AT+CPINR?', '+CME ERROR: SIM not inserted'),
                      ],

        # 3=UNKNOWN --------------------------------------
        'AT+CIMIM': ['IMSI второго аппа (USIM)',
                     ('AT+CIMIM=?', 'ERROR'),
                     ('AT+CIMIM', 'ERROR'),
                     ('AT+CIMIM?', 'ERROR'),
                     ],
        'AT+CNUM': ['основной запрос номера (недоступен на M2M sim)',
                    ('AT+CNUM=?', 'ERROR'),
                    ('AT+CNUM', 'ERROR'),
                    ('AT+CNUM?', 'ERROR'),
                    ],
    },

    # =========================================================================
    "3=V25TER_BASIC(V.25TER БАЗОВЫЕ (управление модемом))": {
        # 0=DANGER+USELESS -------------------------------

        # "A/": "[DANGER]повторить последнюю команду",
        # "ATD": "dial (голосовой/данные)",
        # "ATD><mem><n>": "dial из памяти (SM/ME/DC...)",
        # "ATD><n>": "dial из активной памяти",
        # "ATD><str>": "dial по имени из памяти",
        # "ATA": "[DANGER]answer (ответ на входящий)",
        # "ATH": "[DANGER]hang up (положить трубку)",
        # "ATS0": "[DANGER]auto-answer (число гудков)",
        # "+++": "[DANGER]escape из data mode в command mode",
        # "ATO": "[DANGER]вернуться в data mode",
        # "AT+ICF": "[DANGER]character framing (data/parity/stop)",
        # "AT+IFC": "[DANGER]flow control (RTS/CTS)",
        # "AT&C": "[DANGER]DCD function mode",
        # "ATE": "[DANGER]echo on/off",
        # "AT&D": "[DANGER]DTR function mode",
        # "AT&S": "[DANGER]DSR function mode",
        # "AT&F": "[DANGER]factory defaults",
        # "ATQ": "[DANGER]result code presentation mode",
        # "AT&W": "[DANGER]save user settings",
        # "ATZ": "[DANGER]restore user settings",
        # 'AT+IPR': ['[NONEUSEFULL]baud rate (temporarily)',
        #            ('AT+IPR=?',
        #             '+IPR: (300,600,1200,2400,4800,9600,19200,38400,57600,115200,230400,460800,921600,1842000,3686400)\nOK'),
        #            ('AT+IPR', 'OK'),
        #            ('AT+IPR?', '+IPR: 115200\nOK'),
        #            ('AT+IPR=300', 'OK'),
        #            ('AT+IPR?', '+IPR: 300\nOK'),
        #            ('AT+IPR=600', 'OK'),
        #            ('AT+IPR?', '+IPR: 600\nOK'),
        #            ('AT+IPR=1200', 'OK'),
        #            ('AT+IPR?', '+IPR: 1200\nOK'),
        #            ('AT+IPR=2400', 'OK'),
        #            ('AT+IPR?', '+IPR: 2400\nOK'),
        #            ('AT+IPR=4800', 'OK'),
        #            ('AT+IPR?', '+IPR: 4800\nOK'),
        #            ('AT+IPR=9600', 'OK'),
        #            ('AT+IPR?', '+IPR: 9600\nOK'),
        #            ('AT+IPR=19200', 'OK'),
        #            ('AT+IPR?', '+IPR: 19200\nOK'),
        #            ('AT+IPR=38400', 'OK'),
        #            ('AT+IPR?', '+IPR: 38400\nOK'),
        #            ('AT+IPR=57600', 'OK'),
        #            ('AT+IPR?', '+IPR: 57600\nOK'),
        #            ('AT+IPR=115200', 'OK'),
        #            ('AT+IPR?', '+IPR: 115200\nOK'),
        #            ],
        # 'AT+IPREX': ['[NONEUSEFULL]bbaud rate (permanently)',
        #              ('AT+IPREX=?',
        #               '+IPREX: (300,600,1200,2400,4800,9600,19200,38400,57600,115200,230400,460800,921600,1842000,3686400)\nOK'),
        #              ('AT+IPREX', 'OK'),
        #              ('AT+IPREX?', '+IPREX: 115200\nOK'),
        #              ('AT+IPREX=300', 'OK'),
        #              ('AT+IPREX?', '+IPREX: 300\nOK'),
        #              ('AT+IPREX=600', 'OK'),
        #              ('AT+IPREX?', '+IPREX: 600\nOK'),
        #              ('AT+IPREX=1200', 'OK'),
        #              ('AT+IPREX?', '+IPREX: 1200\nOK'),
        #              ('AT+IPREX=2400', 'OK'),
        #              ('AT+IPREX?', '+IPREX: 2400\nOK'),
        #              ('AT+IPREX=4800', 'OK'),
        #              ('AT+IPREX?', '+IPREX: 4800\nOK'),
        #              ('AT+IPREX=9600', 'OK'),
        #              ('AT+IPREX?', '+IPREX: 9600\nOK'),
        #              ('AT+IPREX=19200', 'OK'),
        #              ('AT+IPREX?', '+IPREX: 19200\nOK'),
        #              ('AT+IPREX=38400', 'OK'),
        #              ('AT+IPREX?', '+IPREX: 38400\nOK'),
        #              ('AT+IPREX=57600', 'OK'),
        #              ('AT+IPREX?', '+IPREX: 57600\nOK'),
        #              ('AT+IPREX=115200', 'OK'),
        #              ('AT+IPREX?', '+IPREX: 115200\nOK'),
        #              ],

        # 1=ACCURATE -------------------------------------
        'ATV': ['result code format (numeric/verbose)',
                ('ATV=?', 'ERROR'),
                ('ATV', 'OK'),
                ('ATV?', 'ERROR'),
                ],
        'ATX': ['CONNECT result code format',
                ('ATX=?', 'ERROR'),
                ('ATX', 'OK'),
                ('ATX?', 'ERROR'),
                ],

        # 2=DOUBT ----------------------------------------

        # 3=UNKNOWN --------------------------------------
        'AT&V': ['display current configuration',
                 ('AT&V=?', 'ERROR'),
                 ('AT&V', 'ERROR'),
                 ('AT&V?', 'ERROR'),
                 ],
        'AT&E': ['CONNECT result code format (speed)',
                 ('AT&E=?', 'ERROR'),
                 ('AT&E', 'ERROR'),
                 ('AT&E?', 'ERROR'),
                 ],
    },

    # =========================================================================
    "4=STATUS_CONTROL(управление состоянием)": {
        # 0=DANGER+USELESS -------------------------------

        # 'AT+CFUN': ["[DANGER]уровень функциональности (0=min, 1=full, 4=offline, 7=reset) # DANGER",
        #     ('AT+CFUN=?', '+CFUN: (0-1,4-8),(0-1)\nOK'),
        #     ('AT+CFUN', 'ERROR'),
        #     ('AT+CFUN?', '+CFUN: 1\nOK'),
        #     ('AT+CFUN=0', '+SIMCARD: NOT AVAILABLE\n+CGEV: ME DETACH\nOK'),
        #     ('AT+CFUN?', '+CFUN: 0\nOK'),
        #     ('AT+CFUN=1', 'OK\n+CPIN: SIM REMOVED\nOK'),
        #     ('AT+CFUN?', '+CFUN: 1\nOK'),
        #     ('AT+CFUN=4', '+CGEV: ME DETACH\nOK'),
        #     ('AT+CFUN?', '+CFUN: 4\nOK'),
        #     ('AT+CFUN=5', 'OK'),
        #     ('AT+CFUN?', '+CFUN: 5\nOK'),
        #     ('AT+CFUN=6', 'OK\n+CGEV: ME DETACH'),
        #     ('AT+CFUN?',
        #      'cat: /dev/ttyUSB4: No such file or directory\n[1]+  Exit 1                  timeout 5.0 cat /dev/ttyUSB4'),
        #     ('AT+CFUN=7', 'AT+CFUN?\n[1]+  Done                    timeout 5.0 cat /dev/ttyUSB4'),
        #     ('AT+CFUN?', 'AT+CFUN=7\n[1]+  Done                    timeout 5.0 cat /dev/ttyUSB4'),
        #     ('AT+CFUN=8', 'AT+CFUN?\n[1]+  Done                    timeout 5.0 cat /dev/ttyUSB4'),
        #     ('AT+CFUN?', 'AT+CFUN=8\n[1]+  Done                    timeout 5.0 cat /dev/ttyUSB4'),
        # ],
        # "AT+CPOF": "[DANGER]power off",
        # "AT+CRESET": "[DANGER]reset",
        # "AT+CMEE": "[DANGER]error format",
        # "AT+SIMEI": "[DANGER]set IMEI",

        # 1=ACCURATE -------------------------------------
        'AT+CSQ': ['signal quality (RSSI, BER)',
                   ('AT+CSQ=?', '+CSQ: (0-31,99),(0-7,99)\nOK'),
                   ('AT+CSQ', '+CSQ: 23,0\nOK'),
                   ('AT+CSQ?', 'ERROR'),
                   ('AT+CSQ=0', 'ERROR'),
                   ('AT+CSQ?', 'ERROR'),
                   ('AT+CSQ=1', 'ERROR'),
                   ('AT+CSQ?', 'ERROR'),
                   ('AT+CSQ=2', 'ERROR'),
                   ('AT+CSQ?', 'ERROR'),
                   ('AT+CSQ=3', 'ERROR'),
                   ('AT+CSQ?', 'ERROR'),
                   ('AT+CSQ=4', 'ERROR'),
                   ('AT+CSQ?', 'ERROR'),
                   ('AT+CSQ=5', 'ERROR'),
                   ('AT+CSQ?', 'ERROR'),
                   ('AT+CSQ=6', 'ERROR'),
                   ('AT+CSQ?', 'ERROR'),
                   ('AT+CSQ=7', 'ERROR'),
                   ('AT+CSQ?', 'ERROR'),
                   ('AT+CSQ=8', 'ERROR'),
                   ('AT+CSQ?', 'ERROR'),
                   ('AT+CSQ=9', 'ERROR'),
                   ('AT+CSQ?', 'ERROR'),
                   ],
        'AT+AUTOCSQ?': ['автоматический отчёт CSQ',
                        ('AT+AUTOCSQ=?', '+AUTOCSQ: (0-1),(0-1)\nOK'),
                        ('AT+AUTOCSQ', 'ERROR'),
                        ('AT+AUTOCSQ?', '+AUTOCSQ: 1,0\nOK'),
                        ('AT+AUTOCSQ=0', 'OK'),
                        ('AT+AUTOCSQ?', '+AUTOCSQ: 0,0\nOK'),
                        ('AT+AUTOCSQ=1', 'OK'),
                        ('AT+AUTOCSQ?', '+AUTOCSQ: 1,0\nOK'),
                        ],
        'AT+CSQDELTA?': ['порог изменения RSSI',
                         ('AT+CSQDELTA=?', '+CSQDELTA: (0-5)\nOK'),
                         ('AT+CSQDELTA', 'OK'),
                         ('AT+CSQDELTA?', '+CSQDELTA: 5\nOK'),
                         ('AT+CSQDELTA=0', 'OK'),
                         ('AT+CSQDELTA?', '+CSQDELTA: 0\nOK'),
                         ('AT+CSQDELTA=1', 'OK'),
                         ('AT+CSQDELTA?', '+CSQDELTA: 1\nOK'),
                         ('AT+CSQDELTA=2', 'OK'),
                         ('AT+CSQDELTA?', '+CSQDELTA: 2\nOK'),
                         ('AT+CSQDELTA=3', 'OK'),
                         ('AT+CSQDELTA?', '+CSQDELTA: 3\nOK'),
                         ('AT+CSQDELTA=4', 'OK'),
                         ('AT+CSQDELTA?', '+CSQDELTA: 4\nOK'),
                         ('AT+CSQDELTA=5', 'OK'),
                         ('AT+CSQDELTA?', '+CSQDELTA: 5\nOK'),
                         ],
        'AT+CCLK?': ['real time clock',
                     ('AT+CCLK=?', 'OK'),
                     ('AT+CCLK', 'ERROR'),
                     ('AT+CCLK?', '+CCLK: "70/01/01,00:50:36+00"\nOK'),
                     ],

        'AT+CPAS': ['phone activity status',
                    ('AT+CPAS=?', '+CPAS: (0,3,4)\nOK'),
                    ('AT+CPAS', '+CPAS: 0\nOK'),
                    ('AT+CPAS?', '+CME ERROR: Operation not supported'),
                    ('AT+CPAS=0', 'ERROR'),
                    ('AT+CPAS?', '+CME ERROR: Operation not supported'),
                    ('AT+CPAS=3', 'ERROR'),
                    ('AT+CPAS?', '+CME ERROR: Operation not supported'),
                    ('AT+CPAS=4', 'ERROR'),
                    ('AT+CPAS?', '+CME ERROR: Operation not supported'),
                    ],

        # 2=DOUBT ----------------------------------------
        'AT+CSIM': ['generic SIM access (APDU)',
                    ('AT+CSIM=?', 'OK'),
                    ('AT+CSIM', 'ERROR'),
                    ('AT+CSIM?', '+CME ERROR: Operation not supported'),
                    ],
        'AT+CRSM': ['restricted SIM access (READ/UPDATE BINARY/RECORD)',
                    ('AT+CRSM=?', 'OK'),
                    ('AT+CRSM', 'ERROR'),
                    ('AT+CRSM?', '+CME ERROR: Operation not supported'),
                    ],

        # 3=UNKNOWN --------------------------------------
        'AT+CSPN': ['service provider name',
                    ('AT+CSPN=?', 'ERROR'),
                    ('AT+CSPN', 'ERROR'),
                    ('AT+CSPN?', 'ERROR'),
                    ],
        'AT+SMEID': ['MEID',
                     ('AT+SMEID=?', 'ERROR'),
                     ('AT+SMEID', 'ERROR'),
                     ('AT+SMEID?', 'ERROR'),
                     ],
        'AT+CSVM': ['voice mail number',
                    ('AT+CSVM=?', 'ERROR'),
                    ('AT+CSVM', 'ERROR'),
                    ('AT+CSVM?', 'ERROR'),
                    ],
    },

    # =========================================================================
    "5=NETWORK(СЕТЬ / РЕГИСТРАЦИЯ / ОПЕРАТОР)": {
        # 0=DANGER+USELESS -------------------------------
        # 'AT+COPS': ["[DANGER]operator selection # DANGER (может долго висеть на =?)",
        #     ('AT+COPS=?', ''),
        #     ('AT+COPS', ''),
        #     ('AT+COPS?', ''),
        # ],
        # "AT+CLCK": "[DANGER]facility lock (network)",
        # "AT+CPWD": "[DANGER]change password",
        # "AT+CCUG": "[DANGER]closed user group",
        # "AT+CNMP": "[DANGER]preferred mode selection",
        # "AT+CNBP": "[DANGER]preferred band selection",
        # "AT+NETMODE": "[DANGER]WCDMA/TDSCDMA mode select",
        # "AT+WS46": "[DANGER]RAT selection (12=LTE, 22=..., 28=...)",

        # 'AT+COPN': ['[#FIXME!]read operator names (BLOCKING)',
        #             ('AT+COPN=?', 'ERROR\n+CME ERROR: SIM failure'),
        #             ('AT+COPN',
        #              'OK\n+COPN: "20201","C-OTE"\n+COPN: "20205","voda GR"\n+COPN: "20209","WIND"\n+COPN: "20210","WIND"\n+COPN: "20402","Tele2"\n+COPN: "20404","voda NL"\n+COPN: "20408","NL KPN"\n+COPN: "20412","NL Tlfrt"\n+COPN: "20416","TMO NL"\n+COPN: "20601","PROXI"\n+COPN: "20610","mobi*"\n+COPN: "20620","BASE"\n+COPN: "20801","Orange"\n+COPN: "20802","Contact"\n+COPN: "20809","SFR"\n+COPN: "20810","SFR"\n+COPN: "20811","SFR"\n+COPN: "20813","Contact"\n+COPN: "20815","Free"\n+COPN: "20820","BYTEL"\n+COPN: "20888","Contact"\n+COPN: "21201","vala"\n+COPN: "21210","MONACO"\n+COPN: "21303","M-AND"\n+COPN: "21401","voda ES"\n+COPN: "21403","Orange"\n+COPN: "21404","YOIGO"\n+COPN: "21407","Movistar"\n+COPN: "21601","TelenorH"\n+COPN: "21630","THU"\n+COPN: "21670","voda HU"\n+COPN: "21803","HT ERONET"\n+COPN: "21805","m:tel"\n+COPN: "21890","BHMobile"\n+COPN: "21901","HT HR"\n+COPN: "21902","Tele2 HR"\n+COPN: "21910","VIP"\n+COPN: "22001","Telenor"\n+COPN: "22002","ProMonte"\n+COPN: "22003","MTS"\n+COPN: "22004","TMO CG"\n+COPN: "22005","Vip SRB"\n+COPN: "22201","TIM"\n+COPN: "22210","voda IT"\n+COPN: "22288","I WIND"\n+COPN: "22299","3 ITA"\n+COPN: "22601","VF-RO"\n+COPN: "22603","COSMOTE"\n+COPN: "22605","Digi"\n+COPN: "22610","ORANGE"\n+COPN: "22801","Swisscom"\n+COPN: "22802","Sunrise"\n+COPN: "22803","Orange"\n+COPN: "22807","In&Phone"\n+COPN: "22815","OnAir"\n+COPN: "23001","TMO CZ"\n+COPN: "23002","O2 - CZ"\n+COPN: "23003","Vodafone"\n+COPN: "23101","Orange"\n+COPN: "23102","Telekom"\n+COPN: "23106","O2 - SK"\n+COPN: "23201","A1"\n+COPN: "23203","TMA"\n+COPN: "23205","3 AT"\n+COPN: "23207","telering"\n+COPN: "23210","3 AT"\n+COPN: "23212","A1"\n+COPN: "23401","UK01"\n+COPN: "23403","ATL-VOD"\n+COPN: "23407","C&W UK"\n+COPN: "23410","O2 - UK"\n+COPN: "23415","voda UK"\n+COPN: "23419","PMN"\n+COPN: "23420","3 UK"\n+COPN: "23428","Marathon"\n+COPN: "23430","EE"\n+COPN: "23431","EE"\n+COPN: "23432","EE"\n+COPN: "23433","EE"\n+COPN: "23450","JT"\n+COPN: "23455","Sure"\n+COPN: "23458","MANX"'),
        #             ('AT+COPN?',
        #              '+COPN: "23802","TelenoDK"\n+COPN: "23806","3 DK"\n+COPN: "23820","Telia"\n+COPN: "23866","TT DK"\n+COPN: "23877","TelenoDK"\n+COPN: "24001","TELIA"\n+COPN: "24002","3 SE"\n+COPN: "24004","SWE"\n+COPN: "24005","Sweden3G"\n+COPN: "24007","Tele2 SE"\n+COPN: "24008","TelenorS"\n+COPN: "24024","MobileS"\n+COPN: "24201","TELENOR"\n+COPN: "24202","NetCom"\n+COPN: "24204","Mobile N"\n+COPN: "24205","Mobile N"\n+COPN: "24403","DNA"\n+COPN: "24405","elisa"\n+COPN: "24412","DNA"\n+COPN: "24414","FI AMT"\n+COPN: "24491","SONERA"\n+COPN: "24601","OMT"\n+COPN: "24602","BITE"\n+COPN: "24603","Tele2 LT"\n+COPN: "24701","LMT"\n+COPN: "24702","Tele2 LV"\n+COPN: "24705","BITE LV"\n+COPN: "24801","EMT"\n+COPN: "24802","elisa"\n+COPN: "24803","Tele2 EE"\n+COPN: "25001","MTS"\n+COPN: "25002","MegaFon"\n+COPN: "25003","RTC"\n+COPN: "25004","RUS_SCN"\n+COPN: "25005","RTC"\n+COPN: "25007","SMARTS"\n+COPN: "25010","DTC"\n+COPN: "25012","RTC"\n+COPN: "25013","KUGSM"\n+COPN: "25015","SMARTS"\n+COPN: "25016","NTC"\n+COPN: "25017","RTC"\n+COPN: "25019","INDIGO"\n+COPN: "25020","TELE2 RU"\n+COPN: "25028","Beeline"\n+COPN: "25035","MOTIV"\n+COPN: "25037","KODOTEL"\n+COPN: "25038","RTC"\n+COPN: "25039","RTC"\n+COPN: "25099","Beeline"\n+COPN: "25501","MTS UKR"\n+COPN: "25502","Beeline"\n+COPN: "25503","UA-KS"\n+COPN: "25505","GT"\n+COPN: "25506","life:)"\n+COPN: "25507","TriMob"\n+COPN: "25701","VELCOM"\n+COPN: "25702","MTS"\n+COPN: "25704","life:) BY"\n+COPN: "25901","Orange"\n+COPN: "25902","MDCELL"\n+COPN: "25905","UNITE"\n+COPN: "26001","PLUS"\n+COPN: "26002","TM PL"\n+COPN: "26003","Orange"\n+COPN: "26004","Tele2"\n+COPN: "26006","Play"\n+COPN: "26007","Premium"\n+COPN: "26008","E-Telko"\n+COPN: "26016","Mobyland"\n+COPN: "26017","Aero2"\n+COPN: "26201","TDG"\n+COPN: "26202","Vodafone"\n+COPN: "26203","E-Plus"\n+COPN: "26207","o2 - de"\n+COPN: "26208","o2 - de"\n+COPN: "26213","MobilCom"\n+COPN: "26601","GIBTEL"\n+COPN: "26606","CTS"\n+COPN: "26609","Shine"\n+COPN: "26801","voda P"\n+COPN: "26803","OPTIM"\n+COPN: "26806","P MEO"\n+COPN: "27001","Post"\n+COPN: "27077","TANGO"\n+COPN: "27099","Orange"\n+COPN: "27201","voda IE"\n+COPN: "27202","O2-IRL"\n+COPN: "27203","METEOR"\n+COPN: "27205","3 IRL"'),
        #             ],
        # 'AT+CNAOP': ['[#FIXME!]acquisitions order preference',
        #              ('AT+CNAOP=?',
        #               '+COPN: "27402","Vodafone"\n+COPN: "27404","Viking"\n+COPN: "27408","On-waves"\n+COPN: "27411","NOVA"\n+COPN: "27412","Siminn"\n+COPN: "27601","A M C"\n+COPN: "27602","Voda AL"\n+COPN: "27603","EAGLE AL"\n+COPN: "27604","PLUS AL"\n+COPN: "27801","voda MT"\n+COPN: "27821","gomobile"\n+COPN: "27877","MT"\n+COPN: "28001","CYTAVODA"\n+COPN: "28010","MTN"\n+COPN: "28201","GCELL"\n+COPN: "28202","MAGTI"\n+COPN: "28204","BEELINE"\n+COPN: "28300","MTS Arm"\n+COPN: "28301","Beeline"\n+COPN: "28305","MTS Arm"\n+COPN: "28310","Orange"\n+COPN: "28401","Mtel"\n+COPN: "28403","Vivacom"\n+COPN: "28405","GLOBUL"\n+COPN: "28601","TCELL"\n+COPN: "28602","VF TR"\n+COPN: "28603","AVEA"\n+COPN: "28801","FT-GSM"\n+COPN: "28802","VODAFONE"\n+COPN: "29001","TELE GRL"\n+COPN: "29201","SMT"\n+COPN: "29340","Si.mobil"\n+COPN: "29341","MOBITEL"\n+COPN: "29364","T-2"\n+COPN: "29370","TUS"\n+COPN: "29401","TMO MK"\n+COPN: "29402","ONE"\n+COPN: "29403","Vip MKD"\n+COPN: "29501","Swiss FL"\n+COPN: "29502","OFL"\n+COPN: "29505","FL1"\n+COPN: "29577","Alpmobil"\n+COPN: "29701","Telenor"\n+COPN: "29702","T.me"\n+COPN: "302066","MTS"\n+COPN: "302072","ROGERS"\n+COPN: "302220","TELUS"\n+COPN: "302270","Eastlink"\n+COPN: "302320","Mobilicity"\n+COPN: "302340","Execulink"\n+COPN: "302370","Fido"\n+COPN: "302380","DMTS"\n+COPN: "302490","WIND"\n+COPN: "302610","Bell"\n+COPN: "302660","MTS"\n+COPN: "302720","ROGERS"\n+COPN: "302730","TStarSol"\n+COPN: "302770","RuralCom"\n+COPN: "302780","SaskTel"\n+COPN: "302880","FastRoam"\n+COPN: "302940","Wightman"\n+COPN: "30801","AMERIS"\n+COPN: "310000","CBW"\n+COPN: "310002","NEPW"\n+COPN: "310009","NEPW"\n+COPN: "310020","UnionTel"\n+COPN: "310030","CENT USA"\n+COPN: "310031","T-Mobile"\n+COPN: "310032","IT&E"\n+COPN: "310046","SIMMETRY"\n+COPN: "310070","AT&T"\n+COPN: "310080","Corr"\n+COPN: "310090","AT&T"\n+COPN: "310100","PLATEAU"\n+COPN: "310120","Sprint"\n+COPN: "310140","GTA"\n+COPN: "310150","AT&T"\n+COPN: "310160","T-Mobile"\n+COPN: "310170","AT&T"\n+COPN: "310190","D-HARBOR"\n+COPN: "310200","T-Mobile"\n+COPN: "310210","T-Mobile"\n+COPN: "310220","T-Mobile"\n+COPN: "310230","T-Mobile"\n+COPN: "310240","T-Mobile"\n+COPN: "310250","T-Mobile"\n+COPN: "310260","T-Mobile"\n+COPN: "310270","T-Mobile"\n+COPN: "310290","NEPW"\n+COPN: "310300","Big Sky"\n+COPN: "310310","T-Mobile"\n+COPN: "310320","Cell"\n+COPN: "310340","WestLink"\n+COPN: "310380","AT&T"\n+COPN: "310390","CELL 1 ET"\n+COPN: "310400","iCAN_GSM"\n+COPN: "310410","AT&T"\n+COPN: "310420","CBW"\n+COPN: "310450","NECCI"\n+COPN: "310460","USA1L"\n+COPN: "310470","DOCOMOPA"\n+COPN: "310490","SunCom"\n+COPN: "310530","IWS"\n+COPN: "310560","AT&T"\n+COPN: "310570","Chinook"\n+COPN: "310580","T-Mobile"\n+COPN: "310590","Verizon"\n+COPN: "310630","AMERLINK"\n+COPN: "310640","ARDGMC"\n+COPN: "310650","Jasper"\n+COPN: "310660","T-Mobile"\n+COPN: "310680","AT&T"\n+COPN: "310690","IMMIX"\n+COPN: "310710","ASTAC"\n+COPN: "310730","USCC"\n+COPN: "310740","OTZ"\n+COPN: "310770","IWS"\n+COPN: "310800","T-Mobile"\n+COPN: "310840","telna"\n+COPN: "310870","PACE"\n+COPN: "310880","ACSIAC"\n+COPN: "310890","Verizon"\n+COPN: "310950","XIT"\n+COPN: "310980","AT&T"\n+COPN: "311000","Mid-Tex"\n+COPN: "311001","WILKES"\n+COPN: "311005","WILKES"\n+COPN: "311030","Indigo"'),
        #              ('AT+CNAOP',
        #               '+COPN: "311080","PINECell"\n+COPN: "311090","SXLP"\n+COPN: "311150","WILKES"\n+COPN: "311170","Broadpoint"\n+COPN: "311180","WCW"\n+COPN: "311190","C1ECI"\n+COPN: "311240","CWCI"\n+COPN: "311260",""\n+COPN: "311310","LamarCel"\n+COPN: "311330","BTW"\n+COPN: "311360","STELERA"\n+COPN: "311370","GCI"\n+COPN: "311380","AT&T"\n+COPN: "311410","AT&T"\n+COPN: "311480","Verizon"\n+COPN: "311500","MOSAIC"\n+COPN: "311530","USANW"\n+COPN: "311540","ProxMo"\n+COPN: "311580","USCC"\n+COPN: "311680","Green Fly"\n+COPN: "311710","NEWN"\n+COPN: "311720","MainePCS"\n+COPN: "311730","ProxMo"\n+COPN: "311940","CLEAR"\n+COPN: "31260","CvgCo"\n+COPN: "312230","SRTW"\n+COPN: "312260","USACL"\n+COPN: "330110","Claro"\n+COPN: "330120","Open Mob"\n+COPN: "33403","movistar"\n+COPN: "33409","Nextel3G"\n+COPN: "33420","TELCEL"\n+COPN: "33450","Iusacell"\n+COPN: "33490","Nextel3G"\n+COPN: "338005","DIGICEL"\n+COPN: "338050","DIGICEL"\n+COPN: "338070","ClaroJam"\n+COPN: "338180","LIME"\n+COPN: "34001","Orange"\n+COPN: "34002","ONLY"\n+COPN: "34003","CHIPPIE"\n+COPN: "34008","DAUPHIN"\n+COPN: "34020","DigicelF"\n+COPN: "342600","LIME"\n+COPN: "342750","DIGICEL"\n+COPN: "344030","imobile"\n+COPN: "344920","LIME"\n+COPN: "344930","Cingular"\n+COPN: "346140","LIME"\n+COPN: "348170","LIME"\n+COPN: "348570","CCTBVI"\n+COPN: "35000","CELLONE"\n+COPN: "35002","M3 WIREL"\n+COPN: "35010","Cingular"\n+COPN: "352030","DIGICEL"\n+COPN: "352110","LIME"\n+COPN: "354860","LIME"\n+COPN: "356110","LIME"\n+COPN: "358050","DIGICEL"\n+COPN: "358110","LIME"\n+COPN: "360070","DIGICEL"\n+COPN: "360110","LIME"\n+COPN: "36251","Telcell"\n+COPN: "36269","CT GSM"\n+COPN: "36291","CHIPPIE"\n+COPN: "362951","CHIPPIE"\n+COPN: "36301","SETARGSM"\n+COPN: "36320","DIGICEL"\n+COPN: "36439","BaTelCel"\n+COPN: "365840","LIME"\n+COPN: "366020","Cingular"\n+COPN: "366110","LIME"\n+COPN: "36801","CUBACEL"\n+COPN: "37001","Orange"\n+COPN: "37002","ClaroDOM"\n+COPN: "37004","VIVA"\n+COPN: "37201","VOILA"\n+COPN: "37203","Natcom"\n+COPN: "37412","TSTT"\n+COPN: "376350","LIME"\n+COPN: "376360","ICOM TCI"\n+COPN: "40001","ACELL"\n+COPN: "40002","BAKCELL"\n+COPN: "40004","Nar"\n+COPN: "40101","Beeline"\n+COPN: "40102","KCELL"\n+COPN: "40107","ALTEL"\n+COPN: "40177","NEO"\n+COPN: "40211","B-Mobile"\n+COPN: "40277","TASHICELL"\n+COPN: "40401","Vodafone"\n+COPN: "40402","airtel"\n+COPN: "40403","airtel"\n+COPN: "40404","IDEA"\n+COPN: "40405","Vodafone"\n+COPN: "40407","IDEA"\n+COPN: "40409","RELIANCE"\n+COPN: "40410","airtel"'),
        #              ('AT+CNAOP?',
        #               '+COPN: "40412","IDEA"\n+COPN: "40413","Vodafone"\n+COPN: "40414","IDEA"\n+COPN: "40415","Vodafone"\n+COPN: "40416","airtel"\n+COPN: "40417","AIRCEL"\n+COPN: "40418","RELIANCE"\n+COPN: "40419","IDEA"\n+COPN: "40420","Vodafone"\n+COPN: "40421","BPL MOBILE"\n+COPN: "40422","IDEA"\n+COPN: "40424","IDEA"\n+COPN: "40425","AIRCEL"\n+COPN: "40427","Vodafone"\n+COPN: "40428","AIRCEL"\n+COPN: "40429","AIRCEL"\n+COPN: "40430","Vodafone"\n+COPN: "40431","airtel"\n+COPN: "40433","AIRCEL"\n+COPN: "40434","CellOne"\n+COPN: "40435","AIRCEL"\n+COPN: "40436","RELIANCE"\n+COPN: "40437","AIRCEL"\n+COPN: "40438","CellOne"\n+COPN: "40440","airtel"\n+COPN: "40441","AIRCEL"\n+COPN: "40442","AIRCEL"\n+COPN: "40443","Vodafone"\n+COPN: "40444","IDEA"\n+COPN: "40445","airtel"\n+COPN: "40446","Vodafone"\n+COPN: "40449","airtel"\n+COPN: "40450","RELIANCE"\n+COPN: "40451","CellOne"\n+COPN: "40452","RELIANCE"\n+COPN: "40453","CellOne"\n+COPN: "40454","CellOne"\n+COPN: "40455","CellOne"\n+COPN: "40456","IDEA"\n+COPN: "40457","CellOne"\n+COPN: "40458","CellOne"\n+COPN: "40459","CellOne"\n+COPN: "40460","Vodafone"\n+COPN: "40462","CellOne"\n+COPN: "40464","CellOne"\n+COPN: "40466","CellOne"\n+COPN: "40467","RELIANCE"\n+COPN: "40468","DOLPHIN"\n+COPN: "40469","DOLPHIN"\n+COPN: "40470","airtel"\n+COPN: "40471","CellOne"\n+COPN: "40472","CellOne"\n+COPN: "40473","CellOne"\n+COPN: "40474","CellOne"\n+COPN: "40475","CellOne"\n+COPN: "40476","CellOne"\n+COPN: "40477","CellOne"\n+COPN: "40478","IDEA"\n+COPN: "40479","CellOne"\n+COPN: "40480","CellOne"\n+COPN: "40481","CellOne"\n+COPN: "40482","IDEA"\n+COPN: "40483","Reliance"\n+COPN: "40484","Vodafone"\n+COPN: "40485","RELIANCE"\n+COPN: "40486","Vodafone"\n+COPN: "40487","IDEA"\n+COPN: "40488","Vodafone"\n+COPN: "40489","IDEA"\n+COPN: "40490","airtel"\n+COPN: "40491","Aircel"\n+COPN: "40492","airtel"\n+COPN: "40493","airtel"\n+COPN: "40494","airtel"\n+COPN: "40495","airtel"\n+COPN: "40496","airtel"\n+COPN: "40497","airtel"\n+COPN: "40498","airtel"\n+COPN: "40501","Reliance"\n+COPN: "40505","Reliance"\n+COPN: "40506","Reliance"\n+COPN: "40507","Reliance"\n+COPN: "40509","Reliance"\n+COPN: "40510","Reliance"\n+COPN: "40511","Reliance"\n+COPN: "40513","Reliance"\n+COPN: "40515","Reliance"\n+COPN: "40518","Reliance"\n+COPN: "40519","Reliance"\n+COPN: "40520","Reliance"\n+COPN: "40521","Reliance"\n+COPN: "40522","Reliance"\n+COPN: "405025","TATA DO"\n+COPN: "405027","TATA DO"\n+COPN: "405029","TATA DO"\n+COPN: "405030","TATA DO"\n+COPN: "405031","TATA DO"\n+COPN: "405032","TATA DO"\n+COPN: "405034","TATA DO"\n+COPN: "405035","TATA DO"\n+COPN: "405036","TATA DO"\n+COPN: "405037","TATA DO"\n+COPN: "405038","TATA DO"'),
        #              ('AT+CNAOP=27402',
        #               '+COPN: "405811","Aircel"\n+COPN: "405812","Aircel"\n+COPN: "405813","UNITECH"\n+COPN: "405814","UNITECH"\n+COPN: "405815","UNITECH"\n+COPN: "405816","UNITECH"\n+COPN: "405817","UNITECH"\n+COPN: "405818","UNITECH"\n+COPN: "405819","UNITECH"\n+COPN: "405820","UNITECH"\n+COPN: "405821","UNITECH"\n+COPN: "405822","UNITECH"\n+COPN: "405823","VIDEOCON"\n+COPN: "405824","VIDEOCON"\n+COPN: "405825","VIDEOCON"\n+COPN: "405827","VIDEOCON"\n+COPN: "405828","VIDEOCON"\n+COPN: "405829","VIDEOCON"\n+COPN: "405830","VIDEOCON"\n+COPN: "405831","VIDEOCON"\n+COPN: "405832","VIDEOCON"\n+COPN: "405833","VIDEOCON"\n+COPN: "405834","VIDEOCON"\n+COPN: "405835","VIDEOCON"\n+COPN: "405836","VIDEOCON"\n+COPN: "405837","VIDEOCON"\n+COPN: "405838","VIDEOCON"\n+COPN: "405839","VIDEOCON"\n+COPN: "405840","VIDEOCON"\n+COPN: "405841","VIDEOCON"\n+COPN: "405842","VIDEOCON"\n+COPN: "405843","VIDEOCON"\n+COPN: "405844","UNITECH"\n+COPN: "405845","IDEA"\n+COPN: "405846","IDEA"\n+COPN: "405848","IDEA"\n+COPN: "405849","IDEA"\n+COPN: "405850","IDEA"\n+COPN: "405852","IDEA"\n+COPN: "405853","IDEA"\n+COPN: "405854","LoopMobile"\n+COPN: "405855","LoopMobile"\n+COPN: "405856","LoopMobile"\n+COPN: "405857","LoopMobile"\n+COPN: "405858","LoopMobile"\n+COPN: "405859","LoopMobile"\n+COPN: "405860","LoopMobile"\n+COPN: "405861","LoopMobile"\n+COPN: "405862","LoopMobile"\n+COPN: "405863","LoopMobile"\n+COPN: "405864","LoopMobile"\n+COPN: "405865","LoopMobile"\n+COPN: "405866","LoopMobile"\n+COPN: "405867","LoopMobile"\n+COPN: "405868","LoopMobile"\n+COPN: "405869","LoopMobile"\n+COPN: "405870","LoopMobile"\n+COPN: "405871","LoopMobile"\n+COPN: "405872","LoopMobile"\n+COPN: "405873","LoopMobile"\n+COPN: "405874","LoopMobile"\n+COPN: "405875","UNITECH"\n+COPN: "405876","UNITECH"\n+COPN: "405877","UNITECH"\n+COPN: "405878","UNITECH"\n+COPN: "405879","UNITECH"\n+COPN: "405880","UNITECH"\n+COPN: "405912","etisalat"\n+COPN: "405913","etisalat"\n+COPN: "405914","etisalat"\n+COPN: "405915","etisalat"\n+COPN: "405916","etisalat"\n+COPN: "405917","etisalat"\n+COPN: "405918","etisalat"\n+COPN: "405919","etisalat"\n+COPN: "405920","etisalat"\n+COPN: "405921","etisalat"\n+COPN: "405922","etisalat"\n+COPN: "405923","etisalat"\n+COPN: "405924","etisalat"\n+COPN: "405925","UNITECH"\n+COPN: "405926","UNITECH"\n+COPN: "405927","UNITECH"\n+COPN: "405928","UNITECH"\n+COPN: "405929","UNITECH"\n+COPN: "405932","VIDEOCON"\n+COPN: "41001","Mobilink"\n+COPN: "41003","UFONE"\n+COPN: "41004","ZONG"\n+COPN: "41006","TELENOR"\n+COPN: "41007","WaridTel"\n+COPN: "41201","AWCC"\n+COPN: "41220","ROSHAN"\n+COPN: "41240","MTN"\n+COPN: "41250","Etisalat"\n+COPN: "41301","MOBITEL"\n+COPN: "41302","DIALOG"\n+COPN: "41303","Etisalat"\n+COPN: "41305","airtel"\n+COPN: "41308","Hutch"\n+COPN: "41401","MPTGSM"\n+COPN: "41501","alfa"\n+COPN: "41503","MTC LIBAN"\n+COPN: "41505","OM"\n+COPN: "41601","Zain JO"\n+COPN: "41603","UMNIAH"\n+COPN: "41677","Orange JO"\n+COPN: "41701","SYRIATEL"\n+COPN: "41702","MTN"\n+COPN: "41800","ASIACELL"\n+COPN: "41805","ASIACELL"\n+COPN: "41820","zain IQ"\n+COPN: "41830","IRAQNA"\n+COPN: "41840","KOREK"\n+COPN: "41902","zain KW"\n+COPN: "41903","WATANIYA"\n+COPN: "41904","VIVA"\n+COPN: "42001","STC"\n+COPN: "42003","Mobily"\n+COPN: "42004","Zain SA"\n+COPN: "42101","SABAFON"\n+COPN: "42102","MTN"\n+COPN: "42104","Y"'),
        #              ('AT+CNAOP?',
        #               '+COPN: "42202","OMAN"\n+COPN: "42203","nawras"\n+COPN: "42402","ETISALAT"\n+COPN: "42403","du"\n+COPN: "42501","Orange IL"\n+COPN: "42502","Cellcom"\n+COPN: "42503","PCL"\n+COPN: "42505","JAWWAL"\n+COPN: "42506","WM"\n+COPN: "42507","Hot Mobile"\n+COPN: "42601","BATELCO"\n+COPN: "42602","Zain BH"\n+COPN: "42604","VIVA BH"\n+COPN: "42701","Ooredoo"\n+COPN: "42702","VF-QA"\n+COPN: "42806","GMOBILE"\n+COPN: "42888","UNTLMN"\n+COPN: "42899","MobiCom"\n+COPN: "42901","NT"\n+COPN: "42902","Ncell"\n+COPN: "43211","IR-TCI"\n+COPN: "43214","KIFZO"\n+COPN: "43219","MTCE"\n+COPN: "43220","IRN 20"\n+COPN: "43232","Taliya"\n+COPN: "43235","Irancell"\n+COPN: "43404","Beeline"\n+COPN: "43405","Ucell"\n+COPN: "43407","UZB MTS"\n+COPN: "43601","TCELL"\n+COPN: "43602","TCELL"\n+COPN: "43603","MegaFon"\n+COPN: "43604","Babilon"\n+COPN: "43605","BEELINE"\n+COPN: "43701","Beeline KG"\n+COPN: "43705","MEGACOM"\n+COPN: "43709","O!"\n+COPN: "43801","MTS TM"\n+COPN: "43802","TM CELL"\n+COPN: "44000","EMOBILE"\n+COPN: "44010","DOCOMO"\n+COPN: "44020","SoftBank"\n+COPN: "44050","KDDI"\n+COPN: "45001","Samsung"\n+COPN: "45002","KT"\n+COPN: "45005","SKT"\n+COPN: "45006","LG U+"\n+COPN: "45008","KT"\n+COPN: "45200","VN MOBIF"\n+COPN: "45201","VN MobiFon"\n+COPN: "45202","GPC"\n+COPN: "45204","VIETTEL"\n+COPN: "45205","VNMOBILE"\n+COPN: "45207","Gmobile"\n+COPN: "45400","CSL"\n+COPN: "45402","CSL"\n+COPN: "45403","3"\n+COPN: "45404","3(2G)"\n+COPN: "45406","SMC HK"\n+COPN: "45410","CSL"\n+COPN: "45412","CMHK"\n+COPN: "45413","CMHK"\n+COPN: "45415","SMC HK"\n+COPN: "45416","PCCW-HKT"\n+COPN: "45417","SMC HK"\n+COPN: "45418","CSL"\n+COPN: "45419","PCCW-HKT"\n+COPN: "45420","PCCW-HKT"\n+COPN: "45500","SMC MAC"\n+COPN: "45501","CTM"\n+COPN: "45503","3 Macau"\n+COPN: "45504","CTM"\n+COPN: "45505","3 Macau"\n+COPN: "45601","Cellcard"\n+COPN: "45602","Hello"\n+COPN: "45604","CADCOMMS"\n+COPN: "45605","SMART"\n+COPN: "45606","SMART"\n+COPN: "45608","Metfone"\n+COPN: "45609","Beeline"\n+COPN: "45618","Mfone"\n+COPN: "45701","LAO GSM"\n+COPN: "45702","ETLMNW"\n+COPN: "45703","UNITEL"\n+COPN: "45708","TIGO"\n+COPN: "46000","CMCC"\n+COPN: "46001","UNICOM"\n+COPN: "46002","CMCC"\n+COPN: "46003","CTCC"\n+COPN: "46005","CTCC"\n+COPN: "46006","UNICOM"\n+COPN: "46007","CMCC"\n+COPN: "46008","CMCC"\n+COPN: "46009","UNICOM"\n+COPN: "46011","CTCC"\n+COPN: "46601","FET"'),
        #              ('AT+CNAOP=Vodafone',
        #               '+COPN: "51505","SUN"\n+COPN: "51511","ACeS"\n+COPN: "52000","TH 3G+"\n+COPN: "52001","TH GSM"\n+COPN: "52002","TH CAT"\n+COPN: "52003","AIS 3G"\n+COPN: "52004","TRUE 3G+"\n+COPN: "52005","dtac"\n+COPN: "52015","TOT3G"\n+COPN: "52018","DTAC"\n+COPN: "52020","ACeS"\n+COPN: "52023","GSM 1800"\n+COPN: "52099","TRUE"\n+COPN: "52501","SingTel"\n+COPN: "52502","SingTel"\n+COPN: "52503","M1"\n+COPN: "52505","STARHUB"\n+COPN: "52507","CallZone"\n+COPN: "52802","b-mobile"\n+COPN: "52811","DSTCom"\n+COPN: "53001","voda NZ"\n+COPN: "53005","Telecom"\n+COPN: "53024","2degrees"\n+COPN: "53701","BMobile"\n+COPN: "53703","DIGICEL"\n+COPN: "53730","Digicel"\n+COPN: "53901","U-CALL"\n+COPN: "53988","Digicel"\n+COPN: "54001","BREEZE"\n+COPN: "54002","Bemobile"\n+COPN: "54101","SMILE"\n+COPN: "54105","Digicel"\n+COPN: "54201","VODAFONE"\n+COPN: "54202","DIGICEL"\n+COPN: "542542","Digicel "\n+COPN: "544110","BLUESKY"\n+COPN: "54509","KI-FRIG"\n+COPN: "54601","MOBNCL"\n+COPN: "54715","VF PF"\n+COPN: "54720","VINI"\n+COPN: "54801","KOKANET"\n+COPN: "54900","DIGICEL"\n+COPN: "54927","Bluesky"\n+COPN: "55001","FSMTC"\n+COPN: "55101","NTA"\n+COPN: "55201","PalauCel"\n+COPN: "55280","PLWPMC"\n+COPN: "60201","MobiNiL"\n+COPN: "60202","voda EG"\n+COPN: "60203","Etisalat"\n+COPN: "60301","Mobilis"\n+COPN: "60302","Djezzy"\n+COPN: "60303","Ooredoo"\n+COPN: "60400","MEDITEL"\n+COPN: "60401","IAM"\n+COPN: "60402","inwi"\n+COPN: "60501","Orange"\n+COPN: "60502","TUNTEL"\n+COPN: "60503","TUNSIANA"\n+COPN: "60600","L"\n+COPN: "60601","Al Madar"\n+COPN: "60701","GAMCEL"\n+COPN: "60702","AFRICELL"\n+COPN: "60703","GMCOMIUM"\n+COPN: "60704","QC"\n+COPN: "60801","ALIZE"\n+COPN: "60802","SENTEL"\n+COPN: "60803","Expresso"\n+COPN: "60901","MATTEL"\n+COPN: "60902","EMR"\n+COPN: "60910","MAURITEL"\n+COPN: "61001","MALITEL"\n+COPN: "61002","OML"\n+COPN: "61101","ORANGEGN"\n+COPN: "61102","LAGUI"\n+COPN: "61104","GNAreeba"\n+COPN: "61105","CellcomGN"\n+COPN: "61202","ETISALAT"\n+COPN: "61203","Orange"\n+COPN: "61204","KoZ"\n+COPN: "61205","MTN CI"\n+COPN: "61302","Celtel"\n+COPN: "61402","CELTEL"\n+COPN: "61403","ETISALAT"\n+COPN: "61404","Orange"\n+COPN: "61501","TGCELL"\n+COPN: "61503","ETISALAT"\n+COPN: "61602","ETISALAT"\n+COPN: "61603","MTN BENIN"\n+COPN: "61604","BBCOM"\n+COPN: "61605","GloBenin"\n+COPN: "61701","CELL +"\n+COPN: "61703","MTML"\n+COPN: "61710","EMTEL"\n+COPN: "61801","LoneStar"\n+COPN: "61804","Novafone"\n+COPN: "61807","Celcom"\n+COPN: "61900","SLE COMI"\n+COPN: "61901","CELTEL"\n+COPN: "61904","SLE COMIUM"\n+COPN: "61905","Africell"\n+COPN: "61907","GreenN "\n+COPN: "62001","MTN"\n+COPN: "62002","Vodafone"\n+COPN: "62003","tiGO GHANA"\n+COPN: "62006","Airtel"\n+COPN: "62007","Glo Ghana"\n+COPN: "62120","AirtelNG"\n+COPN: "62130","MTN-NG"\n+COPN: "62150","glo"\n+COPN: "62160","Etisalat"\n+COPN: "62201","CELTEL"\n+COPN: "62203","Tigo"\n+COPN: "62207","SALAM"\n+COPN: "62301","ETISALAT"\n+COPN: "62302","Telecel"\n+COPN: "62304","NL-RCA"\n+COPN: "62401","MTN CAM"\n+COPN: "62402","Orange"'),
        #              ('AT+CNAOP?',
        #               '+COPN: "62502","T+"\n+COPN: "62601","CSTmovel"\n+COPN: "62701","GETESA"\n+COPN: "62703","Muni-GQ"\n+COPN: "62801","LIBERTIS"\n+COPN: "62802","ETISALAT"\n+COPN: "62803","ZAIN"\n+COPN: "62902","AZUR COG"\n+COPN: "62907","WARIDRC"\n+COPN: "62910","MTN-CG"\n+COPN: "63001","VODACOM"\n+COPN: "63002","CELTEL"\n+COPN: "63005","SCELL"\n+COPN: "63086","Orange"\n+COPN: "63088","Smart"\n+COPN: "63089","TIGO"\n+COPN: "63090","AFRICELL"\n+COPN: "63102","UNITEL"\n+COPN: "63202","MTN"\n+COPN: "63203","ORANGE BS"\n+COPN: "63301","C&W SEY"\n+COPN: "63310","AIRTEL"\n+COPN: "63401","Zain SD"\n+COPN: "63402","MTN"\n+COPN: "63405","Vivacell"\n+COPN: "63510","MTN Rwanda"\n+COPN: "63513","TIGO RW"\n+COPN: "63514","AR"\n+COPN: "63601","ET-MTN"\n+COPN: "63701","Tele"\n+COPN: "63704","SOMAFONE"\n+COPN: "63720","SOMNET"\n+COPN: "63730","Golis"\n+COPN: "63740","MONTYSOM"\n+COPN: "63771","SOMTEL"\n+COPN: "63782","Telsom"\n+COPN: "63801","EVATIS"\n+COPN: "63902","SAF-COM"\n+COPN: "63903","Airtel"\n+COPN: "63907","GSMTKL"\n+COPN: "64002","TIGO"\n+COPN: "64003","ZANTEL"\n+COPN: "64004","VodaCom"\n+COPN: "64005","celtel"\n+COPN: "64008","Smart TZA"\n+COPN: "64101","CELTEL"\n+COPN: "64110","MTN-UG"\n+COPN: "64111","UTL"\n+COPN: "64114","OUL"\n+COPN: "64122","WaridTel"\n+COPN: "64201","EWB"\n+COPN: "64202","TEMPO-AF"\n+COPN: "64203","ONATEL"\n+COPN: "64207","SMART"\n+COPN: "64282","BDITL"\n+COPN: "64301","mCel"\n+COPN: "64303","MOVITEL"\n+COPN: "64304","VodaCom"\n+COPN: "64501","CELTEL"\n+COPN: "64502","MTN ZM"\n+COPN: "64601","ZAIN"\n+COPN: "64602","OrangeMG"\n+COPN: "64604","TELMA"\n+COPN: "64700","Orange"\n+COPN: "64702","OUTREMER"\n+COPN: "64710","SFR RU"\n+COPN: "64801","NETONE"\n+COPN: "64803","TELECEL"\n+COPN: "64804","ECONET"\n+COPN: "64901","MTCNAM"\n+COPN: "64903","tnmobile"\n+COPN: "65001","TNM"\n+COPN: "65010","CELTEL"\n+COPN: "65101","Vodacom-LS"\n+COPN: "65102","ETL"\n+COPN: "65201","MASCOM"\n+COPN: "65202","Orange"\n+COPN: "65204","beMOBILE"\n+COPN: "65310","SwaziMTN"\n+COPN: "65401","HURI"\n+COPN: "65501","VODA"\n+COPN: "65502","TelkomSA"\n+COPN: "65507","Cell C"\n+COPN: "65510","MTN"\n+COPN: "65902","MTN"\n+COPN: "65903","Gemtel"\n+COPN: "65904","Vivacell"'),
        #              ('AT+CNAOP=27404',
        #               '+COPN: "70267","BTL"\n+COPN: "70401","ClaroGTM"\n+COPN: "70402","COMCEL"\n+COPN: "70403","Movistar"\n+COPN: "70601","ClaroSLV"\n+COPN: "70602","DIGICEL"\n+COPN: "70603","TM"\n+COPN: "70604","movistar"\n+COPN: "70801","ClaroHND"\n+COPN: "70802","CELTEL"\n+COPN: "70830","HT - 200"\n+COPN: "71021","ClaroNIC"\n+COPN: "71073","ClaroNIC"\n+COPN: "710300","movistar"\n+COPN: "71200","I.C.E."\n+COPN: "71201","I.C.E."\n+COPN: "71202","I.C.E."\n+COPN: "71203","CLARO CR"\n+COPN: "71204","Movistar"\n+COPN: "71401","PANCW"\n+COPN: "71403","CLARO PA"\n+COPN: "71404","DIGICEL"\n+COPN: "71420","Movistar"\n+COPN: "71606","MOVISTAR"\n+COPN: "71610","ClaroPER"\n+COPN: "71615","VTP"\n+COPN: "71617","NXT3"\n+COPN: "72201","Movistar"\n+COPN: "72207","Movistar"\n+COPN: "72210","Movistar"\n+COPN: "72234","AR TP"\n+COPN: "72236","AR TP"\n+COPN: "722310","CLARO AR"\n+COPN: "722341","AR TP"\n+COPN: "72402","TIM"\n+COPN: "72403","TIM"\n+COPN: "72404","TIM"\n+COPN: "72405","Claro"\n+COPN: "72406","VIVO"\n+COPN: "72410","VIVO"\n+COPN: "72411","VIVO"\n+COPN: "72415","SCTL"\n+COPN: "72416","Oi"\n+COPN: "72423","VIVO"\n+COPN: "72424","AMAZONIA"\n+COPN: "72431","Oi"\n+COPN: "72432","CTBC"\n+COPN: "72433","CTBC"\n+COPN: "72434","CTBC"\n+COPN: "72439","Nextel 3G"\n+COPN: "73001","ENTEL"\n+COPN: "73002","Movistar"\n+COPN: "73003","ClaroCHL"\n+COPN: "73007","Movistar"\n+COPN: "73008","VTR"\n+COPN: "73009","Nextel3G"\n+COPN: "73010","ENTEL"\n+COPN: "730730","Movistar"\n+COPN: "73200","Comcel S"\n+COPN: "732101","Claro"\n+COPN: "732103","TIGO COL"\n+COPN: "732111","TIGO COL"\n+COPN: "732123","Movistar"\n+COPN: "73401","DIGITEL"\n+COPN: "73402","DIGITEL"\n+COPN: "73403","DIGITEL"\n+COPN: "73404","movistar"\n+COPN: "73406","Movilnet"\n+COPN: "73601","VIVA"\n+COPN: "73602","EMOVIL"\n+COPN: "73603","Telecel"\n+COPN: "73801","DIGICEL"\n+COPN: "73802","CLNKPLS"\n+COPN: "738592","CLNKPLS"\n+COPN: "74000","Movistar"\n+COPN: "74001","CLARO"\n+COPN: "74002","CNT"\n+COPN: "74401","HPGYSA"\n+COPN: "74402","CLARO PY"\n+COPN: "74404","TIGO"\n+COPN: "74405","Personal"\n+COPN: "74602","TeleG"\n+COPN: "74603","DIGICEL"\n+COPN: "74604","UNIQA"\n+COPN: "74801","Antel"\n+COPN: "74807","Movistar"\n+COPN: "74810","CLARO UY"\n+COPN: "75001","C&W FLK"\n+COPN: "79502","TM CELL"\n+COPN: "90105","Thuraya"\n+COPN: "90106","Thuraya"\n+COPN: "90111","INX"\n+COPN: "90112","MCP"\n+COPN: "90114","AeroMob"\n+COPN: "90115","OnAir"\n+COPN: "90118","WMS"\n+COPN: "90121","Seanet"\n+COPN: "90126","TIM@sea"\nOK\n+COPN: "20201","C-OTE"\n+COPN: "20205","voda GR"\n+COPN: "20209","WIND"\n+COPN: "20210","WIND"\n+COPN: "20402","Tele2"\n+COPN: "20404","voda NL"\n+COPN: "20408","NL KPN"\n+COPN: "20412","NL Tlfrt"\n+COPN: "20416","TMO NL"\n+COPN: "20601","PROXI"\n+COPN: "20610","mobi*"\n+COPN: "20620","BASE"\n+COPN: "20801","Orange"\n+COPN: "20802","Contact"\n+COPN: "20809","SFR"\n+COPN: "20810","SFR"\n+COPN: "20811","SFR"\n+COPN: "20813","Contact"\n+COPN: "20815","Free"\n+COPN: "20820","BYTEL"\n+COPN: "20888","Contact"\n+COPN: "21201","vala"\n+COPN: "21210","MONACO"\n+COPN: "21303","M-AND"\n+COPN: "21401","voda ES"\n+COPN: "21403","Orange"\n+COPN: "21404","YOIGO"\n+COPN: "21407","Movistar"\n+COPN: "21601","TelenorH"\n+COPN: "21630","THU"\n+COPN: "21670","voda HU"\n+COPN: "21803","HT ERONET"\n+COPN: "21805","m:tel"\n+COPN: "21890","BHMobile"\n+COPN: "21901","HT HR"\n+COPN: "21902","Tele2 HR"\n+COPN: "21910","VIP"\n+COPN: "22001","Telenor"\n+COPN: "22002","ProMonte"\n+COPN: "22003","MTS"\n+COPN: "22004","TMO CG"\n+COPN: "22005","Vip SRB"'),
        #              ('AT+CNAOP?',
        #               '+COPN: "22201","TIM"\n+COPN: "22210","voda IT"\n+COPN: "22288","I WIND"\n+COPN: "22299","3 ITA"\n+COPN: "22601","VF-RO"\n+COPN: "22603","COSMOTE"\n+COPN: "22605","Digi"\n+COPN: "22610","ORANGE"\n+COPN: "22801","Swisscom"\n+COPN: "22802","Sunrise"\n+COPN: "22803","Orange"\n+COPN: "22807","In&Phone"\n+COPN: "22815","OnAir"\n+COPN: "23001","TMO CZ"\n+COPN: "23002","O2 - CZ"\n+COPN: "23003","Vodafone"\n+COPN: "23101","Orange"\n+COPN: "23102","Telekom"\n+COPN: "23106","O2 - SK"\n+COPN: "23201","A1"\n+COPN: "23203","TMA"\n+COPN: "23205","3 AT"\n+COPN: "23207","telering"\n+COPN: "23210","3 AT"\n+COPN: "23212","A1"\n+COPN: "23401","UK01"\n+COPN: "23403","ATL-VOD"\n+COPN: "23407","C&W UK"\n+COPN: "23410","O2 - UK"\n+COPN: "23415","voda UK"\n+COPN: "23419","PMN"\n+COPN: "23420","3 UK"\n+COPN: "23428","Marathon"\n+COPN: "23430","EE"\n+COPN: "23431","EE"\n+COPN: "23432","EE"\n+COPN: "23433","EE"\n+COPN: "23450","JT"\n+COPN: "23455","Sure"\n+COPN: "23458","MANX"\n+COPN: "23801","TDC Mobil"\n+COPN: "23802","TelenoDK"\n+COPN: "23806","3 DK"\n+COPN: "23820","Telia"\n+COPN: "23866","TT DK"\n+COPN: "23877","TelenoDK"\n+COPN: "24001","TELIA"\n+COPN: "24002","3 SE"\n+COPN: "24004","SWE"\n+COPN: "24005","Sweden3G"\n+COPN: "24007","Tele2 SE"\n+COPN: "24008","TelenorS"\n+COPN: "24024","MobileS"\n+COPN: "24201","TELENOR"\n+COPN: "24202","NetCom"\n+COPN: "24204","Mobile N"\n+COPN: "24205","Mobile N"\n+COPN: "24403","DNA"\n+COPN: "24405","elisa"\n+COPN: "24412","DNA"\n+COPN: "24414","FI AMT"\n+COPN: "24491","SONERA"\n+COPN: "24601","OMT"\n+COPN: "24602","BITE"\n+COPN: "24603","Tele2 LT"\n+COPN: "24701","LMT"\n+COPN: "24702","Tele2 LV"\n+COPN: "24705","BITE LV"\n+COPN: "24801","EMT"\n+COPN: "24802","elisa"\n+COPN: "24803","Tele2 EE"\n+COPN: "25001","MTS"\n+COPN: "25002","MegaFon"\n+COPN: "25003","RTC"\n+COPN: "25004","RUS_SCN"\n+COPN: "25005","RTC"\n+COPN: "25007","SMARTS"\n+COPN: "25010","DTC"\n+COPN: "25012","RTC"\n+COPN: "25013","KUGSM"\n+COPN: "25015","SMARTS"\n+COPN: "25016","NTC"\n+COPN: "25017","RTC"\n+COPN: "25019","INDIGO"\n+COPN: "25020","TELE2 RU"\n+COPN: "25028","Beeline"'),
        #              ('AT+CNAOP=Viking',
        #               '+COPN: "25037","KODOTEL"\n+COPN: "25038","RTC"\n+COPN: "25039","RTC"\n+COPN: "25099","Beeline"\n+COPN: "25501","MTS UKR"\n+COPN: "25502","Beeline"\n+COPN: "25503","UA-KS"\n+COPN: "25505","GT"\n+COPN: "25506","life:)"\n+COPN: "25507","TriMob"\n+COPN: "25701","VELCOM"\n+COPN: "25702","MTS"\n+COPN: "25704","life:) BY"\n+COPN: "25901","Orange"\n+COPN: "25902","MDCELL"\n+COPN: "25905","UNITE"\n+COPN: "26001","PLUS"\n+COPN: "26002","TM PL"\n+COPN: "26003","Orange"\n+COPN: "26004","Tele2"\n+COPN: "26006","Play"\n+COPN: "26007","Premium"\n+COPN: "26008","E-Telko"\n+COPN: "26016","Mobyland"\n+COPN: "26017","Aero2"\n+COPN: "26201","TDG"\n+COPN: "26202","Vodafone"\n+COPN: "26203","E-Plus"\n+COPN: "26207","o2 - de"\n+COPN: "26208","o2 - de"\n+COPN: "26213","MobilCom"\n+COPN: "26601","GIBTEL"\n+COPN: "26606","CTS"\n+COPN: "26609","Shine"\n+COPN: "26801","voda P"\n+COPN: "26803","OPTIM"\n+COPN: "26806","P MEO"\n+COPN: "27001","Post"\n+COPN: "27077","TANGO"\n+COPN: "27099","Orange"\n+COPN: "27201","voda IE"\n+COPN: "27202","O2-IRL"\n+COPN: "27203","METEOR"\n+COPN: "27205","3 IRL"\n+COPN: "27401","Siminn"\n+COPN: "27402","Vodafone"\n+COPN: "27404","Viking"\n+COPN: "27408","On-waves"\n+COPN: "27411","NOVA"\n+COPN: "27412","Siminn"\n+COPN: "27601","A M C"\n+COPN: "27602","Voda AL"\n+COPN: "27603","EAGLE AL"\n+COPN: "27604","PLUS AL"\n+COPN: "27801","voda MT"\n+COPN: "27821","gomobile"\n+COPN: "27877","MT"\n+COPN: "28001","CYTAVODA"\n+COPN: "28010","MTN"\n+COPN: "28201","GCELL"\n+COPN: "28202","MAGTI"\n+COPN: "28204","BEELINE"\n+COPN: "28300","MTS Arm"\n+COPN: "28301","Beeline"\n+COPN: "28305","MTS Arm"\n+COPN: "28310","Orange"\n+COPN: "28401","Mtel"\n+COPN: "28403","Vivacom"\n+COPN: "28405","GLOBUL"\n+COPN: "28601","TCELL"\n+COPN: "28602","VF TR"\n+COPN: "28603","AVEA"\n+COPN: "28801","FT-GSM"\n+COPN: "28802","VODAFONE"\n+COPN: "29001","TELE GRL"\n+COPN: "29201","SMT"\n+COPN: "29340","Si.mobil"\n+COPN: "29341","MOBITEL"\n+COPN: "29364","T-2"\n+COPN: "29370","TUS"\n+COPN: "29401","TMO MK"\n+COPN: "29402","ONE"\n+COPN: "29403","Vip MKD"\n+COPN: "29501","Swiss FL"\n+COPN: "29502","OFL"\n+COPN: "29505","FL1"\n+COPN: "29577","Alpmobil"\n+COPN: "29701","Telenor"\n+COPN: "29702","T.me"\n+COPN: "302066","MTS"\n+COPN: "302072","ROGERS"\n+COPN: "302220","TELUS"\n+COPN: "302270","Eastlink"\n+COPN: "302320","Mobilicity"\n+COPN: "302340","Execulink"\n+COPN: "302370","Fido"\n+COPN: "302380","DMTS"\n+COPN: "302490","WIND"\n+COPN: "302610","Bell"\n+COPN: "302660","MTS"\n+COPN: "302720","ROGERS"\n+COPN: "302730","TStarSol"\n+COPN: "302770","RuralCom"\n+COPN: "302780","SaskTel"\n+COPN: "302880","FastRoam"\n+COPN: "302940","Wightman"\n+COPN: "30801","AMERIS"\n+COPN: "310000","CBW"\n+COPN: "310002","NEPW"\n+COPN: "310009","NEPW"\n+COPN: "310020","UnionTel"\n+COPN: "310030","CENT USA"\n+COPN: "310031","T-Mobile"\n+COPN: "310032","IT&E"\n+COPN: "310046","SIMMETRY"\n+COPN: "310070","AT&T"\n+COPN: "310080","Corr"\n+COPN: "310090","AT&T"\n+COPN: "310100","PLATEAU"\n+COPN: "310120","Sprint"\n+COPN: "310140","GTA"\n+COPN: "310150","AT&T"\n+COPN: "310160","T-Mobile"\n+COPN: "310170","AT&T"\n+COPN: "310190","D-HARBOR"\n+COPN: "310200","T-Mobile"\n+COPN: "310210","T-Mobile"\n+COPN: "310220","T-Mobile"\n+COPN: "310230","T-Mobile"\n+COPN: "310240","T-Mobile"\n+COPN: "310250","T-Mobile"'),
        #              ('AT+CNAOP?',
        #               '+COPN: "310270","T-Mobile"\n+COPN: "310290","NEPW"\n+COPN: "310300","Big Sky"\n+COPN: "310310","T-Mobile"\n+COPN: "310320","Cell"\n+COPN: "310340","WestLink"\n+COPN: "310380","AT&T"\n+COPN: "310390","CELL 1 ET"\n+COPN: "310400","iCAN_GSM"\n+COPN: "310410","AT&T"\n+COPN: "310420","CBW"\n+COPN: "310450","NECCI"\n+COPN: "310460","USA1L"\n+COPN: "310470","DOCOMOPA"\n+COPN: "310490","SunCom"\n+COPN: "310530","IWS"\n+COPN: "310560","AT&T"\n+COPN: "310570","Chinook"\n+COPN: "310580","T-Mobile"\n+COPN: "310590","Verizon"\n+COPN: "310630","AMERLINK"\n+COPN: "310640","ARDGMC"\n+COPN: "310650","Jasper"\n+COPN: "310660","T-Mobile"\n+COPN: "310680","AT&T"\n+COPN: "310690","IMMIX"\n+COPN: "310710","ASTAC"\n+COPN: "310730","USCC"\n+COPN: "310740","OTZ"\n+COPN: "310770","IWS"\n+COPN: "310800","T-Mobile"\n+COPN: "310840","telna"\n+COPN: "310870","PACE"\n+COPN: "310880","ACSIAC"\n+COPN: "310890","Verizon"\n+COPN: "310950","XIT"\n+COPN: "310980","AT&T"\n+COPN: "311000","Mid-Tex"\n+COPN: "311001","WILKES"\n+COPN: "311005","WILKES"\n+COPN: "311030","Indigo"\n+COPN: "311040","Commnet"\n+COPN: "311080","PINECell"\n+COPN: "311090","SXLP"\n+COPN: "311150","WILKES"\n+COPN: "311170","Broadpoint"\n+COPN: "311180","WCW"\n+COPN: "311190","C1ECI"\n+COPN: "311240","CWCI"\n+COPN: "311260",""\n+COPN: "311310","LamarCel"\n+COPN: "311330","BTW"\n+COPN: "311360","STELERA"\n+COPN: "311370","GCI"\n+COPN: "311380","AT&T"\n+COPN: "311410","AT&T"\n+COPN: "311480","Verizon"\n+COPN: "311500","MOSAIC"\n+COPN: "311530","USANW"\n+COPN: "311540","ProxMo"\n+COPN: "311580","USCC"\n+COPN: "311680","Green Fly"\n+COPN: "311710","NEWN"\n+COPN: "311720","MainePCS"\n+COPN: "311730","ProxMo"\n+COPN: "311940","CLEAR"\n+COPN: "31260","CvgCo"\n+COPN: "312230","SRTW"\n+COPN: "312260","USACL"\n+COPN: "330110","Claro"\n+COPN: "330120","Open Mob"\n+COPN: "33403","movistar"\n+COPN: "33409","Nextel3G"\n+COPN: "33420","TELCEL"\n+COPN: "33450","Iusacell"\n+COPN: "33490","Nextel3G"\n+COPN: "338005","DIGICEL"\n+COPN: "338050","DIGICEL"\n+COPN: "338070","ClaroJam"\n+COPN: "338180","LIME"\n+COPN: "34001","Orange"\n+COPN: "34002","ONLY"\n+COPN: "34003","CHIPPIE"\n+COPN: "34008","DAUPHIN"\n+COPN: "34020","DigicelF"\n+COPN: "342600","LIME"\n+COPN: "342750","DIGICEL"\n+COPN: "344030","imobile"\n+COPN: "344920","LIME"\n+COPN: "344930","Cingular"'),
        #              ('AT+CNAOP=27408',
        #               '+COPN: "348170","LIME"\n+COPN: "348570","CCTBVI"\n+COPN: "35000","CELLONE"\n+COPN: "35002","M3 WIREL"\n+COPN: "35010","Cingular"\n+COPN: "352030","DIGICEL"\n+COPN: "352110","LIME"\n+COPN: "354860","LIME"\n+COPN: "356110","LIME"\n+COPN: "358050","DIGICEL"\n+COPN: "358110","LIME"\n+COPN: "360070","DIGICEL"\n+COPN: "360110","LIME"\n+COPN: "36251","Telcell"\n+COPN: "36269","CT GSM"\n+COPN: "36291","CHIPPIE"\n+COPN: "362951","CHIPPIE"\n+COPN: "36301","SETARGSM"\n+COPN: "36320","DIGICEL"\n+COPN: "36439","BaTelCel"\n+COPN: "365840","LIME"\n+COPN: "366020","Cingular"\n+COPN: "366110","LIME"\n+COPN: "36801","CUBACEL"\n+COPN: "37001","Orange"\n+COPN: "37002","ClaroDOM"\n+COPN: "37004","VIVA"\n+COPN: "37201","VOILA"\n+COPN: "37203","Natcom"\n+COPN: "37412","TSTT"\n+COPN: "376350","LIME"\n+COPN: "376360","ICOM TCI"\n+COPN: "40001","ACELL"\n+COPN: "40002","BAKCELL"\n+COPN: "40004","Nar"\n+COPN: "40101","Beeline"\n+COPN: "40102","KCELL"\n+COPN: "40107","ALTEL"\n+COPN: "40177","NEO"\n+COPN: "40211","B-Mobile"\n+COPN: "40277","TASHICELL"\n+COPN: "40401","Vodafone"\n+COPN: "40402","airtel"\n+COPN: "40403","airtel"\n+COPN: "40404","IDEA"\n+COPN: "40405","Vodafone"\n+COPN: "40407","IDEA"\n+COPN: "40409","RELIANCE"\n+COPN: "40410","airtel"\n+COPN: "40411","Vodafone"\n+COPN: "40412","IDEA"\n+COPN: "40413","Vodafone"\n+COPN: "40414","IDEA"\n+COPN: "40415","Vodafone"\n+COPN: "40416","airtel"\n+COPN: "40417","AIRCEL"\n+COPN: "40418","RELIANCE"\n+COPN: "40419","IDEA"\n+COPN: "40420","Vodafone"\n+COPN: "40421","BPL MOBILE"\n+COPN: "40422","IDEA"\n+COPN: "40424","IDEA"\n+COPN: "40425","AIRCEL"\n+COPN: "40427","Vodafone"\n+COPN: "40428","AIRCEL"\n+COPN: "40429","AIRCEL"\n+COPN: "40430","Vodafone"\n+COPN: "40431","airtel"\n+COPN: "40433","AIRCEL"\n+COPN: "40434","CellOne"\n+COPN: "40435","AIRCEL"\n+COPN: "40436","RELIANCE"\n+COPN: "40437","AIRCEL"\n+COPN: "40438","CellOne"\n+COPN: "40440","airtel"\n+COPN: "40441","AIRCEL"\n+COPN: "40442","AIRCEL"\n+COPN: "40443","Vodafone"\n+COPN: "40444","IDEA"\n+COPN: "40445","airtel"\n+COPN: "40446","Vodafone"\n+COPN: "40449","airtel"\n+COPN: "40450","RELIANCE"\n+COPN: "40451","CellOne"\n+COPN: "40452","RELIANCE"\n+COPN: "40453","CellOne"\n+COPN: "40454","CellOne"\n+COPN: "40455","CellOne"\n+COPN: "40456","IDEA"\n+COPN: "40457","CellOne"\n+COPN: "40458","CellOne"\n+COPN: "40459","CellOne"\n+COPN: "40460","Vodafone"\n+COPN: "40462","CellOne"\n+COPN: "40464","CellOne"\n+COPN: "40466","CellOne"\n+COPN: "40467","RELIANCE"\n+COPN: "40468","DOLPHIN"\n+COPN: "40469","DOLPHIN"\n+COPN: "40470","airtel"\n+COPN: "40471","CellOne"\n+COPN: "40472","CellOne"\n+COPN: "40473","CellOne"\n+COPN: "40474","CellOne"\n+COPN: "40475","CellOne"\n+COPN: "40476","CellOne"\n+COPN: "40477","CellOne"\n+COPN: "40478","IDEA"\n+COPN: "40479","CellOne"\n+COPN: "40480","CellOne"\n+COPN: "40481","CellOne"\n+COPN: "40482","IDEA"\n+COPN: "40483","Reliance"\n+COPN: "40484","Vodafone"\n+COPN: "40485","RELIANCE"\n+COPN: "40486","Vodafone"\n+COPN: "40487","IDEA"\n+COPN: "40488","Vodafone"\n+COPN: "40489","IDEA"\n+COPN: "40490","airtel"\n+COPN: "40491","Aircel"\n+COPN: "40492","airtel"\n+COPN: "40493","airtel"\n+COPN: "40494","airtel"\n+COPN: "40495","airtel"\n+COPN: "40496","airtel"\n+COPN: "40497","airtel"\n+COPN: "40498","airtel"\n+COPN: "40501","Reliance"\n+COPN: "40505","Reliance"\n+COPN: "40506","Reliance"\n+COPN: "40507","Reliance"'),
        #              ('AT+CNAOP?',
        #               '+COPN: "40510","Reliance"\n+COPN: "40511","Reliance"\n+COPN: "40513","Reliance"\n+COPN: "40515","Reliance"\n+COPN: "40518","Reliance"\n+COPN: "40519","Reliance"\n+COPN: "40520","Reliance"\n+COPN: "40521","Reliance"\n+COPN: "40522","Reliance"\n+COPN: "405025","TATA DO"\n+COPN: "405027","TATA DO"\n+COPN: "405029","TATA DO"\n+COPN: "405030","TATA DO"\n+COPN: "405031","TATA DO"\n+COPN: "405032","TATA DO"\n+COPN: "405034","TATA DO"\n+COPN: "405035","TATA DO"\n+COPN: "405036","TATA DO"\n+COPN: "405037","TATA DO"\n+COPN: "405038","TATA DO"\n+COPN: "405039","TATA DO"\n+COPN: "405041","TATA DO"\n+COPN: "405042","TATA DO"\n+COPN: "405043","TATA DO"\n+COPN: "405044","TATA DO"\n+COPN: "405045","TATA DO"\n+COPN: "405046","TATA DO"\n+COPN: "405047","TATA DO"\n+COPN: "40551","airtel"\n+COPN: "40552","airtel"\n+COPN: "40553","airtel"\n+COPN: "40554","airtel"\n+COPN: "40555","airtel"\n+COPN: "40556","airtel"\n+COPN: "40566","Vodafone"\n+COPN: "40567","Vodafone"\n+COPN: "40570","IDEA"\n+COPN: "405750","Vodafone"\n+COPN: "405751","Vodafone"\n+COPN: "405752","Vodafone"\n+COPN: "405753","Vodafone"\n+COPN: "405754","Vodafone"\n+COPN: "405755","Vodafone"\n+COPN: "405756","Vodafone"\n+COPN: "405799","IDEA"\n+COPN: "405800","Aircel"\n+COPN: "405801","Aircel"\n+COPN: "405802","Aircel"\n+COPN: "405803","Aircel"\n+COPN: "405804","Aircel"\n+COPN: "405805","Aircel"\n+COPN: "405806","Aircel"\n+COPN: "405807","Aircel"\n+COPN: "405808","Aircel"\n+COPN: "405809","Aircel "\n+COPN: "405810","Aircel"\n+COPN: "405811","Aircel"\n+COPN: "405812","Aircel"\n+COPN: "405813","UNITECH"\n+COPN: "405814","UNITECH"\n+COPN: "405815","UNITECH"\n+COPN: "405816","UNITECH"\n+COPN: "405817","UNITECH"\n+COPN: "405818","UNITECH"\n+COPN: "405819","UNITECH"\n+COPN: "405820","UNITECH"\n+COPN: "405821","UNITECH"\n+COPN: "405822","UNITECH"\n+COPN: "405823","VIDEOCON"\n+COPN: "405824","VIDEOCON"\n+COPN: "405825","VIDEOCON"\n+COPN: "405827","VIDEOCON"\n+COPN: "405828","VIDEOCON"\n+COPN: "405829","VIDEOCON"\n+COPN: "405830","VIDEOCON"\n+COPN: "405831","VIDEOCON"\n+COPN: "405832","VIDEOCON"\n+COPN: "405833","VIDEOCON"\n+COPN: "405834","VIDEOCON"\n+COPN: "405835","VIDEOCON"\n+COPN: "405836","VIDEOCON"\n+COPN: "405837","VIDEOCON"\n+COPN: "405838","VIDEOCON"\n+COPN: "405839","VIDEOCON"\n+COPN: "405840","VIDEOCON"\n+COPN: "405841","VIDEOCON"\n+COPN: "405842","VIDEOCON"\n+COPN: "405843","VIDEOCON"\n+COPN: "405844","UNITECH"\n+COPN: "405845","IDEA"\n+COPN: "405846","IDEA"\n+COPN: "405848","IDEA"\n+COPN: "405849","IDEA"\n+COPN: "405850","IDEA"\n+COPN: "405852","IDEA"\n+COPN: "405853","IDEA"\n+COPN: "405854","LoopMobile"\n+COPN: "405855","LoopMobile"\n+COPN: "405856","LoopMobile"\n+COPN: "405857","LoopMobile"\n+COPN: "405858","LoopMobile"'),
        #              ('AT+CNAOP=On-waves',
        #               '+COPN: "405860","LoopMobile"\n+COPN: "405861","LoopMobile"\n+COPN: "405862","LoopMobile"\n+COPN: "405863","LoopMobile"\n+COPN: "405864","LoopMobile"\n+COPN: "405865","LoopMobile"\n+COPN: "405866","LoopMobile"\n+COPN: "405867","LoopMobile"\n+COPN: "405868","LoopMobile"\n+COPN: "405869","LoopMobile"\n+COPN: "405870","LoopMobile"\n+COPN: "405871","LoopMobile"\n+COPN: "405872","LoopMobile"\n+COPN: "405873","LoopMobile"\n+COPN: "405874","LoopMobile"\n+COPN: "405875","UNITECH"\n+COPN: "405876","UNITECH"\n+COPN: "405877","UNITECH"\n+COPN: "405878","UNITECH"\n+COPN: "405879","UNITECH"\n+COPN: "405880","UNITECH"\n+COPN: "405912","etisalat"\n+COPN: "405913","etisalat"\n+COPN: "405914","etisalat"\n+COPN: "405915","etisalat"\n+COPN: "405916","etisalat"\n+COPN: "405917","etisalat"\n+COPN: "405918","etisalat"\n+COPN: "405919","etisalat"\n+COPN: "405920","etisalat"\n+COPN: "405921","etisalat"\n+COPN: "405922","etisalat"\n+COPN: "405923","etisalat"\n+COPN: "405924","etisalat"\n+COPN: "405925","UNITECH"\n+COPN: "405926","UNITECH"\n+COPN: "405927","UNITECH"\n+COPN: "405928","UNITECH"\n+COPN: "405929","UNITECH"\n+COPN: "405932","VIDEOCON"\n+COPN: "41001","Mobilink"\n+COPN: "41003","UFONE"\n+COPN: "41004","ZONG"\n+COPN: "41006","TELENOR"\n+COPN: "41007","WaridTel"\n+COPN: "41201","AWCC"\n+COPN: "41220","ROSHAN"\n+COPN: "41240","MTN"\n+COPN: "41250","Etisalat"\n+COPN: "41301","MOBITEL"\n+COPN: "41302","DIALOG"\n+COPN: "41303","Etisalat"\n+COPN: "41305","airtel"\n+COPN: "41308","Hutch"\n+COPN: "41401","MPTGSM"\n+COPN: "41501","alfa"\n+COPN: "41503","MTC LIBAN"\n+COPN: "41505","OM"\n+COPN: "41601","Zain JO"\n+COPN: "41603","UMNIAH"\n+COPN: "41677","Orange JO"\n+COPN: "41701","SYRIATEL"\n+COPN: "41702","MTN"\n+COPN: "41800","ASIACELL"\n+COPN: "41805","ASIACELL"\n+COPN: "41820","zain IQ"\n+COPN: "41830","IRAQNA"\n+COPN: "41840","KOREK"\n+COPN: "41902","zain KW"\n+COPN: "41903","WATANIYA"\n+COPN: "41904","VIVA"\n+COPN: "42001","STC"\n+COPN: "42003","Mobily"\n+COPN: "42004","Zain SA"\n+COPN: "42101","SABAFON"\n+COPN: "42102","MTN"\n+COPN: "42104","Y"\n+COPN: "421700","Y"\n+COPN: "42202","OMAN"\n+COPN: "42203","nawras"\n+COPN: "42402","ETISALAT"\n+COPN: "42403","du"\n+COPN: "42501","Orange IL"\n+COPN: "42502","Cellcom"\n+COPN: "42503","PCL"\n+COPN: "42505","JAWWAL"\n+COPN: "42506","WM"\n+COPN: "42507","Hot Mobile"\n+COPN: "42601","BATELCO"\n+COPN: "42602","Zain BH"\n+COPN: "42604","VIVA BH"\n+COPN: "42701","Ooredoo"\n+COPN: "42702","VF-QA"\n+COPN: "42806","GMOBILE"\n+COPN: "42888","UNTLMN"\n+COPN: "42899","MobiCom"\n+COPN: "42901","NT"\n+COPN: "42902","Ncell"\n+COPN: "43211","IR-TCI"\n+COPN: "43214","KIFZO"\n+COPN: "43219","MTCE"\n+COPN: "43220","IRN 20"\n+COPN: "43232","Taliya"\n+COPN: "43235","Irancell"\n+COPN: "43404","Beeline"\n+COPN: "43405","Ucell"\n+COPN: "43407","UZB MTS"\n+COPN: "43601","TCELL"\n+COPN: "43602","TCELL"\n+COPN: "43603","MegaFon"\n+COPN: "43604","Babilon"\n+COPN: "43605","BEELINE"\n+COPN: "43701","Beeline KG"\n+COPN: "43705","MEGACOM"\n+COPN: "43709","O!"\n+COPN: "43801","MTS TM"\n+COPN: "43802","TM CELL"\n+COPN: "44000","EMOBILE"\n+COPN: "44010","DOCOMO"\n+COPN: "44020","SoftBank"\n+COPN: "44050","KDDI"\n+COPN: "45001","Samsung"\n+COPN: "45002","KT"\n+COPN: "45005","SKT"\n+COPN: "45006","LG U+"\n+COPN: "45008","KT"\n+COPN: "45200","VN MOBIF"\n+COPN: "45201","VN MobiFon"\n+COPN: "45202","GPC"\n+COPN: "45204","VIETTEL"\n+COPN: "45205","VNMOBILE"\n+COPN: "45207","Gmobile"'),
        #              ('AT+CNAOP?',
        #               '+COPN: "45402","CSL"\n+COPN: "45403","3"\n+COPN: "45404","3(2G)"\n+COPN: "45406","SMC HK"\n+COPN: "45410","CSL"\n+COPN: "45412","CMHK"\n+COPN: "45413","CMHK"\n+COPN: "45415","SMC HK"\n+COPN: "45416","PCCW-HKT"\n+COPN: "45417","SMC HK"\n+COPN: "45418","CSL"\n+COPN: "45419","PCCW-HKT"\n+COPN: "45420","PCCW-HKT"\n+COPN: "45500","SMC MAC"\n+COPN: "45501","CTM"\n+COPN: "45503","3 Macau"\n+COPN: "45504","CTM"\n+COPN: "45505","3 Macau"\n+COPN: "45601","Cellcard"\n+COPN: "45602","Hello"\n+COPN: "45604","CADCOMMS"\n+COPN: "45605","SMART"\n+COPN: "45606","SMART"\n+COPN: "45608","Metfone"\n+COPN: "45609","Beeline"\n+COPN: "45618","Mfone"\n+COPN: "45701","LAO GSM"\n+COPN: "45702","ETLMNW"\n+COPN: "45703","UNITEL"\n+COPN: "45708","TIGO"\n+COPN: "46000","CMCC"\n+COPN: "46001","UNICOM"\n+COPN: "46002","CMCC"\n+COPN: "46003","CTCC"\n+COPN: "46005","CTCC"\n+COPN: "46006","UNICOM"\n+COPN: "46007","CMCC"\n+COPN: "46008","CMCC"\n+COPN: "46009","UNICOM"\n+COPN: "46011","CTCC"\n+COPN: "46601","FET"\n+COPN: "46668","ACeS"\n+COPN: "46688","KGT"\n+COPN: "46689","VIBO"\n+COPN: "46692","Chunghwa"\n+COPN: "46693","TW MOB"\n+COPN: "46697","TWM"\n+COPN: "467005","KL-DPRK"\n+COPN: "47001","Grameen"\n+COPN: "47002","ROBIAXIATA"\n+COPN: "47003","B-LINK"\n+COPN: "47004","bMobile"\n+COPN: "47007","Airtel"\n+COPN: "47201","DHIRAAGU"\n+COPN: "47202","Ooredoo"\n+COPN: "50212","MY MAXIS"\n+COPN: "50213","CELCOM"\n+COPN: "50216","DiGi"\n+COPN: "50218","U MOBILE"\n+COPN: "50219","CELCOM"\n+COPN: "50501","Telstra"\n+COPN: "50502","Optus"\n+COPN: "50503","voda AU"\n+COPN: "50506","3TELSTRA"\n+COPN: "50510","NT"\n+COPN: "51000","ACeS"\n+COPN: "51001","INDOSAT"\n+COPN: "51008","AXIS"\n+COPN: "51010","T-SEL"\n+COPN: "51011","XL"\n+COPN: "51021","INDOSAT"\n+COPN: "51089","3"\n+COPN: "510510","Mobile-8"\n+COPN: "51402","TT"\n+COPN: "51501","ISLACOM"\n+COPN: "51502","GLOBE"\n+COPN: "51503","SMART"\n+COPN: "51505","SUN"\n+COPN: "51511","ACeS"\n+COPN: "52000","TH 3G+"\n+COPN: "52001","TH GSM"\n+COPN: "52002","TH CAT"\n+COPN: "52003","AIS 3G"\n+COPN: "52004","TRUE 3G+"\n+COPN: "52005","dtac"\n+COPN: "52015","TOT3G"\n+COPN: "52018","DTAC"'),
        #              ('AT+CNAOP=27411',
        #               '+COPN: "52023","GSM 1800"\n+COPN: "52099","TRUE"\n+COPN: "52501","SingTel"\n+COPN: "52502","SingTel"\n+COPN: "52503","M1"\n+COPN: "52505","STARHUB"\n+COPN: "52507","CallZone"\n+COPN: "52802","b-mobile"\n+COPN: "52811","DSTCom"\n+COPN: "53001","voda NZ"\n+COPN: "53005","Telecom"\n+COPN: "53024","2degrees"\n+COPN: "53701","BMobile"\n+COPN: "53703","DIGICEL"\n+COPN: "53730","Digicel"\n+COPN: "53901","U-CALL"\n+COPN: "53988","Digicel"\n+COPN: "54001","BREEZE"\n+COPN: "54002","Bemobile"\n+COPN: "54101","SMILE"\n+COPN: "54105","Digicel"\n+COPN: "54201","VODAFONE"\n+COPN: "54202","DIGICEL"\n+COPN: "542542","Digicel "\n+COPN: "544110","BLUESKY"\n+COPN: "54509","KI-FRIG"\n+COPN: "54601","MOBNCL"\n+COPN: "54715","VF PF"\n+COPN: "54720","VINI"\n+COPN: "54801","KOKANET"\n+COPN: "54900","DIGICEL"\n+COPN: "54927","Bluesky"\n+COPN: "55001","FSMTC"\n+COPN: "55101","NTA"\n+COPN: "55201","PalauCel"\n+COPN: "55280","PLWPMC"\n+COPN: "60201","MobiNiL"\n+COPN: "60202","voda EG"\n+COPN: "60203","Etisalat"\n+COPN: "60301","Mobilis"\n+COPN: "60302","Djezzy"\n+COPN: "60303","Ooredoo"\n+COPN: "60400","MEDITEL"\n+COPN: "60401","IAM"\n+COPN: "60402","inwi"\n+COPN: "60501","Orange"\n+COPN: "60502","TUNTEL"\n+COPN: "60503","TUNSIANA"\n+COPN: "60600","L"\n+COPN: "60601","Al Madar"\n+COPN: "60701","GAMCEL"\n+COPN: "60702","AFRICELL"\n+COPN: "60703","GMCOMIUM"\n+COPN: "60704","QC"\n+COPN: "60801","ALIZE"\n+COPN: "60802","SENTEL"\n+COPN: "60803","Expresso"\n+COPN: "60901","MATTEL"\n+COPN: "60902","EMR"\n+COPN: "60910","MAURITEL"\n+COPN: "61001","MALITEL"\n+COPN: "61002","OML"\n+COPN: "61101","ORANGEGN"\n+COPN: "61102","LAGUI"\n+COPN: "61104","GNAreeba"\n+COPN: "61105","CellcomGN"\n+COPN: "61202","ETISALAT"\n+COPN: "61203","Orange"\n+COPN: "61204","KoZ"\n+COPN: "61205","MTN CI"\n+COPN: "61302","Celtel"\n+COPN: "61402","CELTEL"\n+COPN: "61403","ETISALAT"\n+COPN: "61404","Orange"\n+COPN: "61501","TGCELL"\n+COPN: "61503","ETISALAT"\n+COPN: "61602","ETISALAT"\n+COPN: "61603","MTN BENIN"\n+COPN: "61604","BBCOM"\n+COPN: "61605","GloBenin"\n+COPN: "61701","CELL +"\n+COPN: "61703","MTML"\n+COPN: "61710","EMTEL"\n+COPN: "61801","LoneStar"\n+COPN: "61804","Novafone"\n+COPN: "61807","Celcom"\n+COPN: "61900","SLE COMI"\n+COPN: "61901","CELTEL"\n+COPN: "61904","SLE COMIUM"\n+COPN: "61905","Africell"\n+COPN: "61907","GreenN "\n+COPN: "62001","MTN"\n+COPN: "62002","Vodafone"\n+COPN: "62003","tiGO GHANA"\n+COPN: "62006","Airtel"\n+COPN: "62007","Glo Ghana"\n+COPN: "62120","AirtelNG"\n+COPN: "62130","MTN-NG"\n+COPN: "62150","glo"\n+COPN: "62160","Etisalat"\n+COPN: "62201","CELTEL"\n+COPN: "62203","Tigo"\n+COPN: "62207","SALAM"\n+COPN: "62301","ETISALAT"\n+COPN: "62302","Telecel"\n+COPN: "62304","NL-RCA"\n+COPN: "62401","MTN CAM"\n+COPN: "62402","Orange"\n+COPN: "62501","CMOVEL"\n+COPN: "62502","T+"\n+COPN: "62601","CSTmovel"\n+COPN: "62701","GETESA"\n+COPN: "62703","Muni-GQ"\n+COPN: "62801","LIBERTIS"\n+COPN: "62802","ETISALAT"\n+COPN: "62803","ZAIN"\n+COPN: "62902","AZUR COG"\n+COPN: "62907","WARIDRC"\n+COPN: "62910","MTN-CG"\n+COPN: "63001","VODACOM"\n+COPN: "63002","CELTEL"\n+COPN: "63005","SCELL"\n+COPN: "63086","Orange"\n+COPN: "63088","Smart"\n+COPN: "63089","TIGO"\n+COPN: "63090","AFRICELL"'),
        #              ('AT+CNAOP?',
        #               '+COPN: "63202","MTN"\n+COPN: "63203","ORANGE BS"\n+COPN: "63301","C&W SEY"\n+COPN: "63310","AIRTEL"\n+COPN: "63401","Zain SD"\n+COPN: "63402","MTN"\n+COPN: "63405","Vivacell"\n+COPN: "63510","MTN Rwanda"\n+COPN: "63513","TIGO RW"\n+COPN: "63514","AR"\n+COPN: "63601","ET-MTN"\n+COPN: "63701","Tele"\n+COPN: "63704","SOMAFONE"\n+COPN: "63720","SOMNET"\n+COPN: "63730","Golis"\n+COPN: "63740","MONTYSOM"\n+COPN: "63771","SOMTEL"\n+COPN: "63782","Telsom"\n+COPN: "63801","EVATIS"\n+COPN: "63902","SAF-COM"\n+COPN: "63903","Airtel"\n+COPN: "63907","GSMTKL"\n+COPN: "64002","TIGO"\n+COPN: "64003","ZANTEL"\n+COPN: "64004","VodaCom"\n+COPN: "64005","celtel"\n+COPN: "64008","Smart TZA"\n+COPN: "64101","CELTEL"\n+COPN: "64110","MTN-UG"\n+COPN: "64111","UTL"\n+COPN: "64114","OUL"\n+COPN: "64122","WaridTel"\n+COPN: "64201","EWB"\n+COPN: "64202","TEMPO-AF"\n+COPN: "64203","ONATEL"\n+COPN: "64207","SMART"\n+COPN: "64282","BDITL"\n+COPN: "64301","mCel"\n+COPN: "64303","MOVITEL"\n+COPN: "64304","VodaCom"\n+COPN: "64501","CELTEL"\n+COPN: "64502","MTN ZM"\n+COPN: "64601","ZAIN"\n+COPN: "64602","OrangeMG"\n+COPN: "64604","TELMA"\n+COPN: "64700","Orange"\n+COPN: "64702","OUTREMER"\n+COPN: "64710","SFR RU"\n+COPN: "64801","NETONE"\n+COPN: "64803","TELECEL"\n+COPN: "64804","ECONET"\n+COPN: "64901","MTCNAM"\n+COPN: "64903","tnmobile"\n+COPN: "65001","TNM"\n+COPN: "65010","CELTEL"\n+COPN: "65101","Vodacom-LS"\n+COPN: "65102","ETL"\n+COPN: "65201","MASCOM"\n+COPN: "65202","Orange"\n+COPN: "65204","beMOBILE"\n+COPN: "65310","SwaziMTN"\n+COPN: "65401","HURI"\n+COPN: "65501","VODA"\n+COPN: "65502","TelkomSA"\n+COPN: "65507","Cell C"\n+COPN: "65510","MTN"\n+COPN: "65902","MTN"\n+COPN: "65903","Gemtel"\n+COPN: "65904","Vivacell"\n+COPN: "65906","ZAIN SS"\n+COPN: "70267","BTL"\n+COPN: "70401","ClaroGTM"\n+COPN: "70402","COMCEL"\n+COPN: "70403","Movistar"\n+COPN: "70601","ClaroSLV"\n+COPN: "70602","DIGICEL"\n+COPN: "70603","TM"\n+COPN: "70604","movistar"\n+COPN: "70801","ClaroHND"\n+COPN: "70802","CELTEL"\n+COPN: "70830","HT - 200"\n+COPN: "71021","ClaroNIC"\n+COPN: "71073","ClaroNIC"\n+COPN: "710300","movistar"\n+COPN: "71200","I.C.E."\n+COPN: "71201","I.C.E."\n+COPN: "71202","I.C.E."\n+COPN: "71203","CLARO CR"\n+COPN: "71204","Movistar"\n+COPN: "71401","PANCW"\n+COPN: "71403","CLARO PA"\n+COPN: "71404","DIGICEL"\n+COPN: "71420","Movistar"'),
        #              ('AT+CNAOP=NOVA',
        #               '+COPN: "71610","ClaroPER"\n+COPN: "71615","VTP"\n+COPN: "71617","NXT3"\n+COPN: "72201","Movistar"\n+COPN: "72207","Movistar"\n+COPN: "72210","Movistar"\n+COPN: "72234","AR TP"\n+COPN: "72236","AR TP"\n+COPN: "722310","CLARO AR"\n+COPN: "722341","AR TP"\n+COPN: "72402","TIM"\n+COPN: "72403","TIM"\n+COPN: "72404","TIM"\n+COPN: "72405","Claro"\n+COPN: "72406","VIVO"\n+COPN: "72410","VIVO"\n+COPN: "72411","VIVO"\n+COPN: "72415","SCTL"\n+COPN: "72416","Oi"\n+COPN: "72423","VIVO"\n+COPN: "72424","AMAZONIA"\n+COPN: "72431","Oi"\n+COPN: "72432","CTBC"\n+COPN: "72433","CTBC"\n+COPN: "72434","CTBC"\n+COPN: "72439","Nextel 3G"\n+COPN: "73001","ENTEL"\n+COPN: "73002","Movistar"\n+COPN: "73003","ClaroCHL"\n+COPN: "73007","Movistar"\n+COPN: "73008","VTR"\n+COPN: "73009","Nextel3G"\n+COPN: "73010","ENTEL"\n+COPN: "730730","Movistar"\n+COPN: "73200","Comcel S"\n+COPN: "732101","Claro"\n+COPN: "732103","TIGO COL"\n+COPN: "732111","TIGO COL"\n+COPN: "732123","Movistar"\n+COPN: "73401","DIGITEL"\n+COPN: "73402","DIGITEL"\n+COPN: "73403","DIGITEL"\n+COPN: "73404","movistar"\n+COPN: "73406","Movilnet"\n+COPN: "73601","VIVA"\n+COPN: "73602","EMOVIL"\n+COPN: "73603","Telecel"\n+COPN: "73801","DIGICEL"\n+COPN: "73802","CLNKPLS"\n+COPN: "738592","CLNKPLS"\n+COPN: "74000","Movistar"\n+COPN: "74001","CLARO"\n+COPN: "74002","CNT"\n+COPN: "74401","HPGYSA"\n+COPN: "74402","CLARO PY"\n+COPN: "74404","TIGO"\n+COPN: "74405","Personal"\n+COPN: "74602","TeleG"\n+COPN: "74603","DIGICEL"\n+COPN: "74604","UNIQA"\n+COPN: "74801","Antel"\n+COPN: "74807","Movistar"\n+COPN: "74810","CLARO UY"\n+COPN: "75001","C&W FLK"\n+COPN: "79502","TM CELL"\n+COPN: "90105","Thuraya"\n+COPN: "90106","Thuraya"\n+COPN: "90111","INX"\n+COPN: "90112","MCP"\n+COPN: "90114","AeroMob"\n+COPN: "90115","OnAir"\n+COPN: "90118","WMS"\n+COPN: "90121","Seanet"\n+COPN: "90126","TIM@sea"\nOK\n+CME ERROR: Operation not supported\nERROR\nERROR\nERROR\nERROR\nERROR\nERROR\nERROR\nERROR\nERROR\nERROR\nERROR\nERROR\nERROR\nERROR\nERROR\nERROR\nERROR\nERROR'),
        #              ('AT+CNAOP?', 'ERROR'),
        #              ('AT+CNAOP=27412', 'ERROR'),
        #              ('AT+CNAOP?', 'ERROR'),
        #              ('AT+CNAOP=Siminn', 'ERROR'),
        #              ('AT+CNAOP?', 'ERROR'),
        #              ],
        # 1=ACCURATE -------------------------------------
        'AT+CREG?': ['network registration (CS)',
                     ('AT+CREG=?', '+CREG: (0-2)\nOK'),
                     ('AT+CREG', 'OK'),
                     ('AT+CREG?', '+CREG: 0,0\nOK'),
                     ('AT+CREG=0', 'OK'),
                     ('AT+CREG?', '+CREG: 0,0\nOK'),
                     ('AT+CREG=1', 'OK'),
                     ('AT+CREG?', '+CREG: 1,0\nOK'),
                     ('AT+CREG=2', 'OK'),
                     ('AT+CREG?', '+CREG: 2,0\nOK'),
                     ],
        'AT+CGREG?': ['GPRS registration (PS)',
                      ('AT+CGREG=?', '+CGREG: (0-2)\nOK'),
                      ('AT+CGREG', 'OK'),
                      ('AT+CGREG?', '+CGREG: 0,0\nOK'),
                      ('AT+CGREG=0', 'OK'),
                      ('AT+CGREG?', '+CGREG: 0,0\nOK'),
                      ('AT+CGREG=1', 'OK'),
                      ('AT+CGREG?', '+CGREG: 1,0\nOK'),
                      ('AT+CGREG=2', 'OK'),
                      ('AT+CGREG?', '+CGREG: 2,0,"0000","00000000"\nOK'),
                      ],
        'AT+CEREG?': ['EPS registration (LTE)',
                      ('AT+CEREG=?', '+CEREG: (0-2)\nOK'),
                      ('AT+CEREG', 'OK'),
                      ('AT+CEREG?', '+CEREG: 0,0\nOK'),
                      ('AT+CEREG=0', 'OK'),
                      ('AT+CEREG?', '+CEREG: 0,0\nOK'),
                      ('AT+CEREG=1', 'OK'),
                      ('AT+CEREG?', '+CEREG: 1,0\nOK'),
                      ('AT+CEREG=2', 'OK'),
                      ('AT+CEREG?', '+CEREG: 2,0,0000,00000000\nOK'),
                      ],
        'AT+CUSD?': ['USSD',
                     ('AT+CUSD=?', '+CUSD: (0-2)\nOK'),
                     ('AT+CUSD', 'OK'),
                     ('AT+CUSD?', '+CUSD: 0\nOK'),
                     ('AT+CUSD=0', 'OK'),
                     ('AT+CUSD?', '+CUSD: 0\nOK'),
                     ('AT+CUSD=1', 'OK'),
                     ('AT+CUSD?', '+CUSD: 1\nOK'),
                     ('AT+CUSD=2', 'OK'),
                     ('AT+CUSD?', '+CUSD: 1\nOK'),
                     ],
        'AT+CAOC?': ['advice of charge',
                     ('AT+CAOC=?', '+CAOC: (0-2)\nOK'),
                     ('AT+CAOC', 'ERROR'),
                     ('AT+CAOC?', '+CAOC: 2\nOK'),
                     ('AT+CAOC=0', '+CAOC:"000000"\nOK'),
                     ('AT+CAOC?', '+CAOC: 2\nOK'),
                     ('AT+CAOC=1', 'OK'),
                     ('AT+CAOC?', '+CAOC: 1\nOK'),
                     ('AT+CAOC=2', 'OK'),
                     ('AT+CAOC?', '+CAOC: 2\nOK'),
                     ],
        'AT+CSSN?': ['supplementary service notifications',
                     ('AT+CSSN=?', '+CSSN: (0-1),(0-1)\nOK'),
                     ('AT+CSSN', 'ERROR'),
                     ('AT+CSSN?', '+CSSN: 1,0\nOK'),
                     ('AT+CSSN=0', 'OK'),
                     ('AT+CSSN?', '+CSSN: 0,0\nOK'),
                     ('AT+CSSN=1', 'OK'),
                     ('AT+CSSN?', '+CSSN: 1,0\nOK'),
                     ],
        'AT+CPSI?': ['UE system information',
                     ('AT+CPSI=?', 'OK'),
                     ('AT+CPSI', 'ERROR'),
                     ('AT+CPSI?', '+CPSI: NO SERVICE,Online\nOK'),
                     ],
        'AT+CTZU?': ['automatic time zone update',
                     ('AT+CTZU=?', '+CTZU: (0-1)\nOK'),
                     ('AT+CTZU', 'ERROR'),
                     ('AT+CTZU?', '+CTZU: 1\nOK'),
                     ('AT+CTZU=0', 'OK'),
                     ('AT+CTZU?', '+CTZU: 0\nOK'),
                     ('AT+CTZU=1', 'OK'),
                     ('AT+CTZU?', '+CTZU: 1\nOK'),
                     ],
        'AT+CTZR?': ['time zone reporting',
                     ('AT+CTZR=?', '+CTZR: (0-1)\nOK'),
                     ('AT+CTZR', 'OK'),
                     ('AT+CTZR?', '+CTZR: 0\nOK'),
                     ('AT+CTZR=0', 'OK'),
                     ('AT+CTZR?', '+CTZR: 0\nOK'),
                     ('AT+CTZR=1', 'OK'),
                     ('AT+CTZR?', '+CTZR: 1\nOK'),
                     ],
        'AT+CESQ': ['extended signal quality',
                    ('AT+CESQ=?', '+CESQ: (0-63,99),(0-7,99),(0-96,255),(0-49,255),(0-34,255),(0-97,255)\nOK'),
                    ('AT+CESQ', '+CESQ: 45,0,255,255,255,255\nOK'),
                    ('AT+CESQ?', '+CME ERROR: unknown error'),
                    ('AT+CESQ=0', '+CME ERROR: unknown error'),
                    ('AT+CESQ?', '+CME ERROR: unknown error'),
                    ('AT+CESQ=1', '+CME ERROR: unknown error'),
                    ('AT+CESQ?', '+CME ERROR: unknown error'),
                    ('AT+CESQ=2', '+CME ERROR: unknown error'),
                    ('AT+CESQ?', '+CME ERROR: unknown error'),
                    ('AT+CESQ=3', '+CME ERROR: unknown error'),
                    ('AT+CESQ?', '+CME ERROR: unknown error'),
                    ('AT+CESQ=4', '+CME ERROR: unknown error'),
                    ('AT+CESQ?', '+CME ERROR: unknown error'),
                    ('AT+CESQ=5', '+CME ERROR: unknown error'),
                    ('AT+CESQ?', '+CME ERROR: unknown error'),
                    ('AT+CESQ=6', '+CME ERROR: unknown error'),
                    ('AT+CESQ?', '+CME ERROR: unknown error'),
                    ('AT+CESQ=7', '+CME ERROR: unknown error'),
                    ('AT+CESQ?', '+CME ERROR: unknown error'),
                    ('AT+CESQ=8', '+CME ERROR: unknown error'),
                    ('AT+CESQ?', '+CME ERROR: unknown error'),
                    ('AT+CESQ=9', '+CME ERROR: unknown error'),
                    ('AT+CESQ?', '+CME ERROR: unknown error'),
                    ],

        # 2=DOUBT ----------------------------------------
        'AT+CPOL': ['preferred operator list',
                    ('AT+CPOL=?', '+CME ERROR: SIM failure'),
                    ('AT+CPOL', 'ERROR\n+CME ERROR: SIM failure'),
                    ('AT+CPOL?', 'ERROR\n+CME ERROR: SIM failure'),
                    ],
        'AT+CIREG': ['IMS registration (может быть не поддержано)',
                     ('AT+CIREG=?', '+CIREG: (0-3)\nOK'),
                     ('AT+CIREG', '+CME ERROR: Operation not supported'),
                     ('AT+CIREG?', '+CME ERROR: Operation not supported'),
                     ('AT+CIREG=0', '+CME ERROR: Operation not supported'),
                     ('AT+CIREG?', '+CME ERROR: Operation not supported'),
                     ('AT+CIREG=1', '+CME ERROR: Operation not supported'),
                     ('AT+CIREG?', '+CME ERROR: Operation not supported'),
                     ('AT+CIREG=2', '+CME ERROR: Operation not supported'),
                     ('AT+CIREG?', '+CME ERROR: Operation not supported'),
                     ('AT+CIREG=3', '+CME ERROR: Operation not supported'),
                     ('AT+CIREG?', '+CME ERROR: Operation not supported'),
                     ],
        # 3=UNKNOWN --------------------------------------
        'AT+CSMOD': ['show network system mode',
                     ('AT+CSMOD=?', 'ERROR'),
                     ('AT+CSMOD', 'ERROR'),
                     ('AT+CSMOD?', 'ERROR'),
                     ],

        'AT+CIMS': ['IMS status (может быть не поддержано)',
                    ('AT+CIMS=?', 'ERROR'),
                    ('AT+CIMS', 'ERROR'),
                    ('AT+CIMS?', 'ERROR'),
                    ],
        'AT+CLBS': ['base station location (LBS)',
                    (
                        'AT+CLBS=?',
                        '+CLBS: (1,2,3,4,9),(1-15),(-180.000000-180.000000),(-90.000000-90.000000),(0-2)\nOK'),
                    ('AT+CLBS', 'ERROR'),
                    ('AT+CLBS?', 'ERROR'),
                    ('AT+CLBS=0', 'ERROR'),
                    ('AT+CLBS?', 'ERROR'),
                    ('AT+CLBS=1', 'ERROR'),
                    ('AT+CLBS?', 'ERROR'),
                    ('AT+CLBS=2', 'ERROR'),
                    ('AT+CLBS?', 'ERROR'),
                    ('AT+CLBS=3', 'ERROR'),
                    ('AT+CLBS?', 'ERROR'),
                    ('AT+CLBS=4', 'ERROR'),
                    ('AT+CLBS?', 'ERROR'),
                    ('AT+CLBS=5', 'ERROR'),
                    ('AT+CLBS?', 'ERROR'),
                    ('AT+CLBS=6', 'ERROR'),
                    ('AT+CLBS?', 'ERROR'),
                    ('AT+CLBS=7', 'ERROR'),
                    ('AT+CLBS?', 'ERROR'),
                    ('AT+CLBS=8', 'ERROR'),
                    ('AT+CLBS?', 'ERROR'),
                    ('AT+CLBS=9', 'ERROR'),
                    ('AT+CLBS?', 'ERROR'),
                    ],
        'AT+CLBSCFG': ['LBS configure',
                       ('AT+CLBSCFG=?', '+CLBSCFG: (0,1),(1-3),"ParamValue"\nOK'),
                       ('AT+CLBSCFG', 'ERROR'),
                       ('AT+CLBSCFG?', 'ERROR'),
                       ('AT+CLBSCFG=0', '+CLBSCFG: 0,1,""\nOK'),
                       ('AT+CLBSCFG?', 'ERROR'),
                       ('AT+CLBSCFG=1', 'ERROR'),
                       ('AT+CLBSCFG?', 'ERROR'),
                       ('AT+CLBSCFG=2', 'ERROR'),
                       ('AT+CLBSCFG?', 'ERROR'),
                       ('AT+CLBSCFG=3', 'ERROR'),
                       ('AT+CLBSCFG?', 'ERROR'),
                       ('AT+CLBSCFG=ParamValue', 'ERROR'),
                       ('AT+CLBSCFG?', 'ERROR'),
                       ],
        'AT+CASSISTLOC': ['base station location for LTE/CDMA',
                          ('AT+CASSISTLOC=?', 'ERROR'),
                          ('AT+CASSISTLOC', 'ERROR'),
                          ('AT+CASSISTLOC?', 'ERROR'),
                          ],
    },

    # =========================================================================
    "HARDWARE(питание, ADC, GPIO, I2C)": {
        # 0=DANGER+USELESS -------------------------------
        # "AT+CVALARM": "[DANGER]low/high voltage alarm",
        # "AT+CMTE": "[DANGER]temperature control / shutdown",
        # "AT+CPMVT": "[DANGER]low/high voltage power off",
        # "AT+CDELTA": "[DANGER]go to recovery mode",
        # "AT+CRIIC": "[DANGER]read I2C register",
        # "AT+CWIIC": "[DANGER]write I2C register",
        # "AT+CGFUNC": "[DANGER]GPIO function enable/disable",
        # "AT+CGDRT": "[DANGER]GPIO direction (in/out)",
        # "AT+CGSETV": "[DANGER]GPIO set value (high/low)",
        # "AT+CSCLK": "[DANGER]UART sleep",
        # "AT+CMUX": "[DANGER]UART multiplexer # DANGER",

        # 1=ACCURATE -------------------------------------
        'AT+CBC': ['battery/voltage',
                   ('AT+CBC=?', 'ERROR'),
                   ('AT+CBC', '+CBC: 3.820V\nOK'),
                   ('AT+CBC?', 'ERROR'),
                   ],
        'AT+CPMUTEMP': ['module temperature',
                        ('AT+CPMUTEMP=?', 'ERROR'),
                        ('AT+CPMUTEMP', '+CPMUTEMP: 109\nOK'),
                        ('AT+CPMUTEMP?', 'ERROR'),
                        ],
        'AT+CVAUXS?': ['state of VREG_AUX1 pin',
                       ('AT+CVAUXS=?', '+CVAUXS: (0,1)\nOK'),
                       ('AT+CVAUXS', 'ERROR'),
                       ('AT+CVAUXS?', '+CVAUXS: 1\nOK'),
                       ('AT+CVAUXS=0', 'OK'),
                       ('AT+CVAUXS?', '+CVAUXS: 0\nOK'),
                       ('AT+CVAUXS=1', 'OK'),
                       ('AT+CVAUXS?', '+CVAUXS: 1\nOK'),
                       ],
        'AT+CVAUXV?': ['voltage of VREG_AUX1 pin',
                       ('AT+CVAUXV=?', '+CVAUXV: (2500,2600,2700,2800,2850,2900,3000,3100,3300)\nOK'),
                       ('AT+CVAUXV', 'ERROR'),
                       ('AT+CVAUXV?', '+CVAUXV: 3000\nOK'),
                       ('AT+CVAUXV=2500', 'OK'),
                       ('AT+CVAUXV?', '+CVAUXV: 2500\nOK'),
                       ('AT+CVAUXV=2600', 'OK'),
                       ('AT+CVAUXV?', '+CVAUXV: 2600\nOK'),
                       ('AT+CVAUXV=2700', 'OK'),
                       ('AT+CVAUXV?', '+CVAUXV: 2700\nOK'),
                       ('AT+CVAUXV=2800', 'OK'),
                       ('AT+CVAUXV?', '+CVAUXV: 2800\nOK'),
                       ('AT+CVAUXV=2850', 'OK'),
                       ('AT+CVAUXV?', '+CVAUXV: 2850\nOK'),
                       ('AT+CVAUXV=2900', 'OK'),
                       ('AT+CVAUXV?', '+CVAUXV: 2900\nOK'),
                       ('AT+CVAUXV=3000', 'OK'),
                       ('AT+CVAUXV?', '+CVAUXV: 3000\nOK'),
                       ('AT+CVAUXV=3100', 'OK'),
                       ('AT+CVAUXV?', '+CVAUXV: 3100\nOK'),
                       ('AT+CVAUXV=3300', 'OK'),
                       ('AT+CVAUXV?', '+CVAUXV: 3300\nOK'),
                       ],
        'AT+CFGRI?': ['RI pin on URC',
                      ('AT+CFGRI=?', '+CFGRI: (0-1),(10-6000),(20-6000)\nOK'),
                      ('AT+CFGRI', 'OK'),
                      ('AT+CFGRI?', '+CFGRI: 0,60,120\nOK'),
                      ('AT+CFGRI=0', 'OK'),
                      ('AT+CFGRI?', '+CFGRI: 0,60,120\nOK'),
                      ('AT+CFGRI=1', 'OK'),
                      ('AT+CFGRI?', '+CFGRI: 1,60,120\nOK'),
                      ('AT+CFGRI=10', 'ERROR'),
                      ('AT+CFGRI?', '+CFGRI: 1,60,120\nOK'),
                      ('AT+CFGRI=11', 'ERROR'),
                      ('AT+CFGRI?', '+CFGRI: 1,60,120\nOK'),
                      ('AT+CFGRI=12', 'ERROR'),
                      ('AT+CFGRI?', '+CFGRI: 1,60,120\nOK'),
                      ('AT+CFGRI=13', 'ERROR'),
                      ('AT+CFGRI?', '+CFGRI: 1,60,120\nOK'),
                      ('AT+CFGRI=14', 'ERROR'),
                      ('AT+CFGRI?', '+CFGRI: 1,60,120\nOK'),
                      ('AT+CFGRI=15', 'ERROR'),
                      ('AT+CFGRI?', '+CFGRI: 1,60,120\nOK'),
                      ('AT+CFGRI=16', 'ERROR'),
                      ('AT+CFGRI?', '+CFGRI: 1,60,120\nOK'),
                      ('AT+CFGRI=17', 'ERROR'),
                      ('AT+CFGRI?', '+CFGRI: 1,60,120\nOK'),
                      ],
        # 2=DOUBT ----------------------------------------
        # 3=UNKNOWN --------------------------------------
        'AT+CADC': ['read ADC value',
                    ('AT+CADC=?', '+CADC: (0,2)\nOK'),
                    ('AT+CADC', 'ERROR'),
                    ('AT+CADC?', 'ERROR'),
                    ('AT+CADC=0', '+CADC: 205\nOK'),
                    ('AT+CADC?', 'ERROR'),
                    ('AT+CADC=2', '+CADC: 0\nOK'),
                    ('AT+CADC?', 'ERROR'),
                    ],
        'AT+CADC2': ['read ADC2 value',
                     ('AT+CADC2=?', 'ERROR'),
                     ('AT+CADC2', 'ERROR'),
                     ('AT+CADC2?', 'ERROR'),
                     ],
        'AT+CGGETV': ['GPIO get value',
                      ('AT+CGGETV=?', '+CGGETV: (1,2,3,4,5,6)\nOK'),
                      ('AT+CGGETV', 'ERROR'),
                      ('AT+CGGETV?', '+CME ERROR: Operation not supported'),
                      ('AT+CGGETV=1', '+CGGETV: 1,0\nOK'),
                      ('AT+CGGETV?', '+CME ERROR: Operation not supported'),
                      ('AT+CGGETV=2', '+CGGETV: 2,0\nOK'),
                      ('AT+CGGETV?', '+CME ERROR: Operation not supported'),
                      ('AT+CGGETV=3', '+CGGETV: 3,0\nOK'),
                      ('AT+CGGETV?', '+CME ERROR: Operation not supported'),
                      ('AT+CGGETV=4', '+CGGETV: 4,0\nOK'),
                      ('AT+CGGETV?', '+CME ERROR: Operation not supported'),
                      ('AT+CGGETV=5', '+CGGETV: 5,0\nOK'),
                      ('AT+CGGETV?', '+CME ERROR: Operation not supported'),
                      ('AT+CGGETV=6', '+CGGETV: 6,0\nOK'),
                      ('AT+CGGETV?', '+CME ERROR: Operation not supported'),
                      ],
        'AT+CGISR': ['GPIO interrupt trigger',
                     ('AT+CGISR=?', 'ERROR'),
                     ('AT+CGISR', 'ERROR'),
                     ('AT+CGISR?', 'ERROR'),
                     ],
    },

    # =========================================================================
    # "6=CALL_CONTROL": {
    #     # 0=DANGER+USELESS -------------------------------
    #     # "AT+CCWA": "[DANGER]call waiting",
    #     # "AT+VTS": "[DANGER]DTMF and tone generation",
    #     # "AT+CSTA": "[DANGER]select type of address",
    #     # 'AT+CHUP': ['[USELESS]hang up call',
    #     #             ('AT+CHUP=?', 'OK'),
    #     #             ('AT+CHUP', 'OK'),
    #     #             ('AT+CHUP?', 'ERROR'),
    #     #             ],
    #     # 'AT+CMOD?': ['[USELESS]call mode',
    #     #              ('AT+CMOD=?', '+CMOD: (0)\nOK'),
    #     #              ('AT+CMOD', 'OK'),
    #     #              ('AT+CMOD?', '+CMOD: 0\nOK'),
    #     #              ('AT+CMOD=0', 'OK'),
    #     #              ('AT+CMOD?', '+CMOD: 0\nOK'),
    #     #              ],
    #     # 'AT+VTD?': ['[USELESS]tone duration',
    #     #            ('AT+VTD=?', '+VTD: (300-600)\nOK'),
    #     #            ('AT+VTD', 'ERROR'),
    #     #            ('AT+VTD?', '+VTD: 300\nOK'),
    #     #            ('AT+VTD=300', 'OK'),
    #     #            ('AT+VTD?', '+VTD: 300\nOK'),
    #     #            ('AT+VTD=301', 'OK'),
    #     #            ('AT+VTD?', '+VTD: 301\nOK'),
    #     #            ('AT+VTD=302', 'OK'),
    #     #            ('AT+VTD?', '+VTD: 302\nOK'),
    #     #            ('AT+VTD=303', 'OK'),
    #     #            ('AT+VTD?', '+VTD: 303\nOK'),
    #     #            ('AT+VTD=304', 'OK'),
    #     #            ('AT+VTD?', '+VTD: 304\nOK'),
    #     #            ('AT+VTD=305', 'OK'),
    #     #            ('AT+VTD?', '+VTD: 305\nOK'),
    #     #            ('AT+VTD=306', 'OK'),
    #     #            ('AT+VTD?', '+VTD: 306\nOK'),
    #     #            ('AT+VTD=307', 'OK'),
    #     #            ('AT+VTD?', '+VTD: 307\nOK'),
    #     #            ('AT+VTD=308', 'OK'),
    #     #            ('AT+VTD?', '+VTD: 308\nOK'),
    #     #            ('AT+VTD=309', 'OK'),
    #     #            ('AT+VTD?', '+VTD: 309\nOK'),
    #     #            ],
    #     # 'AT+VMUTE': ['[USELESS]speaker mute',
    #     #              ('AT+VMUTE=?', '+VMUTE: (0-1)\nOK'),
    #     #              ('AT+VMUTE', 'ERROR'),
    #     #              ('AT+VMUTE?', '+VMUTE: 0\nOK'),
    #     #              ('AT+VMUTE=0', 'ERROR'),
    #     #              ('AT+VMUTE?', '+VMUTE: 0\nOK'),
    #     #              ('AT+VMUTE=1', 'ERROR'),
    #     #              ('AT+VMUTE?', '+VMUTE: 0\nOK'),
    #     #              ],
    #     # 'AT+CMUT': ['[USELESS]microphone mute',
    #     #             ('AT+CMUT=?', '+CMUT: (0-1)\nOK'),
    #     #             ('AT+CMUT', 'ERROR'),
    #     #             ('AT+CMUT?', '+CMUT: 0\nOK'),
    #     #             ('AT+CMUT=0', 'ERROR'),
    #     #             ('AT+CMUT?', '+CMUT: 0\nOK'),
    #     #             ('AT+CMUT=1', 'ERROR'),
    #     #             ('AT+CMUT?', '+CMUT: 0\nOK'),
    #     #             ],
    #     # 'AT+MORING': ['[USELESS]MO ring URC',
    #     #               ('AT+MORING=?', 'ERROR'),
    #     #               ('AT+MORING', 'ERROR'),
    #     #               ('AT+MORING?', 'ERROR'),
    #     #               ],
    #     # 'AT+CLVL': ['[USELESS]loudspeaker volume',
    #     #             ('AT+CLVL=?', 'ERROR'),
    #     #             ('AT+CLVL', 'ERROR'),
    #     #             ('AT+CLVL?', 'ERROR'),
    #     #             ],
    #     # 'AT+SIDET': ['[USELESS]sidetone',
    #     #              ('AT+SIDET=?', 'ERROR'),
    #     #              ('AT+SIDET', 'ERROR'),
    #     #              ('AT+SIDET?', 'ERROR'),
    #     #              ],
    #     # 1=ACCURATE -------------------------------------
    #     'AT+CVHU?': ['voice hang up control',
    #                  ('AT+CVHU=?', '+CVHU: (0-1)\nOK'),
    #                  ('AT+CVHU', 'OK'),
    #                  ('AT+CVHU?', '+CVHU: 1\nOK'),
    #                  ('AT+CVHU=0', 'OK'),
    #                  ('AT+CVHU?', '+CVHU: 0\nOK'),
    #                  ('AT+CVHU=1', 'OK'),
    #                  ('AT+CVHU?', '+CVHU: 1\nOK'),
    #                  ],
    #     'AT+CRLP?': ['radio link protocol',
    #                  ('AT+CRLP=?', '+CRLP: (0-61),(0-61),(39-255),(1-255),(0-1),(3-255)\nOK'),
    #                  ('AT+CRLP', 'OK'),
    #                  ('AT+CRLP?', '+CRLP: 61,61,128,255,1,3\nOK'),
    #                  ('AT+CRLP=0', 'OK'),
    #                  ('AT+CRLP?', '+CRLP: 0,61,128,255,1,3\nOK'),
    #                  ('AT+CRLP=1', 'OK'),
    #                  ('AT+CRLP?', '+CRLP: 1,61,128,255,1,3\nOK'),
    #                  ('AT+CRLP=2', 'OK'),
    #                  ('AT+CRLP?', '+CRLP: 2,61,128,255,1,3\nOK'),
    #                  ('AT+CRLP=3', 'OK'),
    #                  ('AT+CRLP?', '+CRLP: 3,61,128,255,1,3\nOK'),
    #                  ('AT+CRLP=4', 'OK'),
    #                  ('AT+CRLP?', '+CRLP: 4,61,128,255,1,3\nOK'),
    #                  ('AT+CRLP=5', 'OK'),
    #                  ('AT+CRLP?', '+CRLP: 5,61,128,255,1,3\nOK'),
    #                  ('AT+CRLP=6', 'OK'),
    #                  ('AT+CRLP?', '+CRLP: 6,61,128,255,1,3\nOK'),
    #                  ('AT+CRLP=7', 'OK'),
    #                  ('AT+CRLP?', '+CRLP: 7,61,128,255,1,3\nOK'),
    #                  ('AT+CRLP=8', 'OK'),
    #                  ('AT+CRLP?', '+CRLP: 8,61,128,255,1,3\nOK'),
    #                  ('AT+CRLP=9', 'OK'),
    #                  ('AT+CRLP?', '+CRLP: 9,61,128,255,1,3\nOK'),
    #                  ],
    #     'AT+CRC?': ['cellular result codes',
    #                 ('AT+CRC=?', '+CRC: (0,1)\nOK'),
    #                 ('AT+CRC', 'OK'),
    #                 ('AT+CRC?', '+CRC: 0\nOK'),
    #                 ('AT+CRC=0', 'OK'),
    #                 ('AT+CRC?', '+CRC: 0\nOK'),
    #                 ('AT+CRC=1', 'OK'),
    #                 ('AT+CRC?', '+CRC: 1\nOK'),
    #                 ],
    #     'AT+CLCC?': ['list current calls',
    #                  ('AT+CLCC=?', '+CLCC: (0-1)\nOK'),
    #                  ('AT+CLCC', 'OK'),
    #                  ('AT+CLCC?', '+CLCC: 1\nOK'),
    #                  ('AT+CLCC=0', 'OK'),
    #                  ('AT+CLCC?', '+CLCC: 0\nOK'),
    #                  ('AT+CLCC=1', 'OK'),
    #                  ('AT+CLCC?', '+CLCC: 1\nOK'),
    #                  ],
    #     'AT+CEER': ['extended error report',
    #                 ('AT+CEER=?', 'OK'),
    #                 ('AT+CEER', '+CEER: "0 Unknown"\nOK'),
    #                 ('AT+CEER?', 'ERROR'),
    #                 ],
    #     'AT+CSDVC?': ['switch voice channel device',
    #                   ('AT+CSDVC=?', '+CSDVC: (1,3)\nOK'),
    #                   ('AT+CSDVC', 'ERROR'),
    #                   ('AT+CSDVC?', '+CSDVC: 1\nOK'),
    #                   ('AT+CSDVC=1', 'OK'),
    #                   ('AT+CSDVC?', '+CSDVC: 1\nOK'),
    #                   ('AT+CSDVC=3', 'OK'),
    #                   ('AT+CSDVC?', '+CSDVC: 3\nOK'),
    #                   ],
    #
    #     # 2=DOUBT ----------------------------------------
    #
    #     # 3=UNKNOWN --------------------------------------
    #     'AT+CBST?': ['bearer service type',
    #                 ('AT+CBST=?',
    #                  '+CBST: (0,1,2,3,4,5,6,7,12,14,15,16,17,34,36,38,39,43,47,48,49,50,51,65,66,68,70,71,75,79,80,81,82,83,84,115,116,120,121,130,131,132,133,134),(0-7),(0-3)\nOK'),
    #                 ('AT+CBST', '+CME ERROR: Operation not supported'),
    #                 ('AT+CBST?', '+CME ERROR: unknown error'),
    #                 ('AT+CBST=0', '+CME ERROR: Operation not supported'),
    #                 ('AT+CBST?', '+CME ERROR: unknown error'),
    #                 ('AT+CBST=1', '+CME ERROR: Operation not supported'),
    #                 ('AT+CBST?', '+CME ERROR: unknown error'),
    #                 ('AT+CBST=2', '+CME ERROR: Operation not supported'),
    #                 ('AT+CBST?', '+CME ERROR: unknown error'),
    #                 ('AT+CBST=3', '+CME ERROR: Operation not supported'),
    #                 ('AT+CBST?', '+CME ERROR: unknown error'),
    #                 ('AT+CBST=4', '+CME ERROR: Operation not supported'),
    #                 ('AT+CBST?', '+CME ERROR: unknown error'),
    #                 ('AT+CBST=5', '+CME ERROR: Operation not supported'),
    #                 ('AT+CBST?', '+CME ERROR: unknown error'),
    #                 ('AT+CBST=6', '+CME ERROR: Operation not supported'),
    #                 ('AT+CBST?', '+CME ERROR: unknown error'),
    #                 ('AT+CBST=7', '+CME ERROR: Operation not supported'),
    #                 ('AT+CBST?', '+CME ERROR: unknown error'),
    #                 ('AT+CBST=12', '+CME ERROR: Operation not supported'),
    #                 ('AT+CBST?', '+CME ERROR: unknown error'),
    #                 ('AT+CBST=14', '+CME ERROR: Operation not supported'),
    #                 ('AT+CBST?', '+CME ERROR: unknown error'),
    #                 ],
    #     'AT+CR': ['service reporting control',
    #               ('AT+CR=?', 'ERROR'),
    #               ('AT+CR', 'ERROR'),
    #               ('AT+CR?', 'ERROR'),
    #               ],
    #     'AT+CHLD': ['call related supplementary services',
    #                 ('AT+CHLD=?', '+CHLD: (0,1,1x,2,2x,3,4)\nOK'),
    #                 ('AT+CHLD', 'ERROR'),
    #                 ('AT+CHLD?', '+CME ERROR: Operation not supported'),
    #                 ],
    #     'AT+CCFC': ['call forwarding',
    #                 ('AT+CCFC=?', '+CCFC: (0,1,2,3,4,5)\nOK'),
    #                 ('AT+CCFC', 'ERROR'),
    #                 ('AT+CCFC?', 'ERROR'),
    #                 ('AT+CCFC=0', 'ERROR'),
    #                 ('AT+CCFC?', 'ERROR'),
    #                 ('AT+CCFC=1', 'ERROR'),
    #                 ('AT+CCFC?', 'ERROR'),
    #                 ('AT+CCFC=2', 'ERROR'),
    #                 ('AT+CCFC?', 'ERROR'),
    #                 ('AT+CCFC=3', 'ERROR'),
    #                 ('AT+CCFC?', 'ERROR'),
    #                 ('AT+CCFC=4', 'ERROR'),
    #                 ('AT+CCFC?', 'ERROR'),
    #                 ('AT+CCFC=5', 'ERROR'),
    #                 ('AT+CCFC?', 'ERROR'),
    #                 ],
    #     'AT+CLIP': ['calling line identification presentation',
    #                 ('AT+CLIP=?', '+CLIP: (0-1)\nOK'),
    #                 ('AT+CLIP', 'ERROR'),
    #                 ('AT+CLIP?', 'ERROR'),
    #                 ('AT+CLIP=0', 'ERROR'),
    #                 ('AT+CLIP?', 'ERROR'),
    #                 ('AT+CLIP=1', 'ERROR'),
    #                 ('AT+CLIP?', 'ERROR'),
    #                 ],
    #     'AT+CLIR': ['calling line identification restriction',
    #                 ('AT+CLIR=?', '+CLIR: (0-2)\nOK'),
    #                 ('AT+CLIR', 'ERROR'),
    #                 ('AT+CLIR?', '+CME ERROR: unknown error'),
    #                 ('AT+CLIR=0', 'OK'),
    #                 ('AT+CLIR?', '+CME ERROR: unknown error'),
    #                 ('AT+CLIR=1', 'OK'),
    #                 ('AT+CLIR?', '+CME ERROR: unknown error'),
    #                 ('AT+CLIR=2', 'OK'),
    #                 ('AT+CLIR?', '+CME ERROR: unknown error'),
    #                 ],
    #     'AT+COLP': ['connected line identification presentation',
    #                 ('AT+COLP=?', '+COLP: (0-1)\nOK'),
    #                 ('AT+COLP', 'ERROR'),
    #                 ('AT+COLP?', 'ERROR'),
    #                 ('AT+COLP=0', 'ERROR'),
    #                 ('AT+COLP?', 'ERROR'),
    #                 ('AT+COLP=1', 'ERROR'),
    #                 ('AT+COLP?', 'ERROR'),
    #                 ],
    # },

    # =========================================================================
    # "7=AUDIO/DSP(голосовые параметры)": {
    #     # 0=DANGER+USELESS -------------------------------
    #     # 1=ACCURATE -------------------------------------
    #     # 2=DOUBT ----------------------------------------
    #     # 3=UNKNOWN --------------------------------------
    #
    #
    #     # "AT+CACDBFN": "[DANGER]change default ACDB filename",
    #     # "AT+CCMXPLAY": "[DANGER]play audio (mp3/aac/amr/...)",
    #     # "AT+CCMXSTOP": "[DANGER]stop audio",
    #     # 'AT+CCMXPLAYWAV': ['[NONEUSEFULL]play wav',
    #     #                    ('AT+CCMXPLAYWAV=?', 'ERROR'),
    #     #                    ('AT+CCMXPLAYWAV', 'ERROR'),
    #     #                    ('AT+CCMXPLAYWAV?', 'ERROR'),
    #     #                    ],
    #     # 'AT+CCMXSTOPWAV': ['[NONEUSEFULL]stop wav',
    #     #                    ('AT+CCMXSTOPWAV=?', 'ERROR'),
    #     #                    ('AT+CCMXSTOPWAV', 'ERROR'),
    #     #                    ('AT+CCMXSTOPWAV?', 'ERROR'),
    #     #                    ],
    #
    #     'AT+CPCMREG': ['USB audio control',
    #                    ('AT+CPCMREG=?', 'ERROR'),
    #                    ('AT+CPCMREG', 'ERROR'),
    #                    ('AT+CPCMREG?', 'ERROR'),
    #                    ],
    #     'AT+CMICGAIN': ['mic gain',
    #                     ('AT+CMICGAIN=?', '+CMICGAIN: (0-7)\nOK'),
    #                     ('AT+CMICGAIN', 'ERROR'),
    #                     ('AT+CMICGAIN?', '+CMICGAIN: 7\nOK'),
    #                     ('AT+CMICGAIN=0', 'OK'),
    #                     ('AT+CMICGAIN?', '+CMICGAIN: 0\nOK'),
    #                     ('AT+CMICGAIN=1', 'OK'),
    #                     ('AT+CMICGAIN?', '+CMICGAIN: 1\nOK'),
    #                     ('AT+CMICGAIN=2', 'OK'),
    #                     ('AT+CMICGAIN?', '+CMICGAIN: 2\nOK'),
    #                     ('AT+CMICGAIN=3', 'OK'),
    #                     ('AT+CMICGAIN?', '+CMICGAIN: 3\nOK'),
    #                     ('AT+CMICGAIN=4', 'OK'),
    #                     ('AT+CMICGAIN?', '+CMICGAIN: 4\nOK'),
    #                     ('AT+CMICGAIN=5', 'OK'),
    #                     ('AT+CMICGAIN?', '+CMICGAIN: 5\nOK'),
    #                     ('AT+CMICGAIN=6', 'OK'),
    #                     ('AT+CMICGAIN?', '+CMICGAIN: 6\nOK'),
    #                     ('AT+CMICGAIN=7', 'OK'),
    #                     ('AT+CMICGAIN?', '+CMICGAIN: 7\nOK'),
    #                     ],
    #     'AT+COUTGAIN': ['out gain',
    #                     ('AT+COUTGAIN=?', '+COUTGAIN: (0-7)\nOK'),
    #                     ('AT+COUTGAIN', 'ERROR'),
    #                     ('AT+COUTGAIN?', '+COUTGAIN: 7\nOK'),
    #                     ('AT+COUTGAIN=0', 'OK'),
    #                     ('AT+COUTGAIN?', '+COUTGAIN: 0\nOK'),
    #                     ('AT+COUTGAIN=1', 'OK'),
    #                     ('AT+COUTGAIN?', '+COUTGAIN: 1\nOK'),
    #                     ('AT+COUTGAIN=2', 'OK'),
    #                     ('AT+COUTGAIN?', '+COUTGAIN: 2\nOK'),
    #                     ('AT+COUTGAIN=3', 'OK'),
    #                     ('AT+COUTGAIN?', '+COUTGAIN: 3\nOK'),
    #                     ('AT+COUTGAIN=4', 'OK'),
    #                     ('AT+COUTGAIN?', '+COUTGAIN: 4\nOK'),
    #                     ('AT+COUTGAIN=5', 'OK'),
    #                     ('AT+COUTGAIN?', '+COUTGAIN: 5\nOK'),
    #                     ('AT+COUTGAIN=6', 'OK'),
    #                     ('AT+COUTGAIN?', '+COUTGAIN: 6\nOK'),
    #                     ('AT+COUTGAIN=7', 'OK'),
    #                     ('AT+COUTGAIN?', '+COUTGAIN: 7\nOK'),
    #                     ],
    #     'AT+CTXVOL': ['TX voice mic volume',
    #                   ('AT+CTXVOL=?', 'ERROR'),
    #                   ('AT+CTXVOL', 'ERROR'),
    #                   ('AT+CTXVOL?', 'ERROR'),
    #                   ],
    #     'AT+CTXMICGAIN': ['TX voice mic gain',
    #                       ('AT+CTXMICGAIN=?', 'ERROR'),
    #                       ('AT+CTXMICGAIN', 'ERROR'),
    #                       ('AT+CTXMICGAIN?', 'ERROR'),
    #                       ],
    #     'AT+CRXVOL': ['RX voice output speaker volume',
    #                   ('AT+CRXVOL=?', 'ERROR'),
    #                   ('AT+CRXVOL', 'ERROR'),
    #                   ('AT+CRXVOL?', 'ERROR'),
    #                   ],
    #     'AT+CECH': ['inhibit far-end echo',
    #                 ('AT+CECH=?', 'ERROR'),
    #                 ('AT+CECH', 'ERROR'),
    #                 ('AT+CECH?', 'ERROR'),
    #                 ],
    #     'AT+CECDT': ['inhibit echo during doubletalk',
    #                  ('AT+CECDT=?', 'ERROR'),
    #                  ('AT+CECDT', 'ERROR'),
    #                  ('AT+CECDT?', 'ERROR'),
    #                  ],
    #     'AT+CECWB': ['inhibit echo in high band',
    #                  ('AT+CECWB=?', 'ERROR'),
    #                  ('AT+CECWB', 'ERROR'),
    #                  ('AT+CECWB?', 'ERROR'),
    #                  ],
    #     'AT+CSNS': ['MIC noise suppression',
    #                 ('AT+CSNS=?', 'ERROR'),
    #                 ('AT+CSNS', 'ERROR'),
    #                 ('AT+CSNS?', 'ERROR'),
    #                 ],
    #     'AT+CSLIM': ['MIC noise suppression (limit)',
    #                  ('AT+CSLIM=?', 'ERROR'),
    #                  ('AT+CSLIM', 'ERROR'),
    #                  ('AT+CSLIM?', 'ERROR'),
    #                  ],
    #     'AT+CFNSMOD': ['fnsMode of RX_VOICE_FNS',
    #                    ('AT+CFNSMOD=?', 'ERROR'),
    #                    ('AT+CFNSMOD', 'ERROR'),
    #                    ('AT+CFNSMOD?', 'ERROR'),
    #                    ],
    #     'AT+CFNSIN': ['fnsInputGain of RX_VOICE_FNS',
    #                   ('AT+CFNSIN=?', 'ERROR'),
    #                   ('AT+CFNSIN', 'ERROR'),
    #                   ('AT+CFNSIN?', 'ERROR'),
    #                   ],
    #     'AT+CFNSLVL': ['fnsTargetNS of RX_VOICE_FNS',
    #                    ('AT+CFNSLVL=?', 'ERROR'),
    #                    ('AT+CFNSLVL', 'ERROR'),
    #                    ('AT+CFNSLVL?', 'ERROR'),
    #                    ],
    #     'AT+CECRX': ['VOICE_MOD_ENABLE',
    #                  ('AT+CECRX=?', 'ERROR'),
    #                  ('AT+CECRX', 'ERROR'),
    #                  ('AT+CECRX?', 'ERROR'),
    #                  ],
    #     'AT+CNLPPG': ['NLPP_gain',
    #                   ('AT+CNLPPG=?', 'ERROR'),
    #                   ('AT+CNLPPG', 'ERROR'),
    #                   ('AT+CNLPPG?', 'ERROR'),
    #                   ],
    #     'AT+CNLPPL': ['NLPP_limit',
    #                   ('AT+CNLPPL=?', 'ERROR'),
    #                   ('AT+CNLPPL', 'ERROR'),
    #                   ('AT+CNLPPL?', 'ERROR'),
    #                   ],
    #     'AT+CECM': ['echo canceller mode',
    #                 ('AT+CECM=?', 'ERROR'),
    #                 ('AT+CECM', 'ERROR'),
    #                 ('AT+CECM?', 'ERROR'),
    #                 ],
    #     'AT+CPCMFRM': ['USB audio sample rate 16k',
    #                    ('AT+CPCMFRM=?', 'ERROR'),
    #                    ('AT+CPCMFRM', 'ERROR'),
    #                    ('AT+CPCMFRM?', 'ERROR'),
    #                    ],
    #     'AT+CPTONE': ['play tone',
    #                   ('AT+CPTONE=?', 'ERROR'),
    #                   ('AT+CPTONE', 'ERROR'),
    #                   ('AT+CPTONE?', 'ERROR'),
    #                   ],
    #     'AT+CREC': ['record wav',
    #                 ('AT+CREC=?', '+CREC: (0-3),[{non-ascii}]"FILEPATH"\nOK'),
    #                 ('AT+CREC', 'ERROR'),
    #                 ('AT+CREC?', '+CREC: 0\nOK'),
    #                 ('AT+CREC=0', '+CREC: 0\nOK'),
    #                 ('AT+CREC?', '+CREC: 0\nOK'),
    #                 ('AT+CREC=1', 'ERROR'),
    #                 ('AT+CREC?', '+CREC: 0\nOK'),
    #                 ('AT+CREC=2', 'ERROR'),
    #                 ('AT+CREC?', '+CREC: 0\nOK'),
    #                 ('AT+CREC=3', 'ERROR'),
    #                 ('AT+CREC?', '+CREC: 0\nOK'),
    #                 ('AT+CREC=FILEPATH', 'ERROR'),
    #                 ('AT+CREC?', '+CREC: 0\nOK'),
    #                 ],
    # },

    # =========================================================================
    # "8=SMS": {
    #     # 0=DANGER+USELESS -------------------------------
    #     # 1=ACCURATE -------------------------------------
    #     # 2=DOUBT ----------------------------------------
    #     # 3=UNKNOWN --------------------------------------
    #
    #
    #     # "AT+CMGF": "[DANGER]SMS format (0=PDU, 1=text)",
    #     # "AT+CSMP": "[DANGER]text mode parameters",
    #     # "AT+CMGS": "[DANGER]send SMS # DANGER (ждёт > и Ctrl+Z)",
    #     # "AT+CMSS": "[DANGER]send SMS from storage",
    #     # "AT+CMGW": "[DANGER]write SMS to memory # DANGER (ждёт >)",
    #     # "AT+CMGD": "[DANGER]delete SMS",
    #     # "AT+CMGMT": "[DANGER]change message status",
    #     # "AT+CMGRD": "[DANGER]read+delete SMS",
    #     # "AT+CMGSEX": "[DANGER]send SMS (extended)",
    #     # "AT+CMSSEX": "[DANGER]send multi SMS from storage",
    #     # "AT+CMGP": "[DANGER]cdma/evdo text mode parameters",
    #
    #     'AT+CSMS': ['select message service',
    #                 ('AT+CSMS=?', '+CSMS: (0-1)\nOK'),
    #                 ('AT+CSMS', 'ERROR'),
    #                 ('AT+CSMS?', '+CSMS: 0,1,1,1\nOK'),
    #                 ('AT+CSMS=0', '+CSMS: 1,1,1\nOK'),
    #                 ('AT+CSMS?', '+CSMS: 0,1,1,1\nOK'),
    #                 ('AT+CSMS=1', '+CSMS: 1,1,1\nOK'),
    #                 ('AT+CSMS?', '+CSMS: 1,1,1,1\nOK'),
    #                 ],
    #     'AT+CPMS': ['preferred message storage',
    #                 ('AT+CPMS=?', '+CPMS: ("ME","SM"),("ME","SM"),("ME","SM")\nOK'),
    #                 ('AT+CPMS', '+CMS ERROR: (U)SIM busy'),
    #                 ('AT+CPMS?', '+CMS ERROR: unknown error'),
    #                 ('AT+CPMS=ME', 'ERROR'),
    #                 ('AT+CPMS?', '+CMS ERROR: unknown error'),
    #                 ('AT+CPMS=SM', 'ERROR'),
    #                 ('AT+CPMS?', '+CMS ERROR: unknown error'),
    #                 ],
    #     'AT+CSCA': ['SMS service centre address',
    #                 ('AT+CSCA=?', 'OK'),
    #                 ('AT+CSCA', 'ERROR'),
    #                 ('AT+CSCA?', '+CMS ERROR: unknown error'),
    #                 ],
    #     'AT+CSCB': ['cell broadcast message indication',
    #                 ('AT+CSCB=?', '+CSCB: (0-1)\nOK'),
    #                 ('AT+CSCB', 'ERROR'),
    #                 ('AT+CSCB?', '+CMS ERROR: unknown error'),
    #                 ('AT+CSCB=0', '+CMS ERROR: unknown error'),
    #                 ('AT+CSCB?', '+CMS ERROR: unknown error'),
    #                 ('AT+CSCB=1', '+CMS ERROR: unknown error'),
    #                 ('AT+CSCB?', '+CMS ERROR: unknown error'),
    #                 ],
    #     'AT+CSDH': ['show text mode parameters',
    #                 ('AT+CSDH=?', '+CSDH: (0-1)\nOK'),
    #                 ('AT+CSDH', 'OK'),
    #                 ('AT+CSDH?', '+CSDH: 0\nOK'),
    #                 ('AT+CSDH=0', 'OK'),
    #                 ('AT+CSDH?', '+CSDH: 0\nOK'),
    #                 ('AT+CSDH=1', 'OK'),
    #                 ('AT+CSDH?', '+CSDH: 1\nOK'),
    #                 ],
    #     'AT+CNMA': ['new message acknowledgement',
    #                 ('AT+CNMA=?', '+CNMA: (0-2)\nOK'),
    #                 ('AT+CNMA', '+CMS ERROR: NO +CNMA ACK EXPECTED'),
    #                 ('AT+CNMA?', 'ERROR'),
    #                 ('AT+CNMA=0', '+CMS ERROR: NO +CNMA ACK EXPECTED'),
    #                 ('AT+CNMA?', 'ERROR'),
    #                 ('AT+CNMA=1', '+CMS ERROR: NO +CNMA ACK EXPECTED'),
    #                 ('AT+CNMA?', 'ERROR'),
    #                 ('AT+CNMA=2', '+CMS ERROR: NO +CNMA ACK EXPECTED'),
    #                 ('AT+CNMA?', 'ERROR'),
    #                 ],
    #     'AT+CNMI': ['new message indications',
    #                 ('AT+CNMI=?', '+CNMI: (0,1,2),(0,1,2,3),(0,2),(0,1,2),(0,1)\nOK'),
    #                 ('AT+CNMI', 'OK'),
    #                 ('AT+CNMI?', '+CNMI: 2,1,0,0,0\nOK'),
    #                 ('AT+CNMI=0', 'OK'),
    #                 ('AT+CNMI?', '+CNMI: 0,0,0,0,0\nOK'),
    #                 ('AT+CNMI=1', 'OK'),
    #                 ('AT+CNMI?', '+CNMI: 1,0,0,0,0\nOK'),
    #                 ('AT+CNMI=2', 'OK'),
    #                 ('AT+CNMI?', '+CNMI: 2,0,0,0,0\nOK'),
    #                 ('AT+CNMI=3', '+CMS ERROR: Operation not allowed'),
    #                 ('AT+CNMI?', '+CNMI: 2,0,0,0,0\nOK'),
    #                 ],
    #     'AT+CGMS': ['service for MO SMS',
    #                 ('AT+CGMS=?', 'ERROR'),
    #                 ('AT+CGMS', 'ERROR'),
    #                 ('AT+CGMS?', 'ERROR'),
    #                 ],
    #     'AT+CGSMS': ['service for MO SMS (3GPP)',
    #                  ('AT+CGSMS=?', '+CGSMS: (0-3)\nOK'),
    #                  ('AT+CGSMS', 'ERROR'),
    #                  ('AT+CGSMS?', '+CMS ERROR: unknown error'),
    #                  ('AT+CGSMS=0', '+CMS ERROR: unknown error'),
    #                  ('AT+CGSMS?', '+CMS ERROR: unknown error'),
    #                  ('AT+CGSMS=1', '+CMS ERROR: unknown error'),
    #                  ('AT+CGSMS?', '+CMS ERROR: unknown error'),
    #                  ('AT+CGSMS=2', '+CMS ERROR: unknown error'),
    #                  ('AT+CGSMS?', '+CMS ERROR: unknown error'),
    #                  ('AT+CGSMS=3', '+CMS ERROR: unknown error'),
    #                  ('AT+CGSMS?', '+CMS ERROR: unknown error'),
    #                  ],
    #     'AT+CMGL': ['list SMS',
    #                 ('AT+CMGL=?', '+CMGL: (0-4)\nOK'),
    #                 ('AT+CMGL', 'ERROR'),
    #                 ('AT+CMGL?', '+CMS ERROR: Operation not allowed'),
    #                 ('AT+CMGL=0', '+CMS ERROR: unknown error'),
    #                 ('AT+CMGL?', '+CMS ERROR: Operation not allowed'),
    #                 ('AT+CMGL=1', '+CMS ERROR: unknown error'),
    #                 ('AT+CMGL?', '+CMS ERROR: Operation not allowed'),
    #                 ('AT+CMGL=2', '+CMS ERROR: unknown error'),
    #                 ('AT+CMGL?', '+CMS ERROR: Operation not allowed'),
    #                 ('AT+CMGL=3', '+CMS ERROR: unknown error'),
    #                 ('AT+CMGL?', '+CMS ERROR: Operation not allowed'),
    #                 ('AT+CMGL=4', '+CMS ERROR: unknown error'),
    #                 ('AT+CMGL?', '+CMS ERROR: Operation not allowed'),
    #                 ],
    #     'AT+CMGR': ['read SMS',
    #                 ('AT+CMGR=?', 'OK'),
    #                 ('AT+CMGR', 'ERROR'),
    #                 ('AT+CMGR?', 'ERROR'),
    #                 ],
    #     'AT+CMVP': ['message valid period',
    #                 ('AT+CMVP=?', '+CMVP: (0-255)\nOK'),
    #                 ('AT+CMVP', 'ERROR'),
    #                 ('AT+CMVP?', '+CMVP: 167\nOK'),
    #                 ('AT+CMVP=0', 'OK'),
    #                 ('AT+CMVP?', '+CMVP: 0\nOK'),
    #                 ('AT+CMVP=1', 'OK'),
    #                 ('AT+CMVP?', '+CMVP: 1\nOK'),
    #                 ('AT+CMVP=2', 'OK'),
    #                 ('AT+CMVP?', '+CMVP: 2\nOK'),
    #                 ('AT+CMVP=3', 'OK'),
    #                 ('AT+CMVP?', '+CMVP: 3\nOK'),
    #                 ('AT+CMVP=4', 'OK'),
    #                 ('AT+CMVP?', '+CMVP: 4\nOK'),
    #                 ('AT+CMVP=5', 'OK'),
    #                 ('AT+CMVP?', '+CMVP: 5\nOK'),
    #                 ('AT+CMVP=6', 'OK'),
    #                 ('AT+CMVP?', '+CMVP: 6\nOK'),
    #                 ('AT+CMVP=7', 'OK'),
    #                 ('AT+CMVP?', '+CMVP: 7\nOK'),
    #                 ('AT+CMVP=8', 'OK'),
    #                 ('AT+CMVP?', '+CMVP: 8\nOK'),
    #                 ('AT+CMVP=9', 'OK'),
    #                 ('AT+CMVP?', '+CMVP: 9\nOK'),
    #                 ],
    # },

    # =========================================================================
    # 8. PHONEBOOK
    # =========================================================================
    # "PHONEBOOK": {
    #     # 0=DANGER+USELESS -------------------------------
    #     # 1=ACCURATE -------------------------------------
    #     # 2=DOUBT ----------------------------------------
    #     # 3=UNKNOWN --------------------------------------
    #
    #
    #     # "AT+CPBF": "[DANGER]find phonebook entries",
    #     # "AT+CPBW": "[DANGER]write phonebook entry",
    #
    #     'AT+CPBS': ['select phonebook memory (SM/ME/DC/MC/RC/FD/ON/LD/EN)',
    #                 ('AT+CPBS=?', 'ERROR'),
    #                 ('AT+CPBS', 'ERROR'),
    #                 ('AT+CPBS?', 'ERROR'),
    #                 ],
    #     'AT+CPBR': ['read phonebook entries',
    #                 ('AT+CPBR=?', '+CME ERROR: unknown error'),
    #                 ('AT+CPBR', 'ERROR'),
    #                 ('AT+CPBR?', '+CME ERROR: unknown error'),
    #                 ],
    # },

    # =========================================================================
    # 9. GPRS / PDP
    # =========================================================================
    "GPRS/PDP": {
        # 0=DANGER+USELESS -------------------------------
        # 1=ACCURATE -------------------------------------
        # 2=DOUBT ----------------------------------------
        # 3=UNKNOWN --------------------------------------


        # "AT+CGACT": "[DANGER]PDP context activate/deactivate",
        # "AT+CGDCONT": "[DANGER]define PDP context (APN, type)",
        # "AT+CGDSCONT": "[DANGER]define secondary PDP context",
        # "AT+CGDATA": "[DANGER]enter data state (PPP)",

        'AT+CGREG': ['GPRS registration status',
                     ('AT+CGREG=?', '+CGREG: (0-2)\nOK'),
                     ('AT+CGREG', 'OK'),
                     ('AT+CGREG?', '+CGREG: 0,0\nOK'),
                     ('AT+CGREG=0', 'OK'),
                     ('AT+CGREG?', '+CGREG: 0,0\nOK'),
                     ('AT+CGREG=1', 'OK'),
                     ('AT+CGREG?', '+CGREG: 1,0\nOK'),
                     ('AT+CGREG=2', 'OK'),
                     ('AT+CGREG?', '+CGREG: 2,0,"0000","00000000"\nOK'),
                     ],
        'AT+CGATT': ['packet domain attach/detach',
                     ('AT+CGATT=?', '+CGATT: (0-1)\nOK'),
                     ('AT+CGATT', 'ERROR'),
                     ('AT+CGATT?', '+CGATT: 0\nOK'),
                     ('AT+CGATT=0', 'OK'),
                     ('AT+CGATT?', '+CGATT: 0\nOK'),
                     ('AT+CGATT=1', '+CME ERROR: operation not allowed'),
                     ('AT+CGATT?', '+CGATT: 0\nOK'),
                     ],
        'AT+CGTFT': ['traffic flow template',
                     ('AT+CGTFT=?',
                      '+CGTFT: "IP",(1-15),(0-255),,(0-255),(0-65535.0-65535),(0-65535.0-65535),(0-FFFFFFFF),(0-255.0-255),(0-FFFFF)\n+CGTFT: "IPV6",(1-15),(0-255),,(0-255),(0-65535.0-65535),(0-65535.0-65535),(0-FFFFFFFF),(0-255.0-255),(0-FFFFF)\n+CGTFT: "IPV4V6",(1-15),(0-255),,(0-255),(0-65535.0-65535),(0-65535.0-65535),(0-FFFFFFFF),(0-255.0-255),(0-FFFFF)\nOK'),
                     ('AT+CGTFT', 'OK'),
                     ('AT+CGTFT?', '+CGTFT:\nOK'),
                     ('AT+CGTFT=0', '+CME ERROR: Incorrect parameters'),
                     ('AT+CGTFT?', '+CGTFT:\nOK'),
                     ('AT+CGTFT=1', '+CME ERROR: Operation not supported'),
                     ('AT+CGTFT?', '+CGTFT:\nOK'),
                     ('AT+CGTFT=2', '+CME ERROR: Operation not supported'),
                     ('AT+CGTFT?', '+CGTFT:\nOK'),
                     ('AT+CGTFT=3', '+CME ERROR: Operation not supported'),
                     ('AT+CGTFT?', '+CGTFT:\nOK'),
                     ('AT+CGTFT=4', '+CME ERROR: Operation not supported'),
                     ('AT+CGTFT?', '+CGTFT:\nOK'),
                     ('AT+CGTFT=5', '+CME ERROR: Operation not supported'),
                     ('AT+CGTFT?', '+CGTFT:\nOK'),
                     ('AT+CGTFT=6', '+CME ERROR: Operation not supported'),
                     ('AT+CGTFT?', '+CGTFT:\nOK'),
                     ('AT+CGTFT=7', '+CME ERROR: Operation not supported'),
                     ('AT+CGTFT?', '+CGTFT:\nOK'),
                     ('AT+CGTFT=8', '+CME ERROR: Operation not supported'),
                     ('AT+CGTFT?', '+CGTFT:\nOK'),
                     ('AT+CGTFT=9', '+CME ERROR: Operation not supported'),
                     ('AT+CGTFT?', '+CGTFT:\nOK'),
                     ],
        'AT+CGQREQ': ['QoS profile (requested)',
                      ('AT+CGQREQ=?', '+CGQREQ: "IP",(0-3),(0-4),(0-5),(0-9),(0-18,31)\nOK'),
                      ('AT+CGQREQ', 'OK'),
                      ('AT+CGQREQ?', 'OK'),
                      ('AT+CGQREQ=0', '+CME ERROR: Incorrect parameters'),
                      ('AT+CGQREQ?', 'OK'),
                      ('AT+CGQREQ=1', '+CME ERROR: Operation not supported'),
                      ('AT+CGQREQ?', 'OK'),
                      ('AT+CGQREQ=2', '+CME ERROR: Operation not supported'),
                      ('AT+CGQREQ?', 'OK'),
                      ('AT+CGQREQ=3', '+CME ERROR: Operation not supported'),
                      ('AT+CGQREQ?', 'OK'),
                      ('AT+CGQREQ=4', '+CME ERROR: Operation not supported'),
                      ('AT+CGQREQ?', 'OK'),
                      ('AT+CGQREQ=5', '+CME ERROR: Operation not supported'),
                      ('AT+CGQREQ?', 'OK'),
                      ('AT+CGQREQ=6', '+CME ERROR: Operation not supported'),
                      ('AT+CGQREQ?', 'OK'),
                      ('AT+CGQREQ=7', '+CME ERROR: Operation not supported'),
                      ('AT+CGQREQ?', 'OK'),
                      ('AT+CGQREQ=8', '+CME ERROR: Operation not supported'),
                      ('AT+CGQREQ?', 'OK'),
                      ('AT+CGQREQ=9', '+CME ERROR: Operation not supported'),
                      ('AT+CGQREQ?', 'OK'),
                      ],
        'AT+CGEQREQ': ['3G QoS profile (requested)',
                       ('AT+CGEQREQ=?',
                        '+CGEQREQ: "IP",(0-4),(0-256000),(0-256000),(0-256000),(0-256000),(0-2),(0-1520),("0E0","1E1","1E2","7E3","1E3","1E4","1E5","1E6"),("0E0","5E2","1E2","5E3","4E3","1E3","1E4","1E5","1E6","6E8"),(0-3),(0-950),(0-3),(0-1),(0-1)\nOK'),
                       ('AT+CGEQREQ', 'OK'),
                       ('AT+CGEQREQ?', 'OK'),
                       ('AT+CGEQREQ=0', '+CME ERROR: Incorrect parameters'),
                       ('AT+CGEQREQ?', 'OK'),
                       ('AT+CGEQREQ=1', '+CME ERROR: Operation not supported'),
                       ('AT+CGEQREQ?', 'OK'),
                       ('AT+CGEQREQ=2', '+CME ERROR: Operation not supported'),
                       ('AT+CGEQREQ?', 'OK'),
                       ('AT+CGEQREQ=3', '+CME ERROR: Operation not supported'),
                       ('AT+CGEQREQ?', 'OK'),
                       ('AT+CGEQREQ=4', '+CME ERROR: Operation not supported'),
                       ('AT+CGEQREQ?', 'OK'),
                       ('AT+CGEQREQ=5', '+CME ERROR: Operation not supported'),
                       ('AT+CGEQREQ?', 'OK'),
                       ('AT+CGEQREQ=6', '+CME ERROR: Operation not supported'),
                       ('AT+CGEQREQ?', 'OK'),
                       ('AT+CGEQREQ=7', '+CME ERROR: Operation not supported'),
                       ('AT+CGEQREQ?', 'OK'),
                       ('AT+CGEQREQ=8', '+CME ERROR: Operation not supported'),
                       ('AT+CGEQREQ?', 'OK'),
                       ('AT+CGEQREQ=9', '+CME ERROR: Operation not supported'),
                       ('AT+CGEQREQ?', 'OK'),
                       ],
        'AT+CGQMIN': ['QoS profile (minimum acceptable)',
                      ('AT+CGQMIN=?', '+CGQMIN: "IP",(0-3),(0-4),(0-5),(0-9),(0-18,31)\nOK'),
                      ('AT+CGQMIN', 'OK'),
                      ('AT+CGQMIN?', 'OK'),
                      ('AT+CGQMIN=0', '+CME ERROR: Incorrect parameters'),
                      ('AT+CGQMIN?', 'OK'),
                      ('AT+CGQMIN=1', '+CME ERROR: Operation not supported'),
                      ('AT+CGQMIN?', 'OK'),
                      ('AT+CGQMIN=2', '+CME ERROR: Operation not supported'),
                      ('AT+CGQMIN?', 'OK'),
                      ('AT+CGQMIN=3', '+CME ERROR: Operation not supported'),
                      ('AT+CGQMIN?', 'OK'),
                      ('AT+CGQMIN=4', '+CME ERROR: Operation not supported'),
                      ('AT+CGQMIN?', 'OK'),
                      ('AT+CGQMIN=5', '+CME ERROR: Operation not supported'),
                      ('AT+CGQMIN?', 'OK'),
                      ('AT+CGQMIN=6', '+CME ERROR: Operation not supported'),
                      ('AT+CGQMIN?', 'OK'),
                      ('AT+CGQMIN=7', '+CME ERROR: Operation not supported'),
                      ('AT+CGQMIN?', 'OK'),
                      ('AT+CGQMIN=8', '+CME ERROR: Operation not supported'),
                      ('AT+CGQMIN?', 'OK'),
                      ('AT+CGQMIN=9', '+CME ERROR: Operation not supported'),
                      ('AT+CGQMIN?', 'OK'),
                      ],
        'AT+CGEQMIN': ['3G QoS profile (minimum acceptable)',
                       ('AT+CGEQMIN=?',
                        '+CGEQMIN: "IP",(0-4),(0-256000),(0-256000),(0-256000),(0-256000),(0-2),(0-1520),("0E0","1E1","1E2","7E3","1E3","1E4","1E5","1E6"),("0E0","5E2","1E2","5E3","4E3","1E3","1E4","1E5","1E6","6E8"),(0-3),(0-950),(0-3),(0-1),(0-1)\nOK'),
                       ('AT+CGEQMIN', 'OK'),
                       ('AT+CGEQMIN?', 'OK'),
                       ('AT+CGEQMIN=0', '+CME ERROR: Incorrect parameters'),
                       ('AT+CGEQMIN?', 'OK'),
                       ('AT+CGEQMIN=1', '+CME ERROR: Operation not supported'),
                       ('AT+CGEQMIN?', 'OK'),
                       ('AT+CGEQMIN=2', '+CME ERROR: Operation not supported'),
                       ('AT+CGEQMIN?', 'OK'),
                       ('AT+CGEQMIN=3', '+CME ERROR: Operation not supported'),
                       ('AT+CGEQMIN?', 'OK'),
                       ('AT+CGEQMIN=4', '+CME ERROR: Operation not supported'),
                       ('AT+CGEQMIN?', 'OK'),
                       ('AT+CGEQMIN=5', '+CME ERROR: Operation not supported'),
                       ('AT+CGEQMIN?', 'OK'),
                       ('AT+CGEQMIN=6', '+CME ERROR: Operation not supported'),
                       ('AT+CGEQMIN?', 'OK'),
                       ('AT+CGEQMIN=7', '+CME ERROR: Operation not supported'),
                       ('AT+CGEQMIN?', 'OK'),
                       ('AT+CGEQMIN=8', '+CME ERROR: Operation not supported'),
                       ('AT+CGEQMIN?', 'OK'),
                       ('AT+CGEQMIN=9', '+CME ERROR: Operation not supported'),
                       ('AT+CGEQMIN?', 'OK'),
                       ],
        'AT+CGPADDR': ['show PDP address',
                       ('AT+CGPADDR=?', '+CGPADDR: ()\nOK'),
                       ('AT+CGPADDR', 'OK'),
                       ('AT+CGPADDR?', 'ERROR'),
                       ],
        'AT+CGCLASS': ['GPRS mobile station class',
                       ('AT+CGCLASS=?', '+CGCLASS: ("A")\nOK'),
                       ('AT+CGCLASS', 'OK'),
                       ('AT+CGCLASS?', '+CGCLASS: "A"\nOK'),
                       ('AT+CGCLASS=A', 'OK'),
                       ('AT+CGCLASS?', '+CGCLASS: "A"\nOK'),
                       ],
        'AT+CGEREP': ['GPRS event reporting',
                      ('AT+CGEREP=?', '+CGEREP: (0-2),(0-1)\nOK'),
                      ('AT+CGEREP', 'OK'),
                      ('AT+CGEREP?', '+CGEREP: 2,0\nOK'),
                      ('AT+CGEREP=0', 'OK'),
                      ('AT+CGEREP?', '+CGEREP: 0,0\nOK'),
                      ('AT+CGEREP=1', 'OK'),
                      ('AT+CGEREP?', '+CGEREP: 1,0\nOK'),
                      ('AT+CGEREP=2', 'OK'),
                      ('AT+CGEREP?', '+CGEREP: 2,0\nOK'),
                      ],
        'AT+CGAUTH': ['PDP-IP authentication (PAP/CHAP)',
                      ('AT+CGAUTH=?', 'ERROR'),
                      ('AT+CGAUTH', 'ERROR'),
                      ('AT+CGAUTH?', 'ERROR'),
                      ],
        'AT+CGCONTRDP': ['PDP context dynamic parameters',
                         ('AT+CGCONTRDP=?', 'OK'),
                         ('AT+CGCONTRDP', 'OK'),
                         ('AT+CGCONTRDP?',
                          '+CGCONTRDP: (<p_cid>), (<bearer_id>),(<apn>),(<source_addr and subnet_mask>),(<gw_addr>), (<DNS_prim_addr>), (<DNS_sec_addr>), (<P-CSCF_prim_addr>), (<P-CSCF_sec_addr>),(<IM_CN_Signalling_Flag>)r\nOK'),
                         ],
        'AT+CDNSSRV': ['DNS server IP',
                       ('AT+CDNSSRV=?', 'ERROR'),
                       ('AT+CDNSSRV', 'ERROR'),
                       ('AT+CDNSSRV?', 'ERROR'),
                       ],
    },

    # =========================================================================
    # 11. SIM APPLICATION TOOLKIT (SAT/STK)
    # =========================================================================
    # "SAT_STK": {
    #     # 0=DANGER+USELESS -------------------------------
    #     # 1=ACCURATE -------------------------------------
    #     # 2=DOUBT ----------------------------------------
    #     # 3=UNKNOWN --------------------------------------
    #
    #
    #     # "AT+STK": "[DANGER]STK switch (on/off)",
    #     # "AT+STKFMT": "[DANGER]STK PDU format (0=decoded, 1=PDU) # DANGER (reboot)",
    #     # "AT+STSM": "[DANGER]get STK setup menu list (PDU)",
    #
    #     'AT+STIN': ['SAT indication',
    #                 ('AT+STIN=?', 'ERROR'),
    #                 ('AT+STIN', 'ERROR'),
    #                 ('AT+STIN?', 'ERROR'),
    #                 ],
    #     'AT+STGI': ['get SAT information',
    #                 ('AT+STGI=?', 'ERROR'),
    #                 ('AT+STGI', 'ERROR'),
    #                 ('AT+STGI?', 'ERROR'),
    #                 ],
    #     'AT+STGR': ['SAT respond',
    #                 ('AT+STGR=?', 'ERROR'),
    #                 ('AT+STGR', 'ERROR'),
    #                 ('AT+STGR?', 'ERROR'),
    #                 ],
    #     'AT+STENV': ['original STK PDU envelope command',
    #                  ('AT+STENV=?', 'ERROR'),
    #                  ('AT+STENV', 'ERROR'),
    #                  ('AT+STENV?', 'ERROR'),
    #                  ],
    # },

    # =========================================================================
    # 12. FILE SYSTEM
    # =========================================================================
    # "FILE_SYSTEM": {
    #     # 0=DANGER+USELESS -------------------------------
    #     # 1=ACCURATE -------------------------------------
    #     # 2=DOUBT ----------------------------------------
    #     # 3=UNKNOWN --------------------------------------
    #
    #     # "AT+FSCD": "[DANGER]select current directory",
    #     # "AT+FSMKDIR": "[DANGER]make directory",
    #     # "AT+FSRMDIR": "[DANGER]delete directory",
    #     # "AT+FSDEL": "[DANGER]delete file",
    #     # "AT+FSRENAME": "[DANGER]rename file",
    #     # "AT+FSLOCA": "[DANGER]select storage place",
    #     # "AT+FSCOPY": "[DANGER]copy file",
    #     # "AT+CFTRANRX": "[DANGER]transfer file to EFS",
    #     # "AT+CFTRANTX": "[DANGER]transfer file from EFS",
    #
    #     'AT+FSLS': ['list directories/files',
    #                 ('AT+FSLS=?', '+FSLS: (0-2)\nOK'),
    #                 ('AT+FSLS', 'OK'),
    #                 ('AT+FSLS?', '+FSLS: SUBDIRECTORIES:0,FILES:0\nOK'),
    #                 ('AT+FSLS=0', 'OK'),
    #                 ('AT+FSLS?', '+FSLS: SUBDIRECTORIES:0,FILES:0\nOK'),
    #                 ('AT+FSLS=1', 'OK'),
    #                 ('AT+FSLS?', '+FSLS: SUBDIRECTORIES:0,FILES:0\nOK'),
    #                 ('AT+FSLS=2', 'OK'),
    #                 ('AT+FSLS?', '+FSLS: SUBDIRECTORIES:0,FILES:0\nOK'),
    #                 ],
    #     'AT+FSATTRI': ['file attributes',
    #                    ('AT+FSATTRI=?', 'OK'),
    #                    ('AT+FSATTRI', 'ERROR'),
    #                    ('AT+FSATTRI?', 'ERROR'),
    #                    ],
    #     'AT+FSMEM': ['available memory',
    #                  ('AT+FSMEM=?', 'OK'),
    #                  ('AT+FSMEM', '+FSMEM: C:(720896,438272)\nOK'),
    #                  ('AT+FSMEM?', 'ERROR'),
    #                  ],
    # },

    # =========================================================================
    # 13. INTERNET SERVICE (TCP/IP стек модуля)
    # =========================================================================
    "INTERNET_SERVICE": {
        # 0=DANGER+USELESS -------------------------------
        # "AT+CSOCKSETPN": "[DANGER]set active PDP context profile",
        # "AT+CPING": "[DANGER]ping destination",
        # "AT+CPINGSTOP": "[DANGER]stop ping",
        # "AT+CHTPUPDATE": "[DANGER]update time via HTP",
        # "AT+CNTP": "[DANGER]update time via NTP",

        # 1=ACCURATE -------------------------------------
        'AT+CTCPKA?': ['TCP heartbeat',
                       ('AT+CTCPKA=?', 'OK'),
                       ('AT+CTCPKA', 'ERROR'),
                       ('AT+CTCPKA?', '+CTCPKA: 0,120,10,10\nOK'),
                       ],
        # 2=DOUBT ----------------------------------------
        # 3=UNKNOWN --------------------------------------
        'AT+CIPDNSSET': ['DNS query parameters',
                         ('AT+CIPDNSSET=?', 'ERROR'),
                         ('AT+CIPDNSSET', 'ERROR'),
                         ('AT+CIPDNSSET?', 'ERROR'),
                         ],
        'AT+CDNSGIP': ['query IP by domain name',
                       ('AT+CDNSGIP=?', 'OK'),
                       ('AT+CDNSGIP', 'ERROR'),
                       ('AT+CDNSGIP?', 'ERROR'),
                       ],
        'AT+CDNSGHNAME': ['query domain name by IP',
                          ('AT+CDNSGHNAME=?', 'ERROR'),
                          ('AT+CDNSGHNAME', 'ERROR'),
                          ('AT+CDNSGHNAME?', 'ERROR'),
                          ],
        'AT+CTCPFIN': ['TCP FIN config',
                       ('AT+CTCPFIN=?', 'ERROR'),
                       ('AT+CTCPFIN', 'ERROR'),
                       ('AT+CTCPFIN?', 'ERROR'),
                       ],

        'AT+CTEUTP': ['unknown TCP packet echo',
                      ('AT+CTEUTP=?', 'ERROR'),
                      ('AT+CTEUTP', 'ERROR'),
                      ('AT+CTEUTP?', 'ERROR'),
                      ],
        'AT+CUPURE': ['UDP port unreachable ICMP echo',
                      ('AT+CUPURE=?', 'ERROR'),
                      ('AT+CUPURE', 'ERROR'),
                      ('AT+CUPURE?', 'ERROR'),
                      ],
        'AT+CINICMPALLOW': ['ICMP filter',
                            ('AT+CINICMPALLOW=?', 'ERROR'),
                            ('AT+CINICMPALLOW', 'ERROR'),
                            ('AT+CINICMPALLOW?', 'ERROR'),
                            ],
        'AT+CDNSSRV': ['DNS server IP',
                       ('AT+CDNSSRV=?', 'ERROR'),
                       ('AT+CDNSSRV', 'ERROR'),
                       ('AT+CDNSSRV?', 'ERROR'),
                       ],
        'AT+CHTPSERV': ['HTP server info',
                        ('AT+CHTPSERV=?',
                         '+CHTPSERV: "ADD","HOST",(1-65535),(0-1)[,"PROXY",(1-65535)]\n+CHTPSERV: "DEL",(0-15)\nOK'),
                        ('AT+CHTPSERV', 'ERROR'),
                        ('AT+CHTPSERV?', 'OK'),
                        ('AT+CHTPSERV=0', 'ERROR'),
                        ('AT+CHTPSERV?', 'OK'),
                        ('AT+CHTPSERV=1', 'ERROR'),
                        ('AT+CHTPSERV?', 'OK'),
                        ('AT+CHTPSERV=2', 'ERROR'),
                        ('AT+CHTPSERV?', 'OK'),
                        ('AT+CHTPSERV=3', 'ERROR'),
                        ('AT+CHTPSERV?', 'OK'),
                        ('AT+CHTPSERV=4', 'ERROR'),
                        ('AT+CHTPSERV?', 'OK'),
                        ('AT+CHTPSERV=5', 'ERROR'),
                        ('AT+CHTPSERV?', 'OK'),
                        ('AT+CHTPSERV=6', 'ERROR'),
                        ('AT+CHTPSERV?', 'OK'),
                        ('AT+CHTPSERV=7', 'ERROR'),
                        ('AT+CHTPSERV?', 'OK'),
                        ('AT+CHTPSERV=8', 'ERROR'),
                        ('AT+CHTPSERV?', 'OK'),
                        ('AT+CHTPSERV=9', 'ERROR'),
                        ('AT+CHTPSERV?', 'OK'),
                        ],
    },

    # =========================================================================
    # 14. OPEN/CLOSE NETWORK (для сокетов)
    # =========================================================================
    # "NETWORK_OPEN": {
    #     # 0=DANGER+USELESS -------------------------------
    #     # 1=ACCURATE -------------------------------------
    #     # 2=DOUBT ----------------------------------------
    #     # 3=UNKNOWN --------------------------------------
    #
    #
    #     # "AT+CNETSTART": "[DANGER]open packet network # DANGER",
    #     # "AT+CNETSTOP": "[DANGER]close network",
    #     # "AT+CNETIPADDR": "[DANGER]inquire PDP address",
    # },

    # =========================================================================
    # 15. GPS / GNSS
    # =========================================================================
    "GPS_GNSS": {
        # 0=DANGER+USELESS -------------------------------
        # "AT+CGPSDEL": "[DANGER]delete GPS info",
        # "AT+CGPSXD": "[DANGER]download XTRA file",

        # 1=ACCURATE -------------------------------------
        # 2=DOUBT ----------------------------------------
        # 3=UNKNOWN --------------------------------------
        'AT+CGPS': ['start/stop GPS session',
                    ('AT+CGPS=?', 'ERROR'),
                    ('AT+CGPS', 'ERROR'),
                    ('AT+CGPS?', 'ERROR'),
                    ],
        'AT+CGPSINFO': ['get GPS fixed position',
                        ('AT+CGPSINFO=?', 'ERROR'),
                        ('AT+CGPSINFO', 'ERROR'),
                        ('AT+CGPSINFO?', 'ERROR'),
                        ],
        'AT+CGPSCOLD': ['cold start GPS',
                        ('AT+CGPSCOLD=?', 'ERROR'),
                        ('AT+CGPSCOLD', 'ERROR'),
                        ('AT+CGPSCOLD?', 'ERROR'),
                        ],
        'AT+CGPSHOT': ['hot start GPS',
                       ('AT+CGPSHOT=?', 'ERROR'),
                       ('AT+CGPSHOT', 'ERROR'),
                       ('AT+CGPSHOT?', 'ERROR'),
                       ],
        'AT+CGPSURL': ['AGPS server URL',
                       ('AT+CGPSURL=?', 'ERROR'),
                       ('AT+CGPSURL', 'ERROR'),
                       ('AT+CGPSURL?', 'ERROR'),
                       ],
        'AT+CGPSSSL': ['AGPS transport security',
                       ('AT+CGPSSSL=?', 'ERROR'),
                       ('AT+CGPSSSL', 'ERROR'),
                       ('AT+CGPSSSL?', 'ERROR'),
                       ],
        'AT+CGPSAUTO': ['auto-start GPS',
                        ('AT+CGPSAUTO=?', 'ERROR'),
                        ('AT+CGPSAUTO', 'ERROR'),
                        ('AT+CGPSAUTO?', 'ERROR'),
                        ],
        'AT+CGPSNMEA': ['NMEA sentence type',
                        ('AT+CGPSNMEA=?', 'ERROR'),
                        ('AT+CGPSNMEA', 'ERROR'),
                        ('AT+CGPSNMEA?', 'ERROR'),
                        ],
        'AT+CGPSNEMARATE': ['NMEA output rate',
                            ('AT+CGPSNEMARATE=?', 'ERROR'),
                            ('AT+CGPSNEMARATE', 'ERROR'),
                            ('AT+CGPSNEMARATE?', 'ERROR'),
                            ],
        'AT+CGPSMD': ['AGPS MO method',
                      ('AT+CGPSMD=?', 'ERROR'),
                      ('AT+CGPSMD', 'ERROR'),
                      ('AT+CGPSMD?', 'ERROR'),
                      ],
        'AT+CGPSFTM': ['GPS test mode',
                       ('AT+CGPSFTM=?', 'ERROR'),
                       ('AT+CGPSFTM', 'ERROR'),
                       ('AT+CGPSFTM?', 'ERROR'),
                       ],
        'AT+CGPSXE': ['GPS XTRA enable',
                      ('AT+CGPSXE=?', 'ERROR'),
                      ('AT+CGPSXE', 'ERROR'),
                      ('AT+CGPSXE?', 'ERROR'),
                      ],
        'AT+CGPSXDAUTO': ['auto-download XTRA',
                          ('AT+CGPSXDAUTO=?', 'ERROR'),
                          ('AT+CGPSXDAUTO', 'ERROR'),
                          ('AT+CGPSXDAUTO?', 'ERROR'),
                          ],
        'AT+CGPSINFOCFG': ['report NMEA-0183 sentence',
                           ('AT+CGPSINFOCFG=?', 'ERROR'),
                           ('AT+CGPSINFOCFG', 'ERROR'),
                           ('AT+CGPSINFOCFG?', 'ERROR'),
                           ],
        'AT+CGPSPMD': ['positioning mode',
                       ('AT+CGPSPMD=?', 'ERROR'),
                       ('AT+CGPSPMD', 'ERROR'),
                       ('AT+CGPSPMD?', 'ERROR'),
                       ],
        'AT+CGPSMSB': ['based mode switch to standalone',
                       ('AT+CGPSMSB=?', 'ERROR'),
                       ('AT+CGPSMSB', 'ERROR'),
                       ('AT+CGPSMSB?', 'ERROR'),
                       ],
        'AT+CGPSHOR': ['positioning accuracy',
                       ('AT+CGPSHOR=?', 'ERROR'),
                       ('AT+CGPSHOR', 'ERROR'),
                       ('AT+CGPSHOR?', 'ERROR'),
                       ],
        'AT+CGPSNOTIFY': ['LCS respond positioning request',
                          ('AT+CGPSNOTIFY=?', 'ERROR'),
                          ('AT+CGPSNOTIFY', 'ERROR'),
                          ('AT+CGPSNOTIFY?', 'ERROR'),
                          ],
        'AT+CGNSSINFO': ['GNSS fixed position',
                         ('AT+CGNSSINFO=?', 'ERROR'),
                         ('AT+CGNSSINFO', 'ERROR'),
                         ('AT+CGNSSINFO?', 'ERROR'),
                         ],
        'AT+CGNSSMODE': ['GNSS support mode',
                         ('AT+CGNSSMODE=?', 'ERROR'),
                         ('AT+CGNSSMODE', 'ERROR'),
                         ('AT+CGNSSMODE?', 'ERROR'),
                         ],
    },

    # =========================================================================
    # 16. РАЗНОЕ / ВЕНДОРСКОЕ
    # =========================================================================
    "MISC/VENDOR(может быть не указан в мануале)": {
        # 0=DANGER+USELESS -------------------------------
        # "AT*CNETSCAN": "[DANGER]vendor: network scan (может отсутствовать)",

        # 1=ACCURATE -------------------------------------
        'AT+WS46?': ['RAT selection',
                     ('AT+WS46=?', '+WS46: (12,22,25,28,29,30,31)\nOK'),
                     ('AT+WS46', 'OK'),
                     ('AT+WS46?', '+WS46:12\nOK'),
                     ('AT+WS46=12', 'OK'),
                     ('AT+WS46?', '+WS46:12\nOK'),
                     ('AT+WS46=22', 'OK'),
                     ('AT+WS46?', '+WS46:12\nOK'),
                     ('AT+WS46=25', 'OK'),
                     ('AT+WS46?', '+WS46:12\nOK'),
                     ('AT+WS46=28', 'OK'),
                     ('AT+WS46?', '+WS46:28\nOK'),
                     ('AT+WS46=29', 'OK'),
                     ('AT+WS46?', '+WS46:28\nOK'),
                     ('AT+WS46=30', 'OK'),
                     ('AT+WS46?', '+WS46:30\nOK'),
                     ('AT+WS46=31', 'OK'),
                     ('AT+WS46?', '+WS46:30\nOK'),
                     ],
        'AT+CESQ': ['extended signal quality',
                    ('AT+CESQ=?', '+CESQ: (0-63,99),(0-7,99),(0-96,255),(0-49,255),(0-34,255),(0-97,255)\nOK'),
                    ('AT+CESQ', '+CESQ: 99,99,255,255,9,51\nOK'),
                    ('AT+CESQ?', '+CME ERROR: unknown error'),
                    ('AT+CESQ=0', '+CME ERROR: unknown error'),
                    ('AT+CESQ?', '+CME ERROR: unknown error'),
                    ('AT+CESQ=1', '+CME ERROR: unknown error'),
                    ('AT+CESQ?', '+CME ERROR: unknown error'),
                    ('AT+CESQ=2', '+CME ERROR: unknown error'),
                    ('AT+CESQ?', '+CME ERROR: unknown error'),
                    ('AT+CESQ=3', '+CME ERROR: unknown error'),
                    ('AT+CESQ?', '+CME ERROR: unknown error'),
                    ('AT+CESQ=4', '+CME ERROR: unknown error'),
                    ('AT+CESQ?', '+CME ERROR: unknown error'),
                    ('AT+CESQ=5', '+CME ERROR: unknown error'),
                    ('AT+CESQ?', '+CME ERROR: unknown error'),
                    ('AT+CESQ=6', '+CME ERROR: unknown error'),
                    ('AT+CESQ?', '+CME ERROR: unknown error'),
                    ('AT+CESQ=7', '+CME ERROR: unknown error'),
                    ('AT+CESQ?', '+CME ERROR: unknown error'),
                    ('AT+CESQ=8', '+CME ERROR: unknown error'),
                    ('AT+CESQ?', '+CME ERROR: unknown error'),
                    ('AT+CESQ=9', '+CME ERROR: unknown error'),
                    ('AT+CESQ?', '+CME ERROR: unknown error'),
                    ],
        'AT+CPINR?': ['PIN retries',
                      ('AT+CPINR=?', '+CPINR: (0-3),(0-3),(0-10),(0-10)\nOK'),
                      ('AT+CPINR', '+CME ERROR: Operation not supported'),
                      ('AT+CPINR?', '+CME ERROR: SIM not inserted'),
                      ('AT+CPINR=0', 'ERROR'),
                      ('AT+CPINR?', '+CME ERROR: SIM not inserted'),
                      ('AT+CPINR=1', 'ERROR'),
                      ('AT+CPINR?', '+CME ERROR: SIM not inserted'),
                      ('AT+CPINR=2', 'ERROR'),
                      ('AT+CPINR?', '+CME ERROR: SIM not inserted'),
                      ('AT+CPINR=3', 'ERROR'),
                      ('AT+CPINR?', '+CME ERROR: SIM not inserted'),
                      ('AT+CPINR=4', 'ERROR'),
                      ('AT+CPINR?', '+CME ERROR: SIM not inserted'),
                      ('AT+CPINR=5', 'ERROR'),
                      ('AT+CPINR?', '+CME ERROR: SIM not inserted'),
                      ('AT+CPINR=6', 'ERROR'),
                      ('AT+CPINR?', '+CME ERROR: SIM not inserted'),
                      ('AT+CPINR=7', 'ERROR'),
                      ('AT+CPINR?', '+CME ERROR: SIM not inserted'),
                      ('AT+CPINR=8', 'ERROR'),
                      ('AT+CPINR?', '+CME ERROR: SIM not inserted'),
                      ('AT+CPINR=9', 'ERROR'),
                      ('AT+CPINR?', '+CME ERROR: SIM not inserted'),
                      ],
        'AT+CGCONTRDP?': ['PDP context dynamic params',
                          ('AT+CGCONTRDP=?', 'OK'),
                          ('AT+CGCONTRDP', 'OK'),
                          ('AT+CGCONTRDP?',
                           '+CGCONTRDP: (<p_cid>), (<bearer_id>),(<apn>),(<source_addr and subnet_mask>),(<gw_addr>), (<DNS_prim_addr>), (<DNS_sec_addr>), (<P-CSCF_prim_addr>), (<P-CSCF_sec_addr>),(<IM_CN_Signalling_Flag>)r\nOK'),
                          ],
        # 2=DOUBT ----------------------------------------
        # 3=UNKNOWN --------------------------------------
        'AT*CNTI': ['vendor: cell info (может отсутствовать)',
                    ('AT*CNTI=?', 'ERROR'),
                    ('AT*CNTI', 'ERROR'),
                    ('AT*CNTI?', 'ERROR'),
                    ],
        'AT*CPSI': ['vendor: PSI (может отсутствовать)',
                    ('AT*CPSI=?', 'ERROR'),
                    ('AT*CPSI', 'ERROR'),
                    ('AT*CPSI?', 'ERROR'),
                    ],
        'AT*CELLINFO': ['vendor: cell info (может отсутствовать)',
                    ('AT*CELLINFO=?', 'ERROR'),
                    ('AT*CELLINFO', 'ERROR'),
                    ('AT*CELLINFO?', 'ERROR'),
                    ],
        'AT+CRUSET': ['vendor: RU settings (может отсутствовать)',
                      ('AT+CRUSET=?', 'ERROR'),
                      ('AT+CRUSET', 'ERROR'),
                      ('AT+CRUSET?', 'ERROR'),
                      ],
        'AT+CCED': ['vendor: cell environment description',
                    ('AT+CCED=?', 'ERROR'),
                    ('AT+CCED', 'ERROR'),
                    ('AT+CCED?', 'ERROR'),
                    ],
        'AT+CIREG': ['IMS registration',
                     ('AT+CIREG=?', '+CIREG: (0-3)\nOK'),
                     ('AT+CIREG', '+CME ERROR: Operation not supported'),
                     ('AT+CIREG?', '+CME ERROR: Operation not supported'),
                     ('AT+CIREG=0', '+CME ERROR: Operation not supported'),
                     ('AT+CIREG?', '+CME ERROR: Operation not supported'),
                     ('AT+CIREG=1', '+CME ERROR: Operation not supported'),
                     ('AT+CIREG?', '+CME ERROR: Operation not supported'),
                     ('AT+CIREG=2', '+CME ERROR: Operation not supported'),
                     ('AT+CIREG?', '+CME ERROR: Operation not supported'),
                     ('AT+CIREG=3', '+CME ERROR: Operation not supported'),
                     ('AT+CIREG?', '+CME ERROR: Operation not supported'),
                     ],
        'AT+CIMS': ['IMS status',
                    ('AT+CIMS=?', 'ERROR'),
                    ('AT+CIMS', 'ERROR'),
                    ('AT+CIMS?', 'ERROR'),
                    ],
    },
}


# ----------------------------------------------------------------------------------------------------------------------
# @pytest.mark.skip
@pytest.mark.parametrize(
    argnames="group_name, cmds",
    argvalues=AT_GROUPS.items(),
    ids=AT_GROUPS.keys(),
)
def test__at_param__GROUPS(group_name, cmds, harvest, gsm_at__port):
    harvest.at_cmds__explore(cmds=cmds, port=gsm_at__port)


# ======================================================================================================================
