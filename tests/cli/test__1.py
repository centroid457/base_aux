import pytest

from base_aux.aux_pytester.m1_pytest_aux import *
from base_aux.requirements.m2_strings import *

from base_aux.cli.m1_cli_user import *


# =====================================================================================================================
if ReqCheckStr_Os.bool_if__WINDOWS():
    CMD_PING_1 = "ping -n 1 localhost"      #momentary! less then 0.1sec!
    CMD_PING_2 = "ping -n 2 localhost"      #about 1sec!
else:
    CMD_PING_1 = "ping -c 1 localhost"
    CMD_PING_2 = "ping -c 2 localhost"


# =====================================================================================================================
class Test:
    def test__ok(self):
        victim = CliUser()

        assert victim.send(CMD_PING_1, timeout=2)
        assert victim.last_cmd == CMD_PING_1
        assert victim.last_finished is True

        assert victim.last_exx_timeout is None
        assert bool(victim.last_stdout) is True
        assert bool(victim.last_stderr) is False
        assert victim.last_retcode == 0
        assert victim.last_finished_success
        assert victim.counter == 1
        assert victim.counter_in_list == 0

    def test__count(self):
        victim = CliUser()
        assert victim.counter == 0
        assert victim.counter_in_list == 0

        assert victim.send(CMD_PING_1, timeout=1)
        assert victim.counter == 1
        assert victim.counter_in_list == 0

        assert victim.send(CMD_PING_1, timeout=1)
        assert victim.counter == 2
        assert victim.counter_in_list == 0

        assert victim.send([CMD_PING_1, CMD_PING_1], timeout=1)
        assert victim.counter == 4
        assert victim.counter_in_list == 2

        assert victim.send(CMD_PING_1, timeout=1)
        assert victim.counter == 5
        assert victim.counter_in_list == 0

        assert victim.send([CMD_PING_1, CMD_PING_1, CMD_PING_1], timeout=1)
        assert victim.counter == 8
        assert victim.counter_in_list == 3

        assert not victim.send([CMD_PING_2, CMD_PING_2, CMD_PING_2], timeout=1)
        assert victim.counter == 9
        assert victim.counter_in_list == 1

    def test__list(self):
        victim = CliUser()

        assert not victim.send([CMD_PING_1, CMD_PING_2], timeout=1)
        assert victim.counter_in_list == 2

        assert not victim.send([CMD_PING_1, CMD_PING_2, CMD_PING_2], timeout=2)
        assert victim.counter_in_list == 3

        assert victim.send([CMD_PING_1, CMD_PING_2], timeout=2)
        assert victim.counter_in_list == 2
        assert victim.last_cmd == CMD_PING_2
        assert victim.last_finished is True

        assert victim.last_exx_timeout is None
        assert bool(victim.last_stdout) is True
        assert bool(victim.last_stderr) is False
        assert victim.last_retcode == 0
        assert victim.last_finished_success

    def test__list_not_passed_timeout(self):
        victim = CliUser()
        assert not victim.send([CMD_PING_1, CMD_PING_2], timeout=0.1)
        assert victim.send([CMD_PING_1, CMD_PING_2])

    @pytest.mark.parametrize(
        argnames="cmds, timeout, _EXPECTED",
        argvalues=[

            (CMD_PING_2, 0.1, False),
            ((CMD_PING_2, 0.1), 0.1, False),
            ((CMD_PING_2, 1.1), 0.1, True),

            # ([(CMD_PING_1, 0.1), CMD_PING_1], 0.1, True),         # here is wrong/now i dont anderstand what is goingOn/testing here!
            ([(CMD_PING_1, 0.1), CMD_PING_2], 0.1, False),
            # ([(CMD_PING_1, 0.1), (CMD_PING_2, 1.1)], 0.1, True),  # here is wrong
            ([(CMD_PING_1, 0.1), (CMD_PING_2, None)], 0.1, False),
            ([(CMD_PING_1, 0.1), (CMD_PING_2, None)], 1.3, True),
        ]
    )
    def test__tuple(self, cmds, timeout, _EXPECTED):        # HERE - NOT ALWAYS PASSED!!! dont panic! maybe need to skip it or ref!
        func_link = CliUser().send(cmd=cmds, timeout=timeout)
        PytestAux(func_link).assert_check(_EXPECTED)

    def test__list__till_first_true(self):
        victim = CliUser()

        assert not victim.send([CMD_PING_1, CMD_PING_2], timeout=1)
        assert victim.counter_in_list == 2

        assert victim.send([CMD_PING_1, CMD_PING_2], timeout=1, till_first_true=True)
        assert victim.counter_in_list == 1

        assert victim.last_cmd == CMD_PING_1
        assert victim.last_finished is True

        assert victim.last_exx_timeout is None
        assert bool(victim.last_stdout) is True
        assert bool(victim.last_stderr) is False
        assert victim.last_retcode == 0
        assert victim.last_finished_success

    def test__exx_timeout(self):
        victim = CliUser()

        assert not victim.send(CMD_PING_2, timeout=0.1)
        assert victim.last_cmd == CMD_PING_2
        assert victim.last_finished is True

        assert isinstance(victim.last_exx_timeout, Exx_CliTimeout)
        # assert bool(victim.last_stdout) is False
        assert bool(victim.last_stderr) is False
        assert victim.last_retcode is None
        assert not victim.last_finished_success

    def test__exx_not_exists(self):
        victim = CliUser()

        cmd_line = "ping123"
        assert not victim.send(cmd_line, timeout=10)
        assert victim.last_cmd == cmd_line
        assert victim.last_finished is True

        assert victim.last_exx_timeout is None
        # assert bool(victim.last_stdout) is False
        assert bool(victim.last_stderr) is True
        assert victim.last_retcode not in [0, None]
        assert not victim.last_finished_success

    def test__exx_cli_available(self):
        # one cmd ------------------------------------------------
        class CliUserForAvailable(CliUser):
            CMDS_REQUIRED = {"ping123": None, }

        try:
            victim = CliUserForAvailable()
        except Exception as exx:
            assert isinstance(exx, Exx_CliNotAvailable)

        # two cmd ------------------------------------------------
        class CliUserForAvailable(CliUser):
            CMDS_REQUIRED = {CMD_PING_1: None, }

        victim = CliUserForAvailable()
        assert victim.cli_check_available()


# =====================================================================================================================
