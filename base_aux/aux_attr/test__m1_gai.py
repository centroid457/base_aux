import pytest

from base_aux.aux_expect.m1_expect_aux import ExpectAux
from base_aux.aux_attr.m2_annot2_nest1_gsai_ic import *


# =====================================================================================================================
class Test__Attr:
    @classmethod
    def setup_class(cls):
        pass

        class Victim(NestGAI_AnnotAttrIC):
            attr_lowercase = "value"
            ATTR_UPPERCASE = "VALUE"
            Attr_CamelCase = "Value"
            # NOT_EXISTS

        cls.Victim = Victim

    @classmethod
    def teardown_class(cls):
        pass

    # -----------------------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        argnames="attr, _EXPECTED",
        argvalues=[
            (0, Exception),
            (1, Exception),
            (None, Exception),
            (True, Exception),
            ("", Exception),
            (" TRUE", Exception),
            ("NOT_EXISTS", Exception),

            ("__name__", Exception),

            ("attr_lowercase", "value"),
            ("ATTR_LOWERCASE", "value"),

            ("ATTR_UPPERCASE", "VALUE"),
            ("attr_uppercase", "VALUE"),

            ("     attr_uppercase", "VALUE"),
        ]
    )
    def test__get(self, attr, _EXPECTED):
        ExpectAux(lambda: getattr(self.Victim(), attr)).check_assert(_EXPECTED)
        ExpectAux(lambda: self.Victim()[attr]).check_assert(_EXPECTED)

    # @pytest.mark.parametrize(
    #     argnames="attr, _EXPECTED",
    #     argvalues=[
    #         (None, Exception),
    #         (True, Exception),
    #         ("", Exception),
    #         (" TRUE", Exception),
    #
    #         ("attr_lowercase", None),
    #         ("ATTR_LOWERCASE", None),
    #
    #         ("ATTR_UPPERCASE", None),
    #         ("attr_uppercase", None),
    #
    #         ("     attr_uppercase", None),
    #     ]
    # )
    # def test__set(self, attr, _EXPECTED):
    #     NEW_VALUE = "NEW_VALUE"
    #     victim = Victim()
    #     ExpectAux(lambda: setattr(victim, attr, NEW_VALUE)).check_assert(_EXPECTED)
    #     if _EXPECTED == Exception:
    #         return
    #     ExpectAux(lambda: getattr(victim, attr)).check_assert(NEW_VALUE)
    #     # ExpectAux(lambda: Victim()[attr] = NEW_VALUE).check_assert(_EXPECTED)


# =====================================================================================================================
class Test__Annot:
    @classmethod
    def setup_class(cls):
        pass

        class Victim(NestGAI_AnnotAttrIC):
            attr_lowercase: str = "value"
            ATTR_UPPERCASE = "VALUE"
            Attr_CamelCase = "Value"
            # NOT_EXISTS

        cls.Victim = Victim

    @classmethod
    def teardown_class(cls):
        pass

    # -----------------------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        argnames="attr, _EXPECTED",
        argvalues=[
            (0, "value"),
            (1, Exception),
            (None, Exception),
            (True, Exception),
            ("", Exception),
            (" TRUE", Exception),
            ("NOT_EXISTS", Exception),

            ("__name__", Exception),

            ("attr_lowercase", "value"),
            ("ATTR_LOWERCASE", "value"),

            ("ATTR_UPPERCASE", "VALUE"),
            ("attr_uppercase", "VALUE"),

            ("     attr_uppercase", "VALUE"),
        ]
    )
    def test__get(self, attr, _EXPECTED):
        # ExpectAux(lambda: getattr(self.Victim(), attr)).check_assert(_EXPECTED)
        ExpectAux(lambda: self.Victim()[attr]).check_assert(_EXPECTED)


# =====================================================================================================================
