from typing import *
import time

from base_aux.threads.m1_item import *


# =====================================================================================================================
class Test__ThreadItem:
    # -----------------------------------------------------------------------------------------------------------------
    def setup_method(self, method):
        # self.victim = ThreadItem()
        pass

    # -----------------------------------------------------------------------------------------------------------------
    def test_SecondaryStart(self):
        def target():
            time.sleep(0.2)

        victim = ThreadItem(target)
        victim.start()
        victim.wait()
        victim.start()
        victim.wait()
        assert True


# =====================================================================================================================
