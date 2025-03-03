from typing import *
import threading
import re

import imaplib
import email

from base_aux.aux_attr.m4_kits import *
from base_aux.privates.m1_privates import *
from base_aux.aux_attr.m1_attr2_nest2_lambdas_resolve import NestInit_AttrsLambdaResolve
from base_aux.alerts.m2_select import *
from base_aux.alerts.m0_base import *


# =====================================================================================================================
# TODO: SEPARATE BASE+INTERFACE!
# TODO: realise MARK_AS_READ = False!
# TODO: start reading from last read not just unseen!


# =====================================================================================================================
class ImapAddress(NamedTuple):
    """class for keeping connection parameters/settings for exact imap server

    :ivar ADDR: server address like "imap.mail.ru"
    :ivar PORT: server port like 993
    """
    ADDR: str
    PORT: int


class ImapServers:
    """well known servers addresses.

    Here we must collect servers like MilRu/GmailCom, and not to create it in any new project.
    """
    MAIL_RU: ImapAddress = ImapAddress("imap.mail.ru", 993)


class AlertImap(AlertSelect.TELEGRAM_DEF):
    """Just created exact class for Alerts in Imap!
    """
    pass


# =====================================================================================================================
class MonitorImap(NestInit_AttrsLambdaResolve, threading.Thread):
    """Monitor (threaded) email box for new letters. Notify if new letter appears corresponding to folder name and subject regexp.

    :ivar INTERVAL: monitoring interval in seconds
    :ivar SERVER: server address
    :ivar AUTH: server authentication data object
    :ivar FOLDER: email folder name where wait new emails
        None - for Inbox/Входящие!
    :ivar SUBJECT_REGEXP: regexp for email subject
        None - for all,
        example - r"\[ALERT\]test1"
    # :ivar MARK_AS_READ: after reading mark as read - NOT REALISED!
    :ivar ALERT: object which will send the alerts
    :ivar _conn: connection object
    :ivar stop_flag: flag for stop monitoring, now is stops only after calculating
    :ivar step_counter: just a counter for actually finished CALCULATING cycles

    :ivar _detected: detected email aux_types
    """
    INTERVAL: int = 1 * 1 * 10

    SERVER: ImapAddress = ImapServers.MAIL_RU
    AUTH: AttrKit_AuthNamePwd = PvLoaderIni(target=AttrKit_AuthNamePwd, keypath=("AUTH_EMAIL_DEF",))
    FOLDER: Optional[str] = None
    SUBJECT_REGEXP: Optional[str] = None
    # MARK_AS_READ: bool = True

    ALERT: type[AlertBase] = AlertImap
    _conn: Optional[imaplib.IMAP4_SSL] = None
    stop_flag: Optional[bool] = None
    step_counter: int = 0

    def __init__(self):
        super().__init__(daemon=True)

        self._detected: list[str] = []
        self.start()

    # CONNECT =========================================================================================================
    def _connect(self) -> Union[bool, NoReturn]:
        """connect, create connection object and establish connection.
        """
        if self._conn:
            return True

        print(f"\n _connect {self.__class__.__name__}")
        try:
            self._conn = imaplib.IMAP4_SSL(self.SERVER.ADDR, self.SERVER.PORT)
        except:
            pass

        if self._conn:
            print(self._conn.login(self.AUTH.USER, self.AUTH.PWD))
            self.folder_select(self.FOLDER)
            print(self._conn.search(None, 'UNSEEN'))  # ('OK', [b''])

        return bool(self._conn)

    def folder_select(self, name: Optional[str] = None) -> Optional[NoReturn]:
        """Select folder for monitoring
        """
        try:
            if name:
                print(self._conn.select(name))  # ('OK', [b'5'])
            else:
                print(self._conn.select())  # ('OK', [b'5'])

        except Exception as exx:
            msg = f"[CRITICAL] not exists [folder={name}]"
            print(msg)
            raise Exception(msg)
            # raise exx

    def _conn_close(self) -> None:
        """close connection
        """
        if self._conn:
            self._conn.close()
            self._conn.logout()

    def _conn_clear(self) -> None:
        """delete conn object
        """
        self._conn = None

    def _conn_check_empty(self) -> bool:
        """check if connection obj exists
        """
        return self._conn is None

    # START ===========================================================================================================
    def run(self):
        """MAIN function working in thread
        """
        while True:
            if self._connect():
                subjects = self.get_unseen_subject_list()
                for subject in subjects:
                    if not self.SUBJECT_REGEXP or re.fullmatch(self.SUBJECT_REGEXP, subject):
                        self._detected.append(subject)
                        self.ALERT(subject, subj_suffix=f"{self.__class__.__name__}/{self.FOLDER or 'Inbox'}")

            self._conn_close()
            self.step_counter += 1

            if self.stop_flag:
                return
            time.sleep(self.INTERVAL)
            if self.stop_flag:
                return

    def wait_cycle(self, sleep: int = 1) -> None:
        """wait finished calculated cycles

        :param sleep: sleep period in seconds between checks
        """
        step_finish = self.step_counter + 1

        while self.step_counter < step_finish:
            time.sleep(sleep)

    # MAIL ============================================================================================================
    def get_unseen_subject_list(self) -> list[str]:
        """get all subgects for unseen emails
        """
        result = []

        try:
            for num in self._conn.search(None, "UNSEEN")[1][0].split():    # UNSEEN/ALL
                _, msg = self._conn.fetch(num, '(RFC822)')
                msg = email.message_from_bytes(msg[0][1])

                try:
                    # has russian
                    subject = email.header.decode_header(msg["Subject"])[0][0].decode()
                except Exception as exx:
                    # english only!
                    subject = msg["Subject"]

                subject = subject or ""
                result.append(subject)
        except Exception as exx:
            self._conn_clear()

        return result

    # UNSORTED ========================================================================================================
    def _data_blocks__print(self):
        """just an explorer and research
        """
        _, msg = self._conn.fetch("6", '(RFC822)')
        msg = email.message_from_bytes(msg[0][1])
        print(type(msg))  # <class 'email.message.Message'>
        print(list(
            msg))  # ['Delivered-To', 'Return-path', 'Received-SPF', 'Received', 'Received', 'DKIM-Signature', 'DKIM-Signature', 'Precedence', 'List-Id', 'List-Issue', 'List-Unsubscribe', 'List-Subscribe', 'List-Archive', 'List-Post', 'X-Felis-L', 'X-rpcampaign', 'X-Mailru-Msgtype', 'Feedback-Id', 'Message-Id', 'Date', 'From', 'To', 'Subject', 'MIME-Version', 'Content-Type', 'Content-Transfer-Encoding', 'X-Mailru-Src', 'X-4EC0790', 'X-6b629377', 'X-7564579A', 'X-77F55803', 'X-7FA49CB5', 'X-C1DE0DAB', 'X-C8649E89', 'X-D57D3AED', 'X-F696D7D5', 'X-Mailru-BIMI-Organization', 'X-Mailru-Dmarc-Auth', 'X-Mailru-ThreadID', 'X-Mras', 'X-Spam', 'Authentication-Results', 'X-Mailru-Intl-Transport']

        for name in list(msg):
            print(f"[{name}]===[{msg[name]}]")


# =====================================================================================================================
