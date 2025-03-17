from typing import *

from PyQt5.QtCore import QThread

from base_aux.base_nest_dunders.m1_init1_source2_kwargs import *
from base_aux.base_statics.m1_types import *


# =====================================================================================================================
class ThreadItem(NestInit_SourceKwArgs_Explicite, QThread):     # TODO+FIXME: deprecate! use direct Lambda as thread!!!
    """Object for keeping thread data for better managing.
    """
    SOURCE: Callable
    ARGS: TYPING.ARGS_FINAL
    KWARGS: TYPING.KWARGS_FINAL

    result: Optional[Any] = None
    exx: Optional[Exception] = None

    def run(self):
        try:
            self.result = self.SOURCE(*self.ARGS, **self.KWARGS)
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
