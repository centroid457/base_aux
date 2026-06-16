import subprocess
import threading
import time
import errno

from base_aux.cmds.m5_terminal0_abc1_user import *
from base_aux.cmds.m5_terminal2_serial0_base import *
from base_aux.cmds.m5_terminal0_abc3_paradigm import BaseSync_CmdTerminal


# =====================================================================================================================
class CmdTerminal_OsSync(Base_CmdTerminal_Serial, BaseSync_CmdTerminal):
   pass


# =====================================================================================================================
if __name__ == "__main__":
    pass
    # _explore__ping()
    # _explore__cd()
    # _explore__cd_reconnect()
    # explore__smth()


# =====================================================================================================================
