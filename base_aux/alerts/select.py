from base_aux.alerts.alerts__1_smtp import AlertSmtp
from base_aux.alerts.alerts__2_telegram import AlertTelegram


# =====================================================================================================================
class AlertSelect:
    SMTP_DEF = AlertSmtp
    TELEGRAM_DEF = AlertTelegram


# =====================================================================================================================
