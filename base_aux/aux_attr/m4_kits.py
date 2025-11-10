from base_aux.base_nest_dunders.m1_init0_annots_required import *
from base_aux.base_nest_dunders.m1_init0_reinit1_mutable_attrs import *
from base_aux.base_nest_dunders.m1_init2_annots1_attrs_by_args_kwargs import *
from base_aux.base_nest_dunders.m2_str2_attrs import *
from base_aux.base_nest_dunders.m6_eq1_attrs import *
from base_aux.base_nest_dunders.m8_contains_attrs import *
from base_aux.base_nest_dunders.m8_len_attrs import *


# =====================================================================================================================
class Base_AttrKit(
    NestInit_AnnotsAttr_ByArgsKwargs,

    NestGAI_AnnotAttrIC,
    NestInit_MutableClsValues,
    NestInit_AnnotsRequired,

    NestEq_AttrsNotHidden,
    NestStR_AttrsNotHidden,
    NestLen_AttrNotHidden,
    NestContains_AttrIcNotHidden,
):     # TODO: decide to delete! use only dynamic?? - NO! keep it!!!
    """
    SAME AS - 1=ATTRS
    -----------------
    https://www.attrs.org/en/stable/examples.html
    yes! but more simple! and not so complicated! clear one way logic!

    SAME AS - 2=NAMEDTUPLE
    ----------------------

    GOAL
    ----
    just show that child is a kit
    1/ attrs need to init by args/kwargs
    2/ all annotated - must set!
    3/ IgnoreCase applied!

    NOTE
    ----
    !/ DONT USE DIRECTLY! use AttrKit_Blank instead! direct usage acceptable only for isinstance checking!
    1/ used in final CHILDs
    2/ basically used for static values like parsed from ini/json files

    SPECIALLY CREATED FOR
    ---------------------
    create special final kits like AttrKit_AuthNamePwd

    OLD docstr
    =======================
        GOAL
        ----
        1/ generate object with exact attrs values by Kwargs like template
        2/ for further comparing by Eq
        3/ all callables will resolve as Exc
    """
    def _redefine_nones(self, *args, **kwargs) -> None:
        """
        GOAL
        ----
        after created instance you can reapply defaults
        so if values keep None and you vant ro reinit it - just pass nes values!

        SPECIALLY CREATED FOR
        ---------------------
        Base_ReAttempts when you want to pass attempts by Rexp-patterns (with some nones) and define default values later in future methods
        """
        # TODO: finish!
        for index, value in enumerate(args):
            pass

        for name, value in kwargs.items():
            pass


# =====================================================================================================================
@final
class AttrKit_Blank(Base_AttrKit):
    """
    GOAL
    ----
    jast show that you can create any kwargs kit without raising (when check annots required)
    """
    pass


# ---------------------------------------------------------------------------------------------------------------------
@final
class AttrKit_AuthNamePwd(Base_AttrKit):
    NAME: str
    PWD: str


@final
class AttrKit_AuthTgBot(Base_AttrKit):
    LINK_ID: str = None     # @mybot20230913
    NAME: str = None        # MyBotPublicName
    TOKEN: str


@final
class AttrKit_AuthServer(Base_AttrKit):
    NAME: str
    PWD: str
    SERVER: str


@final
class AttrKit_AddrPort(Base_AttrKit):
    """class for keeping connection parameters/settings for exact smtp server

    :ivar ADDR: smtp server address like "smtp.mail.ru"
    :ivar PORT: smtp server port like 465
    """
    ADDR: str
    PORT: int


# =====================================================================================================================
if __name__ == '__main__':
    pass


# =====================================================================================================================
