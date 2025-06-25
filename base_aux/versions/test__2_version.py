from base_aux.versions.m2_version import *
from base_aux.lambdas.m1_lambda import *
from base_aux.aux_values.m3_exceptions import *


# =====================================================================================================================
class Test__Version:
    # -----------------------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        argnames="source, _EXPECTED",
        argvalues=[
            # ONE BLOCK ---------------------
            (True, ["", (), "", False]),
            (None, ["", (), "", False]),
            ("True", ["", (), "", False]),
            ("HELLO", ["", (), "", False]),

            (0, ["0", (VersionBlock("0"), ), "0", False]),
            ("0", ["0", (VersionBlock("0"), ), "0", False]),

            (1, ["1", (VersionBlock("1"), ), "1", True]),
            ("1", ["1", (VersionBlock("1"), ), "1", True]),

            ("11rc22", ["11rc22", (VersionBlock("11rc22"), ), "11rc22", True]),
            ("11r c22", ["11r c22", (), "", False]),
            (" 11 rc-2 2", ["11 rc-2 2", (), "", False]),

            # zeros invaluable
            ("01rc02", ["01rc02", (VersionBlock("1rc2"), ), "1rc2", True]),

            # not clean chars
            ("[11:rc.22]", ["11:rc.22", (), "", False]),

            # iterables
            ([11, "r c---", 22], ["11.r c---.22", (), "", False]),

            # inst
            (VersionBlock("11rc22"), ["11rc22", (VersionBlock("11rc22"), ), "11rc22", True]),

            # # BLOCKS ---------------------
            ("1.1rc2.2", ["1.1rc2.2", (VersionBlock(1), VersionBlock("1rc2"), VersionBlock(2), ), "1.1rc2.2", True]),
            ("ver1.1rc2.2", ["1.1rc2.2", (VersionBlock(1), VersionBlock("1rc2"), VersionBlock(2), ), "1.1rc2.2", True]),
            ("ver(1.1rc2.2)ver", ["1.1rc2.2", (VersionBlock(1), VersionBlock("1rc2"), VersionBlock(2), ), "1.1rc2.2", True]),

            # # BLOCKS inst ---------------------
            ([1, VersionBlock("11rc22")], ["1.11rc22", (VersionBlock(1), VersionBlock("11rc22"), ), "1.11rc22", True]),
            ([1, "hello"], ["1.hello", (VersionBlock(1), VersionBlock("hello"), ), "1.hello", True]),
        ]
    )
    def test__all(self, source, _EXPECTED):
        inst = Version(source, _raise=False)

        func_link = inst._prepare_source
        Lambda(func_link).expect__check_assert(_EXPECTED[0])

        func_link = inst._parse_blocks
        Lambda(func_link).expect__check_assert(_EXPECTED[1])

        func_link = str(inst)
        Lambda(func_link).expect__check_assert(_EXPECTED[2])

        func_link = bool(inst)
        Lambda(func_link).expect__check_assert(_EXPECTED[3])

    # -----------------------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        argnames="args, _EXPECTED",
        argvalues=[
            (("1rc2", "1rc2"), True),

            # zeros invaluable
            (("01rc02", "1rc2"), True),
            (("01rc02", "1rc20"), False),

            # not clean chars
            (("1rc2", "[11:rc.22]"), Exx__Incompatible),

            # iterables
            (("1rc2", [1, "rc", 2]), False),
            (("1rc2", [1, "rc2", ]), False),
            (("1rc2", ["1rc2", ]), True),
            (("1.rc.2", [1, "rc", 2]), True),

            # inst
            (("1rc2", VersionBlock("1rc2")), True),
            (("1rc2", Version("1rc2")), True),
            (("11rc22", Version("11rc22")), True),
            (("1.1rc2.2", Version("1.1rc2.2")), True),
            (("1.1rc2.2", "01.01rc02.02"), True),
            (("1.1rc2.2", (1, "1rc2", 2)), True),

            (("1.1rc2.2", Version("1.1rc2.2finish")), False),
            (("1.1rc2.2", Version("1.1rc2.2finish", preparse=r"(.*)finish")), True),
        ]
    )
    def test__eq(self, args, _EXPECTED):
        func_link = lambda source1, source2: Version(source1) == source2
        Lambda(func_link, *args).expect__check_assert(_EXPECTED)

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
    def test__cmp(self, expression):
        Lambda(expression).expect__check_assert()

    # PARTS -----------------------------------------------------------------------------------------------------------
    def test__parts_mmm(self):
        assert Version("1.2rc2.3").MAJOR == 1

        assert Version("1.2rc2.3").MAJOR == 1
        assert Version("1.2rc2.3").MINOR == "2rc2"
        assert Version("1.2rc2.3").MICRO == 3

        assert Version("1.2rc2.").MICRO is None
        assert Version("1.2rc2.").MICRO is None


# =====================================================================================================================
