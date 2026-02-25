from base_aux.cmds.m4_terminal0_abc2_paradigm import AbcParadigm_CmdTerminal


# =====================================================================================================================
class Mark_CmdTerminal_Os(AbcParadigm_CmdTerminal):
    """
    GOAL
    ----
    access to OS terminal with continuous connection - keeping state!

    hints
    "check if cmds commands are accessible (special utilities is installed)",
    "access to standard parts of result in a simple ready-to-use form (stdout/stderr/_retcode/full state)",
    "use batch timeout for list",
    "till_first_true",

    :ivar CMDS_REQUIRED: commands for cli_check_available
        dict with NAME - exact commands which will send into terminal in order to check some utility is installed,
        VALUE - message if command get any error

        RECOMMENDATIONS
        --------------
        1. --HELP never works as expected! always timed_out!!!!
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

        2. DIRECT SIMPLE CLI COMMAND AS UTILITY_NAME.EXE without any parameter MAY NOT WORK!!! may timed_out! implied the same as HELP parameter!
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


# =====================================================================================================================
