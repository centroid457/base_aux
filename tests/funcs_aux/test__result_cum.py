from typing import *
import pytest

from base_aux.funcs_aux import *
from base_aux.classes_aux import *


# =====================================================================================================================
VALIDATE__TRUE = Valid(True)


# =====================================================================================================================
def test__log_lines():
    victim = ResultCum("Hello")
    assert victim.LOG_LINES == []

    # SINGLE --------------------------
    victim.log_lines__add("line1")
    assert victim.LOG_LINES == ["line1"]

    # LIST --------------------------
    victim.clear()
    assert victim.LOG_LINES == []
    victim.log_lines__add([f"line{i}" for i in range(3)])
    assert victim.LOG_LINES == ["line0", "line1", "line2"]

    # Valid --------------------------
    victim.clear()
    assert victim.LOG_LINES == []
    victim.result__apply_step(VALIDATE__TRUE)
    assert victim.LOG_LINES == [str(VALIDATE__TRUE)]

    # msg --------------------------
    victim.clear()
    assert victim.LOG_LINES == []
    assert victim.log_last__get() is None
    victim.result__apply_step(VALIDATE__TRUE, msg="newMsg")
    assert victim.LOG_LINES == [str(VALIDATE__TRUE), "newMsg"]
    assert victim.log_last__get() == "newMsg"


def test__step_history():
    victim = ResultCum("Hello")
    assert victim.STEP_HISTORY == []

    victim.result__apply_step(True)
    assert victim.STEP_HISTORY == [(True, True)]

    victim.result__apply_step(False)
    assert victim.STEP_HISTORY == [(True, True), (False, False)]

    victim.result__apply_step(None)
    assert victim.STEP_HISTORY == [(True, True), (False, False), (False, None)]

    victim.result__apply_step("Hello", False)
    assert victim.STEP_HISTORY == [(True, True), (False, False), (False, None), (True, "Hello")]

    victim.result__apply_step(VALIDATE__TRUE)
    assert victim.STEP_HISTORY == [(True, True), (False, False), (False, None), (True, "Hello"), (True, VALIDATE__TRUE)]

    victim.clear()
    assert victim.STEP_HISTORY == []


def test__step_last():
    victim = ResultCum()
    try:
        victim.step_last__get()
    except:
        pass
    else:
        assert False

    victim.result__apply_step(None)
    assert victim.step_last__get() is None

    victim.result__apply_step(True)
    assert victim.step_last__get() is True

    victim.result__apply_step("True")
    assert victim.step_last__get() == "True"

    victim.result__apply_step(VALIDATE__TRUE)
    assert victim.step_last__get() == VALIDATE__TRUE

    victim.clear()
    try:
        victim.step_last__get()
    except:
        pass
    else:
        assert False


def test__clear():
    victim = ResultCum()
    assert victim.result is True
    assert bool(victim) is True

    victim.result__apply_step(False, False)
    assert victim.result is True
    assert bool(victim) is True

    victim.result__apply_step(False)
    assert victim.result is False
    assert bool(victim) is False

    victim.clear()
    assert victim.result is True
    assert bool(victim) is True


def test__result_blank():
    victim = ResultCum()
    assert victim.result is True
    assert bool(victim) is True


def test__result():
    victim = ResultCum()
    victim.result__apply_step(False, False)
    assert victim.result is True
    assert bool(victim) is True

    victim.result__apply_step(False)
    assert victim.result is False
    assert bool(victim) is False

    victim.result__apply_step(True)
    assert victim.result is False
    assert bool(victim) is False

    # ----------------------
    victim.clear()
    victim.result__apply_step(None)
    assert victim.result is False
    assert bool(victim) is False

    # ----------------------
    victim.clear()
    victim.result__apply_step(VALIDATE__TRUE)
    assert victim.result is True
    assert bool(victim) is True


# =====================================================================================================================
