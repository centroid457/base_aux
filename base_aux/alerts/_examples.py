# =========================================================================================
### 0. BEST PRACTICE
from base_aux.alerts.m2_select import *
from base_aux.alerts.m1_alerts1_smtp import *
from base_aux.alerts.m1_alerts2_telegram import *


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
from base_aux.alerts import *


class SmtpServersMOD(SmtpServers):
    EXAMPLE_RU: SmtpAddress = SmtpAddress("smtp.EXAMPLE.ru", 123)


class AlertSmtpMOD(AlertSmtp):
    SERVER_SMTP: SmtpAddress = SmtpServersMOD.EXAMPLE_RU  # or direct =SmtpAddress("smtp.EXAMPLE.ru", 123)

# =========================================================================================
#### 2. change authorisation data (see `privates` for details)
from base_aux.alerts import *
from base_aux.privates.m1_loader5_auto import *


class AlertSmtpMOD(AlertSmtp):
    AUTH: PrivateAuto = PrivateAuto(_section="AUTH_EMAIL_MOD")

# =========================================================================================
#### 3. change other settings (see source for other not mentioned)
from base_aux.alerts import *


class AlertSmtpMOD(AlertSmtp):
    RECONNECT_PAUSE: int = 60
    RECONNECT_LIMIT: int = 10

    TIMEOUT_RATELIMIT: int = 600

    RECIPIENT_SPECIAL: str = "my_address_2@mail.ru"

# =========================================================================================
#### 4. send
# if no mods
from base_aux.alerts import *

AlertSmtp(_subj_name="Hello", body="World!")

# with mods
from base_aux.alerts import *


class AlertSmtpMOD(AlertSmtp):
    pass  # changed


AlertSmtpMOD(_subj_name="Hello", body="World!")

# =========================================================================================
#### 5. using in class with saving alert object
from base_aux.alerts import *

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
from base_aux.alerts import *

class MyMonitor:
    ALERT = AlertTelegram

monitor = MyMonitor()
monitor.ALERT("Hello")
