from typing import *
import pytest
from pytest import mark

from base_aux.base_source.m1_source import InitSource
from base_aux.base_objects.obj_types import TypeCheck

from base_aux.aux_callable.callable_aux import CallableAux
from base_aux.aux_argskwargs.m1_argskwargs import TYPE__LAMBDA_CONSTRUCTOR, TYPE__ARGS_DRAFT, TYPE__KWARGS_DRAFT

from base_aux.funcs.static import TYPE__VALID_RESULT


# =====================================================================================================================
@final
class PytestAux(InitSource):
    SOURCE: TYPE__LAMBDA_CONSTRUCTOR    # if func would get Exx - instance of exx would be returned for value!

    def assert_check(
            self,
            args: TYPE__ARGS_DRAFT = (),
            kwargs: TYPE__KWARGS_DRAFT = None,

            _EXPECTED: TYPE__VALID_RESULT = True,  # EXACT VALUE OR ExxClass
            _MARK: pytest.MarkDecorator | None = None,
            _COMMENT: str | None = None,
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
        if not kwargs:
            kwargs = {}

        comment = _COMMENT or ""
        actual_value = CallableAux(self.SOURCE).resolve_exx(*args, **kwargs)

        print(f"pytest={args=}/{kwargs=}//{actual_value=}/{_EXPECTED=}")

        # MARKS -------------------------
        # print(f"{mark.skipif(True)=}")
        if _MARK == mark.skip:
            pytest.skip("skip")
        elif isinstance(_MARK, pytest.MarkDecorator) and _MARK.name == "skipif" and all(_MARK.args):
            pytest.skip("skipIF")

        if _MARK == mark.xfail:
            if TypeCheck(_EXPECTED).check__exception():
                assert not TypeCheck(actual_value).check__nested__by_cls_or_inst(_EXPECTED), f"[xfail]{comment}"
            else:
                assert actual_value != _EXPECTED, f"[xfail]{comment}"
        else:
            if TypeCheck(_EXPECTED).check__exception():
                assert TypeCheck(actual_value).check__nested__by_cls_or_inst(_EXPECTED)
            else:
                assert actual_value == _EXPECTED


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
    PytestAux(func_link, *args, **kwargs).assert_check(_EXPECTED, _MARK, _COMMENT)


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
    PytestAux(func_link, *args, **kwargs).assert_check(_EXPECTED)


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
    PytestAux(func_link, *args).assert_check(_EXPECTED)


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
    PytestAux(expression).assert_check()


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
