import pytest

from base_aux.base_lambdas.m1_lambda import *
from base_aux.aux_text.m4_ini import ConfigParserMod
from base_aux.aux_text.m0_text_examples import *


# =====================================================================================================================
class Test__Ini:
    @pytest.mark.parametrize(
        argnames="source, _EXPECTED",
        argvalues=[
            (None, (None, None)),
            ("", (None, None)),
            ("1", Exception),
            (INI_EXAMPLES.INT_KEY__TEXT, (INI_EXAMPLES.INT_KEY__DICT_DIRECT, INI_EXAMPLES.INT_KEY__DICT_DIRECT)),
            (INI_EXAMPLES.NOT_MESHED__TEXT, (INI_EXAMPLES.NOT_MESHED__DICT_DIRECT, INI_EXAMPLES.NOT_MESHED__DICT_MERGED)),
            (INI_EXAMPLES.MESHED__TEXT, (INI_EXAMPLES.MESHED__DICT_DIRECT, INI_EXAMPLES.MESHED__DICT_MERGED)),
        ]
    )
    def test__to_dict(self, source, _EXPECTED):
        victim = ConfigParserMod()

        try:
            victim.read_string(source)
        except Exception as exc:
            Lambda(exc).check_expected__assert(_EXPECTED)
            return

        Lambda(victim.to_dict__direct).check_expected__assert(_EXPECTED[0])
        Lambda(victim.to_dict__merged).check_expected__assert(_EXPECTED[1])


def _explore():
    victim = ConfigParserMod()
    victim.set("DEFAULT", "n0", "000")
    victim.add_section("SEC1")
    victim.set("SEC1", "n1", "111")
    result = victim.to_dict__direct()
    print(victim.to_dict__merged())


# =====================================================================================================================
