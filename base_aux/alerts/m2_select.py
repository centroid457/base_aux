from base_aux.alerts.m1_alerts1_smtp import AlertSmtp
from base_aux.alerts.m1_alerts2_telegram import AlertTelegram


# =====================================================================================================================
class AlertSelect:
    SMTP_DEF = AlertSmtp
    TELEGRAM_DEF = AlertTelegram


# =====================================================================================================================
