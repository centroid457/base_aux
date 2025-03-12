# =========================================================================================
### 0. BEST PRACTICE
from base_aux.alerts.m2_select import *
from base_aux.alerts.m1_alerts1_smtp import *
from base_aux.alerts.m1_alerts2_telegram import *
from base_aux.aux_attr.m4_kits import AttrKit_AddrPort


class AlertADX(AlertSelect.TELEGRAM_DEF):
    pass

AlertADX("hello")
AlertADX("World")
AlertADX.threads_wait_all()

# =========================================================================================
# =========================================================================================
# =========================================================================================
### AlertSmtp
#### 1. add new server if not exists


class SmtpServersMOD(SmtpServers):
    EXAMPLE_RU: AttrKit_AddrPort = AttrKit_AddrPort("smtp.EXAMPLE.ru", 123)


class AlertSmtpMOD(AlertSmtp):
    CONN_ADDRESS: AttrKit_AddrPort = SmtpServersMOD.EXAMPLE_RU  # or direct =AttrKit_AddrPort("smtp.EXAMPLE.ru", 123)

# =========================================================================================
#### 2. change authorisation data (see `privates` for details)
from base_aux.privates.m1_privates import *


class AlertSmtpMOD(AlertSmtp):
    CONN_AUTH: AttrKit_AuthNamePwd = PvLoaderIni(target=AttrKit_AuthNamePwd, keypath=("AUTH_EMAIL_MOD",))


# =========================================================================================
#### 3. change other settings (see source for other not mentioned)


class AlertSmtpMOD(AlertSmtp):
    RECONNECT_PAUSE: int = 60
    RECONNECT_LIMIT: int = 10
    TIMEOUT_RATELIMIT: int = 600
    RECIPIENT: str = "my_address_2@mail.ru"

# =========================================================================================
#### 4. send
# if no mods

AlertSmtp(_subj_name="Hello", body="World!")

# with mods


class AlertSmtpMOD(AlertSmtp):
    pass  # changed


AlertSmtpMOD(_subj_name="Hello", body="World!")

# =========================================================================================
#### 5. using in class with saving alert object

class AlertSmtpMOD(AlertSmtp):
    pass    # changed

class MyMonitor:
    ALERT = AlertSmtpMOD

monitor = MyMonitor()
monitor.ALERT("Hello")

# =========================================================================================
# =========================================================================================
### AlertTelegram
# All idea is similar to AlertSmtp.

# add auth data
# add pv.json or do smth else (for details see privates.PrivateJsonTgBotAddress)
# json
{
    "TG_ID": {"MyTgID": 1234567890},
    "TGBOT_DEF": {
        "LINK_ID": "@my_bot_20230916",
        "NAME": "my_bot",
        "TOKEN": "9876543210xxxxxxxxxxxxxxxxxxxxxxxxx"
    }
}

# =========================================================================================

class MyMonitor:
    ALERT = AlertTelegram

monitor = MyMonitor()
monitor.ALERT("Hello")
