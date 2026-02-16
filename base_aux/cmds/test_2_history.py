import pytest

from base_aux.cmds.m2_history import *


# =====================================================================================================================
# @pytest.mark.parametrize(argnames="source, _EXPECTED", argvalues=[
#     (None, Exception),
# ])
# def test__eq(source, _EXPECTED):
#     assert
#     Lambda(func_link, args).check_expected__assert(_EXPECTED)


# =====================================================================================================================
def test__finished():
    victim: CmdHistory = CmdHistory()
    assert victim.check_finished() is False

    victim.add_data__stdin("")
    assert victim.check_finished() is False

    # with pytest.raises(Exception):
    #     victim.add_input("")

    assert victim.check_finished() is False

    victim.set_finished()
    assert victim.check_finished() is True

    victim.add_data__stdin("")
    assert victim.check_finished() is False


def test__add_list_asdict_eq():
    victim: CmdHistory = CmdHistory()
    assert victim == []
    assert victim._history == []
    assert victim._as_dict() == {}

    victim.add_data__stdin("in1")
    assert victim == [("in1", []), ]
    assert victim == [CmdResult("in1", []), ]
    assert victim._history == [CmdResult("in1", []), ]
    assert victim.list_input() == ["in1", ]
    assert victim.list_stdout_lines() == []
    assert victim._as_dict() == {"in1": []}
    victim.set_finished()

    victim.add_data__stdin("in2")
    assert victim == [("in1", []), ("in2", [])]
    assert victim == [CmdResult("in1", []), CmdResult("in2", [])]
    assert victim._history == [CmdResult("in1", []), CmdResult("in2", [])]
    assert victim.list_input() == ["in1", "in2"]
    assert victim.list_stdout_lines() == []
    assert victim._as_dict() == {"in1": [], "in2": []}

    victim.add_data__stdout("out2")
    assert victim == [("in1", []), ("in2", ["out2", ])]
    assert victim == [CmdResult("in1", []), CmdResult("in2", ["out2", ])]
    assert victim._history == [CmdResult("in1", []), CmdResult("in2", ["out2", ])]
    assert victim.list_input() == ["in1", "in2"]
    assert victim.list_stdout_lines() == ["out2", ]

    victim.add_data__stdout("out22")
    assert victim == [("in1", []), ("in2", ["out2", "out22", ])]
    assert victim == [CmdResult("in1", []), CmdResult("in2", ["out2", "out22", ])]
    assert victim._history == [CmdResult("in1", []), CmdResult("in2", ["out2", "out22", ])]
    assert victim.list_input() == ["in1", "in2"]
    assert victim.list_stdout_lines() == ["out2", "out22", ]

    victim.add_data__stdout(["out222", "out2222"])
    assert victim == [("in1", []), ("in2", ["out2", "out22", "out222", "out2222", ])]
    assert victim == [CmdResult("in1", []), CmdResult("in2", ["out2", "out22", "out222", "out2222", ])]
    assert victim._history == [CmdResult("in1", []), CmdResult("in2", ["out2", "out22", "out222", "out2222", ])]
    assert victim.list_input() == ["in1", "in2"]
    assert victim.list_stdout_lines() == ["out2", "out22", "out222", "out2222", ]

    victim.print_io()


def test__add_io__list_last():
    victim: CmdHistory = CmdHistory()
    assert victim._history == []
    assert victim.last_input == ""
    assert victim.last_stdout_line == ""

    victim.add_data__stdioe("in1", "out1")
    assert victim._history == [CmdResult("in1", ["out1", ]), ]
    assert victim.list_input() == ["in1", ]
    assert victim.list_stdout_lines() == ["out1", ]
    assert victim.last_input == "in1"
    assert victim.last_stdout_line == "out1"
    victim.set_finished()

    victim.add_data__stdioe("in2", ["out2", "out22", ])
    assert victim._history == [CmdResult("in1", ["out1", ]), CmdResult("in2", ["out2", "out22", ]), ]
    assert victim.list_input() == ["in1", "in2"]
    assert victim.list_stdout_lines() == ["out1", "out2", "out22", ]
    assert victim.last_input == "in2"
    assert victim.last_stdout_line == "out22"


def test__add_history():
    victim: CmdHistory = CmdHistory()
    assert victim._history == []

    history = CmdHistory()
    history.add_data__stdioe("in1", "out1")

    victim._add_history(history)
    assert victim._history == [CmdResult("in1", ["out1", ]), ]


def test__first_output():
    victim: CmdHistory = CmdHistory()
    assert victim._history == []

    victim.add_data__stdout("out0")
    assert victim._history == [CmdResult("", ["out0", ])]
    assert victim.list_input() == ["", ]
    assert victim.list_stdout_lines() == ["out0"]

    victim.clear()
    assert victim._history == []


# =====================================================================================================================
