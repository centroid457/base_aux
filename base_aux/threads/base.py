from typing import *
import time

from PyQt5.QtCore import QThread
from base_aux.classes import *


# =====================================================================================================================
pass


# =====================================================================================================================
class ThreadItem(QThread):
    """Object for keeping thread data for better managing.
    """
    target: Callable
    args: Tuple[Any, ...]
    kwargs: Dict[str, Any]

    result: Optional[Any] = None
    exx: Optional[Exception] = None

    def __init__(self, target: Callable, args: Union[Tuple, Any, ] = None, kwargs=None, *_args, **_kwargs):
        super().__init__(*_args, **_kwargs)

        if args and not isinstance(args, (tuple, list, )):
            args = (args, )

        self.target = target
        self.args = args or ()
        self.kwargs = kwargs or {}

    def run(self):
        try:
            self.result = self.target(*self.args, **self.kwargs)
        except Exception as exx:
            msg = f"{exx!r}"
            print(msg)
            self.exx = exx

    def SLOTS_EXAMPLES(self):
        """DON'T START! just for explore!
        """
        # checkers --------------------
        self.started
        self.isRunning()

        self.finished
        self.isFinished()

        self.destroyed
        self.signalsBlocked()

        # settings -------------------
        self.setTerminationEnabled()

        # NESTING --------------------
        self.currentThread()
        self.currentThreadId()
        self.thread()
        self.children()
        self.parent()

        # info --------------------
        self.priority()
        self.loopLevel()
        self.stackSize()
        self.idealThreadCount()

        self.setPriority()
        self.setProperty()
        self.setObjectName()

        self.tr()

        self.dumpObjectInfo()
        self.dumpObjectTree()

        # CONTROL --------------------
        self.run()
        self.start()
        self.startTimer()

        self.sleep(100)
        self.msleep(100)
        self.usleep(100)

        self.wait()

        self.killTimer()

        self.disconnect()
        self.deleteLater()
        self.terminate()
        self.quit()
        self.exit(100)

        # WTF --------------------


# =====================================================================================================================
class ThreadsManager(SingletonByCallMeta):
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

    :ivar _PARAM__NOTHREAD: parameter for passing in decorated function which can run target without thread

    :param args: NAME for manager instance
    :param thread_items: ThreadItem instances,
    :param MUTEX: mutex for safe collecting threads in this manager, creates in init
    :param counter: counter for collected threads in this manager
    """
    THREADS: List[ThreadItem]

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

        always collect objects threads in result object! even if nothread! so you can get results from group!

        :param _func: decorated target
        """
        def _wrapper__spawn_thread(*args, **kwargs) -> Optional[Any]:
            """actual wrapper which spawn thread from decorated target.

            :param args: args passed into target/method,
            :param kwargs: kwargs passed into target/method,
            """
            nothread = self._PARAM__NOTHREAD in kwargs and kwargs.pop(self._PARAM__NOTHREAD)

            thread_item = ThreadItem(target=_func, args=args, kwargs=kwargs)
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
