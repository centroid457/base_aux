from typing import *
import time

from base_aux.base_singletons.m1_singleton import *
from base_aux.aux_argskwargs.m1_argskwargs import *
from base_aux.aux_callable.m2_lambda2_thread import LambdaThread


# =====================================================================================================================
class ThreadsDeCollector(SingletonCallMeta):
    """
    TODO: DEPRECATE??? use clearly direct other methods/objects!

    NOTE
    ----
    1/ maybe you dont need use it if you need only one class method - use direct QThread

    GOAL
    ----
    Manager for spawning threads and keep its instances with additional data (result/exx).
    Singleton! do you dont need saving instances!

    USAGE
    -----
    use different managers for different funcs/methods if needed
    use just one decorator to spawn threads from func / methods
    keep all spawned threads in list by LambdaThread aux_types

    1. BEST PRACTICE
    Not recommended using it directly, use as simple nested:
        class ThreadsManager1(ThreadsDeCollector):
            pass

        @ThreadsManager1().decorator__to_thread
        def func(*args, **kwargs):
            pass

    2. Direct usage
    But if you need only one manager - do use directly without nesting.
        @ThreadsDeCollector().decorator__to_thread
        def func(*args, **kwargs):
            pass

    :param args: NAME for manager instance
    :param thread_items: LambdaThread instances,
    :param MUTEX: mutex for safe collecting threads in this manager, creates in init
    :param counter: counter for collected threads in this manager

    SPECIALLY CREATED FOR
    ---------------------
    stock strategies/monitors
    """
    THREADS: list[LambdaThread]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.THREADS = []

    @classmethod
    @property
    def NAME(cls) -> str:
        """class name for manager
        """
        return cls.__name__

    @property
    def count(self) -> int:
        return len(self.THREADS)

    # =================================================================================================================
    def decorator__to_thread(self, _func) -> Callable:
        """Decorator which start thread from funcs and methods.

        always collect aux_types threads in result object! even if nothread! so you can get results from group!

        :param _func: decorated SOURCE
        """
        def _wrapper__spawn_thread(*args, nothread: bool = None, **kwargs) -> Optional[Any]:
            """actual wrapper which spawn thread from decorated SOURCE.

            :param args: args passed into SOURCE/method,
            :param kwargs: kwargs passed into SOURCE/method,
            """
            thread_item = LambdaThread(_func, *args, **kwargs)
            self.THREADS.append(thread_item)
            thread_item.start()

            if nothread:
                thread_item.wait()
                return thread_item.RESULT

        return _wrapper__spawn_thread

    # =================================================================================================================
    def clear(self) -> None:
        """clear collected thread_items.

        useful if you dont need collected items any more after some step. and need to manage new portion.
        """
        self.THREADS.clear()

    def wait_all(self) -> None:
        """wait while all spawned threads finished.
        """
        # wait all started
        if not self.count:
            time.sleep(0.2)

        for _ in range(3):
            for item in self.THREADS:
                item.wait()

            time.sleep(0.1)

    def terminate_all(self) -> None:
        for thread in self.THREADS:
            thread.terminate()

    def check_results_all(self, value: Any = True, func_validate: Callable[[Any], bool] = None) -> bool:
        """check if result values for all threads are equal to the value

        :param value: expected comparing value for all thread results
        :param func_validate:
        """
        for thread in self.THREADS:
            if func_validate is not None:
                if not func_validate(thread.RESULT):
                    return False
            else:
                if thread.RESULT != value:
                    return False
        return True


# =====================================================================================================================
