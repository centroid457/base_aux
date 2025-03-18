from typing import *

from PyQt5.QtCore import QThread

from base_aux.aux_callable.m2_lambdas import *


# =====================================================================================================================
TYPING__LAMBDA_LIST__DRAFT = list[Lambda | Callable | type | Any]
TYPING__LAMBDA_LIST__FINAL = list[Lambda]


# =====================================================================================================================
class LambdaList(QThread):
    """
    GOAL
    ----
    call all lambdas in list one by one + return there Lambda-objects in list
    results will kept in objects
    """
    LAMBDAS: TYPING__LAMBDA_LIST__FINAL
    PROCESS_ACTIVE: Enum_ProcessActive = Enum_ProcessActive.NONE

    def __init__(self, lambdas: TYPING__LAMBDA_LIST__DRAFT, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        result = []
        for obj in lambdas:
            if not isinstance(obj, Lambda):
                obj = Lambda(obj)
            result.append(obj)
        self.LAMBDAS = result

    def run(self) -> None:
        # ONLY ONE EXECUTION on instance!!! dont use locks! -------------
        if self.PROCESS_ACTIVE == Enum_ProcessActive.STARTED:
            return
        self.PROCESS_ACTIVE = Enum_ProcessActive.STARTED

        # FIN ----------------------------------------------------------
        for obj in self.LAMBDAS:
            obj.run()

        self.PROCESS_ACTIVE = Enum_ProcessActive.FINISHED

    # OVERWRITE! ======================================================================================================
    def __call__(self, *args, **kwargs) -> TYPING__LAMBDA_LIST__FINAL | NoReturn:
        self.run()
        return self.LAMBDAS

    # =================================================================================================================
    def check_raise__any(self) -> bool:
        self.run()
        self.wait_finished()

        for obj in self.LAMBDAS:
            if obj.EXX is not None:
                return True
            else:
                return False

    def check_no_raise__any(self) -> bool:
        return not self.check_raise__any()

    def wait_finished(self, sleep: float = 1) -> None:
        if self.PROCESS_ACTIVE == Enum_ProcessActive.NONE:
            self.run()

        count = 1
        while self.PROCESS_ACTIVE != Enum_ProcessActive.FINISHED:
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
