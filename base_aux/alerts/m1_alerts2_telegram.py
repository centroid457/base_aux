from typing import *

from base_aux.lambdas.m1_lambdas import Lambda
from base_aux.aux_attr.m1_attr2_nest2_lambdas_resolve import NestInit_AttrsLambdaResolve
from base_aux.privates.m1_privates import *
from base_aux.aux_attr.m4_kits import *
from .m0_base import *


# =====================================================================================================================
class RecipientTgID(Nest_AttrKit):
    MyTgID: str


# =====================================================================================================================
class AlertTelegram(NestInit_AttrsLambdaResolve, AlertBase):
    """realisation for sending Telegram msg
    """
    # SETTINGS ------------------------------------
    SERVER_TG: AttrKit_AuthNamePwd = PvLoaderIni_AuthTgBot(keypath=("TGBOT_DEF",))
    RecipientTgID: AttrKit_AuthNamePwd = PvLoaderIni(target=RecipientTgID, keypath=("TG_ID",))

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
        return self.RecipientTgID.MyTgID


# =====================================================================================================================
