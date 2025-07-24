from PyQt5.QtCore import QThread

from base_aux.base_lambdas.m1_lambda import *
from base_aux.base_lambdas.m2_lambda3_thread import LambdaThread
from base_aux.base_types.m0_static_typing import *


# =====================================================================================================================
TYPING__LAMBDA_LIST__DRAFT = list[Lambda | Callable | type | Any]
TYPING__LAMBDA_LIST__FINAL = list[Lambda]


# =====================================================================================================================
class LambdaListThread(QThread):
    """
    GOAL
    ----
    call all base_lambdas in list one by one + return there Lambda-objects in list
    results will kept in objects
    """
    LAMBDAS: TYPING__LAMBDA_LIST__FINAL
    PROCESS_ACTIVE: EnumAdj_ProcessStateActive = EnumAdj_ProcessStateActive.NONE

    def __init__(self, lambdas: TYPING__LAMBDA_LIST__DRAFT, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        result = []
        for item in lambdas:
            if not isinstance(item, Lambda):
                item = Lambda(item)
            result.append(item)
        self.LAMBDAS = result

    def run(self) -> None:
        # ONLY ONE EXECUTION on instance!!! dont use locks! -------------
        if self.PROCESS_ACTIVE == EnumAdj_ProcessStateActive.STARTED:
            return
        self.PROCESS_ACTIVE = EnumAdj_ProcessStateActive.STARTED

        # FIN ----------------------------------------------------------
        for item in self.LAMBDAS:
            if isinstance(item, LambdaThread):
                item.start()
            else:
                item.run()

        self.wait_finished__all()
        self.PROCESS_ACTIVE = EnumAdj_ProcessStateActive.FINISHED

    # OVERWRITE! ======================================================================================================
    def __call__(self, *args, **kwargs) -> TYPING__LAMBDA_LIST__FINAL:
        self.run()
        return self.LAMBDAS

    # =================================================================================================================
    def check_raise__any(self) -> bool:
        self.run()
        self.wait_finished()

        for item in self.LAMBDAS:
            if item.EXX is not None:
                return True
            else:
                return False

    def check_no_raise__any(self) -> bool:
        return not self.check_raise__any()

    def wait_finished__all(self, sleep: float = 1) -> None:
        if self.PROCESS_ACTIVE == EnumAdj_ProcessStateActive.NONE:
            self.run()

        for item in self.LAMBDAS:
            item.wait_finished(sleep)

    def wait_finished(self, sleep: float = 1) -> None:
        if self.PROCESS_ACTIVE == EnumAdj_ProcessStateActive.NONE:
            self.run()

        count = 1
        while self.PROCESS_ACTIVE != EnumAdj_ProcessStateActive.FINISHED:
            print(f"wait_finished {count=}")
            count += 1
            time.sleep(sleep)


# =====================================================================================================================
def _explore():
    pass


# =====================================================================================================================
if __name__ == "__main__":
    _explore()
    pass


# =====================================================================================================================
