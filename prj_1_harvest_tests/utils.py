from typing import *

import time
import re
import threading
import logging
import base64

from base_aux.buses.d1_serial2_new.m1_serial_client import SerialClient2


# ======================================================================================================================
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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
            data = self.conn.write_read_bytes(data="1", timeout_continue=3)
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

    # ------------------------------------------------------------------------------------------------------------------
    def _cmd_with_timeout(self, cmd: str, timeout: float | None = None) -> str:
        result = ""
        if timeout:
            result += f"timeout {timeout} "

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

        return self.conn.write_bytes(self._cmd_with_timeout(cmd, timeout))

    def cmd_timeout__write_read_bytes(self, cmd: str, timeout: float | None = None, **r_kwargs) -> bytes:
        return self.conn.write_read_bytes(self._cmd_with_timeout(cmd, timeout), **r_kwargs)

    def cmd_timeout__write_read_lines(self, cmd: str, timeout: float | None = None, **r_kwargs) -> str | list[str]:
        return self.conn.write_read_lines(self._cmd_with_timeout(cmd, timeout), **r_kwargs)

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
        try:
            # Используем обёртку cmd_timeout__write_read_bytes, но она возвращает bytes,
            # а нам нужна только полезная часть, отсекая эхо команды и приглашение.
            # Можно написать специальную обработку, но проще выполнить через read_lines
            # и склеить всё, кроме первой и последней строк (эхо + приглашение).
            raw = self.cmd_timeout__write_read_lines(cmd, timeout=timeout, timeout_continue=timeout_continue, **r_kwargs)
            if isinstance(raw, list):
                # Обычно формат: [эхо команды, ... вывод ..., последнее приглашение]
                # Отсекаем первую строку (эхо) и последнюю (если она содержит '#')
                lines = raw[1:] if len(raw) > 1 else []

                while lines and (re.match(r".+@.+:.*#\s*", lines[-1]) or lines[-1].strip() == ''):
                    lines = lines[:-1]
                return '\n'.join(lines)
            else:
                return raw
        except Exception:
            return ''

    # ------------------------------------------------------------------------------------------------------------------
    def cmd__check_executed_success(self, cmd: str, timeout_continue: float = 1.5, **wr_kwargs) -> bool:
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
        out = self.conn.write_read_lines(f"{cmd} 2>/dev/null || echo {ERROR_MSG}", timeout_continue=timeout_continue, **wr_kwargs)
        print(f"{out=}")
        return ERROR_MSG not in out[1:]

    # ------------------------------------------------------------------------------------------------------------------
    def apt_install(self, module: str, timeout_continue: float = 5, **wr_kwargs) -> bool:
        """
        if need DELETE
            sudo apt remove picocom
        """
        result = self.cmd__check_executed_success(f"apt install -y {module}", timeout_continue=timeout_continue, **wr_kwargs)
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
        return self.cmd__check_executed_success(
                "ping -c 1 -W 1 8.8.8.8",
                timeout_continue=2,
            )

    # ------------------------------------------------------------------------------------------------------------------
    def push_text_file(self, text: str, filepath: str = "/tmp/script.py") -> bool:
        """
        GOAL
        transfer file scripts into device,
        original purpose is for *.py, but may any!

        dirpath - MAINLY USE "/tmp"!!! if want to place into current - pass NONE!!!
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
            if not self.cmd__check_executed_success(cmd):
                return False

        # 2=PUSH --------------------
        text_b64 = base64.b64encode(text.encode()).decode()
        # printf не добавляет '\n', в отличие от echo; одинарные кавычки защищают от пробелов.
        cmd = f"printf '%s' '{text_b64}' | base64 -d > {filepath}"
        return self.cmd__check_executed_success(cmd)

    # PARSERS ----------------------------------------------------------------------------------------------------------
    def get_system_info(self) -> dict:
        info = {}

        # ----- Идентификация и версия ОС -----
        info['hostname'] = self.cmd_timeout__write_read__payload_str("hostname").strip()

        raw_os = self.cmd_timeout__write_read__payload_str("cat /etc/os-release 2>/dev/null")
        os_dict = {}
        for line in raw_os.split('\n'):
            if '=' in line:
                k, v = line.split('=', 1)
                os_dict[k.strip()] = v.strip().strip('"')
        info['os'] = os_dict

        info['kernel'] = self.cmd_timeout__write_read__payload_str("uname -r").strip()
        info['architecture'] = self.cmd_timeout__write_read__payload_str("uname -m").strip()

        # ----- Модель платы -----
        # Попытка через device-tree, иначе через dmesg
        model = self.cmd_timeout__write_read__payload_str(
            "cat /proc/device-tree/model 2>/dev/null || cat /sys/firmware/devicetree/base/model 2>/dev/null"
        ).strip()
        if not model:
            dmesg_model = self.cmd_timeout__write_read__payload_str(
                "dmesg | grep 'Machine model' | head -1 | cut -d: -f2-"
            ).strip()
            model = dmesg_model if dmesg_model else "N/A"
        info['board_model'] = model

        # ----- CPU -----
        cpu_lines = self.cmd_timeout__write_read__payload_str("cat /proc/cpuinfo 2>/dev/null")
        cores = 0
        model_name = ""
        for line in cpu_lines.split('\n'):
            if line.startswith("processor"):
                cores += 1
            if line.startswith("model name") and not model_name:
                model_name = line.split(":")[1].strip()
            if line.startswith("Hardware") and not model_name:
                model_name = line.split(":")[1].strip()
        info['cpu'] = {
            'model': model_name or 'ARM',
            'cores': cores
        }

        # ----- Память -----
        mem_lines = self.cmd_timeout__write_read__payload_str("free -m 2>/dev/null || cat /proc/meminfo")
        if 'Mem:' in mem_lines:
            mem_parts = mem_lines.split('\n')[1].split()
            total = mem_parts[1]
            used = mem_parts[2]
            free = mem_parts[3]
            info['memory'] = {'total_mb': int(total), 'used_mb': int(used), 'free_mb': int(free)}
        else:
            mem = {}
            for line in mem_lines.split('\n'):
                parts = line.split()
                if len(parts) >= 2:
                    mem[parts[0].rstrip(':')] = parts[1]
            info['memory'] = mem

        # ----- Накопители -----
        disk_lines = self.cmd_timeout__write_read__payload_str("df -h / 2>/dev/null || echo 'N/A'")
        if disk_lines and disk_lines != 'N/A':
            parts = disk_lines.split('\n')[1].split()
            info['disk'] = {'total': parts[1], 'used': parts[2], 'available': parts[3], 'use%': parts[4]}
        else:
            info['disk'] = 'N/A'

        # ----- Uptime -----
        uptime_raw = self.cmd_timeout__write_read__payload_str("cat /proc/uptime")
        info['uptime'] = uptime_raw.split()[0] if uptime_raw else 'N/A'

        # ----- Сетевые интерфейсы -----
        net = {}
        iface_list = self.cmd_timeout__write_read__payload_str("ls /sys/class/net/").split()
        for iface in iface_list:
            iface = iface.strip()
            if not iface or iface == 'lo':
                continue
            mac = self.cmd_timeout__write_read__payload_str(f"cat /sys/class/net/{iface}/address 2>/dev/null").strip()
            ip_addr = self.cmd_timeout__write_read__payload_str(
                f"ip -4 addr show {iface} 2>/dev/null | grep inet | head -1")
            net[iface] = {
                'mac': mac if mac else 'N/A',
                'ip': ip_addr.split()[1].split('/')[0] if 'inet' in ip_addr else 'N/A'
            }
        info['network'] = net

        # ----- USB‑устройства (исправляем таймаут и убираем лишний stderr) -----
        # Используем timeout_continue=2 для гарантированного чтения вывода
        usb_raw = self.cmd_timeout__write_read__payload_str(
            "timeout 2 lsusb",
            timeout=None,  # команда сама содержит timeout
            timeout_continue=2.0  # ждём до 2 секунд после эхо
        )
        info['usb_devices'] = [line.strip() for line in usb_raw.split('\n') if line.strip() and 'lsusb' not in line]

        # ----- I2C‑шины -----
        i2c_list = self.cmd_timeout__write_read__payload_str("i2cdetect -l 2>/dev/null").split('\n')
        info['i2c_buses'] = {}
        for bus_line in i2c_list:
            if 'i2c-' in bus_line:
                bus_num = bus_line.split()[0].split('-')[1]
                scan = self.cmd_timeout__write_read__payload_str(f"i2cdetect -y {bus_num} 2>/dev/null",
                                                                 timeout_continue=1.5)
                # Оставляем только строки с данными
                info['i2c_buses'][f'i2c-{bus_num}'] = [x.strip() for x in scan.split('\n')[1:] if x.strip()]

        # ----- Версия U‑Boot (ищем через grep) -----
        uboot_raw = self.cmd_timeout__write_read__payload_str(
            "dmesg | grep -i 'u-boot\|uboot' | head -1"
        ).strip()
        info['uboot'] = uboot_raw if uboot_raw else 'N/A'

        return info

    # PARSERS ----------------------------------------------------------------------------------------------------------
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
