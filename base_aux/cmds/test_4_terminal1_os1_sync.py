from base_aux.aux_argskwargs.m4_kwargs_eq_expect import *

from base_aux.cmds.m4_terminal1_os1_sync import *


# =====================================================================================================================
if KwargsEqExpect_OS().bool_if__any_true(windows=True):
    CMD_PING_1 = "ping -n 1 localhost"      #momentary! less then 0.1sec!
    CMD_PING_2 = "ping -n 2 localhost"      #about 1sec!
else:
    CMD_PING_1 = "ping -c 1 localhost"
    CMD_PING_2 = "ping -c 2 localhost"


# =====================================================================================================================
class Test:
    def test__ok(self):
        victim = CmdTerminal_OsSync()
        assert victim.connect()

        time.sleep(0.3)
        assert len(victim.history) == 1

        assert victim.send_cmd(CMD_PING_1, timeout_read_start=1)

        assert victim.history.last_input == CMD_PING_1
        assert victim.history.check_finished() is True
        assert victim.history.check_all_success() is True
        assert victim.history.check_any_fail() is False
        assert victim.history.last_retcode is None

        assert victim.history.last_stdout_buff
        assert not victim.history.last_stderr_buff

        assert len(victim.history) == 2









    def test__list(self):
        victim = CmdTerminal_OsSync()

        assert not victim.send([CMD_PING_1, CMD_PING_2], timeout=1)
        assert not victim.send([CMD_PING_1, CMD_PING_2, CMD_PING_2], timeout=2)
        assert victim.send([CMD_PING_1, CMD_PING_2], timeout=2)
        assert victim.last_cmd == CMD_PING_2
        assert victim.last_finished is True

        assert victim.last_exc_timeout is None
        assert bool(victim.last_stdout) is True
        assert bool(victim.last_stderr) is False
        assert victim.last_retcode == 0

    def test__list_not_passed_timeout(self):
        victim = CmdTerminal_OsSync()
        assert not victim.send([CMD_PING_1, CMD_PING_2], timeout=0.1)
        assert victim.send([CMD_PING_1, CMD_PING_2])

    @pytest.mark.parametrize(
        argnames="cmds, timeout_def, _EXPECTED",
        argvalues=[
            # FIXME:HERE - NOT ALWAYS PASSED!!! dont panic! maybe need to skip it or ref!
            # FIXME:HERE - NOT ALWAYS PASSED!!! dont panic! maybe need to skip it or ref!
            # FIXME:HERE - NOT ALWAYS PASSED!!! dont panic! maybe need to skip it or ref!
            # FIXME:HERE - NOT ALWAYS PASSED!!! dont panic! maybe need to skip it or ref!
            # FIXME:HERE - NOT ALWAYS PASSED!!! dont panic! maybe need to skip it or ref!
            # FIXME:HERE - NOT ALWAYS PASSED!!! dont panic! maybe need to skip it or ref!
            # FIXME:HERE - NOT ALWAYS PASSED!!! dont panic! maybe need to skip it or ref!
            (CMD_PING_2, 0.1, False),
            ((CMD_PING_2, 0.1), 0.1, False),
            ((CMD_PING_2, 2), 0.1, True),

            # ([(CMD_PING_1, 0.1), CMD_PING_1], 0.1, True),      # here is wrong/now i dont anderstand what is goingOn/testing here!??????
            ([(CMD_PING_1, 0.1), CMD_PING_2], 0.1, False),
            ([(CMD_PING_1, 0.1), (CMD_PING_2, 2)], 0.1, True),
            ([(CMD_PING_1, 0.1), (CMD_PING_2, None)], 0.1, False),
            ([(CMD_PING_1, 0.1), (CMD_PING_2, None)], 2, True),
        ]
    )
    def test__tuple(self, cmds, timeout_def, _EXPECTED):
        func_link = CmdTerminal_OsSync().send(cmd=cmds, timeout=timeout_def)
        Lambda(func_link).check_expected__assert(_EXPECTED)

    def test__list__till_first_true(self):
        victim = CmdTerminal_OsSync()

        assert not victim.send([CMD_PING_1, CMD_PING_2], timeout=1)
        assert victim.send([CMD_PING_1, CMD_PING_2], timeout=1, till_first_true=True)

        assert victim.last_cmd == CMD_PING_1
        assert victim.last_finished is True

        assert victim.last_exc_timeout is None
        assert bool(victim.last_stdout) is True
        assert bool(victim.last_stderr) is False
        assert victim.last_retcode == 0

    def test__exc_timeout(self):
        victim = CmdTerminal_OsSync()

        assert not victim.send(CMD_PING_2, timeout=0.1)
        assert victim.last_cmd == CMD_PING_2
        assert victim.last_finished is True

        assert isinstance(victim.last_exc_timeout, TimeoutError)
        # assert bool(victim.last_stdout) is False
        assert bool(victim.last_stderr) is False
        assert victim.last_retcode is None

    def test__exc_not_exists(self):
        victim = CmdTerminal_OsSync()

        cmd_line = "ping123"
        assert not victim.send(cmd_line, timeout=10)
        assert victim.last_cmd == cmd_line
        assert victim.last_finished is True

        assert victim.last_exc_timeout is None
        # assert bool(victim.last_stdout) is False
        assert bool(victim.last_stderr) is True
        assert victim.last_retcode not in [0, None]

    def test__exc_cli_available(self):
        # one cmd ------------------------------------------------
        class CliUserForAvailable(CmdTerminal_OsSync):
            CMDS_REQUIRED = {"ping123": None, }

        try:
            victim = CliUserForAvailable()
        except Exception as exc:
            assert isinstance(exc, Exc__NotAvailable)

        # two cmd ------------------------------------------------
        class CliUserForAvailable(CmdTerminal_OsSync):
            CMDS_REQUIRED = {CMD_PING_1: None, }

        victim = CliUserForAvailable()
        assert victim.check__cmds_required()


# =====================================================================================================================
