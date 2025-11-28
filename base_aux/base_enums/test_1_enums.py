from base_aux.base_lambdas.m1_lambda import *

from base_aux.base_enums.m2_enum1_adj import *
from base_aux.base_values.m2_value_special import NoValue


# =====================================================================================================================
class VictimStd(Enum):
    NONE = None
    A1 = 1
    TUPLE = (1, 2)
    STR_LOWER = "str_lower"
    STR_UPPER = "STR_UPPER"


class VictimEq(NestEq_EnumAdj):
    NONE = None
    A1 = 1
    TUPLE = (1, 2)
    STR_LOWER = "str_lower"
    STR_UPPER = "STR_UPPER"


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="source, _EXPECTED",
    argvalues=[
        (None, None),
        (1, 1),
        ((1, 2), (1, 2)),
        ((1, 22), NoValue),
        ("str_lower", "str_lower"),
        ("STR_LOWER", "str_lower"),
    ]
)
def test___value__get_original(source, _EXPECTED):
    Lambda(VictimEq._value__get_original, source).expect__check_assert(_EXPECTED)

# ---------------------------------------------------------------------------------------------------------------------
@pytest.mark.parametrize(
    argnames="source, _EXPECTED",
    argvalues=[
        (None, VictimEq.NONE),
        (1, VictimEq.A1),
        ((1, 2), VictimEq.TUPLE),
        ((1, 22), Exception),
        ("str_lower", VictimEq.STR_LOWER),
        # ("STR_LOWER", VictimEq.STR_LOWER),    # FIXME: CANT CREATE!
    ]
)
def test__init(source, _EXPECTED):
    Lambda(VictimEq, source).expect__check_assert(_EXPECTED)


# =====================================================================================================================
class Test_EnumStd:
    @pytest.mark.parametrize(
        argnames="source, other, _EXPECTED",
        argvalues=[
            # NONE --------
            (VictimStd, None, (False, True)),
            (VictimStd, VictimStd(None), (False, True)),
            (VictimStd, VictimStd.NONE, (False, True)),

            (VictimStd(None), None, (False, Exception)),
            (VictimStd(None), VictimStd.NONE, (True, Exception)),

            (VictimStd.NONE, None, (False, Exception)),
            (VictimStd.NONE, VictimStd(None), (True, Exception)),

            # 1 --------
            (VictimStd, 1, (False, True)),
            (VictimStd, VictimStd(1), (False, True)),
            (VictimStd, VictimStd.A1, (False, True)),

            (VictimStd(1), 1, (False, Exception)),
            (VictimStd(1), VictimStd.A1, (True, Exception)),

            (VictimStd.A1, 1, (False, Exception)),
            (VictimStd.A1, VictimStd(1), (True, Exception)),

            # DIFF --------
            (VictimStd.A1, VictimStd.NONE, (False, Exception)),
        ]
    )
    def test__eq_in(self, source, other, _EXPECTED):
        Lambda(source == other).expect__check_assert(_EXPECTED[0])

        func_link = lambda x: x in source
        Lambda(func_link, other).expect__check_assert(_EXPECTED[1])


# =====================================================================================================================
class Test_EnumEq:
    @pytest.mark.parametrize(
        argnames="source, other, _EXPECTED",
        argvalues=[
            # NONE --------
            (VictimEq, None, (False, True)),
            (VictimEq, VictimEq(None), (False, True)),
            (VictimEq, VictimEq.NONE, (False, True)),

            (VictimEq(None), None, (True, Exception)),
            (VictimEq(None), VictimEq.NONE, (True, Exception)),

            (VictimEq.NONE, None, (True, Exception)),
            (VictimEq.NONE, VictimEq(None), (True, Exception)),

            # 1 --------
            (VictimEq, 1, (False, True)),
            (VictimEq, VictimEq(1), (False, True)),
            (VictimEq, VictimEq.A1, (False, True)),

            (VictimEq(1), 1, (True, Exception)),
            (VictimEq(1), VictimEq.A1, (True, Exception)),

            (VictimEq.A1, 1, (True, Exception)),
            (VictimEq.A1, VictimEq(1), (True, Exception)),

            # TUPLE --------
            (VictimEq, (1,2), (False, True)),
            (VictimEq, VictimEq((1,2)), (False, True)),
            (VictimEq, VictimEq.TUPLE, (False, True)),

            (VictimEq((1,2)), (1,2), (True, Exception)),
            (VictimEq((1,2)), VictimEq.TUPLE, (True, Exception)),

            (VictimEq.TUPLE, (1,2), (True, Exception)),
            (VictimEq.TUPLE, VictimEq((1,2)), (True, Exception)),

            # STR --------
            (VictimEq, "str_lower", (False, True)),
            (VictimEq, "STR_LOWER", (False, False)),

            (VictimEq("str_lower"), "str_lower", (True, Exception)),
            (VictimEq("str_lower"), "STR_LOWER", (False, Exception)),

            # DIFF values = same cls--------
            (VictimEq.A1, VictimEq.NONE, (False, Exception)),

            # DIFF clss --------
            (VictimEq.NONE, VictimStd.NONE, (False, Exception)),
            (VictimEq, VictimStd, (False, False)),
            (VictimStd, VictimEq, (False, False)),
        ]
    )
    def test__eq_in(self, source, other, _EXPECTED):
        funk_link = lambda: source == other
        Lambda(funk_link).expect__check_assert(_EXPECTED[0])

        func_link = lambda x: x in source
        Lambda(func_link, other).expect__check_assert(_EXPECTED[1])


# =====================================================================================================================
def _examples() -> None:
    WHEN = EnumAdj_When2.BEFORE
    if WHEN is EnumAdj_When2.BEFORE:
        pass

    print(EnumAdj_NumFPoint.COMMA)  # EnumAdj_NumFPoint.COMMA
    print(EnumAdj_NumFPoint("."))  # EnumAdj_NumFPoint.DOT

    print("." in EnumAdj_NumFPoint)  # True
    print(EnumAdj_NumFPoint.DOT in EnumAdj_NumFPoint)  # True

    print(EnumAdj_NumFPoint(".") == ".")  # False
    print(EnumAdj_NumFPoint(EnumAdj_NumFPoint.DOT))  # EnumAdj_NumFPoint.DOT     # BEST WAY to init value!

    # ObjectInfo(VictimEq).print()

    # ITERATE
    print()
    for i in VictimEq:
        print(i, i.name, i.value)
        print()


# =====================================================================================================================
if __name__ == "__main__":
    _examples()


# =====================================================================================================================
