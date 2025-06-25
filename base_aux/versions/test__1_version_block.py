import pytest

from base_aux.lambdas.m1_lambda import *
from base_aux.versions.m2_version import *


# =====================================================================================================================
class Test__VersionBlock:
    @pytest.mark.parametrize(
        argnames="source, _EXPECTED",
        argvalues=[
            (True, ("true", ("true", ), "true", )),
            (1, ("1", (1, ), "1", )),

            ("1.2", ("1.2", (), "", )),
            ("1-2", ("1-2", (), "", )),
            ("1", ("1", (1, ), "1", )),
            ("hello", ("hello", ("hello", ), "hello", )),
            ("HELLO", ("hello", ("hello", ), "hello", )),
            ("11rc22", ("11rc22", (11, "rc", 22), "11rc22", )),
            ("11r c22", ("11r c22", (), "", )),
            (" 11 rc-2 2", ("11 rc-2 2", (), "", )),

            # zeros invaluable
            ("01rc02", ("01rc02", (1, "rc", 2), "1rc2", )),
            ("01rc020", ("01rc020", (1, "rc", 20), "1rc20", )),

            # not clean chars
            ("[11:rc.22]", ("[11:rc.22]", (), "", )),

            # iterables
            ([11, "r c---", 22], ("11r c---22", (), "", )),

            # inst
            (VersionBlock("11rc22"), ("11rc22", (11, "rc", 22), "11rc22", )),
        ]
    )
    def test__all(self, source, _EXPECTED):
        func_link = VersionBlock(source, _raise=False)._prepare_source
        Lambda(func_link).expect__check_assert(_EXPECTED[0])

        func_link = VersionBlock(source, _raise=False)._parse_elements
        Lambda(func_link).expect__check_assert(_EXPECTED[1])

        func_link = lambda: str(VersionBlock(source, _raise=False))
        Lambda(func_link).expect__check_assert(_EXPECTED[2])

    # INST ------------------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        argnames="args, _EXPECTED",
        argvalues=[
            ((None, ""), True),
            ((None, "0"), True),
            ((None, 0), True),
            ((None, None), True),
            (("", None), True),
            (("None", None), False),
            (("None", "None"), True),
            (("1rc2", None), False),

            (("1rc2", "1rc2"), True),

            # zeros invaluable
            (("01rc02", "1rc2"), True),
            (("01rc02", "1rc20"), False),

            # not clean chars
            (("1rc2", "[11:rc.22]"), False),
            (("", "[11:rc.22]"), True),

            # iterables
            (("1rc2", [1, "rc", 2]), True),
            (("1rc2", [1, "rc2", ]), True),
            (("1rc2", ["1rc2", ]), True),

            # inst
            (("1rc2", VersionBlock("1rc2")), True),
        ]
    )
    def test__cmp_eq(self, args, _EXPECTED):
        func_link = lambda source1, source2: VersionBlock(source1) == source2
        Lambda(func_link, *args).expect__check_assert(_EXPECTED)


# =====================================================================================================================
