import pytest
from typing import *

from base_aux.pyqt import *
from PyQt5.QtCore import pyqtSignal


# =====================================================================================================================
class Test__Signals:
    # -----------------------------------------------------------------------------------------------------------------
    def setup_method(self, method):
        class Signals(SignalsTemplate):
            signal__send_no = pyqtSignal()

            signal__send_one__wo_def = pyqtSignal(int)
            signal__send_one__wo_def__not_used = pyqtSignal(int)
            signal__send_one__with_def = pyqtSignal(int)

            signal__send_several__wo_def = pyqtSignal(int, int)
            signal__send_several__with_def2 = pyqtSignal(int, int)
            signal__send_several__with_def12 = pyqtSignal(int, int)

            signal__send_any = pyqtSignal(Any)

        class Victim:
            SIGNALS = Signals()

            value: Union[None, int, list[int]] = None

            def __init__(self):
                self.slots_connect()

            def slots_connect(self):
                self.SIGNALS.signal__send_no.connect(self.clear)

                self.SIGNALS.signal__send_one__wo_def.connect(self.value__set_one__wo_def)
                self.SIGNALS.signal__send_one__wo_def__not_used.connect(self.value__set_one__wo_def__not_used)
                self.SIGNALS.signal__send_one__with_def.connect(self.value__set_one__with_def)

                self.SIGNALS.signal__send_several__wo_def.connect(self.value__set_several__wo_def)
                self.SIGNALS.signal__send_several__with_def2.connect(self.value__set_several__with_def2)
                self.SIGNALS.signal__send_several__with_def12.connect(self.value__set_several__with_def12)

            def clear(self):
                self.value = None

            # -----------------------------------------------
            def value__set_one__wo_def(self, value):
                self.value = value

            def value__set_one__wo_def__not_used(self, value):
                self.value = 999

            def value__set_one__with_def(self, value=None):
                self.value = value

            # -----------------------------------------------
            def value__set_several__wo_def(self, value1, value2):
                self.value = [value1, value2]

            def value__set_several__with_def2(self, value1, value2=None):
                self.value = [value1, value2]

            def value__set_several__with_def12(self, value1=None, value2=None):
                self.value = [value1, value2]

        self.victim = Victim()

    # -----------------------------------------------------------------------------------------------------------------
    def test__several_emits(self):
        victim = self.victim

        victim.SIGNALS.signal__send_no.emit()
        victim.SIGNALS.signal__send_no.emit()
        victim.SIGNALS.signal__send_no.emit()
        victim.SIGNALS.signal__send_no.emit()
        assert victim.value is None

    # -----------------------------------------------------------------------------------------------------------------
    def test__NO_PARAMS(self):
        victim = self.victim
        assert victim.value is None

        victim.value = 1
        assert victim.value == 1

        # CORRECT -----------------------------------------
        victim.SIGNALS.signal__send_no.emit()
        assert victim.value is None

        # INCORRECT -----------------------------------------
        victim.value = 1
        try:
            victim.SIGNALS.signal__send_no.emit(1)  # EXTRA
        except TypeError:
            assert True
        else:
            assert False

        assert victim.value == 1

    # -----------------------------------------------------------------------------------------------------------------
    def test__ONE(self):
        victim = self.victim
        assert victim.value is None

        # CORRECT -----------------------------------------------------------------------------------
        victim.SIGNALS.signal__send_one__wo_def.emit(1)
        assert victim.value == 1

        victim.SIGNALS.signal__send_one__wo_def__not_used.emit(11)
        assert victim.value == 999

        victim.SIGNALS.signal__send_one__with_def.emit(111)
        assert victim.value == 111

        # BLANK -----------------------------------------------------------------------------------
        # -----------------------------------------------
        try:
            victim.SIGNALS.signal__send_one__wo_def.emit()
        except TypeError:
            assert True
        else:
            assert False

        assert victim.value == 111

        # -----------------------------------------------
        try:
            victim.SIGNALS.signal__send_one__wo_def__not_used.emit()
        except TypeError:
            assert True
        else:
            assert False

        assert victim.value == 111

        # -----------------------------------------------
        try:
            victim.SIGNALS.signal__send_one__with_def.emit()        # ATTENTION!!! func woun't be called!
        except TypeError:
            assert True
        else:
            assert False

        assert victim.value == 111

        # WRONG TYPE -----------------------------------------------------------
        victim.SIGNALS.signal__send_one__wo_def.emit(True)
        # assert victim.value == int(True)
        assert victim.value == 1

        # in all such other cases always will be new different value!!!
        # WHY? dont matter! DECISION - DONT USE IT IN THIS WAY!!!

        # victim.SIGNALS.signal__send_one__wo_def.emit("1")
        # print(int("1"))     # 1
        # # assert victim.value == int("1")
        # # assert victim.value == 132102104
        # victim.SIGNALS.signal__send_one__wo_def.emit("2")
        # assert victim.value == 132102152                    # WHY????
        # victim.SIGNALS.signal__send_one__wo_def.emit("True")
        # assert victim.value == 132063408                    # WHY????
        # victim.SIGNALS.signal__send_one__wo_def.emit(None)
        # assert victim.value == 131245568                   # WHY????
        # # victim.SIGNALS.signal__send_one__wo_def.emit(0.1)
        # assert victim.value == -1428486704                   # WHY???? different value any time!!!

        # EXTRA COUNT -----------------------------------------------------------
        try:
            victim.SIGNALS.signal__send_one__wo_def.emit(11, 11)
        except TypeError:
            assert True
        else:
            assert False

    # -----------------------------------------------------------------------------------------------------------------
    def test__SEVERAL(self):
        victim = self.victim
        assert victim.value is None

        # CORRECT -----------------------------------------------------------
        victim.SIGNALS.signal__send_several__wo_def.emit(1, 2)
        assert victim.value == [1, 2]

        victim.SIGNALS.signal__send_several__with_def2.emit(11, 22)
        assert victim.value == [11, 22]

        victim.SIGNALS.signal__send_several__with_def12.emit(111, 222)
        assert victim.value == [111, 222]

        # INCORRECT -----------------------------------------------------------
        try:
            victim.SIGNALS.signal__send_several__wo_def.emit()                # LESS COUNT
        except TypeError:
            assert True
        else:
            assert False
        assert victim.value == [111, 222]

        try:
            victim.SIGNALS.signal__send_several__wo_def.emit(11)                # LESS COUNT
        except TypeError:
            assert True
        else:
            assert False
        assert victim.value == [111, 222]

        try:
            victim.SIGNALS.signal__send_several__wo_def.emit(11, 22, 33)     # EXTRA COUNT
        except TypeError:
            assert True
        else:
            assert False
        assert victim.value == [111, 222]


# =====================================================================================================================
