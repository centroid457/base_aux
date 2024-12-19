import pytest
import time
import pathlib

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
    victim = ResolveFilePath(name="name")
    assert victim.NAME == "name"
    assert victim.EXT == None
    assert victim.NAMEEXT == "name"
    assert victim.DIRPATH == CWD
    assert victim.FILEPATH == CWD.joinpath(victim.NAMEEXT)

def test__name_ext():
    victim = ResolveFilePath(name="name", ext="ext")
    assert victim.NAME == "name"
    assert victim.EXT == "ext"
    assert victim.NAMEEXT == "name.ext"
    assert victim.DIRPATH == CWD
    assert victim.FILEPATH == CWD.joinpath(victim.NAMEEXT)

def test__nameext():
    victim = ResolveFilePath(nameext="name.ext")
    assert victim.NAME == "name"
    assert victim.EXT == "ext"
    assert victim.NAMEEXT == "name.ext"
    assert victim.DIRPATH == CWD
    assert victim.FILEPATH == CWD.joinpath(victim.NAMEEXT)

    victim = ResolveFilePath(nameext="name")
    assert victim.NAME == "name"
    assert victim.EXT == None
    assert victim.NAMEEXT == "name"
    assert victim.DIRPATH == CWD
    assert victim.FILEPATH == CWD.joinpath(victim.NAMEEXT)

    victim = ResolveFilePath(nameext="name.")
    assert victim.NAME == "name"
    assert victim.EXT == ""
    assert victim.NAMEEXT == "name."
    assert victim.DIRPATH == CWD
    assert victim.FILEPATH == CWD.joinpath(victim.NAMEEXT)

    victim = ResolveFilePath(nameext=".ext")
    assert victim.NAME == ""
    assert victim.EXT == "ext"
    assert victim.NAMEEXT == ".ext"
    assert victim.DIRPATH == CWD
    assert victim.FILEPATH == CWD.joinpath(victim.NAMEEXT)

def test__ext():
    victim = ResolveFilePath(ext="ext")
    assert victim.NAME == None
    assert victim.EXT == "ext"
    assert victim.NAMEEXT == ".ext"
    assert victim.DIRPATH == CWD
    assert victim.FILEPATH == CWD.joinpath(victim.NAMEEXT)


def test__filepath():
    victim = ResolveFilePath(filepath=CWD.joinpath("name.ext"))
    assert victim.NAME == "name"
    assert victim.EXT == "ext"
    assert victim.NAMEEXT == "name.ext"
    assert victim.DIRPATH == CWD
    assert victim.FILEPATH == CWD.joinpath(victim.NAMEEXT)

    victim = ResolveFilePath(name="name2", filepath=CWD.joinpath("name.ext"))
    assert victim.NAME == "name2"
    assert victim.EXT == "ext"
    assert victim.NAMEEXT == "name2.ext"
    assert victim.DIRPATH == CWD
    assert victim.FILEPATH == CWD.joinpath("name2.ext")

    victim = ResolveFilePath(filepath=CWD.joinpath("path1", "name.ext"))
    assert victim.NAME == "name"
    assert victim.EXT == "ext"
    assert victim.NAMEEXT == "name.ext"
    assert victim.DIRPATH == CWD.joinpath("path1")
    assert victim.FILEPATH == CWD.joinpath("path1", victim.NAMEEXT)


# =====================================================================================================================
