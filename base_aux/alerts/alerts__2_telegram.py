import time
from typing import *

from base_aux.classes import ConstructOnInit_Item, ConstructOnInit
from base_aux.privates import *
from .base import *


# =====================================================================================================================
class RecipientTgID(PrivateAuto):
    """Object to get telegram RecipientId
    """
    SECTION = "TG_ID"
    MyTgID: str


# =====================================================================================================================
class AlertTelegram(ConstructOnInit, AlertBase):
    """realisation for sending Telegram msg
    """
    # SETTINGS ------------------------------------
    SERVER_TG: PrivateTgBotAddressAuto = ConstructOnInit_Item(PrivateTgBotAddressAuto, _section="TGBOT_DEF")

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
