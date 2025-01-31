from base_aux.files.m2_res_filepath import Resolve_FilePath
from tests.files.test__1_dirpath import CWD


# =====================================================================================================================
class Test_Filepath:
    def test__name(self):
        victim = Resolve_FilePath(name="name")
        assert victim.NAME == "name"
        assert victim.EXTLAST == ""
        assert victim.NAMEEXT == "name"
        assert victim.DIRPATH == CWD
        assert victim.FILEPATH == CWD.joinpath(victim.NAMEEXT)

    def test__nameext(self):
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

    def test__ext(self):
        victim = Resolve_FilePath(extlast="extlast")
        assert victim.NAME == ""
        assert victim.EXTLAST == "extlast"
        assert victim.NAMEEXT == ".extlast"
        assert victim.DIRPATH == CWD
        assert victim.FILEPATH == CWD.joinpath(victim.NAMEEXT)

    def test__extlast(self):
        victim = Resolve_FilePath(name="name", extlast="extlast")
        assert victim.NAME == "name"
        assert victim.EXTLAST == "extlast"
        assert victim.NAMEEXT == "name.extlast"
        assert victim.DIRPATH == CWD
        assert victim.FILEPATH == CWD.joinpath(victim.NAMEEXT)

    def test__filepath(self):
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
