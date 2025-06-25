import time

from base_aux.base_lambdas.m2_lambda3_thread import LambdaThread


# =====================================================================================================================
class Test__ThreadItem:
    # -----------------------------------------------------------------------------------------------------------------
    def setup_method(self, method):
        # self.victim = LambdaThread()
        pass

    # -----------------------------------------------------------------------------------------------------------------
    def test_SecondaryStart(self):
        def target():
            time.sleep(0.2)

        victim = LambdaThread(target)
        victim.start()
        victim.wait()
        victim.start()
        victim.wait()
        assert True


# =====================================================================================================================
