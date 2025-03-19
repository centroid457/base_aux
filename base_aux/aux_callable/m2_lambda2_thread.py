from typing import *
from PyQt5.QtCore import QThread

from base_aux.aux_callable.m2_lambda import Lambda


# =====================================================================================================================
class LambdaThread(Lambda, QThread):
    """
    NOTE
    ----
    same as Lambda but just add nesting QThread!

    GOAL
    ----
    Object for keeping thread data for better managing.
    """
    def __SLOTS_EXAMPLES(self):
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
