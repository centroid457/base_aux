from typing import *
import pytest
from pytest import mark

from base_aux.base_source import InitSourceKwArgs
from base_aux.base_argskwargs import *
from base_aux.base_objects import *

from base_aux.aux_callable import CallableAux

from base_aux.funcs import TYPE__VALID_RESULT


# =====================================================================================================================
@final
class PytestAux(InitSourceKwArgs):
    SOURCE: TYPE__LAMBDA_CONSTRUCTOR    # if func would get Exx - instance of exx would be returned for value!

def check(
        self,
        EXPECTED: TYPE__VALID_RESULT = True,  # EXACT VALUE OR ExxClass
        _MARK: pytest.MarkDecorator | None = None,
        _COMMENT: str | None = None
) -> None | NoReturn:
    """
    NOTE
    ----
    this is same as funcs.Valid! except following:
        - if validation is Fail - raise assert!
        - no skips/cumulates/logs/ last_results/*values

    GOAL
    ----
    test target func/obj with exact parameters
    no exception withing target func!

    TODO: apply Valid or merge them into single one!
    """
    comment = _COMMENT or ""
    actual_value = CallableAux(self.SOURCE).resolve_exx(*self.ARGS, **self.KWARGS)

    print(f"pytest=ARGS={self.ARGS}/KWARGS={self.KWARGS}//{actual_value=}/{EXPECTED=}")

    # MARKS -------------------------
    # print(f"{mark.skipif(True)=}")
    if _MARK == mark.skip:
        pytest.skip("skip")
    elif isinstance(_MARK, pytest.MarkDecorator) and _MARK.name == "skipif" and all(_MARK.args):
        pytest.skip("skipIF")

    if _MARK == mark.xfail:
        if TypeCheck(EXPECTED).check__exception():
            assert not TypeCheck(actual_value).check__nested__by_cls_or_inst(EXPECTED), f"[xfail]{comment}"
        else:
            assert actual_value != EXPECTED, f"[xfail]{comment}"
    else:
        if TypeCheck(EXPECTED).check__exception():
            assert TypeCheck(actual_value).check__nested__by_cls_or_inst(EXPECTED)
        else:
            assert actual_value == EXPECTED


# ---------------------------------------------------------------------------------------------------------------------
def pytest_func_tester__no_args_kwargs():
    pass


# ---------------------------------------------------------------------------------------------------------------------
def pytest_func_tester__no_kwargs():
    pass


# ---------------------------------------------------------------------------------------------------------------------
def pytest_func_tester__no_args():
    pass


# =====================================================================================================================
pass    # USAGE EXAMPLES ----------------------------------------------------------------------------------------------
pass    # USAGE EXAMPLES ----------------------------------------------------------------------------------------------
pass    # USAGE EXAMPLES ----------------------------------------------------------------------------------------------
pass    # USAGE EXAMPLES ----------------------------------------------------------------------------------------------
pass    # USAGE EXAMPLES ----------------------------------------------------------------------------------------------
pass    # USAGE EXAMPLES ----------------------------------------------------------------------------------------------
pass    # USAGE EXAMPLES ----------------------------------------------------------------------------------------------
pass    # USAGE EXAMPLES ----------------------------------------------------------------------------------------------
pass    # USAGE EXAMPLES ----------------------------------------------------------------------------------------------
pass    # USAGE EXAMPLES ----------------------------------------------------------------------------------------------
pass    # USAGE EXAMPLES ----------------------------------------------------------------------------------------------
pass    # USAGE EXAMPLES ----------------------------------------------------------------------------------------------
pass    # USAGE EXAMPLES ----------------------------------------------------------------------------------------------
pass    # USAGE EXAMPLES ----------------------------------------------------------------------------------------------
pass    # USAGE EXAMPLES ----------------------------------------------------------------------------------------------


def _func_example(arg1: Any, arg2: Any) -> str:
    return f"{arg1}{arg2}"


# =====================================================================================================================
@pytest.mark.parametrize(argnames="func_link", argvalues=[_func_example, ])
@pytest.mark.parametrize(
    argnames="args, kwargs, EXPECTED, _MARK, _COMMENT",
    argvalues=[
        # TRIVIAL -------------
        ((1, None), {}, "1None", None, "ok"),
        ((1, 2), {}, "12", None, "ok"),

        # LIST -----------------
        ((1, []), {}, "1[]", None, "ok"),

        # MARKS -----------------
        ((1, 2), {}, None, mark.skip, "skip"),
        ((1, 2), {}, None, mark.skipif(True), "skip"),
        ((1, 2), {}, "12", mark.skipif(False), "ok"),
        ((1, 2), {}, None, mark.xfail, "ok"),
        # ((1, 2), {}, "12", mark.xfail, "SHOULD BE FAIL!"),
    ]
)
def test__full_params(func_link, args, kwargs, _EXPECTED, _MARK, _COMMENT):     # NOTE: all params passed by TUPLE!!!! so you cant miss any in the middle!
    PytestAux(func_link, *args, **kwargs).check(_EXPECTED, _MARK, _COMMENT)


# =====================================================================================================================
@pytest.mark.parametrize(argnames="func_link", argvalues=[int, ])
@pytest.mark.parametrize(
    argnames="args, kwargs, EXPECTED",
    argvalues=[
        (("1", ), {}, 1),
        ("1", {}, 1),                   # ARGS - direct one value acceptable
        (("hello", ), {}, Exception),   # EXPECT - direct exceptions
    ]
)
def test__short_variant(func_link, args, kwargs, _EXPECTED):
    PytestAux(func_link, *args, **kwargs).check(_EXPECTED)


# =====================================================================================================================
@pytest.mark.parametrize(argnames="func_link", argvalues=[int, ])
@pytest.mark.parametrize(
    argnames="args, EXPECTED",
    argvalues=[
        (("1", ), 1),
        ("1", 1),
        ("", ValueError),
        (("hello", ), Exception),
    ]
)
def test__shortest_variant(func_link, args, _EXPECTED):
    PytestAux(func_link, *args).check(_EXPECTED)


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="expression",
    argvalues=[
        ("1rc2") == "1rc2",
        ("1rc2") != "1rc1",

        ("1.1rc2") > "1.0rc1",
        ("1.1rc2") > "1.1rc0",
        ("1.1rc2.0") > "1.1rc2",

        # ("01.01rc02") > "1.1rc1",
        ("01.01rc02") < "1.1rd1",
    ]
)
def test__expressions(expression):
    PytestAux(expression).check()


# =====================================================================================================================
# @pytest.mark.parametrize(
#     argnames="args, EXPECTED",
#     argvalues=[
#         ((1, 1),        (True, True, False)),
#         ((1, 2),        (False, False, True)),
#         ((LAMBDA_TRUE, True), (False, False, True)),
#
#         ((ClsEq(1), 1), (True, True, False)),
#         ((ClsEq(1), 2), (False, False, True)),
#         ((1, ClsEq(1)), (True, True, False)),
#         ((2, ClsEq(1)), (False, False, True)),
#
#         ((ClsEqRaise(), 1), (Exception, False, True)),
#         ((1, ClsEqRaise()), (Exception, False, True)),
#     ]
# )
# def test__compare_doublesided(args, EXPECTED):
#     func_link = Valid.compare_doublesided_or_exx
#     pytest_func_tester__no_kwargs(func_link, args, EXPECTED[0])
#
#     func_link = Valid.compare_doublesided__bool
#     pytest_func_tester__no_kwargs(func_link, args, EXPECTED[1])
#
#     func_link = Valid.compare_doublesided__reverse
#     pytest_func_tester__no_kwargs(func_link, args, EXPECTED[2])


# =====================================================================================================================
