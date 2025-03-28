import pytest

from base_aux.aux_expect.m1_expect_aux import *
from base_aux.path1_dir.m1_dirpath import *


# =====================================================================================================================
CWD = pathlib.Path().cwd()


# =====================================================================================================================
class Test_Dirpath:
    def test__resolve(self):
        assert Resolve_DirPath().resolve() == CWD
        assert Resolve_DirPath("").resolve() != CWD

    @pytest.mark.parametrize(
        argnames="source, _EXPECTED",
        argvalues=[
            # dirs ---------
            (None, CWD),
            ('', pathlib.Path(".")),
            ('.', pathlib.Path(".")),
            ('hello', pathlib.Path("hello")),

            # files --------
            (CWD.joinpath('fileNotExisted.txt'), CWD),
            (CWD.joinpath('txt'), CWD.joinpath('txt')),
            (CWD.joinpath('.txt'), CWD),
            (CWD.joinpath('fileNotExisted.'), CWD.joinpath('fileNotExisted.')),
            (CWD.joinpath('fileNotExisted.txt1'), CWD.joinpath('fileNotExisted.txt1')),
        ]
    )
    def test__1(self, source, _EXPECTED):
        func_link = Resolve_DirPath(source).resolve
        ExpectAux(func_link).check_assert(_EXPECTED)


# =====================================================================================================================
