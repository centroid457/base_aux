from typing import *
import pytest

from base_aux.aux_dict.m2_dict_ic import *


# =====================================================================================================================
def test__dict_ic():
    victim1 = DictIcKeys()
    victim1['NAme'] = 'VALUE'
    victim1[1] = 1

    victim2 = DictIcKeys(NAme='VALUE')
    victim2[1] = 1

    victim3 = DictIcKeys({"NAme": 'VALUE', 1: 1})

    for victim in [victim1, victim2, victim3, ]:
        assert len(victim) == 2

        assert list(victim) == ["NAme", 1]

        # EQ
        assert victim == {1: 1, "naME": 'VALUE'}
        assert victim == {"naME": 'VALUE', 1: 1}

        assert victim != {"naME": 'VALUE', 1: 11}
        assert victim != {"naME": 'VALUE', 11: 1}
        assert victim != {"naME": 'VALUE2', 1: 1}
        assert victim != {"naME2": 'VALUE', 1: 1}

        # CONTAIN
        assert 'naME' in victim
        assert 1 in victim
        assert 0 not in victim

        # ACCESS
        Lambda(lambda: victim[0]).expect__check_assert(Exception)   # keep original behaviour - maybe need switch to None???
        Lambda(lambda: victim.get(0)).expect__check_assert(None)

        assert victim[1] == 1
        assert victim.get(1) == 1
        assert victim['name'] == "VALUE"
        assert victim['NAME'] == "VALUE"
        assert victim.get('NAME') == "VALUE"

        # update
        len0 = len(victim)
        victim['name'] = 'VALUE2'
        assert len(victim) == len0
        assert victim['name'] == victim['NAME'] == "VALUE2"

        victim['NAME'] = 'VALUE3'
        assert len(victim) == len0
        assert victim['name'] == victim['NAME'] == "VALUE3"

        victim.update({'NaMe': 'VALUE4'})
        assert len(victim) == len0
        assert victim['name'] == victim['NAME'] == "VALUE4"

        assert list(victim) == ["NAme", 1]

        # del ------
        try:
            del victim['name222']
        except:
            assert True
        else:
            assert False

        del victim['name']
        assert list(victim) == [1, ]
        victim['NAme'] = 'VALUE'

        # pop ------
        try:
            victim.pop('name222')
        except:
            assert True
        else:
            assert False

        assert victim.pop('name') == "VALUE"
        assert list(victim) == [1, ]
        # victim['NAme'] = 'VALUE'


# =====================================================================================================================
