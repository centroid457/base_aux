import time
import pytest

from PyQt5.QtCore import QThread

from base_aux.base_types.m2_info import *


# =====================================================================================================================
class Test_FREEZE:
    # @classmethod
    # def setup_class(cls):
    #     pass
    #
    # @classmethod
    # def teardown_class(cls):
    #     pass
    #
    # def setup_method(self, method):
    #     pass

    # -----------------------------------------------------------------------------------------------------------------
    def test__zero(self):
        class Victim:
            A1 = 1
            def meth1(self):
                return 1

        ObjectInfo(Victim(), skip__build_in=False).print()
        assert True

    # -----------------------------------------------------------------------------------------------------------------
    def test__QThread(self):
        class Victim(QThread):
            def run(self):
                time.sleep(0.3)

            def hello(self):
                pass

        ObjectInfo(Victim(), skip__build_in=False).print()
        assert True


# =====================================================================================================================
