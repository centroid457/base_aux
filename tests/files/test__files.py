import pytest
import time
import pathlib

from base_aux.base_argskwargs import *
from base_aux.classes.lambdas import *
from base_aux.funcs import *
from base_aux.objects.primitives import *
from base_aux.files import *


# =====================================================================================================================
CWD = pathlib.Path().cwd()

# @pytest.mark.parametrize(
#     argnames="kwargs",
#     argvalues=[
#         Kwargs(name="name"),
#     ]
# )

def test__name():
    victim = FilePath(name="name")
    assert victim.NAME == "name"
    assert victim.EXT == None
    assert victim.NAMEEXT == "name"
    assert victim.DIRPATH == CWD
    assert victim.FILEPATH == CWD.joinpath(victim.NAMEEXT)

def test__name_ext():
    victim = FilePath(name="name", ext="ext")
    assert victim.NAME == "name"
    assert victim.EXT == "ext"
    assert victim.NAMEEXT == "name.ext"
    assert victim.DIRPATH == CWD
    assert victim.FILEPATH == CWD.joinpath(victim.NAMEEXT)

def test__nameext():
    victim = FilePath(nameext="name.ext")
    assert victim.NAME == "name"
    assert victim.EXT == "ext"
    assert victim.NAMEEXT == "name.ext"
    assert victim.DIRPATH == CWD
    assert victim.FILEPATH == CWD.joinpath(victim.NAMEEXT)

    victim = FilePath(nameext="name")
    assert victim.NAME == "name"
    assert victim.EXT == None
    assert victim.NAMEEXT == "name"
    assert victim.DIRPATH == CWD
    assert victim.FILEPATH == CWD.joinpath(victim.NAMEEXT)

    victim = FilePath(nameext="name.")
    assert victim.NAME == "name"
    assert victim.EXT == ""
    assert victim.NAMEEXT == "name."
    assert victim.DIRPATH == CWD
    assert victim.FILEPATH == CWD.joinpath(victim.NAMEEXT)

    victim = FilePath(nameext=".ext")
    assert victim.NAME == ""
    assert victim.EXT == "ext"
    assert victim.NAMEEXT == ".ext"
    assert victim.DIRPATH == CWD
    assert victim.FILEPATH == CWD.joinpath(victim.NAMEEXT)

def test__ext():
    victim = FilePath(ext="ext")
    assert victim.NAME == None
    assert victim.EXT == "ext"
    assert victim.NAMEEXT == ".ext"
    assert victim.DIRPATH == CWD
    assert victim.FILEPATH == CWD.joinpath(victim.NAMEEXT)


def test__filepath():
    victim = FilePath(filepath=CWD.joinpath("name.ext"))
    assert victim.NAME == "name"
    assert victim.EXT == "ext"
    assert victim.NAMEEXT == "name.ext"
    assert victim.DIRPATH == CWD
    assert victim.FILEPATH == CWD.joinpath(victim.NAMEEXT)

    victim = FilePath(name="name2", filepath=CWD.joinpath("name.ext"))
    assert victim.NAME == "name2"
    assert victim.EXT == "ext"
    assert victim.NAMEEXT == "name2.ext"
    assert victim.DIRPATH == CWD
    assert victim.FILEPATH == CWD.joinpath("name2.ext")

    victim = FilePath(filepath=CWD.joinpath("path1", "name.ext"))
    assert victim.NAME == "name"
    assert victim.EXT == "ext"
    assert victim.NAMEEXT == "name.ext"
    assert victim.DIRPATH == CWD.joinpath("path1")
    assert victim.FILEPATH == CWD.joinpath("path1", victim.NAMEEXT)


# =====================================================================================================================
