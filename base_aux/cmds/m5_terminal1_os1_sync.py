import subprocess
import threading
import time
import errno

from base_aux.cmds.m5_terminal0_abc1_user_conn import *
from base_aux.cmds.m5_terminal2_serial0_mark import *
from base_aux.cmds.m5_terminal0_abc2_paradigm import BaseSync_CmdTerminal


# =====================================================================================================================
class CmdTerminal_OsSync(Mark_CmdTerminal_Serial, BaseSync_CmdTerminal):
   pass


# =====================================================================================================================
if __name__ == "__main__":
    pass
    # _explore__ping()
    # _explore__cd()
    # _explore__cd_reconnect()
    # explore__smth()


# =====================================================================================================================
