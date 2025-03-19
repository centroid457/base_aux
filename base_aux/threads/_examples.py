from base_aux.threads.m1_manager import *
import time


# =====================================================================================================================
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
assert {item.result for item in ThreadManager1().THREADS} == {num * 1000 for num in range(count)}

ThreadManager1().clear()

# spawn ------------------
for i in range(count):
    assert Cls().func1(i) is None


# =====================================================================================================================
