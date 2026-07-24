from typing import *

import time
import threading
import logging

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
    def cmd__send_with_timeout(self, cmd: str, timeout: float = 1.0) -> bool:
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
        # return self.conn.write_bytes(f"{cmd} & sleep {timeout}; kill %1")
        return self.conn.write_bytes(f"timeout {timeout} {cmd}")

    def cmd__check_success(self, cmd: str, timeout_continue: float = 1.5, **wr_kwargs) -> bool:
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
        result = self.cmd__check_success(f"apt install -y {module}", timeout_continue=timeout_continue, **wr_kwargs)
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
        return self.cmd__check_success(
                "ping -c 1 -W 1 8.8.8.8",
                timeout_continue=2,
            )

    # ------------------------------------------------------------------------------------------------------------------


# ======================================================================================================================
