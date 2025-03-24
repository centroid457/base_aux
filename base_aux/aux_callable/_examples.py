from base_aux.aux_callable.m3_thread_collector import *
import time


# =====================================================================================================================
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


# =====================================================================================================================
