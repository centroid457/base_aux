import pytest
import json

from base_aux.lambdas.m1_lambda import *
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

            ('{"1": "2025-04-29 18:23:19.599746", \n}', ({"1": "2025-04-29 18:23:19.599746"}, {"1": "2025-04-29 18:23:19.599746"}, {"1": "2025-04-29 18:23:19.599746"}),),
        ]
    )
    def test__json(self, source, _EXPECTED):
        # assert json.loads(str(source)) == _EXPECTED

        victim = TextAux(source)
        Lambda(victim.parse__json).expect__check_assert(_EXPECTED[0])
        Lambda(victim.parse__dict).expect__check_assert(_EXPECTED[1])
        Lambda(victim.parse__dict_auto).expect__check_assert(_EXPECTED[2])


# =====================================================================================================================
