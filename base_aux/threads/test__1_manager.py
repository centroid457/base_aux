from typing import *
import time

from base_aux.threads.m1_manager import ThreadsManager


# =====================================================================================================================
class Test__Manager:
    # VICTIM: type[ThreadsManager] = type("VICTIM", (ThreadsManager,), {})

    def test__singleton(self):
        class ThreadManager1(ThreadsManager):
            pass

        class ThreadManager2(ThreadsManager):
            pass

        inst1 = ThreadManager1()
        inst2 = ThreadManager2()
        assert id(inst1) != id(inst2)
        assert id(inst1) == id(ThreadManager1())

    # -----------------------------------------------------------------------------------------------------------------
    def test__noClass_severalManagers(self):
        # settings ------------------
        count = 5
        time_start = time.time()

        # define victim ------------------
        class ThreadManager1(ThreadsManager):
            pass

        class ThreadManager2(ThreadsManager):
            pass

        assert ThreadManager1() != ThreadManager2()
        assert ThreadManager1() is not ThreadManager2()

        assert ThreadManager1().count == 0
        assert ThreadManager2().count == 0

        @ThreadManager1().decorator__to_thread
        def func1(num):
            time.sleep(1)
            return num * 10

        @ThreadManager2().decorator__to_thread
        def func2(num):
            time.sleep(1)
            return num * 100

        # spawn ------------------
        for i in range(count):
            assert func1(i) is None

        assert ThreadManager1().count == count
        assert ThreadManager2().count == 0

        for i in range(count):
            assert func2(i) is None

        assert ThreadManager1().count == count
        assert ThreadManager2().count == count

        # wait ------------------
        ThreadManager1().wait_all()
        ThreadManager2().wait_all()

        # checks ------------------
        for item in ThreadManager1().THREADS:
            assert item.isRunning() is False

        assert time.time() - time_start < 5

        assert {item.RESULT for item in ThreadManager1().THREADS} == {num * 10 for num in range(count)}
        assert {item.RESULT for item in ThreadManager2().THREADS} == {num * 100 for num in range(count)}

    def test__Class(self):
        # settings ------------------
        count = 5
        time_start = time.time()

        # define victim ------------------
        class ThreadManager1(ThreadsManager):
            pass

        class Cls:
            @ThreadManager1().decorator__to_thread
            def func1(self, num):
                time.sleep(1)
                return num * 1000

        # spawn ------------------
        for i in range(count):
            assert Cls().func1(i) is None

        assert ThreadManager1().count == count
        ThreadManager1().wait_all()
        assert {item.RESULT for item in ThreadManager1().THREADS} == {num * 1000 for num in range(count)}

        ThreadManager1().clear()

        # spawn ------------------
        for i in range(count):
            assert Cls().func1(i) is None

        assert ThreadManager1().count == count
        ThreadManager1().wait_all()
        assert {item.RESULT for item in ThreadManager1().THREADS} == {num * 1000 for num in range(count)}

    def test__check_results_all(self):
        # define victim ------------------
        class ThreadManager1(ThreadsManager):
            pass

        @ThreadManager1().decorator__to_thread
        def func1(value):
            return value

        # bool ----------
        ThreadManager1().clear()
        [func1(True), func1(True)]
        ThreadManager1().wait_all()
        assert ThreadManager1().check_results_all() is True

        ThreadManager1().clear()
        [func1(True), func1(False)]
        ThreadManager1().wait_all()
        assert ThreadManager1().check_results_all() is False

        ThreadManager1().clear()
        [func1(False), func1(False)]
        ThreadManager1().wait_all()
        assert ThreadManager1().check_results_all(False) is True

        # int ----------
        ThreadManager1().clear()
        [func1(1), func1(1)]
        ThreadManager1().wait_all()
        assert ThreadManager1().check_results_all(1) is True

        ThreadManager1().clear()
        [func1(1), func1(2)]
        ThreadManager1().wait_all()
        assert ThreadManager1().check_results_all(1) is False

        # func_validate ----------
        ThreadManager1().clear()
        [func1(0), func1(1)]
        ThreadManager1().wait_all()
        assert ThreadManager1().check_results_all(func_validate=bool) is False

        ThreadManager1().clear()
        [func1(1), func1(2)]
        ThreadManager1().wait_all()
        assert ThreadManager1().check_results_all(func_validate=bool) is True

        def validate_int(obj: Any) -> bool:
            return isinstance(obj, int)

        ThreadManager1().clear()
        [func1(0), func1(1)]
        ThreadManager1().wait_all()
        assert ThreadManager1().check_results_all(func_validate=validate_int) is True

    def test__PARAM__NOTHREAD(self):
        # define victim ------------------
        class ThreadManager1(ThreadsManager):
            pass

        @ThreadManager1().decorator__to_thread
        def func1(value):
            time.sleep(0.2)
            return value

        # bool ----------
        ThreadManager1().clear()

        assert func1(True, nothread=False) is None
        assert func1(True, nothread=True) is True
        assert ThreadManager1().count == 2

    def test__AS_FUNC(self):
        class ThreadManager1(ThreadsManager):
            pass

        def func1(value):
            time.sleep(0.2)
            return value

        ThreadManager1().clear()
        thread = ThreadManager1().decorator__to_thread(func1)

        assert thread(True, nothread=False) is None
        assert thread(True, nothread=True) is True
        assert ThreadManager1().count == 2

    def _test__twice_execute_7777(self):    # not expected???
        class ThreadManager1(ThreadsManager):
            pass

        @ThreadManager1().decorator__to_thread
        def func1(value):
            time.sleep(0.2)
            return value

        ThreadManager1().clear()

        assert ThreadManager1().count == 0
        assert func1(True) is None
        assert ThreadManager1().count == 1
        ThreadManager1().wait_all()


# =====================================================================================================================
