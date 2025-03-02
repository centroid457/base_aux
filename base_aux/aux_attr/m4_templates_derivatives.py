from typing import *

from base_aux.aux_attr.m4_templates import *


# =====================================================================================================================
class AttrKit_AuthNamePwd(AttrTemplate_Direct):
    NAME: str
    PWD: str


class AttrKit_AuthTgBot(AttrTemplate_Direct):
    LINK_ID: str = None     # @mybot20230913
    NAME: str = None        # MyBotPublicName
    TOKEN: str


# =====================================================================================================================
