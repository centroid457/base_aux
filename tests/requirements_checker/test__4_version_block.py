from typing import *
import pytest
from pytest import mark
from pytest_aux import *

from requirements_checker import *
from pytest_aux import *


# =====================================================================================================================
class Test__VersionBlock:
    Victim: Type[VersionBlock]
    @classmethod
    def setup_class(cls):
        pass
        cls.Victim = VersionBlock

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
            (True, True),
            (1, True),

            ("1", True),
            ("hello", True),
            ("HELLO", True),
            ("11rc22", True),
            ("11r c22", True),
            (" 11 rc-2 2", False),

            # zeros invaluable
            ("01rc02", True),

            # not clean chars
            ("[11:rc.22]", True),

            # iterables
            (([11, "r c---", 22], ), True),

            # inst
            (VersionBlock("11rc22"), True),
        ]
    )
    def test__validate_source(self, args, _EXPECTED):
        func_link = self.Victim._validate_source
        pytest_func_tester__no_kwargs(func_link, args, _EXPECTED)

    @pytest.mark.parametrize(
        argnames="args, _EXPECTED",
        argvalues=[
            (True, "true"),
            (1, "1"),

            ("1", "1"),
            ("hello", "hello"),
            ("HELLO", "hello"),
            ("11rc22", "11rc22"),
            ("11r c22", "11rc22"),
            (" 11 rc-2 2", "11rc22"),

            # zeros invaluable
            ("01rc02", "01rc02"),

            # not clean chars
            ("[11:rc.22]", "[11:rc.22]"),

            # iterables
            (([11, "r c---", 22], ), "11rc22"),

            # inst
            (VersionBlock("11rc22"), "11rc22"),
        ]
    )
    def test___prepare_string(self, args, _EXPECTED):
        func_link = self.Victim._prepare_string
        pytest_func_tester__no_kwargs(func_link, args, _EXPECTED)

    @pytest.mark.parametrize(
        argnames="args, _EXPECTED",
        argvalues=[
            (True, False),
            (1, False),

            ("1", True),
            ("hello", True),
            ("HELLO", False),
            ("11rc22", True),
            ("11r c22", False),
            (" 11 rc-2 2", False),

            # zeros invaluable
            ("01rc02", True),

            # not clean chars
            ("[11:rc.22]", False),

            # iterables
            (([11, "r c---", 22], ), False),

            # inst
            (VersionBlock("11rc22"), False),  # not useful
        ]
    )
    def test__validate_string(self, args, _EXPECTED):
        func_link = self.Victim._validate_string
        pytest_func_tester__no_kwargs(func_link, args, _EXPECTED)

    @pytest.mark.parametrize(
        argnames="args, _EXPECTED",
        argvalues=[

            # NOTE: THIS TESTS IS NOT USEFUL!!! many values is not accured in real parced string!!

            (True, ()),
            (1, ()),

            ("1", (1, )),
            ("hello", ("hello", )),
            ("HELLO", ()),
            ("11rc22", (11, "rc", 22)),
            ("11r c22", (11, "r", "c", 22)),    # not useful
            (" 11 rc-2 2", (11, "rc", 2, 2)),

            # zeros invaluable
            ("01rc02", (1, "rc", 2)),
            ("01rc020", (1, "rc", 20)),

            # not clean chars
            ("[11:rc.22]", (11, "rc", 22)),

            # iterables
            (([11, "r c---", 22], ), ()),

            # inst
            (VersionBlock("11rc22"), ()),   # not useful
        ]
    )
    def test__parce_elements(self, args, _EXPECTED):
        func_link = self.Victim._parse_elements
        pytest_func_tester__no_kwargs(func_link, args, _EXPECTED)

    # INST ------------------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        argnames="args, _EXPECTED",
        argvalues=[
            (True, "true"),
            (1, "1"),

            ("1", "1"),
            ("hello", "hello"),
            ("HELLO", "hello"),
            ("11rc22", "11rc22"),
            ("11r c22", "11rc22"),
            (" 11 rc-2 2", Exx_VersionIncompatibleBlock),

            # zeros invaluable
            ("01rc02", "1rc2"),

            # not clean chars
            ("[11:rc.22]", Exx_VersionIncompatibleBlock),

            # iterables
            (([11, "r c---", 22], ), "11rc22"),

            # inst
            (VersionBlock("11rc22"), "11rc22"),
        ]
    )
    def test__inst__string(self, args, _EXPECTED):
        func_link = lambda source: str(self.Victim(source))
        pytest_func_tester__no_kwargs(func_link, args, _EXPECTED)

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
            (" 11 rc-2 2", Exx_VersionIncompatibleBlock),

            # zeros invaluable
            ("01rc02", 3),

            # not clean chars
            ("[11:rc.22]", Exx_VersionIncompatibleBlock),

            # iterables
            (([11, "r c---", 22], ), 3),

            # inst
            (VersionBlock("11rc22"), 3),
        ]
    )
    def test__inst__len(self, args, _EXPECTED):
        func_link = lambda source: len(self.Victim(source))
        pytest_func_tester__no_kwargs(func_link, args, _EXPECTED)

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
            (("1rc2", "[11:rc.22]"), Exx_VersionIncompatibleBlock),

            # iterables
            (("1rc2", [1, "rc", 2]), True),
            (("1rc2", [1, "rc2", ]), True),
            (("1rc2", ["1rc2", ]), True),

            # inst
            (("1rc2", VersionBlock("1rc2")), True),
        ]
    )
    def test__inst__cmp__eq(self, args, _EXPECTED):
        func_link = lambda source1, source2: self.Victim(source1) == source2
        pytest_func_tester__no_kwargs(func_link, args, _EXPECTED)


# =====================================================================================================================
