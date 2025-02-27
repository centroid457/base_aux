import pytest

from base_aux.aux_expect.m1_expect_aux import ExpectAux
from base_aux.aux_text.m4_ini import ConfigParserMod


# =====================================================================================================================
NOT_MESHED__TEXT = """
a0=00
[S1]
a1=11
"""
NOT_MESHED__DICT_DIRECT = {
    "a0": "00",
    "DEFAULT": {
        "a0": "00",
    },
    "S1": {
        "a1": "11",
    },
}
NOT_MESHED__DICT_MERGED = {
    "a0": "00",
    "DEFAULT": {
        "a0": "00",
    },
    "S1": {
        "a0": "00",
        "a1": "11",
    },
}


MESHED__TEXT = """
a0=00
[S1]
a0=11
a1=11
"""
MESHED__DICT_DIRECT = MESHED__DICT_MERGED = {
    "a0": "00",
    "DEFAULT": {
        "a0": "00",
    },
    "S1": {
        "a0": "11",
        "a1": "11",
    },
}


# =====================================================================================================================
class Test__Ini:
    @pytest.mark.parametrize(
        argnames="source, _EXPECTED",
        argvalues=[
            (NOT_MESHED__TEXT, (NOT_MESHED__DICT_DIRECT, NOT_MESHED__DICT_MERGED)),
            (MESHED__TEXT, (MESHED__DICT_DIRECT, MESHED__DICT_MERGED)),
        ]
    )
    def test__to_dict(self, source, _EXPECTED):
        obj = ConfigParserMod()
        obj.read_string(source)

        ExpectAux(obj.to_dict__direct).check_assert(_EXPECTED[0])
        ExpectAux(obj.to_dict__merged).check_assert(_EXPECTED[1])


def _explore():
    config = ConfigParserMod()
    config.set("DEFAULT", "n0", "000")
    config.add_section("SEC1")
    config.set("SEC1", "n1", "111")
    result = config.to_dict__direct()
    print(config.to_dict__merged())


# =====================================================================================================================
