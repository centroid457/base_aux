from base_aux.aux_attr.m4_kits import *
from base_aux.base_statics.m4_enums import Enum_DictTextFormat
from base_aux.path2_file.m4_attrs_dict_loader import AttrsLoader_DictTextFile


# =====================================================================================================================
class PvLoaderIni(AttrsLoader_DictTextFile):
    """
    GOAL
    ----

    NOTE
    ----
    redefine only TARGET-kit/KEYPATH in __init
    """
    STYLE = Enum_DictTextFormat.INI
    FILEPATH = pathlib.Path.home().joinpath("pv.ini")

    # INIT -------
    TARGET: type[NestInit_AnnotsAttrByKwArgs] | Any
    KEYPATH: tuple[str | int, ...]


# ---------------------------------------------------------------------------------------------------------------------
class PvLoaderIni_AuthNamePwd(PvLoaderIni):
    TARGET = AttrKit_AuthNamePwd


class PvLoaderIni_AuthTgBot(PvLoaderIni):
    TARGET = AttrKit_AuthTgBot


class PvLoaderIni_AuthServer(PvLoaderIni):
    TARGET = AttrKit_AuthServer


# =====================================================================================================================
class PvLoaderJson(AttrsLoader_DictTextFile):
    STYLE = Enum_DictTextFormat.JSON
    FILEPATH = pathlib.Path.home().joinpath("pv.json")

    # INIT -------
    TARGET: type[NestInit_AnnotsAttrByKwArgs] | Any
    KEYPATH: tuple[str | int, ...]


# ---------------------------------------------------------------------------------------------------------------------
class PvLoaderJson_AuthNamePwd(PvLoaderJson):
    TARGET = AttrKit_AuthNamePwd


class PvLoaderJson_AuthTgBot(PvLoaderJson):
    TARGET = AttrKit_AuthTgBot


class PvLoaderJson_AuthServer(PvLoaderJson):
    TARGET = AttrKit_AuthServer


# =====================================================================================================================
def _explore():
    pass


# =====================================================================================================================
if __name__ == "__main__":
    _explore()


# =====================================================================================================================
