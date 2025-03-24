from typing import *
import time

from base_aux.aux_callable.m3_thread_collector import ThreadsDecorCollector


# =====================================================================================================================
class Test__Manager:
    # VICTIM: type[ThreadsDecorCollector] = type("VICTIM", (ThreadsDecorCollector,), {})

    def test__singleton(self):
        class ThreadDeCollector1(ThreadsDecorCollector):
            pass

        class ThreadDeCollector2(ThreadsDecorCollector):
            pass

        inst1 = ThreadDeCollector1()
        inst2 = ThreadDeCollector2()
        assert id(inst1) != id(inst2)
        assert id(inst1) == id(ThreadDeCollector1())

    # -----------------------------------------------------------------------------------------------------------------
    def test__noClass_severalManagers(self):
        # settings ------------------
        count = 5
        time_start = time.time()

        # define victim ------------------
        class ThreadDeCollector1(ThreadsDecorCollector):
            pass

        class ThreadDeCollector2(ThreadsDecorCollector):
            pass

        assert ThreadDeCollector1() != ThreadDeCollector2()
        assert ThreadDeCollector1() is not ThreadDeCollector2()

        assert ThreadDeCollector1().count == 0
        assert ThreadDeCollector2().count == 0

        @ThreadDeCollector1().decorator__to_thread
        def func1(num):
            time.sleep(1)
            return num * 10

        @ThreadDeCollector2().decorator__to_thread
        def func2(num):
            time.sleep(1)
            return num * 100

        # spawn ------------------
        for i in range(count):
            assert func1(i) is None

        assert ThreadDeCollector1().count == count
        assert ThreadDeCollector2().count == 0

        for i in range(count):
            assert func2(i) is None

        assert ThreadDeCollector1().count == count
        assert ThreadDeCollector2().count == count

        # wait ------------------
        ThreadDeCollector1().wait_all()
        ThreadDeCollector2().wait_all()

        # checks ------------------
        for item in ThreadDeCollector1().THREADS:
            assert item.isRunning() is False

        assert time.time() - time_start < 5

        assert {item.RESULT for item in ThreadDeCollector1().THREADS} == {num * 10 for num in range(count)}
        assert {item.RESULT for item in ThreadDeCollector2().THREADS} == {num * 100 for num in range(count)}

    def test__Class(self):
        # settings ------------------
        count = 5
        time_start = time.time()

        # define victim ------------------
        class ThreadDeCollector1(ThreadsDecorCollector):
            pass

        class Cls:
            @ThreadDeCollector1().decorator__to_thread
            def func1(self, num):
                time.sleep(1)
                return num * 1000

        # spawn ------------------
        for i in range(count):
            assert Cls().func1(i) is None

        assert ThreadDeCollector1().count == count
        ThreadDeCollector1().wait_all()
        assert {item.RESULT for item in ThreadDeCollector1().THREADS} == {num * 1000 for num in range(count)}

        ThreadDeCollector1().clear()

        # spawn ------------------
        for i in range(count):
            assert Cls().func1(i) is None

        assert ThreadDeCollector1().count == count
        ThreadDeCollector1().wait_all()
        assert {item.RESULT for item in ThreadDeCollector1().THREADS} == {num * 1000 for num in range(count)}

    def test__check_results_all(self):
        # define victim ------------------
        class ThreadDeCollector1(ThreadsDecorCollector):
            pass

        @ThreadDeCollector1().decorator__to_thread
        def func1(value):
            return value

        # bool ----------
        ThreadDeCollector1().clear()
        [func1(True), func1(True)]
        ThreadDeCollector1().wait_all()
        assert ThreadDeCollector1().check_results_all() is True

        ThreadDeCollector1().clear()
        [func1(True), func1(False)]
        ThreadDeCollector1().wait_all()
        assert ThreadDeCollector1().check_results_all() is False

        ThreadDeCollector1().clear()
        [func1(False), func1(False)]
        ThreadDeCollector1().wait_all()
        assert ThreadDeCollector1().check_results_all(False) is True

        # int ----------
        ThreadDeCollector1().clear()
        [func1(1), func1(1)]
        ThreadDeCollector1().wait_all()
        assert ThreadDeCollector1().check_results_all(1) is True

        ThreadDeCollector1().clear()
        [func1(1), func1(2)]
        ThreadDeCollector1().wait_all()
        assert ThreadDeCollector1().check_results_all(1) is False

        # func_validate ----------
        ThreadDeCollector1().clear()
        [func1(0), func1(1)]
        ThreadDeCollector1().wait_all()
        assert ThreadDeCollector1().check_results_all(func_validate=bool) is False

        ThreadDeCollector1().clear()
        [func1(1), func1(2)]
        ThreadDeCollector1().wait_all()
        assert ThreadDeCollector1().check_results_all(func_validate=bool) is True

        def validate_int(obj: Any) -> bool:
            return isinstance(obj, int)

        ThreadDeCollector1().clear()
        [func1(0), func1(1)]
        ThreadDeCollector1().wait_all()
        assert ThreadDeCollector1().check_results_all(func_validate=validate_int) is True

    def test__PARAM__NOTHREAD(self):
        # define victim ------------------
        class ThreadDeCollector1(ThreadsDecorCollector):
            pass

        @ThreadDeCollector1().decorator__to_thread
        def func1(value):
            time.sleep(0.2)
            return value

        # bool ----------
        ThreadDeCollector1().clear()

        assert func1(True, nothread=False) is None
        assert func1(True, nothread=True) is True
        assert ThreadDeCollector1().count == 2

    def test__AS_FUNC(self):
        class ThreadDeCollector1(ThreadsDecorCollector):
            pass

        def func1(value):
            time.sleep(0.2)
            return value

        ThreadDeCollector1().clear()
        thread = ThreadDeCollector1().decorator__to_thread(func1)

        assert thread(True, nothread=False) is None
        assert thread(True, nothread=True) is True
        assert ThreadDeCollector1().count == 2

    def _test__twice_execute_7777(self):    # not expected???
        class ThreadDeCollector1(ThreadsDecorCollector):
            pass

        @ThreadDeCollector1().decorator__to_thread
        def func1(value):
            time.sleep(0.2)
            return value

        ThreadDeCollector1().clear()

        assert ThreadDeCollector1().count == 0
        assert func1(True) is None
        assert ThreadDeCollector1().count == 1
        ThreadDeCollector1().wait_all()


# =====================================================================================================================
