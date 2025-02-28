import pytest

from base_aux.aux_expect.m1_expect_aux import ExpectAux
from base_aux.aux_attr.m1_attr2_nest_gsai_anycase import *


# =====================================================================================================================
class Victim(NestGSAI_AnnotsAttrAnycase):
    attr_lowercase = "value"
    ATTR_UPPERCASE = "VALUE"
    Attr_CamelCase = "Value"
    # NOT_EXISTS


# =====================================================================================================================
class Test__Attr:
    @pytest.mark.parametrize(
        argnames="attr, _EXPECTED",
        argvalues=[
            (None, Exception),
            (True, Exception),
            ("", Exception),
            (" TRUE", Exception),
            ("NOT_EXISTS", Exception),

            ("attr_lowercase", "value"),
            ("ATTR_LOWERCASE", "value"),

            ("ATTR_UPPERCASE", "VALUE"),
            ("attr_uppercase", "VALUE"),

            ("     attr_uppercase", "VALUE"),
        ]
    )
    def test__get(self, attr, _EXPECTED):
        ExpectAux(lambda: getattr(Victim(), attr)).check_assert(_EXPECTED)
        ExpectAux(lambda: Victim()[attr]).check_assert(_EXPECTED)

    @pytest.mark.parametrize(
        argnames="attr, _EXPECTED",
        argvalues=[
            # (None, Exception),
            # (True, Exception),
            # ("", Exception),
            # (" TRUE", Exception),

            ("attr_lowercase", None),
            ("ATTR_LOWERCASE", None),

            ("ATTR_UPPERCASE", None),
            ("attr_uppercase", None),

            ("     attr_uppercase", None),
        ]
    )
    def test__set(self, attr, _EXPECTED):
        NEW_VALUE = "NEW_VALUE"
        victim = Victim()
        ExpectAux(lambda: setattr(victim, attr, NEW_VALUE)).check_assert(_EXPECTED)
        if _EXPECTED == Exception:
            return
        ExpectAux(lambda: getattr(victim, attr)).check_assert(NEW_VALUE)
        # ExpectAux(lambda: Victim()[attr] = NEW_VALUE).check_assert(_EXPECTED)


# =====================================================================================================================
