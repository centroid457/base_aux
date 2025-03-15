from typing import *
import time
from collections import deque

from PyQt5.QtCore import QThread, QTimer

from base_aux.aux_text.m7_text_formatted import *
from base_aux.base_nest_dunders.m1_init3_reinit_lambdas_resolve import NestInit_AttrsLambdaResolve


# =====================================================================================================================
class Interface_Alert:
    """Interface for Alerts

    RULES:
    - if some method cant exists (like for telegram) - just return True!
    - Dont return None!
    - Dont use Try sentences inside - it will be applied in upper logic!
    - Decide inside if it was success or not, and return conclusion True/False only.
    """
    MSGS_UNSENT: deque[str | TextFormatted | Any]
    MSG_ACTIVE: Any

    def _connect_unsafe(self) -> Union[bool, NoReturn]:
        """establish connection to source
        """
        # self._conn = None
        return True

    def _disconnect_unsafe(self) -> Union[bool, NoReturn]:
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
        return str(self.MSG_ACTIVE)

    def _recipient_get(self) -> str:
        """RECIPIENT SelfSending, get from obvious class aux_types!
        """
        pass


# =====================================================================================================================
class Base_Alert(NestInit_AttrsLambdaResolve, Interface_Alert, QThread):     # REM: DONT ADD SINGLETON!!! SNMP WILL NOT WORK!!! and calling logic will be not simple!
    """
    GOAL
    ----
    alert msg sender
    """
    # SETTINGS ------------------------------------
    CONN_ADDRESS: AttrKit_Blank = None
    CONN_AUTH: AttrKit_AuthNamePwd = None
    RECIPIENT: Any = None

    TIMER_TIMEOUT:  int = 60
    TIMEOUT_SEND: float = 1.2
    RECONNECT_LIMIT: int = 3
    RECONNECT_PAUSE: int = 60
    # TIMEOUT_RATELIMIT: int = 600    # when EXX 451, b'Ratelimit exceeded

    MSGS_UNSENT: deque[str | TextFormatted | Any]

    # AUX -----------------------------------------
    _conn: Any = None
    result_connect: bool | None = None
    result_login: bool | None = None
    result_sent_all: bool | None = None

    timer: QTimer

    @property
    def MSG_ACTIVE(self) -> str | TextFormatted | Any | None:
        if len(self.MSGS_UNSENT) > 0:
            return self.MSGS_UNSENT[0]

    # =================================================================================================================
    def __init__(self, conn_address: AttrKit_Blank = None, conn_auth: AttrKit_AuthNamePwd = None, recipient: Any = None):
        """
        GOAL
        ----
        Send msg on init
        """
        # params --------------
        if conn_address is not None:
            self.CONN_ADDRESS = conn_address
        if conn_auth is not None:
            self.CONN_AUTH = conn_auth

        if recipient is not None:
            self.RECIPIENT = recipient
        if self.RECIPIENT is None:
            self.RECIPIENT = self._recipient_get()

        self.MSGS_UNSENT = deque()

        super().__init__()
        self.init_timer()

        # START ---------------
        self.start()

    def init_timer(self) -> None:
        self.timer = QTimer()
        self.timer.setInterval(self.TIMER_TIMEOUT * 1000)
        self.timer.timeout.connect(self.start)
        self.timer.start()

    # =================================================================================================================
    def send_msg(self, body):
        self.MSGS_UNSENT.append(body)
        self.start()

    def start(self, **kwargs):
        if not self.isRunning():
            super().start()

    # =================================================================================================================
    def _connect(self) -> Optional[bool]:
        """create connection object
        """
        while True:
            counter = 0
            self.ready_to_send = None
            while counter <= self.RECONNECT_LIMIT:
                counter += 1

                if not self.result_connect:
                    print(f"[connect] TRY {self.__class__.__name__}")
                    try:
                        self.result_connect = self._connect_unsafe()
                        if self.result_connect:
                            print("[connect] SUCCESS")
                    except Exception as exx:
                        print(f"[connect] ERROR [{exx!r}]")

                if self.result_connect and not self.result_login:
                    try:
                        self.result_login = self._login_unsafe()
                        if self.result_login:
                            print("[login] SUCCESS")
                    except Exception as exx:
                        print(f"[LOGIN] ERROR [{exx!r}]")

                print("=" * 100)
                print("=" * 100)
                print("=" * 100)
                print()

                self.ready_to_send = self.result_connect and self.result_login
                if self.ready_to_send:
                    break
                else:
                    time.sleep(self.RECONNECT_PAUSE)

            # -------------------------------------------
            if self.ready_to_send:
                break
            else:
                print(f"RECONNECT_PAUSE[{counter=}]")
                print("=" * 100)
                print()
                time.sleep(10)
                continue

        return self.ready_to_send

    def _disconnect(self):
        self.result_connect = None
        self.result_login = None

        try:
            self._disconnect_unsafe()
        except:
            pass

    # =================================================================================================================
    def run(self) -> None:
        print()
        print()
        print()
        print(f"RUN START")
        self.result_sent_all = None

        while self.MSG_ACTIVE is not None:
            if not self._connect():
                break

            MSG = self._msg_compose()
            print("[Try send", "-" * 80)
            print(MSG)
            print("Try send]", "-" * 80)

            try:
                sent_result = self._send_unsafe()
                if sent_result:
                    self.MSGS_UNSENT.popleft()
                    print("[send] SUCCESS")
            except Exception as exx:
                msg = f"[sent] ERROR [{exx!r}]"
                # [send] ERROR [SMTPDataError(451, b'Ratelimit exceeded for mailbox centroid@mail.ru. Try again later.')]
                print(msg)
                break

        self.result_sent_all = self.MSG_ACTIVE is None
        print(f"{self.result_sent_all=}")
        self._disconnect()
        print(f"RUN FINISH")


# =====================================================================================================================
