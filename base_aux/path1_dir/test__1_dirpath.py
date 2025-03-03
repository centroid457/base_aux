from base_aux.path1_dir.m1_dirpath import *


# =====================================================================================================================
CWD = pathlib.Path().cwd()


# =====================================================================================================================
class Test_Dirpath:
    def test__cwd(self):
        assert Resolve_DirPath().resolve() == CWD

        assert Resolve_DirPath(None).resolve() == CWD

        assert Resolve_DirPath("").resolve() != CWD
        assert Resolve_DirPath("").resolve() == pathlib.Path(".")

        assert Resolve_DirPath("hello").resolve() == pathlib.Path("hello")


# =====================================================================================================================
