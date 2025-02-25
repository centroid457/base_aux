from base_aux.versions.m2_version import *
from base_aux.aux_expect.m1_expect_aux import *


# =====================================================================================================================
class Test__Version:
    # -----------------------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        argnames="source, _EXPECTED",
        argvalues=[
            # ONE BLOCK ---------------------
            (True, ["", ()]),
            (None, ["", ()]),
            (0, ["0", (VersionBlock("0"), )]),
            (1, ["1", (VersionBlock("1"), )]),

            ("1", ["1", (VersionBlock("1"), )]),
            ("hello", ["", ()]),
            ("HELLO", ["", ()]),
            ("11rc22", ["11rc22", (VersionBlock("11rc22"), )]),
            ("11r c22", ["11r c22", (VersionBlock("11rc22"),)]),
            (" 11 rc-2 2", ["11 rc-2 2", Exx__IncompatibleItem]),

            # zeros invaluable
            ("01rc02", ["01rc02", (VersionBlock("01rc02"),)]),

            # not clean chars
            ("[11:rc.22]", ["11:rc.22", Exx__IncompatibleItem]),

            # iterables
            (([11, "r c---", 22], ), ["11.r c---.22", (VersionBlock(11), VersionBlock("rc"), VersionBlock(22), )]),

            # inst
            (VersionBlock("11rc22"), ["11rc22", (VersionBlock("11rc22"), )]),

            # # BLOCKS ---------------------
            ("1.1rc2.2", ["1.1rc2.2", (VersionBlock(1), VersionBlock("1rc2"), VersionBlock(2), )]),
            ("ver1.1rc2.2", ["1.1rc2.2", (VersionBlock(1), VersionBlock("1rc2"), VersionBlock(2), )]),
            ("ver(1.1rc2.2)ver", ["1.1rc2.2", (VersionBlock(1), VersionBlock("1rc2"), VersionBlock(2), )]),

            # # BLOCKS inst ---------------------
            (([1, VersionBlock("11rc22")],), ["1.11rc22", (VersionBlock(1), VersionBlock("11rc22"), )]),
            (([1, "hello"], ), ["1.hello", (VersionBlock(1), VersionBlock("hello"), )]),
        ]
    )
    def test___prepare_string(self, source, _EXPECTED):
        func_link = lambda: Version(source)._prepare_string()
        ExpectAux(func_link).check_assert(_EXPECTED[0])

        prep = func_link()
        func_link = lambda: Version(prep)._parse_blocks()
        ExpectAux(func_link).check_assert(_EXPECTED[1])

    # INST ------------------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        argnames="args, _EXPECTED",
        argvalues=[
            # ONE BLOCK ---------------------
            (True, Exx__Incompatible),
            (1, "1"),

            ("1", "1"),
            ("hello", Exx__Incompatible),
            ("HELLO", Exx__Incompatible),
            ("11rc22", "11rc22"),
            ("11r c22", "11rc22"),
            (" 11 rc-2 2", Exx__IncompatibleItem),

            # zeros invaluable
            ("01rc02", "1rc2"),

            # not clean chars
            ("[11:rc.22]", Exx__IncompatibleItem),

            # iterables
            (([11, "r c---", 22], ), "11.rc.22"),

            # inst
            (VersionBlock("11rc22"), "11rc22"),

            # BLOCKS ---------------------
            ("1.1rc2.2", "1.1rc2.2"),
            ("ver1.1rc2.2", "1.1rc2.2"),
            ("ver(1.1rc2.2)ver", "1.1rc2.2"),

            # BLOCKS inst ---------------------
            (([1, VersionBlock("11rc22")],), "1.11rc22"),
            (([1, "hello"],), "1.hello"),
        ]
    )
    def test__inst__string(self, args, _EXPECTED):
        func_link = lambda source: str(Version(source))
        ExpectAux(func_link, args).check_assert(_EXPECTED)

    @pytest.mark.parametrize(
        argnames="args, _EXPECTED",
        argvalues=[
            (True, Exx__Incompatible),
            (1, 1),

            ("1", 1),
            ("hello", Exx__Incompatible),
            ("HELLO", Exx__Incompatible),
            ("11rc22", 1),
            ("11r c22", 1),
            (" 11 rc-2 2", Exx__IncompatibleItem),

            # zeros invaluable
            ("01rc02", 1),

            # not clean chars
            ("[11:rc.22]", Exx__IncompatibleItem),

            # iterables
            (([11, "r c---", 22],), 3),

            # inst
            (VersionBlock("11rc22"), 1),
        ]
    )
    def test__inst__len(self, args, _EXPECTED):
        func_link = lambda source: len(Version(source))
        ExpectAux(func_link, args).check_assert(_EXPECTED)

    @pytest.mark.parametrize(
        argnames="args, _EXPECTED",
        argvalues=[
            (("1rc2", "1rc2"), True),

            # zeros invaluable
            (("01rc02", "1rc2"), True),
            (("01rc02", "1rc20"), False),

            # not clean chars
            (("1rc2", "[11:rc.22]"), Exx__IncompatibleItem),

            # iterables
            (("1rc2", [1, "rc", 2]), False),
            (("1rc2", [1, "rc2", ]), False),
            (("1rc2", ["1rc2", ]), True),

            # inst
            (("1rc2", VersionBlock("1rc2")), True),
            (("1rc2", Version("1rc2")), True),
            (("11rc22", Version("11rc22")), True),
            (("1.1rc2.2", Version("1.1rc2.2")), True),
            (("1.1rc2.2", "01.01rc02.02"), True),
            (("1.1rc2.2", (1, "1rc2", 2)), True),
        ]
    )
    def test__inst__cmp__eq(self, args, _EXPECTED):
        func_link = lambda source1, source2: Version(source1) == source2
        ExpectAux(func_link, args).check_assert(_EXPECTED)

    @pytest.mark.parametrize(
        argnames="source, _EXPECTED",
        argvalues=[
            (True, False),
            (1, True),

            ("1", True),
            ("hello", False),
            ("HELLO", False),
            ("11rc22", True),
            ("11r c22", True),
            (" 11 rc-2 2", False),

            # zeros invaluable
            ("01rc02", True),

            # not clean chars
            ("[11:rc.22]", False),

            # iterables
            (([11, "r c---", 22],), True),

            # inst
            (VersionBlock("11rc22"), True),
        ]
    )
    def test__bool(self, source, _EXPECTED):
        func_link = lambda x: bool(Version(x, _raise=False))
        ExpectAux(func_link, source).check_assert(_EXPECTED)

    @pytest.mark.parametrize(
        argnames="expression",
        argvalues=[
            Version("1rc2") == "1rc2",
            Version("1rc2") != "1rc1",

            Version("1.1rc2") > "1.0rc1",
            Version("1.1rc2") > "1.1rc0",
            Version("1.1rc2.0") > "1.1rc2",

            Version("01.01rc02") > "1.1rc1",
            Version("01.01rc02") < "1.1rd1",

            Version("hello", _raise=False) < "1.1rd1",
            Version("hello", _raise=False) == 0,
            Version("hello", _raise=False) == "",
        ]
    )
    def test__inst__cmp(self, expression):
        ExpectAux(expression).check_assert()

    # PARTS -----------------------------------------------------------------------------------------------------------
    def test__parts(self):
        assert Version("1.2rc2.3").major == 1

        assert Version("1.2rc2.3").major == 1
        assert Version("1.2rc2.3").minor == "2rc2"
        assert Version("1.2rc2.3").micro == 3

        assert Version("1.2rc2.").micro is None
        assert Version("1.2rc2.").micro is None


# =====================================================================================================================
