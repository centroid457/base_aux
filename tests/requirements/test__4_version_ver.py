from base_aux.versions.m1_version import *
from base_aux.aux_expect.m1_expect_aux import *


# =====================================================================================================================
class Test__Version:
    Victim: type[Version]
    @classmethod
    def setup_class(cls):
        pass
        cls.Victim = Version

    # @classmethod
    # def teardown_class(cls):
    #     if cls.victim:
    #         cls.victim.disconnect()
    #
    # def setup_method(self, method):
    #     pass
    #
    # def teardown_method(self, method):
    #     pass

    # -----------------------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        argnames="args, _EXPECTED",
        argvalues=[
            # ONE BLOCK ---------------------
            (True, ""),     # Exx__VersionIncompatible
            (1, "1"),

            ("1", "1"),
            ("hello", ""),  # Exx__VersionIncompatible
            ("HELLO", ""),     # Exx__VersionIncompatible
            ("11rc22", "11rc22"),
            ("11r c22", "11r c22"),
            (" 11 rc-2 2", "11 rc-2 2"),

            # zeros invaluable
            ("01rc02", "01rc02"),

            # not clean chars
            ("[11:rc.22]", "11:rc.22"),

            # iterables
            (([11, "r c---", 22], ), "11.r c---.22"),

            # inst
            (VersionBlock("11rc22"), "11rc22"),

            # BLOCKS ---------------------
            ("1.1rc2.2", "1.1rc2.2"),
            ("ver1.1rc2.2", "1.1rc2.2"),
            ("ver(1.1rc2.2)ver", "1.1rc2.2"),

            # BLOCKS inst ---------------------
            (([1, VersionBlock("11rc22")],), "1.11rc22"),
            (([1, "hello"], ), "1.hello"),
        ]
    )
    def test___prepare_string(self, args, _EXPECTED):
        func_link = self.Victim._prepare_string
        ExpectAux(func_link, args).check_assert(_EXPECTED)

    # INST ------------------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        argnames="args, _EXPECTED",
        argvalues=[
            # ONE BLOCK ---------------------
            (True, Exx__VersionIncompatible),
            (1, "1"),

            ("1", "1"),
            ("hello", Exx__VersionIncompatible),
            ("HELLO", Exx__VersionIncompatible),
            ("11rc22", "11rc22"),
            ("11r c22", "11rc22"),
            (" 11 rc-2 2", Exx__VersionIncompatibleBlock),

            # zeros invaluable
            ("01rc02", "1rc2"),

            # not clean chars
            ("[11:rc.22]", Exx__VersionIncompatibleBlock),

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
        func_link = lambda source: str(self.Victim(source))
        ExpectAux(func_link, args).check_assert(_EXPECTED)

    @pytest.mark.parametrize(
        argnames="args, _EXPECTED",
        argvalues=[
            (True, Exx__VersionIncompatible),
            (1, 1),

            ("1", 1),
            ("hello", Exx__VersionIncompatible),
            ("HELLO", Exx__VersionIncompatible),
            ("11rc22", 1),
            ("11r c22", 1),
            (" 11 rc-2 2", Exx__VersionIncompatibleBlock),

            # zeros invaluable
            ("01rc02", 1),

            # not clean chars
            ("[11:rc.22]", Exx__VersionIncompatibleBlock),

            # iterables
            (([11, "r c---", 22],), 3),

            # inst
            (VersionBlock("11rc22"), 1),
        ]
    )
    def test__inst__len(self, args, _EXPECTED):
        func_link = lambda source: len(self.Victim(source))
        ExpectAux(func_link, args).check_assert(_EXPECTED)

    @pytest.mark.parametrize(
        argnames="args, _EXPECTED",
        argvalues=[
            (("1rc2", "1rc2"), True),

            # zeros invaluable
            (("01rc02", "1rc2"), True),
            (("01rc02", "1rc20"), False),

            # not clean chars
            (("1rc2", "[11:rc.22]"), Exx__VersionIncompatibleBlock),

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
        func_link = lambda source1, source2: self.Victim(source1) == source2
        ExpectAux(func_link, args).check_assert(_EXPECTED)

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
