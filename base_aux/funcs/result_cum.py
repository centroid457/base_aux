"""
# TODO: NEED DEPRECATE IT!!! APPLY IN VALIDCHAINS!!!
# TODO: NEED DEPRECATE IT!!! APPLY IN VALIDCHAINS!!!
# TODO: NEED DEPRECATE IT!!! APPLY IN VALIDCHAINS!!!
# TODO: NEED DEPRECATE IT!!! APPLY IN VALIDCHAINS!!!
# TODO: NEED DEPRECATE IT!!! APPLY IN VALIDCHAINS!!!
# TODO: NEED DEPRECATE IT!!! APPLY IN VALIDCHAINS!!!
but maybe leave it on!
"""

from typing import *

from base_aux.funcs import *
from base_aux.classes import *


# =====================================================================================================================
TYPE__RESULT_CUM_STEP = Union[bool, Any, "Valid"]     # DONT USE CALLABLES!!! Valid is most PREFIRED! specially in case of EXX!!
TYPE__RESULT_CUM_STEPS = Union[TYPE__RESULT_CUM_STEP, list[TYPE__RESULT_CUM_STEP]]


# =====================================================================================================================
class ResultStep:
    """
    # TODO: this is just as idea! but just create clear correct log msgs and this is will be enough!
    GOAL
    ----
    item for steps in sequence

    CREATED SPECIALLY FOR
    ---------------------
    for ResultCum as internal aux

    CONSTRAINTS
    -----------

    BEST USAGE
    ----------
    """
    pass


# =====================================================================================================================
class ResultCum:
    """
    GOAL
    ----
    apply cumulated result with log lines

    CREATED SPECIALLY FOR
    ---------------------
    testplans

    REPLACE: ResultExpected

    CONSTRAINTS
    -----------
    1. dont use callables in steps! only final result (as expression) or Valid as most preferred
    2. if no steps - return True!

    BEST USAGE
    ----------
        # some example
        def meth() -> ResultCum:
            result_cum = ResultCum()

            result_step = 1+1 == 2
            result_cum.result__apply_step(result_step)
            result_cum.log_lines__add('check 1+1 == 2')

            result_step = 1+2 == 4
            result_cum.result__apply_step(result_step)
            result_cum.log_lines__add('check 1+2 == 4')

            result_cum.finish()
            return result_cum

    """

    TITLE: str = ""
    # COMMENT: str = ""

    result: bool = True
    finished: bool | None = None    # as help to see if process is finished - maybe need deprecate!

    LOG_LINES: list[str]
    STEP_HISTORY: list[tuple[TYPE__RESULT_CUM_STEP, bool]]     # as history! result+step

    def __init__(self, title: str = None):        #, steps=None):  #dont use steps here
        if title:
            self.TITLE = title

        self.clear()

    def clear(self) -> None:
        self.result = True
        self.finished = None

        self.LOG_LINES = []
        self.STEP_HISTORY = []

    def result__apply_step(self, step: TYPE__RESULT_CUM_STEPS, cumulate: bool | Any = True, msg: Union[None, str, list[str]] = None) -> bool:
        """

        :param step:
        :param cumulate: False - if you dont mind step result! but want to keep it in log
        :param msg:
        :return:
        """
        if isinstance(step, list):
            # LIST ------------------------------------------
            for step_i in step:
                if not self.result__apply_step(step_i, cumulate):
                    break
        else:
            # SINGLE ------------------------------------------
            # TODO: if isinstance(step, ResultCum):   - what do i need to do here?? decide!
            if isinstance(step, Valid):
                if not step.finished:
                    step.run()
                self.log_lines__add(str(step))

        if msg:
            self.log_lines__add(msg)

        step_result = bool(step)
        self.STEP_HISTORY.append((step_result, step))

        if bool(cumulate):
            if self.result is None:
                self.result = step_result
            else:
                self.result &= step_result

        return self.result

    def log_lines__add(self, new: Union[str, list[str]]) -> None:
        if isinstance(new, list):
            self.LOG_LINES.extend(new)
        if isinstance(new, str):
            self.LOG_LINES.append(new)

    def finish(self) -> None:
        self.finished = True

    def __bool__(self) -> bool:
        return bool(self.result)

    def __str__(self):
        result = f"{self.__class__.__name__}(result={self.result},finished={self.finished},TITLE={self.TITLE},LOG_LINES:"
        for i, line in enumerate(self.LOG_LINES):
            result += f"\n{i:->5d}:{line}"
        return result

    def __repr__(self):
        return str(self)

    def step_last__get(self) -> Any | NoReturn:
        return self.STEP_HISTORY[-1][1]

    def log_last__get(self) -> str | None:
        try:
            return self.LOG_LINES[-1]
        except:
            pass


# =====================================================================================================================
