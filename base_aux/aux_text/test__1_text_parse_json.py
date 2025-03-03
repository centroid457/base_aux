import pytest
import json

from base_aux.aux_expect.m1_expect_aux import ExpectAux
from base_aux.aux_text.m4_ini import ConfigParserMod
from base_aux.aux_text.m0_text_examples import *
from base_aux.aux_text.m1_text_aux import *


# =====================================================================================================================
class Test__Json:
    @pytest.mark.parametrize(
        argnames="source, _EXPECTED",
        argvalues=[
            (None, (None, None, None), ),
            ("None", (None, None, None), ),
            ("hello", (NoValue, None, None), ),
            ("null", (None, None, None), ),
            ("1", (1, None, None), ),
            ('{"1": 1}', ({"1": 1}, {"1": 1}, {"1": 1}), ),
            ('{"1": 1,}', ({"1": 1}, {"1": 1}, {"1": 1}), ),
            ('{"1": 1, }', ({"1": 1}, {"1": 1}, {"1": 1}), ),
            ('{"1": 1, \n}', ({"1": 1}, {"1": 1}, {"1": 1}), ),

            ('{"1": 1, /*cmt*/\n}', ({"1": 1}, {"1": 1}, {"1": 1}), ),

            ('''
            {
            "1": 1, /*cmt*/ 
            /* cm t */ 
            /* cm 
            t */ 
            "2": 2,
            }
            ''',
             ({"1": 1, "2": 2}, {"1": 1, "2": 2}, {"1": 1, "2": 2}), ),
        ]
    )
    def test__json(self, source, _EXPECTED):
        # assert json.loads(str(source)) == _EXPECTED

        victim = TextAux(source)
        ExpectAux(victim.parse__json).check_assert(_EXPECTED[0])
        ExpectAux(victim.parse__dict).check_assert(_EXPECTED[1])
        ExpectAux(victim.parse__dict_auto).check_assert(_EXPECTED[2])


# =====================================================================================================================
