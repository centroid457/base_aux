from typing import *

import time
import re
import threading
import json
import logging
import base64

from base_aux.buses.d1_serial2_new.m1_serial_client import SerialClient2
from base_aux.aux_eq.m3_eq_valid3_derivatives import *


# ======================================================================================================================
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ======================================================================================================================
SCRIPTS: dict[str, str] = {     # PATH/TEXT
    "/tmp/get__gnss_info__ubx.py": r"""
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
    """,
    #     get__gnss_info__ubx = r"""
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

    "/tmp/at_client.py": r"""
import sys, time, serial, os

if len(sys.argv) < 2:
    print("Usage: python3 /tmp/at_client.py <AT command> [port] [baudrate]")
    sys.exit(1)

cmd = sys.argv[1]
port = sys.argv[2] if len(sys.argv) > 2 else "/dev/ttyUSB2"
baudrates = [115200, 9600, 57600, 38400, 19200]
if len(sys.argv) > 3:
    baudrates = [int(sys.argv[3])]

# Попытка освободить порт, если занят
os.system(f"fuser -k {port} 2>/dev/null")

last_err = None
for baud in baudrates:
    try:
        s = serial.Serial(port, baud, timeout=0.3,
                          rtscts=False, dsrdtr=False, exclusive=True)
        s.reset_input_buffer()
        s.write((cmd + "\r\n").encode())
        time.sleep(0.4)  # ждём ответ
        result = s.read(4096).decode(errors='replace')
        print(result)
        s.close()
        sys.exit(0)
    except Exception as exc:
        last_err = exc
        try: s.close()
        except: pass
        continue

print(f"AT_ERROR:{last_err!r}")
sys.exit(1)
    """
}


# ======================================================================================================================
class HarvestDevice:
    def __init__(self, conn: SerialClient2):
        self.conn = conn

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
        return self.login_try() and self.login_check()

    def login_try(self) -> bool:
        data = self.conn.write_read_bytes(data="root", timeout_continue=0.5)
        if b"command not found" in data:
            # already logged in!
            return True

        elif b"Password:" in data:
            data = self.conn.write_read_bytes(data="1", timeout_continue=6)
            if b"root@harvest" in data:
                return True

        return False

    def login_check(self) -> bool:
        data = self.conn.write_read_bytes(data="hostname")
        return b"root@harvest" in data

    def get_hostname_and_occupy(self) -> str:
        data = self.conn.write_read_lines(data="hostname")
        device_name = data[1]
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

    def cmd_timeout__write_read_lines(
            self,
            cmd: str,
            timeout: float | None = None,

            payload_only: bool | None = None,
            return_str: bool | None = None,
            **r_kwargs,
    ) -> str | list[str]:
        cmd_ = self._cmd_cover_timeout(cmd, timeout)
        output = self.conn.write_read_lines(cmd_, **r_kwargs)
        if not payload_only:
            return output

        result = output[1:]
        while result and (re.match(r".+@.+:.*#\s*", result[-1]) or result[-1].strip() == ''):
            result = result[:-1]
        if return_str:
            result = '\n'.join(result)
        return result

    # ------------------------------------------------------------------------------------------------------------------
    # Вспомогательный приватный метод для выполнения команды и получения строки
    def cmd_timeout__write_read__payload_str(
            self,
            cmd: str,
            timeout: float | None = None,
            timeout_continue: float = 1.0,
            **r_kwargs,
    ) -> str:
        """
        Выполняет команду на устройстве и возвращает stdout в виде строки.
        При ошибке возвращает пустую строку.
        """
        return self.cmd_timeout__write_read_lines(
            cmd,
            timeout=timeout,
            timeout_continue=timeout_continue,
            payload_only=True,
            return_str=True ,
            **r_kwargs)

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
        out = self.cmd_timeout__write_read__payload_str(f"{cmd} 2>/dev/null || echo {ERROR_MSG}", **wr_kwargs)
        return ERROR_MSG not in out[1:]

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
        output = self.cmd_timeout__write_read__payload_str(
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
        text = SCRIPTS[name]
        return self._file_text__push(filepath=name, text=text)

    def _file_text__push(self, filepath: str = "/tmp/script.py", text: str = "") -> bool:
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

    # ------------------------------------------------------------------------------------------------------------------
    def send__at_command__simple(self, cmd: str, port="/dev/ttyUSB2", timeout=1.0) -> str:
        # Отправить команду, прочитать ответ с таймаутом через утилиту timeout
        # - ВАЖНО: bash -c нужен, чтобы пайп обрабатывался целиком
        full_cmd = (
            f"timeout {timeout} bash -c 'echo -e \"{cmd}\\r\\n\" > {port}; "
            f"timeout {timeout} cat {port}'"
        )
        output = self.cmd_timeout__write_read__payload_str(full_cmd, timeout=timeout * 2)
        # Убираем возможное эхо команды
        output = output.replace(cmd + "\n", "")
        return output

    def send__at_command__raw(
            self,
            cmd: str,
            bridge: str = "/tmp/at_client.py",
            port: str = "/dev/ttyUSB2",
            baudrate: int = 115200,
            timeout: float = 2.0,
            **read_kwargs
    ) -> str | NoReturn:
        """
        Отправляет AT-команду через скрипт на устройстве и возвращает строку ответа.
        """
        command_line = f"python3 {bridge} '{cmd}' {port} {baudrate}"
        output = ""
        for _ in range(2):
            output = self.cmd_timeout__write_read__payload_str(
                command_line,
                timeout=timeout,
                timeout_continue=timeout * 1.5,
                **read_kwargs
            )
            # Убираем возможное эхо команды
            output = output.replace(cmd + "\n", "")

            if "No such file or directory" in output:
                if not self.file_name__push(bridge):
                    break

        return output

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
        for service in ["ModemManager", ]:
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
            )

    # INFO =============================================================================================================
    def get_info__system(self) -> dict[str, Any]:
        result = {}

        # ----- Идентификация и версия ОС -----
        result['hostname'] = self.cmd_timeout__write_read__payload_str("hostname", timeout=1).strip()

        raw_os = self.cmd_timeout__write_read__payload_str("cat /etc/os-release 2>/dev/null", timeout=3)
        os_dict = {}
        for line in raw_os.split('\n'):
            if '=' in line:
                k, v = line.split('=', 1)
                os_dict[k.strip()] = v.strip().strip('"')
        result['os'] = os_dict

        result['kernel'] = self.cmd_timeout__write_read__payload_str("uname -r", timeout=1).strip()
        result['architecture'] = self.cmd_timeout__write_read__payload_str("uname -m", timeout=1).strip()

        # ----- Модель платы -----
        # Попытка через device-tree, иначе через dmesg
        model = self.cmd_timeout__write_read__payload_str(
            "cat /proc/device-tree/model 2>/dev/null || cat /sys/firmware/devicetree/base/model 2>/dev/null"
            , timeout=5
        ).strip()
        if not model:
            dmesg_model = self.cmd_timeout__write_read__payload_str(
                "dmesg | grep 'Machine model' | head -1 | cut -d: -f2-",
                timeout=3
            ).strip()
            model = dmesg_model if dmesg_model else "N/A"
        result['board_model'] = model

        # ----- CPU -----
        cpu_lines = self.cmd_timeout__write_read__payload_str("cat /proc/cpuinfo 2>/dev/null", timeout=3)
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
        mem_lines = self.cmd_timeout__write_read__payload_str("free -m 2>/dev/null || cat /proc/meminfo", timeout=3)
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
        disk_lines = self.cmd_timeout__write_read__payload_str("df -h / 2>/dev/null || echo NA", timeout=3)
        if disk_lines and disk_lines != 'N/A':
            parts = disk_lines.split('\n')[1].split()
            result['disk'] = {'total': parts[1], 'used': parts[2], 'available': parts[3], 'use%': parts[4]}
        else:
            result['disk'] = 'N/A'

        # ----- Uptime -----
        uptime_raw = self.cmd_timeout__write_read__payload_str("cat /proc/uptime", timeout=1)
        result['uptime'] = uptime_raw.split()[0] if uptime_raw else 'N/A'

        # ----- Сетевые интерфейсы -----
        net = {}
        iface_list = self.cmd_timeout__write_read__payload_str("ls /sys/class/net/", timeout=3).split()
        for iface in iface_list:
            iface = iface.strip()
            if not iface or iface == 'lo':
                continue
            mac = self.cmd_timeout__write_read__payload_str(f"cat /sys/class/net/{iface}/address 2>/dev/null", timeout=3).strip()
            ip_addr = self.cmd_timeout__write_read__payload_str(
                f"ip -4 addr show {iface} 2>/dev/null | grep inet | head -1")
            net[iface] = {
                'mac': mac if mac else 'N/A',
                'ip': ip_addr.split()[1].split('/')[0] if 'inet' in ip_addr else 'N/A'
            }
        result['network'] = net

        # ----- USB‑устройства (исправляем таймаут и убираем лишний stderr) -----
        # Используем timeout_continue=2 для гарантированного чтения вывода
        usb_raw = self.cmd_timeout__write_read__payload_str(
            "lsusb",
            timeout = 3,
            timeout_continue=2.0  # ждём до 2 секунд после эхо
        )
        result['usb_devices'] = [line.strip() for line in usb_raw.split('\n') if line.strip() and 'lsusb' not in line]

        # ----- I2C‑шины -----
        i2c_list = self.cmd_timeout__write_read__payload_str("i2cdetect -l 2>/dev/null", timeout=2).split('\n')
        result['i2c_buses'] = {}
        for bus_line in i2c_list:
            if 'i2c-' in bus_line:
                bus_num = bus_line.split()[0].split('-')[1]
                scan = self.cmd_timeout__write_read__payload_str(
                    f"i2cdetect -y {bus_num} 2>/dev/null",
                    timeout_continue=1.5,
                    timeout=2,
                )
                # Оставляем только строки с данными
                result['i2c_buses'][f'i2c-{bus_num}'] = [x.strip() for x in scan.split('\n')[1:] if x.strip()]

        # ----- Версия U‑Boot (ищем через grep) -----
        uboot_raw = self.cmd_timeout__write_read__payload_str(
            "dmesg | grep -i 'u-boot\|uboot' | head -1",
            timeout=2
        ).strip()
        result['uboot'] = uboot_raw if uboot_raw else 'N/A'

        return result

    # ------------------------------------------------------------------------------------------------------------------
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
        output = self.cmd_timeout__write_read__payload_str(
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

    # PARSERS ==========================================================================================================
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


# ======================================================================================================================
