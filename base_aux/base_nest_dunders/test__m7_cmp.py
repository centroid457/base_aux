from base_aux.base_lambdas.m1_lambda import *
from base_aux.base_nest_dunders.m7_cmp import *


# =====================================================================================================================
class Victim(NestCmp_LGET):
    def __init__(self, val):
        self.VAL = val

    def __len__(self):
        try:
            return len(self.VAL)
        except:
            pass

        return int(self.VAL)

    def __cmp__(self, other):
        other = self.__class__(other)

        # equel ----------------------
        if len(self) == len(other):
            return 0

        # final ------------
        return int(len(self) > len(other)) or -1


# =====================================================================================================================
class Test__Cmp:
    # @classmethod
    # def setup_class(cls):
    #     pass
    #     cls.Victim = Victim
    # @classmethod
    # def teardown_class(cls):
    #     pass
    #
    # def setup_method(self, method):
    #     pass
    #
    # def teardown_method(self, method):
    #     pass

    # -----------------------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        argnames="expr",
        argvalues=[
            # INT ----------------
            Victim(1) == 1,
            Victim(1) != 11,

            Victim(1) < 2,
            Victim(1) <= 2,
            Victim(1) <= 1,

            Victim(1) > 0,
            Victim(1) >= 0,
            Victim(1) >= 1,

            # STR ----------------
            Victim("a") == "a",
            Victim("a") == "b",
            Victim("a") == 1,
            Victim("aa") > 1,
        ]
    )
    def test__inst__cmp__eq(self, expr):
        Lambda(expr).expect__check_assert()

    # -----------------------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        argnames="expr, _EXPECTED",
        argvalues=[
            (Victim(0).check_ltgt(1, 3), False),
            (Victim(1).check_ltgt(1, 3), False),
            (Victim(2).check_ltgt(1, 3), True),
            (Victim(3).check_ltgt(1, 3), False),
            (Victim(4).check_ltgt(1, 3), False),

            (Victim(0).check_ltge(1, 3), False),
            (Victim(1).check_ltge(1, 3), False),
            (Victim(2).check_ltge(1, 3), True),
            (Victim(3).check_ltge(1, 3), True),
            (Victim(4).check_ltge(1, 3), False),

            (Victim(0).check_legt(1, 3), False),
            (Victim(1).check_legt(1, 3), True),
            (Victim(2).check_legt(1, 3), True),
            (Victim(3).check_legt(1, 3), False),
            (Victim(4).check_legt(1, 3), False),

            (Victim(0).check_lege(1, 3), False),
            (Victim(1).check_lege(1, 3), True),
            (Victim(2).check_lege(1, 3), True),
            (Victim(3).check_lege(1, 3), True),
            (Victim(4).check_lege(1, 3), False),
        ]
    )
    def test__inst__cmp__lg(self, expr, _EXPECTED):
        Lambda(expr).expect__check_assert(_EXPECTED)


# =====================================================================================================================

