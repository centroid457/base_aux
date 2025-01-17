from typing import *

from base_aux.lambdas.m1_lambdas import Lambda
from base_aux.aux_attr.m1_attr3_lambdas_resolve import AttrsLambdasResolve
from base_aux.privates.m5_auto import *
from .m0_base import *


# =====================================================================================================================
class RecipientTgID(PrivateAuto):
    """Object to get telegram RecipientId
    """
    SECTION = "TG_ID"
    MyTgID: str


# =====================================================================================================================
class AlertTelegram(AttrsLambdasResolve, AlertBase):
    """realisation for sending Telegram msg
    """
    # SETTINGS ------------------------------------
    SERVER_TG: PrivateTgBotAddressAuto = Lambda(PrivateTgBotAddressAuto, _section="TGBOT_DEF")

    # AUX -----------------------------------------
    _conn: telebot.TeleBot

    def _connect_unsafe(self) -> Union[bool, NoReturn]:
        self._conn = telebot.TeleBot(token=self.SERVER_TG.TOKEN)
        return True

    def _send_unsafe(self) -> Union[bool, NoReturn]:
        self._conn.send_message(chat_id=self.RECIPIENT, text=self._msg_compose())
        return True

    def _msg_compose(self) -> str:
        msg = f"{self.SUBJECT}\n{self.body}"
        return msg

    def _recipient_self_get(self) -> str:
        return RecipientTgID().MyTgID


# =====================================================================================================================
