from base_aux.aux_attr.m4_kits import *
from base_aux.base_statics.m4_enums import DictTextFormat
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
    STYLE = DictTextFormat.INI
    FILEPATH = pathlib.Path.home().joinpath("pv.ini")

    # INIT -------
    TARGET: type[NestInit_AnnotsAttrByKwArgs] | Any
    KEYPATH: tuple[str | int, ...]


# ---------------------------------------------------------------------------------------------------------------------
class PvLoaderIni_NamePwd(PvLoaderIni):
    TARGET = AttrKit_NamePwd


class PvLoaderIni_AuthTgBot(PvLoaderIni):
    TARGET = AttrKit_AuthTgBot


# =====================================================================================================================
class PvLoaderJson(AttrsLoader_DictTextFile):
    STYLE = DictTextFormat.JSON
    FILEPATH = pathlib.Path.home().joinpath("pv.json")

    # INIT -------
    TARGET: type[NestInit_AnnotsAttrByKwArgs] | Any
    KEYPATH: tuple[str | int, ...]


# ---------------------------------------------------------------------------------------------------------------------
class PvLoaderJson_NamePwd(PvLoaderJson):
    TARGET = AttrKit_NamePwd


class PvLoaderJson_AuthTgBot(PvLoaderJson):
    TARGET = AttrKit_AuthTgBot


# =====================================================================================================================
def _explore():
    pass


# =====================================================================================================================
if __name__ == "__main__":
    _explore()


# =====================================================================================================================
