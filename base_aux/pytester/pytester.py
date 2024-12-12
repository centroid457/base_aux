from typing import *
import pytest
from pytest import mark

from base_aux.base_argskwargs import *
from base_aux.base_objects import *

from base_aux.funcs import TYPE__VALID_RESULT


# =====================================================================================================================
def pytest_func_tester(
        func_link: TYPE__LAMBDA_CONSTRUCTOR, # if func would get Exx - instance of exx would be returned for value!
        args: TYPE__VALID_ARGS = Args(),
        kwargs: TYPE__VALID_KWARGS = Kwargs(),
        _EXPECTED: TYPE__VALID_RESULT = True,  # EXACT VALUE OR ExxClass

        # TODO: add validation func like in Valid!??
        _MARK: pytest.MarkDecorator | None = None,
        _COMMENT: str | None = None
) -> NoReturn | None:
    """
    NOTE
    ----
    this is same as funcs.Valid! except following:
        - if validation is Fail - raise assert!
        - no skips/cumulates/logs/ last_results/*values

    GOAL
    ----
    test target func with exact parameters
    no exception withing target func!

    TODO: apply Valid or merge them into single one!
    """
    if isinstance(args, ArgsKwargs):
        args = args.ARGS
    if isinstance(kwargs, ArgsKwargs):
        kwargs = kwargs.KWARGS

    if isinstance(args, NoValue):
        args = ()
    if isinstance(kwargs, NoValue):
        kwargs = dict()

    args = args__ensure_tuple(args)
    kwargs = kwargs or dict()
    comment = _COMMENT or ""

    if TypeChecker.check__callable_func_meth_inst(func_link):
        try:
            actual_value = func_link(*args, **kwargs)
        except Exception as exx:
            actual_value = exx
    else:
        actual_value = func_link

    print(f"pytest_func_tester={args=}/{kwargs=}//{actual_value=}/{_EXPECTED=}")

    # MARKS -------------------------
    # print(f"{mark.skipif(True)=}")
    if _MARK == mark.skip:
        pytest.skip("skip")
    elif isinstance(_MARK, pytest.MarkDecorator) and _MARK.name == "skipif" and all(_MARK.args):
        pytest.skip("skipIF")

    if _MARK == mark.xfail:
        if TypeChecker.check__exception(_EXPECTED):
            assert not TypeChecker.check__nested__by_cls_or_inst(actual_value, _EXPECTED), f"[xfail]{comment}"
        else:
            assert actual_value != _EXPECTED, f"[xfail]{comment}"
    else:
        if TypeChecker.check__exception(_EXPECTED):
            assert TypeChecker.check__nested__by_cls_or_inst(actual_value, _EXPECTED)
        else:
            assert actual_value == _EXPECTED


# ---------------------------------------------------------------------------------------------------------------------
def pytest_func_tester__no_args_kwargs(
        func_link: TYPE__LAMBDA_CONSTRUCTOR,
        _EXPECTED: TYPE__VALID_RESULT = True,

        _MARK: pytest.MarkDecorator | None = None,
        _COMMENT: str | None = None
) -> NoReturn | None:
    """
    created specially for using inline operators like 'func_link=A>=B'

    CAREFUL
    -------
    BUT be careful cause of exceptions!
    recommended using pytest_func_tester__no_args instead with 'func_link=lambda: A>=B'!!!
    """
    pytest_func_tester(func_link=func_link, _EXPECTED=_EXPECTED, _MARK=_MARK, _COMMENT=_COMMENT)


# ---------------------------------------------------------------------------------------------------------------------
def pytest_func_tester__no_kwargs(
        func_link: TYPE__LAMBDA_CONSTRUCTOR,
        args: TYPE__VALID_ARGS,
        _EXPECTED: TYPE__VALID_RESULT = True,

        _MARK: pytest.MarkDecorator | None = None,
        _COMMENT: str | None = None
) -> NoReturn | None:
    """
    short variant in case of kwargs is not needed

    WHY IT NEED
    -----------
    params passed by pytest while parametrisation as TUPLE!!!! so you cant miss any param in the middle!
    """
    pytest_func_tester(func_link=func_link, args=args, _EXPECTED=_EXPECTED, _MARK=_MARK, _COMMENT=_COMMENT)


# ---------------------------------------------------------------------------------------------------------------------
def pytest_func_tester__no_args(
        func_link: TYPE__LAMBDA_CONSTRUCTOR,
        kwargs: TYPE__VALID_KWARGS,
        _EXPECTED: TYPE__VALID_RESULT = True,

        _MARK: pytest.MarkDecorator | None = None,
        _COMMENT: str | None = None
) -> NoReturn | None:
    """
    short variant in case of args is not needed
    """
    pytest_func_tester(func_link=func_link, kwargs=kwargs, _EXPECTED=_EXPECTED, _MARK=_MARK, _COMMENT=_COMMENT)


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
    argnames="args, kwargs, _EXPECTED, _MARK, _COMMENT",
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
    pytest_func_tester(func_link, args, kwargs, _EXPECTED, _MARK, _COMMENT)


# =====================================================================================================================
@pytest.mark.parametrize(argnames="func_link", argvalues=[int, ])
@pytest.mark.parametrize(
    argnames="args, kwargs, _EXPECTED",
    argvalues=[
        (("1", ), {}, 1),
        ("1", {}, 1),                   # ARGS - direct one value acceptable
        (("hello", ), {}, Exception),   # EXPECT - direct exceptions
    ]
)
def test__short_variant(func_link, args, kwargs, _EXPECTED):
    pytest_func_tester(func_link, args, kwargs, _EXPECTED)


# =====================================================================================================================
@pytest.mark.parametrize(argnames="func_link", argvalues=[int, ])
@pytest.mark.parametrize(
    argnames="args, _EXPECTED",
    argvalues=[
        (("1", ), 1),
        ("1", 1),
        ("", ValueError),
        (("hello", ), Exception),
    ]
)
def test__shortest_variant(func_link, args, _EXPECTED):
    pytest_func_tester__no_kwargs(func_link, args, _EXPECTED)


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
    pytest_func_tester__no_args_kwargs(expression)


# =====================================================================================================================
# @pytest.mark.parametrize(
#     argnames="args, _EXPECTED",
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
# def test__compare_doublesided(args, _EXPECTED):
#     func_link = Valid.compare_doublesided_or_exx
#     pytest_func_tester__no_kwargs(func_link, args, _EXPECTED[0])
#
#     func_link = Valid.compare_doublesided__bool
#     pytest_func_tester__no_kwargs(func_link, args, _EXPECTED[1])
#
#     func_link = Valid.compare_doublesided__reverse
#     pytest_func_tester__no_kwargs(func_link, args, _EXPECTED[2])


# =====================================================================================================================
