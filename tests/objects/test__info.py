from typing import *
import time
import pytest

from PyQt5.QtCore import QThread

from base_aux.base_objects import *


# =====================================================================================================================
class Test_FREEZE:
    @classmethod
    def setup_class(cls):
        pass

    @classmethod
    def teardown_class(cls):
        pass

    def setup_method(self, method):
        pass

    # -----------------------------------------------------------------------------------------------------------------
    def test__QThread(self):
        class Victim(QThread):
            def run(self):
                time.sleep(0.3)

        ObjectInfo(Victim()).print()
        assert True


# =====================================================================================================================
