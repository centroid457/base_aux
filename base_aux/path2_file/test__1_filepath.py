import pathlib
from base_aux.path2_file.m1_filepath import *


# =====================================================================================================================
CWD = pathlib.Path().cwd()


# =====================================================================================================================
class Test_Filepath:
    def test__1_name1_single(self):
        victim = Resolve_FilePath(name="name")
        assert victim.name_PREFIX == ""
        assert victim.name_SUFFIX == ""
        assert victim.NAME == "name"
        assert victim.EXTLAST == ""
        assert victim.NAMEFULL == "name"
        assert victim.DIRPATH == CWD
        assert victim.FILEPATH == CWD.joinpath(victim.NAMEFULL)

        # filepath ----
        victim = Resolve_FilePath(name="name2", filepath=CWD.joinpath("name.extlast"))
        assert victim.NAME == "name2"
        assert victim.EXTLAST == "extlast"
        assert victim.NAMEFULL == "name2.extlast"
        assert victim.DIRPATH == CWD
        assert victim.FILEPATH == CWD.joinpath("name2.extlast")

    def test__1_name2_several(self):
        victim = Resolve_FilePath(name="name1.name2", extlast="extlast")
        assert victim.NAME == "name1.name2"
        assert victim.EXTLAST == "extlast"
        assert victim.NAMEFULL == "name1.name2.extlast"
        assert victim.DIRPATH == CWD
        assert victim.FILEPATH == CWD.joinpath(victim.NAMEFULL)

        # dots -----
        victim = Resolve_FilePath(name="name1.name2..", extlast="extlast")
        assert victim.NAME == "name1.name2.."
        assert victim.EXTLAST == "extlast"
        assert victim.NAMEFULL == "name1.name2...extlast"
        assert victim.DIRPATH == CWD
        assert victim.FILEPATH == CWD.joinpath(victim.NAMEFULL)

        # dots -----
        victim = Resolve_FilePath(namefull="name1.name2...extlast", )
        assert victim.NAME == "name1.name2.."
        assert victim.EXTLAST == "extlast"
        assert victim.NAMEFULL == "name1.name2...extlast"
        assert victim.DIRPATH == CWD
        assert victim.FILEPATH == CWD.joinpath(victim.NAMEFULL)

    def test__2_extlast(self):
        victim = Resolve_FilePath(extlast="extlast")
        assert victim.NAME == ""
        assert victim.EXTLAST == "extlast"
        assert victim.NAMEFULL == ".extlast"
        assert victim.DIRPATH == CWD
        assert victim.FILEPATH == CWD.joinpath(victim.NAMEFULL)

        victim = Resolve_FilePath(name="name", extlast="extlast")
        assert victim.NAME == "name"
        assert victim.EXTLAST == "extlast"
        assert victim.NAMEFULL == "name.extlast"
        assert victim.DIRPATH == CWD
        assert victim.FILEPATH == CWD.joinpath(victim.NAMEFULL)

        # filepath ----
        victim = Resolve_FilePath(extlast="extlast2", filepath=CWD.joinpath("name.extlast"))
        assert victim.NAME == "name"
        assert victim.EXTLAST == "extlast2"
        assert victim.NAMEFULL == "name.extlast2"
        assert victim.DIRPATH == CWD
        assert victim.FILEPATH == CWD.joinpath("name.extlast2")

    def test__3_nameext(self):
        victim = Resolve_FilePath(namefull="name.extlast")
        assert victim.NAME == "name"
        assert victim.EXTLAST == "extlast"
        assert victim.NAMEFULL == "name.extlast"
        assert victim.DIRPATH == CWD
        assert victim.FILEPATH == CWD.joinpath(victim.NAMEFULL)

        victim = Resolve_FilePath(namefull="name")
        assert victim.NAME == "name"
        assert victim.EXTLAST == ""
        assert victim.NAMEFULL == "name"
        assert victim.DIRPATH == CWD
        assert victim.FILEPATH == CWD.joinpath(victim.NAMEFULL)

        victim = Resolve_FilePath(namefull="name.")
        assert victim.NAME == "name"
        assert victim.EXTLAST == ""
        assert victim.NAMEFULL == "name."
        assert victim.DIRPATH == CWD
        assert victim.FILEPATH == CWD.joinpath(victim.NAMEFULL)

        victim = Resolve_FilePath(namefull=".extlast")
        assert victim.NAME == ""
        assert victim.EXTLAST == "extlast"
        assert victim.NAMEFULL == ".extlast"
        assert victim.DIRPATH == CWD
        assert victim.FILEPATH == CWD.joinpath(victim.NAMEFULL)

        # filepath ----
        victim = Resolve_FilePath(namefull="name2.extlast2", filepath=CWD.joinpath("name.extlast"))
        assert victim.NAME == "name2"
        assert victim.EXTLAST == "extlast2"
        assert victim.NAMEFULL == "name2.extlast2"
        assert victim.DIRPATH == CWD
        assert victim.FILEPATH == CWD.joinpath("name2.extlast2")

    def test__4_dirpath(self):
        victim = Resolve_FilePath(dirpath=CWD.joinpath("path2"))
        assert victim.NAME == ""
        assert victim.EXTLAST == ""
        assert victim.NAMEFULL == ""
        assert victim.DIRPATH == CWD.joinpath("path2")
        assert victim.FILEPATH == CWD.joinpath("path2")

        victim = Resolve_FilePath(dirpath=CWD.joinpath("path2"), filepath=CWD.joinpath("path1", "name.extlast"))
        assert victim.NAME == "name"
        assert victim.EXTLAST == "extlast"
        assert victim.NAMEFULL == "name.extlast"
        assert victim.DIRPATH == CWD.joinpath("path2")
        assert victim.FILEPATH == CWD.joinpath("path2", "name.extlast")

    def test__5_filepath(self):
        victim = Resolve_FilePath(filepath=CWD.joinpath("name.extlast"))
        assert victim.NAME == "name"
        assert victim.EXTLAST == "extlast"
        assert victim.NAMEFULL == "name.extlast"
        assert victim.DIRPATH == CWD
        assert victim.FILEPATH == CWD.joinpath(victim.NAMEFULL)

        victim = Resolve_FilePath(filepath=CWD.joinpath("path1", "name.extlast"))
        assert victim.NAME == "name"
        assert victim.EXTLAST == "extlast"
        assert victim.NAMEFULL == "name.extlast"
        assert victim.DIRPATH == CWD.joinpath("path1")
        assert victim.FILEPATH == CWD.joinpath("path1", "name.extlast")

    def test__6_all(self):
        victim = Resolve_FilePath(
            prefix="prefix",
            suffix="suffix",
            name="name3",
            extlast="extlast3",
            namefull="name2.extlast2",
            dirpath=CWD.joinpath("path2"),
            filepath=CWD.joinpath("name.extlast")
        )
        assert victim.name_PREFIX == "prefix"
        assert victim.name_SUFFIX == "suffix"

        assert victim.NAME == "name3"
        assert victim.EXTLAST == "extlast3"
        assert victim.NAMEFULL == "prefixname3suffix.extlast3"
        assert victim.DIRPATH == CWD.joinpath("path2")
        assert victim.FILEPATH == CWD.joinpath("path2", "prefixname3suffix.extlast3")


# =====================================================================================================================
