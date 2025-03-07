from typing import *
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from base_aux.alerts.m0_base import *
from base_aux.privates.m1_privates import *
from base_aux.aux_attr.m4_kits import *
from base_aux.aux_attr.m1_attr2_nest2_lambdas_resolve import NestInit_AttrsLambdaResolve


# =====================================================================================================================
class SmtpAddress(NamedTuple):
    """class for keeping connection parameters/settings for exact smtp server

    :ivar ADDR: smtp server address like "smtp.mail.ru"
    :ivar PORT: smtp server port like 465
    """
    ADDR: str
    PORT: int


class SmtpServers:
    """well known servers addresses.

    Here we must collect servers like MilRu/GmailCom, and not to create it in any new project.
    """
    MAIL_RU: SmtpAddress = SmtpAddress("smtp.mail.ru", 465)


# =====================================================================================================================
class AlertSmtp(NestInit_AttrsLambdaResolve, AlertBase):
    """SMTP realisation for sending msg (email).
    """
    # SETTINGS ------------------------------------
    SERVER_SMTP: SmtpAddress = SmtpServers.MAIL_RU
    AUTH: AttrKit_AuthNamePwd = PvLoaderIni_AuthNamePwd(keypath=("AUTH_EMAIL_DEF",))
    TIMEOUT_SEND = 5

    # AUX -----------------------------------------
    _conn:  smtplib.SMTP_SSL

    def _connect_unsafe(self) -> Union[bool, NoReturn]:
        self._conn = smtplib.SMTP_SSL(self.SERVER_SMTP.ADDR, self.SERVER_SMTP.PORT, timeout=self.TIMEOUT_SEND)
        return True

    def _login_unsafe(self) -> Union[bool, NoReturn]:
        response = self._conn.login(self.AUTH.NAME, self.AUTH.PWD)
        print(response)
        print("=" * 100)
        return response and response[0] in [235, 503]

    def _send_unsafe(self) -> Union[bool, NoReturn]:
        self._conn.send_message(self._msg_compose())
        return True

    def _msg_compose(self) -> MIMEMultipart:
        msg = MIMEMultipart()
        msg["From"] = self.AUTH.NAME
        msg["To"] = self.RECIPIENT_SPECIAL or self.AUTH.NAME
        msg['Subject'] = self.SUBJECT
        msg.attach(MIMEText(self.body, _subtype=self._subtype))
        return msg

    def _recipient_self_get(self) -> str:
        return self.AUTH.NAME


# =====================================================================================================================
