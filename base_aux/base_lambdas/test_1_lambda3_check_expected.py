import pytest
from base_aux.base_lambdas.m1_lambda import *

from base_aux.base_values.m4_primitives import *
from base_aux.aux_argskwargs.m1_argskwargs import *
from base_aux.aux_eq.m3_eq_valid3_derivatives import *
from base_aux.base_nest_dunders.m7_cmp import *


# =====================================================================================================================
class Cls(NestCmp_GLET_Any):
    def __init__(self, value):
        self.VALUE = value

    def __cmp__(self, other):
        other = Cls(other)
        if self.VALUE == other.VALUE:
            return 0
        if self.VALUE > other.VALUE:
            return 1
        if self.VALUE < other.VALUE:
            return -1


def test____LE__():
    func_link = lambda result: result == 1
    Lambda(func_link, Cls(1)).check_expected__assert(True)


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="func_link, args, _EXPECTED_RAISED",
    argvalues=[
        # Special Values -------
        # (NoValue, (), False),   # CANT CHECK NoValue))))

        # not callable ------------
        (True, (), False),
        (True, (111, ), False),
        (False, (), False),

        # callable ------------
        (LAMBDA_ECHO, (), True),
        (LAMBDA_ECHO, (None, ), False),
        (LAMBDA_ECHO, (True, ), False),
        (lambda value: value, (), True),

        # TYPES -------
        (int, (), False),
        (1, (), False),
        (Exception, (), False),
        (Exception(), (), False),
        (LAMBDA_RAISE, (), True),
    ]
)
def test__check_all_meth__simple(
        func_link: Any | Callable,
        args: Any,

        _EXPECTED_RAISED: bool,
):
    assert Lambda(func_link, *args).check_raised__bool() is _EXPECTED_RAISED
    assert Lambda(func_link, *args).check_no_raised__bool() is not _EXPECTED_RAISED

    if _EXPECTED_RAISED:
        assert Lambda(func_link, *args).check_raised__assert() is None

        try:
            Lambda(func_link, *args).check_no_raised__assert()
        except:
            assert True
        else:
            assert False

    else:
        try:
            Lambda(func_link, *args).check_raised__assert()
        except:
            assert True
        else:
            assert False

        assert Lambda(func_link, *args).check_no_raised__assert() is None


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="func_link, args, kwargs, _EXPECTED, _Expected_pytestResult, _EXP_raised",
    argvalues=[
        # Special Values -------
        # (NoValue, (), {}, NoValue, True, False),   # CANT CHECK NoValue))))

        # not callable ------------
        (True, (), {}, True, True, False),

        (True, (111, ), {"111": 222}, True, True, False),
        (True, (111, ), {"111": 222}, False, False, False),

        (False, (), {}, True, False, False),

        # callable ------------
        (LAMBDA_ECHO, (), {}, True, False, True),

        (LAMBDA_ECHO, (None, ), {}, True, False, False),
        (LAMBDA_ECHO, (None, ), {}, None, True, False),
        (LAMBDA_ECHO, (True, ), {}, True, True, False),
        (LAMBDA_ECHO, (True, ), {}, True, True, False),
        (lambda value: value, (), {"value": True}, True, True, False),
        (lambda value: value, (), {"value": None}, True, False, False),

        # TYPES -------
        (int, (), {}, int, True, False),
        (1, (), {}, int, True, False),
        (1, (), {}, float, False, False),

        (1, (), {}, Exception, False, False),
        (Exception, (), {}, Exception, True, False),
        (Exception(), (), {}, Exception, True, False),

        (LAMBDA_RAISE, (), {}, Exception, True, True),
    ]
)
def test__check_all_meth__complex(
        func_link: Any | Callable,
        args: Any,
        kwargs: Any,
        _EXPECTED: Any | type[Any],
        _Expected_pytestResult: bool,
        _EXP_raised: bool
):
    # check_RAISED ----------------------------
    assert Lambda(func_link, *args, **kwargs).check_raised__bool() is _EXP_raised
    assert Lambda(func_link, *args, **kwargs).check_no_raised__bool() is not _EXP_raised

    if _EXP_raised:
        # ---------------
        assert Lambda(func_link, *args, **kwargs).check_raised__assert() is None

        # ---------------
        try:
            Lambda(func_link, *args, **kwargs).check_no_raised__assert()
        except:
            assert True
        else:
            assert False

    else:
        # ---------------
        assert Lambda(func_link, *args, **kwargs).check_no_raised__assert() is None

        # ---------------
        try:
            Lambda(func_link, *args, **kwargs).check_raised__assert()
        except:
            assert True
        else:
            assert False

    # check_EXPECTED --------------------------
    assert Lambda(func_link, *args, **kwargs).check_expected__bool(_EXPECTED) == _Expected_pytestResult
    try:
        Lambda(func_link, *args, **kwargs).check_expected__assert(_EXPECTED)
    except:
        assert not _Expected_pytestResult
    else:
        assert _Expected_pytestResult
        # assert result == _Expected_pytestResult


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="args, kwargs, _EXPECTED",
    argvalues=[
        ((), {}, []),
        ((None, ), {}, [None, ]),
        ((1, ), {}, [1, ]),
        ((1, 1), {}, [1, 1]),

        ((1, 1), {}, [1, 1]),
        ((1, 1), {"2": 22}, [1, 1, "2"]),
        ((1, 1), {"2": 22, "3": 33}, [1, 1, "2", "3"]),
    ]
)
def test__func_list_direct(args, kwargs, _EXPECTED):
    Lambda(LAMBDA_LIST_KEYS, *args, **kwargs).check_expected__assert(_EXPECTED)


# ---------------------------------------------------------------------------------------------------------------------
@pytest.mark.parametrize(
    argnames="args, kwargs, _EXPECTED",
    argvalues=[
        ((), {}, []),
        ((None, ), {}, [None, ]),
        ((1, ), {}, [1, ]),
        ((1, 1), {}, [1, 1]),

        ((1, 1), {}, [1, 1]),
        ((1, 1), {"2": 22}, [1, 1, 22]),
        ((1, 1), {"2": 22, "3": 33}, [1, 1, 22, 33]),
    ]
)
def test__func_list_values(args, kwargs, _EXPECTED):
    Lambda(LAMBDA_LIST_VALUES, *args, **kwargs).check_expected__assert(_EXPECTED)


# ---------------------------------------------------------------------------------------------------------------------
@pytest.mark.parametrize(
    argnames="args, kwargs, _EXPECTED",
    argvalues=[
        ((), {}, {}),
        ((None, ), {}, {None: None}),
        ((1, ), {}, {1: None}),
        ((1, 1), {}, {1: None}),

        ((1, 1), {}, {1: None}),
        ((1, 1), {"2": 22}, {1: None, "2": 22}),
        ((1, 1), {"2": 22, "3": 33}, {1: None, "2": 22, "3": 33}),
    ]
)
def test__func_dict(args, kwargs, _EXPECTED):
    Lambda(LAMBDA_DICT_KEYS, *args, **kwargs).check_expected__assert(_EXPECTED)


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="args, kwargs, _EXPECTED",
    argvalues=[
        ((), {}, True),
        ((None, ), {}, False),
        ((1, ), {}, True),
        ((1, 1), {}, True),

        ((1, 1), {}, True),
        ((1, 1), {"2": 22}, True),
        ((1, 1), {"2": 22, "3": 33}, True),

        ((1, 1), {"2": 22, "3": None}, False),
    ]
)
def test__func_all(args, kwargs, _EXPECTED):
    Lambda(LAMBDA_ALL_VALUES, *args, **kwargs).check_expected__assert(_EXPECTED)


# ---------------------------------------------------------------------------------------------------------------------
@pytest.mark.parametrize(
    argnames="args, kwargs, _EXPECTED",
    argvalues=[
        ((), {}, False),
        ((None, ), {}, False),
        ((1, ), {}, True),
        ((1, 1), {}, True),

        ((1, 1), {}, True),
        ((1, 1), {"2": 22}, True),
        ((1, 1), {"2": 22, "3": 33}, True),

        ((1, 1), {"2": 22, "3": None}, True),
        ((1, None), {"2": 22, "3": None}, True),
        ((None, None), {"2": True, "3": None}, True),
        ((None, None), {"2": False, "3": None}, False),

        (Args(None, None), {"2": False, "3": None}, False),
    ]
)
def test__func_any(args, kwargs, _EXPECTED):
    Lambda(LAMBDA_ANY_VALUES, *args, **kwargs).check_expected__assert(_EXPECTED)


# ---------------------------------------------------------------------------------------------------------------------
@pytest.mark.parametrize(
    argnames="source, other, _EXPECTED",
    argvalues=[
        ("11.688889V", EqValid_Regexp(r"\d+[.,]?\d*V"), True),
        (INST_EQ_TRUE, INST_EQ_TRUE, True),
        (INST_EQ_TRUE, INST_EQ_FALSE, True),
        (INST_EQ_FALSE, INST_EQ_TRUE, True),
        (INST_EQ_FALSE, INST_EQ_FALSE, False),
    ]
)
def test__EQ(source, other, _EXPECTED):
    assert Lambda(source).check_expected__bool(other) == _EXPECTED


# =====================================================================================================================
