from typing import *
import pytest
import time
from threading import Thread


class WithPrintWaiting:
    """
    GOAL
    use logging waiting seconds on processes with blind timeout like connect()
    so you can see exact waiting process
    """
    _thread: Thread = None
    _active: bool = None

    msg_main: str = ""
    msg_separator: str = '...waiting...'

    def __init__(self, msg_main: str = None):
        self._thread = Thread(target=self.target, daemon=True)
        self.index = 0

        if msg_main:
            self.msg_main = msg_main

    def __enter__(self):
        self.print_msg("START")
        self._active = True
        self._thread.start()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._active = False
        self._thread.join()
        self.print_msg("FINISH")

    def target(self) -> Never | None:
        while self._active:
            self.print_msg()
            time.sleep(1)
            self.index += 1

    def print_msg(self, suffix: str | None = None) -> None:
        suffix = "" if suffix is None else suffix
        if self.msg_main:
            msg_main = f"[{self.msg_main}]"
        else:
            msg_main = ""
        msg = f"{msg_main}{self.msg_separator}{self.index} {suffix}"
        print(msg)



def test__1():
    class Target:
        def connect(self, timeout: float = 3):
            time.sleep(timeout)

    with WithPrintWaiting():
        Target().connect()

    with WithPrintWaiting("hello"):
        Target().connect()
