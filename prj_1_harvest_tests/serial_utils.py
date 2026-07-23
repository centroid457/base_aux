from typing import *

import time
import threading
import logging

from base_aux.buses.d1_serial2_new.m1_serial_client import *
from base_aux.buses.d1_serial2_new.m2_manager import *


# =====================================================================================================================
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# =====================================================================================================================
class SerialManager_Harvest(SerialManager):
    def harvest__validate(self, conn: SerialClient2) -> bool:
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
        return self.harvest__try_login(conn) and self.harvest__check_login(conn)

    def harvest__try_login(self, conn: SerialClient2) -> bool:
        data = conn.write_read_bytes(data="root", timeout_continue=0.5)
        if b"command not found" in data:
            # already logged in!
            return True

        elif b"Password:" in data:
            data = conn.write_read_bytes(data="1", timeout_continue=3)
            if b"root@harvest" in data:
                return True

        return False

    def harvest__check_login(self, conn: SerialClient2) -> bool:
        data = conn.write_read_bytes(data="hostname")
        return b"root@harvest" in data

    def harvest__get_name_and_occupy(self, conn: SerialClient2) -> str:
        data = conn.write_read_lines(data="hostname")
        device_name = data[1]
        conn.occupy(device_name)
        return device_name


# =====================================================================================================================
manager = SerialManager_Harvest()


# =====================================================================================================================
