from typing import *

import subprocess
import time

from base_aux.loggers.m1_print import *
from base_aux.base_values.m3_exceptions import *
from base_aux.cmds.m2_history import *


# =====================================================================================================================
class CmdExecutor:
    """
    GOAL
    ----
    send commands into OS terminal

    "check if cmds commands are accessible (special utilities is installed)",
    "access to standard parts of result in a simple ready-to-use form (stdout/stderr/retcode/full state)",
    "use batch timeout for list",
    "till_first_true",

    :ivar TIMEOUT: default timeout for execution process
        if timeout expired and process still not finished - raise exc
    :ivar _last_sp: Popen object
    :ivar CMDS_REQUIRED: commands for cli_check_available
        dict with NAME - exact commands which will send into terminal in order to check some utility is installed,
        VALUE - message if command get any error

        RECOMMENDATIONS
        --------------
        1. --HELP never works as expected! always timedout!!!!
            [#####################ERROR#####################]
            self.last_cmd='STM32_Programmer_CLI --help'
            self.last_duration=2.029675
            self.last_retcode=None
            --------------------------------------------------
            self.last_stdout=
            --------------------------------------------------
            self.last_stderr=
            --------------------------------------------------
            self._last_exc_timeout=TimeoutError("TimeoutExpired('STM32_Programmer_CLI --help', 2)")
            ==================================================
            [ERROR] cmd NOT available [STM32_Programmer_CLI --help]
            ==================================================

        2. DIRECT SIMPLE CLI COMMAND AS UTILITY_NAME.EXE without any parameter MAY NOT WORK!!! may timedout! implied the same as HELP parameter!
            [#####################ERROR#####################]
            self.last_cmd='STM32_Programmer_CLI'
            self.last_duration=2.022585
            self.last_retcode=None
            --------------------------------------------------
            self.last_stdout=
            --------------------------------------------------
            self.last_stderr=
            --------------------------------------------------
            self._last_exc_timeout=TimeoutError("TimeoutExpired('STM32_Programmer_CLI', 2)")
            ==================================================

        3. use --VERSION! instead! - seems work fine always!
    """
    # SETTINGS ------------------------------------
    TIMEOUT: Optional[float] = 2
    RAISE: Optional[bool] = None

    CMDS_REQUIRED: dict[str, Optional[str]] | None = None

    # init ------------------------------------------------------------------------------------------------------------
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.history = CmdHistory()

        if not self.cli_check_available():
            msg = f"CLI not available"
            raise Exc__NotAvailable(msg)

    # SEND ------------------------------------------------------------------------------------------------------------
    def send(
            self,
            cmd: TYPING__CMDS_CONDITIONS,
            timeout: Optional[float] = None,
            till_first_true: Optional[bool] = None,
            _raise: Optional[bool] = None,
            print_all_states: Optional[bool] = None,
    ) -> bool | NoReturn:
        """execute CLI command in terminal

        :param cmd: commands for execution
        :param timeout: use special timeout step_result_enum, instead of default, for cms_list will used as cumulated!
            # TODO: need decide about cumulation! more preferable apply as default! -NO its OK!
            so if you use list - apply timeout for CUMULATED! and dont pass it if no need cumulation!
            if single - apply as single!
        :param till_first_true: useful for detection or just multiPlatform usage
        :param _raise: if till_first_true=True it will not work (return always bool in this case)!!!
        :param print_all_states: all or only Failed
        """
        # CMDS LIST ---------------------------------------------------------------------------------------------------
        if isinstance(cmd, list):
            time_start = time.time()
            result = True

            _raise_list = _raise
            if till_first_true:
                _raise_list = False

            for cmd_item in cmd:
                time_passed = time.time() - time_start
                try:
                    timeout = timeout - time_passed
                except:
                    pass

                result = self.send(cmd=cmd_item, timeout=timeout, _raise=_raise_list)

                if till_first_true:
                    if result:
                        return True
                else:
                    if not result:
                        Warn(f"{cmd_item=} in full sequence {cmd=}")
                        return False

            return result

        # params apply ------------------------------------------------------------------------------------------------
        Print(f"[CLI_SEND]{cmd}")

        if isinstance(cmd, tuple) and len(cmd) == 2:
            cmd, timeout_i = cmd
            if timeout_i is not None:
                timeout = timeout_i

        self.last_cmd = cmd

        if timeout is None:
            timeout = self.TIMEOUT
        if _raise is None:
            _raise = self.RAISE

        # work --------------------------------------------------------------------------------------------------------
        if timeout < 0:
            msg = f"{timeout=} is sub zero"
            self.last_exc_timeout = TimeoutError(msg)
            print(msg)
            if _raise:
                raise TimeoutError(msg)
            else:
                return False

        # todo: check for linux! encoding is not necessary!
        self._last_sp = subprocess.Popen(args=cmd, text=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="cp866")    #, encoding="cp866"

        # WORK --------------------------------
        time_start = time.time()
        lines = []
        while self._last_sp.poll() is None:
            self.last_duration = round(time.time() - time_start, 3)
            if timeout < self.last_duration:
                self._last_sp.kill()
                self.last_exc_timeout = TimeoutError()
                break
            line = self._last_sp.stdout.readline()
            if line != "":
                lines.append(line)
                print(".", end="")
            # print(f"[{repr(line)}]")

        if lines:
            self.last_stdout = "".join(lines)
            print()

        self.last_stderr = self._last_sp.stderr.read()
        self.last_retcode = self._last_sp.returncode
        self.last_finished = True

        if _raise:
            if self.last_exc_timeout:
                raise self.last_exc_timeout
            if self.last_retcode or self.last_stderr:
                msg = f"{self.last_retcode=}/{self.last_stderr=}"
                raise Exception(msg)

        return self.history.last_result.check_finished_and_success()

    # AUXILIARY -------------------------------------------------------------------------------------------------------
    def cli_check_available(self) -> bool:
        """check list of commands which will show that further work will executable and your environment is ready.

        Useful because commands uwually depends on installed programs and OS.
        so if you want to be sure of it on start point - run it!
        """
        if self.CMDS_REQUIRED:
            for cmd, error_msg in self.CMDS_REQUIRED.items():
                if not self.send(cmd, _raise=False):
                    Print(f"cmd NOT available [{cmd}]")
                    self.history.print_io()
                    return False
        return True


# =====================================================================================================================
if __name__ == "__main__":
    print()
    print()
    print()
    print()
    victim = CmdExecutor()
    victim.send("ping localhost", timeout=0.1)
    print()
    # victim.print_state()
    """
    [CLI_SEND] [ping localhost]
    ....
    ==================================================
    [#####################ERROR#####################]
    self.counter=1
    self.last_cmd='ping localhost'
    self.last_duration=1.041
    self.last_retcode=None
    --------------------------------------------------
    self.last_stdout=
    	|''
    	|'Обмен пакетами с starichenko.corp.element-t.ru [::1] с 32 байтами данных:'
    	|'Ответ от ::1: время<1мс '
    	|'Ответ от ::1: время<1мс '
    	|''
    --------------------------------------------------
    self.last_stderr=
    --------------------------------------------------
    self.last_exc_timeout=TimeoutError()
    ==================================================
    """

    print()
    print()
    print()
    print()
    victim.send(["python --version", ("ping localhost", 0.1), ])
    """
    [CLI_SEND] [python --version]
    .
    [CLI_SEND] [('ping localhost', 0.1)]
    ....
    ==================================================
    [#####################ERROR#####################]
    self.counter=3
    self.last_cmd='ping localhost'
    self.last_duration=1.042
    self.last_retcode=None
    --------------------------------------------------
    self.last_stdout=
    	|''
    	|'Обмен пакетами с starichenko.corp.element-t.ru [::1] с 32 байтами данных:'
    	|'Ответ от ::1: время<1мс '
    	|'Ответ от ::1: время<1мс '
    	|''
    --------------------------------------------------
    self.last_stderr=
    --------------------------------------------------
    self.last_exc_timeout=TimeoutError()
    ==================================================
    [ERROR] cmd_item=('ping localhost', 0.1) in full sequence cmd=['python --version', ('ping localhost', 0.1)]
    """


# =====================================================================================================================
