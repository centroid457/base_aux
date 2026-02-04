from types import *
import pytest
from pytest import mark

from base_aux.base_histories.m2_io_history import *
from base_aux.base_lambdas.m1_lambda import *


# =====================================================================================================================
# @pytest.mark.parametrize(argnames="source, _EXPECTED", argvalues=[
#     (None, Exception),
# ])
# def test__eq(source, _EXPECTED):
#     assert
#     Lambda(func_link, args).check_expected__assert(_EXPECTED)


# =====================================================================================================================
def test__add_list_asdict_eq():
    victim: IoHistory = IoHistory()
    assert victim == []
    assert victim._history == []
    assert victim.as_dict() == {}

    victim.add_input("in1")
    assert victim == [("in1", []), ]
    assert victim == [IoItem("in1", []), ]
    assert victim._history == [IoItem("in1", []), ]
    assert victim.list_input() == ["in1", ]
    assert victim.list_output() == []
    assert victim.as_dict() == {"in1": []}

    victim.add_input("in2")
    assert victim == [("in1", []), ("in2", [])]
    assert victim == [IoItem("in1", []), IoItem("in2", [])]
    assert victim._history == [IoItem("in1", []), IoItem("in2", [])]
    assert victim.list_input() == ["in1", "in2"]
    assert victim.list_output() == []
    assert victim.as_dict() == {"in1": [], "in2": []}

    victim.add_output("out2")
    assert victim == [("in1", []), ("in2", ["out2", ])]
    assert victim == [IoItem("in1", []), IoItem("in2", ["out2", ])]
    assert victim._history == [IoItem("in1", []), IoItem("in2", ["out2", ])]
    assert victim.list_input() == ["in1", "in2"]
    assert victim.list_output() == ["out2", ]

    victim.add_output("out22")
    assert victim == [("in1", []), ("in2", ["out2", "out22", ])]
    assert victim == [IoItem("in1", []), IoItem("in2", ["out2", "out22", ])]
    assert victim._history == [IoItem("in1", []), IoItem("in2", ["out2", "out22", ])]
    assert victim.list_input() == ["in1", "in2"]
    assert victim.list_output() == ["out2", "out22", ]

    victim.add_output(["out222", "out2222"])
    assert victim == [("in1", []), ("in2", ["out2", "out22", "out222", "out2222", ])]
    assert victim == [IoItem("in1", []), IoItem("in2", ["out2", "out22", "out222", "out2222", ])]
    assert victim._history == [IoItem("in1", []), IoItem("in2", ["out2", "out22", "out222", "out2222", ])]
    assert victim.list_input() == ["in1", "in2"]
    assert victim.list_output() == ["out2", "out22", "out222", "out2222", ]

    victim.print_io()


def test__add_io__list_last():
    victim: IoHistory = IoHistory()
    assert victim._history == []
    assert victim.last_input == ""
    assert victim.last_output == ""

    victim.add_io("in1", "out1")
    assert victim._history == [IoItem("in1", ["out1", ]), ]
    assert victim.list_input() == ["in1", ]
    assert victim.list_output() == ["out1", ]
    assert victim.last_input == "in1"
    assert victim.last_output == "out1"

    victim.add_io("in2", ["out2", "out22", ])
    assert victim._history == [IoItem("in1", ["out1", ]), IoItem("in2", ["out2", "out22", ]), ]
    assert victim.list_input() == ["in1", "in2"]
    assert victim.list_output() == ["out1", "out2", "out22", ]
    assert victim.last_input == "in2"
    assert victim.last_output == "out22"


def test__add_history():
    victim: IoHistory = IoHistory()
    assert victim._history == []

    history = IoHistory()
    history.add_io("in1", "out1")

    victim.add_history(history)
    assert victim._history == [IoItem("in1", ["out1", ]), ]


def test__first_output():
    victim: IoHistory = IoHistory()
    assert victim._history == []

    victim.add_output("out0")
    assert victim._history == [IoItem("", ["out0", ])]
    assert victim.list_input() == ["", ]
    assert victim.list_output() == ["out0"]

    victim.clear()
    assert victim._history == []


# =====================================================================================================================
