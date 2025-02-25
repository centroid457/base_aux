import pytest

from base_aux.aux_expect.m1_expect_aux import ExpectAux
from base_aux.versions.m2_version import *


# =====================================================================================================================
class Test__VersionBlock:
    @pytest.mark.parametrize(
        argnames="source, _EXPECTED",
        argvalues=[
            (True, (True, "true", ("true", ), "true", )),
            (1, (True, "1", (1, ), "1", )),

            ("1.2", (False, "1.2", (), "", )),
            ("1-2", (True, "12", (12, ), "12", )),
            ("1", (True, "1", (1, ), "1", )),
            ("hello", (True, "hello", ("hello", ), "hello", )),
            ("HELLO", (True, "hello", ("hello", ), "hello", )),
            ("11rc22", (True, "11rc22", (11, "rc", 22), "11rc22", )),
            ("11r c22", (True, "11rc22", (11, "rc", 22), "11rc22", )),
            (" 11 rc-2 2", (True, "11rc22", (11, "rc", 22), "11rc22", )),

            # zeros invaluable
            ("01rc02", (True, "01rc02", (1, "rc", 2), "1rc2", )),
            ("01rc020", (True, "01rc020", (1, "rc", 20), "1rc20", )),

            # not clean chars
            ("[11:rc.22]", (False, "[11:rc.22]", (), "", )),

            # iterables
            ([11, "r c---", 22], (True, "11rc22", (11, "rc", 22), "11rc22", )),

            # inst
            (VersionBlock("11rc22"), (True, "11rc22", (11, "rc", 22), "11rc22", )),
        ]
    )
    def test__1(self, source, _EXPECTED):
        func_link = VersionBlock(source, _raise=False)._validate
        ExpectAux(func_link).check_assert(_EXPECTED[0])

        func_link = VersionBlock(source, _raise=False)._prepare
        ExpectAux(func_link).check_assert(_EXPECTED[1])

        func_link = VersionBlock(source, _raise=False)._parse_elements
        ExpectAux(func_link).check_assert(_EXPECTED[2])

        func_link = lambda: str(VersionBlock(source, _raise=False))
        ExpectAux(func_link).check_assert(_EXPECTED[3])

    # INST ------------------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        argnames="args, _EXPECTED",
        argvalues=[
            (True, 1),
            (1, 1),

            ("1", 1),
            ("hello", 1),
            ("HELLO", 1),
            ("11rc22", 3),
            ("11r c22", 3),
            (" 11 rc-2 2", Exx__IncompatibleItem),

            # zeros invaluable
            ("01rc02", 3),

            # not clean chars
            ("[11:rc.22]", Exx__IncompatibleItem),

            # iterables
            (([11, "r c---", 22], ), 3),

            # inst
            (VersionBlock("11rc22"), 3),
        ]
    )
    def test__inst__len(self, args, _EXPECTED):
        func_link = lambda source: len(VersionBlock(source))
        ExpectAux(func_link, args).check_assert(_EXPECTED)

    @pytest.mark.parametrize(
        argnames="args, _EXPECTED",
        argvalues=[
            (("None", None), True),
            (("1rc2", None), False),

            (("1rc2", "1rc2"), True),

            # zeros invaluable
            (("01rc02", "1rc2"), True),
            (("01rc02", "1rc20"), False),

            # not clean chars
            (("1rc2", "[11:rc.22]"), Exx__IncompatibleItem),

            # iterables
            (("1rc2", [1, "rc", 2]), True),
            (("1rc2", [1, "rc2", ]), True),
            (("1rc2", ["1rc2", ]), True),

            # inst
            (("1rc2", VersionBlock("1rc2")), True),
        ]
    )
    def test__inst__cmp__eq(self, args, _EXPECTED):
        func_link = lambda source1, source2: VersionBlock(source1) == source2
        ExpectAux(func_link, args).check_assert(_EXPECTED)


# =====================================================================================================================
