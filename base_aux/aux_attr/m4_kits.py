from typing import *

from base_aux.aux_attr.m1_attr2_nest3_eq_attrs import NestEq_AttrsNotPrivate
from base_aux.aux_attr.m1_attr2_nest4_str import NestStR_Attrs
from base_aux.aux_attr.m1_attr2_nest5_contains import NestContains_AttrIC
from base_aux.aux_attr.m1_attr2_nest6_len import NestLen_AttrNotPrivate

from base_aux.base_inits.m3_nest_init_annots_attrs_by_kwargs import *
from base_aux.aux_attr.m2_annot1_aux import *
from base_aux.aux_attr.m1_attr2_nest3_eq_attrs import *
from base_aux.base_inits.m3_nest_init_annots_attrs_by_kwargs import NestInit_AnnotsAttrByKwArgs


# =====================================================================================================================
class Nest_AttrKit(
    NestInit_AnnotsAttrByKwArgs,    # GAI+Required

    NestEq_AttrsNotPrivate,
    NestStR_Attrs,
    NestContains_AttrIC,
    NestLen_AttrNotPrivate
):     # TODO: decide to delete! use only dynamic?? - NO! keep it!!!
    """
    GOAL
    ----
    just show that child is a kit
    1/ attrs need to init by args/kwargs
    2/ all annotated - must set!

    NOTE
    ----
    !/ DONT USE DIRECTLY! use AttrKit_Blank instead! direct usage acceptable only for isinstance checking!
    1/ used in final CHILDs
    2/ basically used for static values like parsed from ini/json files

    SPECIALLY CREATED FOR
    ---------------------


    OLD docstr
    =======================
        GOAL
        ----
        1/ generate object with exact attrs values by Kwargs like template
        2/ for further comparing by Eq
        3/ all callables will resolve as Exx

        NOTE
        ----
        IgnoreCase applied!

        SAME AS - NestInit_AnnotsAttrByKwArgs
        --------------------------------------
        but
            - args useless - if no annots

        WHY NOT - just EqValid_*
        ------------------------
        1/ cause you will not keep simple direct object with attrs!
        2/ EqValid_* will be created! further!
    """


# =====================================================================================================================
@final      # TODO: decide not use final and use nesting any kit, by collecting attrs???
class AttrKit_Blank(Nest_AttrKit):
    """
    GOAL
    ----
    jast show that you can create any kwargs kit without raising (when check annots required)
    """
    pass


# ---------------------------------------------------------------------------------------------------------------------
@final
class AttrKit_AuthNamePwd(Nest_AttrKit):
    NAME: str
    PWD: str


@final
class AttrKit_AuthTgBot(Nest_AttrKit):
    LINK_ID: str = None     # @mybot20230913
    NAME: str = None        # MyBotPublicName
    TOKEN: str


@final
class AttrKit_AuthServer(Nest_AttrKit):
    NAME: str
    PWD: str
    SERVER: str


# =====================================================================================================================
if __name__ == '__main__':
    pass


# =====================================================================================================================
