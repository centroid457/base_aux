from base_aux.files.m2_res_filepath import *
from base_aux.files.m1_res_dirpath import Resolve_DirPath


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
