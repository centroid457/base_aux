from typing import *

from base_aux.aux_attr.m5_templates import *


# =====================================================================================================================
class AttrKit_AuthNamePwd(AttrTemplate_Static):
    NAME: str
    PWD: str


class AttrKit_AuthTgBot(AttrTemplate_Static):
    LINK_ID: str = None     # @mybot20230913
    NAME: str = None        # MyBotPublicName
    TOKEN: str


# =====================================================================================================================
