import pytest
import time


class PrintSecs:
    """
    NOT REALISED!!!

    GOAL
    use logging waiting seconds on processes with blind timeout like connect()
    so you can see exact waiting process
    """
    def __init__(self, msg: str = None):
        pass

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass



def test__1():
    class Target:
        def connect(self, timeout: float = 5):
            time.sleep(timeout)


    with PrintSecs():
        Target().connect()

