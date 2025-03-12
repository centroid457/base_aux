from typing import *
import time

from PyQt5.QtCore import QThread

import smtplib
import telebot

from base_aux.aux_text.m7_text_formatted import *


# =====================================================================================================================
class Interface_Alert:
    """Interface for Alerts

    RULES:
    - if some method cant exists (like for telegram) - just return True!
    - Dont return None!
    - Dont use Try sentences inside - it will be applied in upper logic!
    - Decide inside if it was success or not, and return conclusion True/False only.
    """
    BODY: Any

    def _connect_unsafe(self) -> Union[bool, NoReturn]:
        """establish connection to source
        """
        return True

    def _login_unsafe(self) -> Union[bool, NoReturn]:
        """authorise to source
        """
        return True

    def _send_unsafe(self) -> Union[bool, NoReturn]:
        """send msg
        """
        return True

    def _msg_compose(self) -> Union[str, 'MIMEMultipart']:
        """generate msg from existed data in attributes (passed before on init)
        """
        return str(self.BODY)

    def _recipient_get(self) -> str:
        """RECIPIENT SelfSending, get from obvious class aux_types!
        """
        pass


# =====================================================================================================================
class Base_Alert(Interface_Alert, QThread):     # REM: DONT ADD SINGLETON!!! SNMP WILL NOT WORK!!! and calling logic will be not simple!
    """
    GOAL
    ----
    alert msg sender

    NOTE
    ----
    - threading
        - daemons
        - collect all active threads
        - wait all spawned threads finished

    :ivar RECONNECT_LIMIT: how many times it will try to reconnect, after - just close object
    :ivar RECONNECT_PAUSE: pause between reconnecting in seconds
    :ivar _conn: actual connection object
    :ivar _result: result for alert state
        None - in process,
        False - finished UnSuccess,
        True - finished success!

    :ivar _threads_active: spawned (only active) threads
    """
    # SETTINGS ------------------------------------
    CONN_ADDRESS: Any
    CONN_AUTH: AttrKit_AuthNamePwd

    TIMEOUT_SEND: float = 1.2
    RECONNECT_LIMIT: int = 10
    RECONNECT_PAUSE: int = 60
    # TIMEOUT_RATELIMIT: int = 600    # when EXX 451, b'Ratelimit exceeded

    RECIPIENT: Any = None
    body: str | TextFormatted | Any = None

    # AUX -----------------------------------------
    _conn: Union[None, smtplib.SMTP_SSL, telebot.TeleBot] = None
    _result: Optional[bool] = None

    _threads_active: set[Self] = set()

    # =================================================================================================================
    def __init__(self, body: Any = None, recipient: Any = None):
        """
        GOAL
        ----
        Send msg on init
        """
        super().__init__()
        # self._mutex: threading.Lock = threading.Lock()

        if recipient is not None:
            self.RECIPIENT = recipient
        if self.RECIPIENT is None:
            self.RECIPIENT = self._recipient_get()

        # BODY ---------------
        if body is not None:
            body = str(body)
            self.body = body
            self.start()

    # =================================================================================================================
    @classmethod
    @property
    def NAME(cls) -> str:
        """name for AlertClass.
        Accustom ourselves to name you classes recognisable without adding new one redundant attributes.
        """
        return cls.__name__

    # =================================================================================================================
    def start(self, *args):
        """this is just add ability to collect started threads in class
        """
        self.__class__._threads_active.add(self)
        super().start()

    def _thread_finished(self):
        """del thread object from collection.
        called then thread finished.
        """
        self.__class__._threads_active.discard(self)

    @classmethod
    def threads_wait_all(cls):
        """wait while all spawned active threads will finished.
        """
        try:
            time.sleep(1)
            while cls._threads_active:
                list(cls._threads_active)[0].wait()
        except:
            pass

    def result_wait(self) -> Optional[bool]:
        """wait for finish thread and get succession result.
        Created for tests mainly! but you can use!
        """
        self.wait()
        return self._result

    # =================================================================================================================
    def _conn__check_exists(self) -> bool:
        """check if connection object exists
        """
        return self._conn is not None

    def _conn__disconnect(self) -> None:
        """disconnect connection object
        """
        if self._conn:
            self._conn.quit()
        self._conn__clear()

    def _conn__clear(self) -> None:
        """del connection object
        """
        self._conn = None

    def _connect(self) -> Optional[bool]:
        """create connection object
        """
        result = None
        if not self._conn__check_exists():
            print(f"TRY _connect {self.__class__.__name__}")
            try:
                if self._connect_unsafe():
                    print("[READY] connect")

            except Exception as exx:
                print(f"[CRITICAL] CONNECT [{exx!r}]")
                self._conn__clear()

        if self._conn__check_exists():
            try:
                result = self._login_unsafe()
                if result:
                    print("[READY] login")
            except Exception as exx:
                print(f"[CRITICAL] LOGIN [{exx!r}]")
                self._conn__clear()

        print("="*100)
        print("="*100)
        print("="*100)
        print()

        return result

    # =================================================================================================================
    def run(self) -> None:
        """main logic which manage started thread
        """
        self._result = None

        counter = 0
        while not self._conn__check_exists() and counter <= self.RECONNECT_LIMIT:
            counter += 1
            if not self._connect():
                print(f"[WARNING]try [{counter=}]")
                print("=" * 100)
                print()
                time.sleep(self.RECONNECT_PAUSE)

        print("[Try send", "-" * 80)
        print(self._msg_compose())
        print("Try send]", "-" * 80)

        if self._conn__check_exists():
            try:
                result = self._send_unsafe()
                if result:
                    print("[READY] send")
                    self._result = True
            except Exception as exx:
                msg = f"[CRITICAL]unexpected [{exx!r}]"
                print(msg)
                self._conn__clear()

        print()
        print()
        print()

        if self._result is None:
            self._result = False

        self._thread_finished()


# =====================================================================================================================
