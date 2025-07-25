from typing import *

import subprocess
import time

from base_aux.loggers.m1_print import *


# =====================================================================================================================
TYPING__CMD = Union[str, tuple[str, float | None]]
TYPING__CMDS = Union[TYPING__CMD, list[TYPING__CMD]]


# =====================================================================================================================
class Exx_CliNotAvailable(Exception):
    """
    GOAL
    ----
    cli can not be available due to have not some of required commands.
    """


class Exx_CliTimeout(Exception):    #use direct subprocess.TimeoutExpired??? NO!!!
    """
    GOAL
    ----
    timeout expired
    """


class Exx_CliRetcode(Exception):
    """
    GOAL
    ----
    returnCode is not zero.
    """


class Exx_CliStderr(Exception):
    """
    GOAL
    ----
    stderr have any data
    """


# =====================================================================================================================
class CliCmd:
    # TODO: ADD
    pass


# =====================================================================================================================
class CliUser:
    """
    GOAL
    ----
    send commands into OS terminal

    "check if cli commands are accessible (special utilities is installed)",
    "access to standard parts of result in a simple ready-to-use form (stdout/stderr/retcode/full state)",
    "use batch timeout for list",
    "till_first_true",
    "counter/counter_in_list",

    :ivar TIMEOUT: default timeout for execution process
        if timeout expired and process still not finished - raise exx
    :ivar _last_sp: Popen object
    :ivar last_exx_timeout: saved Exx_CliTimeout if it was
    :ivar last_cmd: command for execution
    :ivar last_stdout: full stdout data
    :ivar last_stderr: full stderr data
    :ivar last_retcode: returned code if process was last_finished
    :ivar last_finished: flag shows if command process was finished
        useful if execute in threading.

    :ivar CMDS_REQUIRED: commands for cli_check_available
        dict with NAME - exact commands which will send into terminal in order to check some utility is installed,
        VALUE - message if command get any error

        RECOMMENDATIONS
        --------------
        1. --HELP never works as expected! always timedout!!!!
            [#####################ERROR#####################]
            self.last_cmd='STM32_Programmer_CLI --help'
            self.last_duration=2.029675
            self.last_finished=True
            self.last_finished_success=False
            self.last_retcode=None
            --------------------------------------------------
            self.last_stdout=
            --------------------------------------------------
            self.last_stderr=
            --------------------------------------------------
            self._last_exx_timeout=Exx_CliTimeout("TimeoutExpired('STM32_Programmer_CLI --help', 2)")
            ==================================================
            [ERROR] cmd NOT available [STM32_Programmer_CLI --help]
            ==================================================

        2. DIRECT SIMPLE CLI COMMAND AS UTILITY_NAME.EXE without any parameter MAY NOT WORK!!! may timedout! implied the same as HELP parameter!
            [#####################ERROR#####################]
            self.last_cmd='STM32_Programmer_CLI'
            self.last_duration=2.022585
            self.last_finished=True
            self.last_finished_success=False
            self.last_retcode=None
            --------------------------------------------------
            self.last_stdout=
            --------------------------------------------------
            self.last_stderr=
            --------------------------------------------------
            self._last_exx_timeout=Exx_CliTimeout("TimeoutExpired('STM32_Programmer_CLI', 2)")
            ==================================================

        3. use --VERSION! instead! - seems work fine always!
    """
    # SETTINGS ------------------------------------
    TIMEOUT: Optional[float] = 2
    RAISE: Optional[bool] = None

    CMDS_REQUIRED: Optional[dict[str, Optional[str]]] = None

    _buffer_indent: str = "\t|"

    # VALUES --------------------------------------
    _last_sp: Optional[subprocess.Popen] = None

    counter: int = 0
    counter_in_list: int = 0

    last_duration: float = 0
    last_cmd: str = ""
    last_stdout: str = ""         # USE ONLY "" AS DEFAULT!!!
    last_stderr: str = ""         # USE ONLY "" AS DEFAULT!!!
    last_exx_timeout: Optional[Exx_CliTimeout] = None
    last_retcode: Optional[int] = None
    last_finished: Optional[bool] = None

    # init ------------------------------------------------------------------------------------------------------------
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._reinit_values()       # need to keep always one values!

        if not self.cli_check_available():
            raise Exx_CliNotAvailable

    def _reinit_values(self) -> None:
        self._last_sp = None

        self.last_duration = 0
        self.last_cmd = ""
        self.last_stdout = ""
        self.last_stderr = ""
        self.last_exx_timeout = None
        self.last_retcode = None
        self.last_finished = None

    @property
    def last_finished_success(self) -> Optional[bool]:
        """check if process last_finished correct

        :return: True if last_finished with no errors
        """
        return all([self.last_finished, self.last_retcode == 0, not self.last_stderr, not self.last_exx_timeout])

    # SEND ------------------------------------------------------------------------------------------------------------
    def send(
            self,
            cmd: TYPING__CMDS,
            timeout: Optional[float] = None,
            till_first_true: Optional[bool] = None,
            _raise: Optional[bool] = None,
            _use_counter_list: Optional[bool] = None,
            print_all_states: Optional[bool] = None
    ) -> Union[bool, NoReturn]:
        """execute CLI command in terminal

        :param cmd: commands for execution
        :param timeout: use special timeout step_result_enum, instead of default, for cms_list will used as cumulated!
            # TODO: need decide about cumulation! more preferable apply as default! -NO its OK!
            so if you use list - apply timeout for CUMULATED! and dont pass it if no need cumulation!
            if single - apply as single!
        :param till_first_true: useful for detection or just multiPlatform usage
        :param _raise: if till_first_true=True it will not work (return always bool in this case)!!!
        :param _use_counter_list: DONT USE! internal flag for counter_in_list
        :param print_all_states: all or only Failed
        """
        # CMDS LIST ---------------------------------------------------------------------------------------------------
        if isinstance(cmd, list):
            self.counter_in_list = 0
            time_start = time.time()
            result = True

            _raise_list = _raise
            if till_first_true:
                _raise_list = False

            for cmd_item in cmd:
                self.counter_in_list += 1
                time_passed = time.time() - time_start
                try:
                    timeout = timeout - time_passed
                except:
                    pass

                result = self.send(cmd=cmd_item, timeout=timeout, _raise=_raise_list, _use_counter_list=True)

                if till_first_true:
                    if result:
                        return True
                else:
                    if not result:
                        Warn(f"{cmd_item=} in full sequence {cmd=}")
                        return False

            return result

        # params reinit -----------------------------------------------------------------------------------------------
        self._reinit_values()
        if not _use_counter_list:
            self.counter_in_list = 0

        # params apply ------------------------------------------------------------------------------------------------
        Print(f"[CLI_SEND]{cmd}")

        if isinstance(cmd, tuple) and len(cmd) == 2:
            cmd, timeout_i = cmd
            if timeout_i is not None:
                timeout = timeout_i

        self.last_cmd = cmd
        self.counter += 1

        if timeout is None:
            timeout = self.TIMEOUT
        if _raise is None:
            _raise = self.RAISE

        # work --------------------------------------------------------------------------------------------------------
        if timeout < 0:
            msg = f"{timeout=} is sub zero"
            self.last_exx_timeout = Exx_CliTimeout(msg)
            print(msg)
            if _raise:
                raise Exx_CliTimeout(msg)
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
                self.last_exx_timeout = Exx_CliTimeout()
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
        if print_all_states or not self.last_finished_success:
            self.print_state()

        if _raise:
            if self.last_exx_timeout:
                raise self.last_exx_timeout
            if self.last_retcode != 0:
                raise Exx_CliRetcode(self.last_retcode)
            if self.last_stderr:
                raise Exx_CliStderr(self.last_stderr)

        return self.last_finished_success

    # AUXILIARY -------------------------------------------------------------------------------------------------------
    def print_state(self) -> None:
        print(f"="*50)
        if not self.last_finished_success:
            print(f"[{'#'*21}ERROR{'#'*21}]")

        print(f"{self.counter=}")
        print(f"{self.counter_in_list=}")

        print(f"{self.last_cmd=}")
        print(f"{self.last_duration=}")
        print(f"{self.last_finished=}")
        print(f"{self.last_finished_success=}")
        print(f"{self.last_retcode=}")
        print(f"-" * 50)
        print("self.last_stdout=")
        if self.last_stdout:
            for line in self.last_stdout.split("\n"):
                print(f"{self._buffer_indent}{line!r}")
        print(f"-"*50)
        print("self.last_stderr=")
        if self.last_stderr:
            for line in self.last_stderr.split("\n"):
                print(f"{self._buffer_indent}{line!r}")
        print(f"-" * 50)
        print(f"{self.last_exx_timeout=}")
        print(f"="*50)

    def cli_check_available(self) -> bool:
        """check list of commands which will show that further work will executable and your environment is ready.

        Useful because commands uwually depends on installed programs and OS.
        so if you want to be sure of it on start point - run it!
        """
        if self.CMDS_REQUIRED:
            for cmd, error_msg in self.CMDS_REQUIRED.items():
                if not self.send(cmd, _raise=False):
                    Print(f"cmd NOT available [{cmd}]")
                    self.print_state()
                    return False
        return True


# =====================================================================================================================
