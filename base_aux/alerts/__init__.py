# =====================================================================================================================
# VERSION = (0, 0, 1)   # use import EXACT_OBJECTS! not *
#   from .main import *                 # INcorerct
#   from .main import EXACT_OBJECTS     # CORERCT


# =====================================================================================================================
from .base import AlertBase
from .alerts__1_smtp import SmtpAddress, SmtpServers, AlertSmtp
from .alerts__2_telegram import RecipientTgID, AlertTelegram


# =====================================================================================================================
# FIXME: move to main!
class AlertSelect:
    SMTP_DEF = AlertSmtp
    TELEGRAM_DEF = AlertTelegram


# =====================================================================================================================
