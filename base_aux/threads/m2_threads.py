"""
manage spawned threads

Designed to working with spawned threads

NOTE: maybe you dont need use it if you need only one class method - use direct QThread

use different managers for different funcs/methods if needed
use just one decorator to spawn threads from func / methods
keep all spawned threads in list by ThreadItem aux_types
ThreadItem keeps result/exx/is_alive attributes!
use wait_all/terminate_all()
"""
# =====================================================================================================================
import time

from base_aux.base_singletons.m1_singleton import *
from base_aux.aux_argskwargs.m1_argskwargs import *
from base_aux.threads.m1_item import ThreadItem


# =====================================================================================================================
class ThreadsManager(SingletonCallMeta):
    """Manager for spawning threads and keep its instances with additional data.
    Singleton! do you dont need saving instances!

    USAGE
    -----
    1. BEST PRACTICE
    Not recommended using it directly, use as simple nested:
        class ThreadsManager1(ThreadsManager):
            pass

        @ThreadsManager1.decorator__to_thread
        def func(*args, **kwargs):
            pass

    2. Direct usage
    But if you need only one manager - do use directly.
        @ThreadsManager.decorator__to_thread
        def func(*args, **kwargs):
            pass

    :ivar _PARAM__NOTHREAD: parameter for passing in decorated function which can run SOURCE without thread

    :param args: NAME for manager instance
    :param thread_items: ThreadItem instances,
    :param MUTEX: mutex for safe collecting threads in this manager, creates in init
    :param counter: counter for collected threads in this manager
    """
    THREADS: list[ThreadItem]

    _PARAM__NOTHREAD: str = "nothread"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.THREADS = []

    @property
    def NAME(self) -> str:
        """classname for manager
        """
        return self.__class__.__name__

    @property
    def count(self) -> int:
        return len(self.THREADS)

    # =================================================================================================================
    def decorator__to_thread(self, _func) -> Callable:
        """Decorator which start thread from funcs and methods.

        always collect aux_types threads in result object! even if nothread! so you can get results from group!

        :param _func: decorated SOURCE
        """
        def _wrapper__spawn_thread(*args, **kwargs) -> Optional[Any]:
            """actual wrapper which spawn thread from decorated SOURCE.

            :param args: args passed into SOURCE/method,
            :param kwargs: kwargs passed into SOURCE/method,
            """
            nothread = self._PARAM__NOTHREAD in kwargs and kwargs.pop(self._PARAM__NOTHREAD)

            thread_item = ThreadItem(source=_func, args=args, kwargs=kwargs)
            self.THREADS.append(thread_item)
            thread_item.start()

            if nothread:
                thread_item.wait()
                return thread_item.result

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
                if not func_validate(thread.result):
                    return False
            else:
                if thread.result != value:
                    return False
        return True


# =====================================================================================================================
