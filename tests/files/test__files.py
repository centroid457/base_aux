import pytest
import time
import pathlib

from base_aux.files.m0_filepath import *


# =====================================================================================================================
CWD = pathlib.Path().cwd()

# @pytest.mark.parametrize(
#     argnames="kwargs",
#     argvalues=[
#         Kwargs(name="name"),
#     ]
# )


def test__name():
    victim = Resolve_FilePath(name="name")
    assert victim.NAME == "name"
    assert victim.EXTLAST == None
    assert victim.NAMEEXT == "name"
    assert victim.DIRPATH == CWD
    assert victim.FILEPATH == CWD.joinpath(victim.NAMEEXT)


def test__nameext():
    victim = Resolve_FilePath(nameext="name.extlast")
    assert victim.NAME == "name"
    assert victim.EXTLAST == "extlast"
    assert victim.NAMEEXT == "name.extlast"
    assert victim.DIRPATH == CWD
    assert victim.FILEPATH == CWD.joinpath(victim.NAMEEXT)

    victim = Resolve_FilePath(nameext="name")
    assert victim.NAME == "name"
    assert victim.EXTLAST == None
    assert victim.NAMEEXT == "name"
    assert victim.DIRPATH == CWD
    assert victim.FILEPATH == CWD.joinpath(victim.NAMEEXT)

    victim = Resolve_FilePath(nameext="name.")
    assert victim.NAME == "name"
    assert victim.EXTLAST == ""
    assert victim.NAMEEXT == "name."
    assert victim.DIRPATH == CWD
    assert victim.FILEPATH == CWD.joinpath(victim.NAMEEXT)

    victim = Resolve_FilePath(nameext=".extlast")
    assert victim.NAME == ""
    assert victim.EXTLAST == "extlast"
    assert victim.NAMEEXT == ".extlast"
    assert victim.DIRPATH == CWD
    assert victim.FILEPATH == CWD.joinpath(victim.NAMEEXT)


def test__ext():
    victim = Resolve_FilePath(extlast="extlast")
    assert victim.NAME == None
    assert victim.EXTLAST == "extlast"
    assert victim.NAMEEXT == ".extlast"
    assert victim.DIRPATH == CWD
    assert victim.FILEPATH == CWD.joinpath(victim.NAMEEXT)


def test__extlast():
    victim = Resolve_FilePath(name="name", extlast="extlast")
    assert victim.NAME == "name"
    assert victim.EXTLAST == "extlast"
    assert victim.NAMEEXT == "name.extlast"
    assert victim.DIRPATH == CWD
    assert victim.FILEPATH == CWD.joinpath(victim.NAMEEXT)


def test__filepath():
    victim = Resolve_FilePath(filepath=CWD.joinpath("name.extlast"))
    assert victim.NAME == "name"
    assert victim.EXTLAST == "extlast"
    assert victim.NAMEEXT == "name.extlast"
    assert victim.DIRPATH == CWD
    assert victim.FILEPATH == CWD.joinpath(victim.NAMEEXT)

    victim = Resolve_FilePath(name="name2", filepath=CWD.joinpath("name.extlast"))
    assert victim.NAME == "name2"
    assert victim.EXTLAST == "extlast"
    assert victim.NAMEEXT == "name2.extlast"
    assert victim.DIRPATH == CWD
    assert victim.FILEPATH == CWD.joinpath("name2.extlast")

    victim = Resolve_FilePath(filepath=CWD.joinpath("path1", "name.extlast"))
    assert victim.NAME == "name"
    assert victim.EXTLAST == "extlast"
    assert victim.NAMEEXT == "name.extlast"
    assert victim.DIRPATH == CWD.joinpath("path1")
    assert victim.FILEPATH == CWD.joinpath("path1", victim.NAMEEXT)


# =====================================================================================================================
