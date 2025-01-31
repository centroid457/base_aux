from base_aux.files.m2_res_filepath import Resolve_FilePath
from tests.files.test__1_dirpath import CWD


# =====================================================================================================================
class Test_Filepath:
    def test__1_name(self):
        victim = Resolve_FilePath(name="name")
        assert victim.NAME == "name"
        assert victim.EXTLAST == ""
        assert victim.NAMEEXT == "name"
        assert victim.DIRPATH == CWD
        assert victim.FILEPATH == CWD.joinpath(victim.NAMEEXT)

        # filepath ----
        victim = Resolve_FilePath(name="name2", filepath=CWD.joinpath("name.extlast"))
        assert victim.NAME == "name2"
        assert victim.EXTLAST == "extlast"
        assert victim.NAMEEXT == "name2.extlast"
        assert victim.DIRPATH == CWD
        assert victim.FILEPATH == CWD.joinpath("name2.extlast")

    def test__2_extlast(self):
        victim = Resolve_FilePath(extlast="extlast")
        assert victim.NAME == ""
        assert victim.EXTLAST == "extlast"
        assert victim.NAMEEXT == ".extlast"
        assert victim.DIRPATH == CWD
        assert victim.FILEPATH == CWD.joinpath(victim.NAMEEXT)

        victim = Resolve_FilePath(name="name", extlast="extlast")
        assert victim.NAME == "name"
        assert victim.EXTLAST == "extlast"
        assert victim.NAMEEXT == "name.extlast"
        assert victim.DIRPATH == CWD
        assert victim.FILEPATH == CWD.joinpath(victim.NAMEEXT)

        # filepath ----
        victim = Resolve_FilePath(extlast="extlast2", filepath=CWD.joinpath("name.extlast"))
        assert victim.NAME == "name"
        assert victim.EXTLAST == "extlast2"
        assert victim.NAMEEXT == "name.extlast2"
        assert victim.DIRPATH == CWD
        assert victim.FILEPATH == CWD.joinpath("name.extlast2")

    def test__3_nameext(self):
        victim = Resolve_FilePath(nameext="name.extlast")
        assert victim.NAME == "name"
        assert victim.EXTLAST == "extlast"
        assert victim.NAMEEXT == "name.extlast"
        assert victim.DIRPATH == CWD
        assert victim.FILEPATH == CWD.joinpath(victim.NAMEEXT)

        victim = Resolve_FilePath(nameext="name")
        assert victim.NAME == "name"
        assert victim.EXTLAST == ""
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

        # filepath ----
        victim = Resolve_FilePath(nameext="name2.extlast2", filepath=CWD.joinpath("name.extlast"))
        assert victim.NAME == "name2"
        assert victim.EXTLAST == "extlast2"
        assert victim.NAMEEXT == "name2.extlast2"
        assert victim.DIRPATH == CWD
        assert victim.FILEPATH == CWD.joinpath("name2.extlast2")

    def test__4_dirpath(self):
        victim = Resolve_FilePath(dirpath=CWD.joinpath("path2"))
        assert victim.NAME == ""
        assert victim.EXTLAST == ""
        assert victim.NAMEEXT == ""
        assert victim.DIRPATH == CWD.joinpath("path2")
        assert victim.FILEPATH == CWD.joinpath("path2")

        victim = Resolve_FilePath(dirpath=CWD.joinpath("path2"), filepath=CWD.joinpath("path1", "name.extlast"))
        assert victim.NAME == "name"
        assert victim.EXTLAST == "extlast"
        assert victim.NAMEEXT == "name.extlast"
        assert victim.DIRPATH == CWD.joinpath("path2")
        assert victim.FILEPATH == CWD.joinpath("path2", "name.extlast")

    def test__5_filepath(self):
        victim = Resolve_FilePath(filepath=CWD.joinpath("name.extlast"))
        assert victim.NAME == "name"
        assert victim.EXTLAST == "extlast"
        assert victim.NAMEEXT == "name.extlast"
        assert victim.DIRPATH == CWD
        assert victim.FILEPATH == CWD.joinpath(victim.NAMEEXT)

        victim = Resolve_FilePath(filepath=CWD.joinpath("path1", "name.extlast"))
        assert victim.NAME == "name"
        assert victim.EXTLAST == "extlast"
        assert victim.NAMEEXT == "name.extlast"
        assert victim.DIRPATH == CWD.joinpath("path1")
        assert victim.FILEPATH == CWD.joinpath("path1", "name.extlast")

    def test__6_all(self):
        victim = Resolve_FilePath(name="name3", extlast="extlast3", nameext="name2.extlast2", dirpath=CWD.joinpath("path2"), filepath=CWD.joinpath("name.extlast"))
        assert victim.NAME == "name3"
        assert victim.EXTLAST == "extlast3"
        assert victim.NAMEEXT == "name3.extlast3"
        assert victim.DIRPATH == CWD.joinpath("path2")
        assert victim.FILEPATH == CWD.joinpath("path2", "name3.extlast3")


# =====================================================================================================================
