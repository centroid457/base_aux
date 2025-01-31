from typing import *
import pytest
from pytest import mark

from base_aux.base_inits.m2_source_kwargs import *
from base_aux.aux_types.m1_type_aux import TypeAux

from base_aux.aux_callable.m1_callable_aux import CallableAux
from base_aux.aux_argskwargs.m1_argskwargs import TYPE__ARGS_DRAFT, TYPE__KWARGS_DRAFT

from base_aux.aux_types.m0_types import TYPE__VALID_RESULT, TYPE__LAMBDA_CONSTRUCTOR


# =====================================================================================================================
@final
class ExpectAux(InitSourceKwArgs_Explicite):
    """
    SPECIALLY CREATED FOR
    ---------------------
    unit tests bypytest
    """
    SOURCE: TYPE__LAMBDA_CONSTRUCTOR    # if func would get Exx - instance of exx would be returned for value!

    def check_assert(
            self,
            # args: TYPE__ARGS_DRAFT = (),      # DONT USE HERE!!!
            # kwargs: TYPE__KWARGS_DRAFT = None,

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
        args = self.ARGS
        kwargs = self.KWARGS

        comment = _COMMENT or ""
        actual_value = CallableAux(self.SOURCE).resolve_exx(*args, **kwargs)

        print(f"Expected[{self.SOURCE}/{args=}/{kwargs=}//{actual_value=}/{_EXPECTED=}]")

        # MARKS -------------------------
        # print(f"{mark.skipif(True)=}")
        if _MARK == mark.skip:
            pytest.skip("skip")
        elif isinstance(_MARK, pytest.MarkDecorator) and _MARK.name == "skipif" and all(_MARK.args):
            pytest.skip("skipIF")

        if _MARK == mark.xfail:
            if TypeAux(_EXPECTED).check__exception():
                assert not TypeAux(actual_value).check__nested__by_cls_or_inst(_EXPECTED), f"[xfail]{comment}"
            else:
                assert actual_value != _EXPECTED, f"[xfail]{comment}"
        else:
            if TypeAux(_EXPECTED).check__exception():
                assert TypeAux(actual_value).check__nested__by_cls_or_inst(_EXPECTED)
            else:
                assert actual_value == _EXPECTED

    def check_bool(self, *args, **kwargs) -> bool:
        """
        GOAL
        ----
        extend work for not only in unittests
        """
        try:
            self.check_assert(*args, **kwargs)
            return True
        except:
            return False


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
    ExpectAux(func_link, args, kwargs).check_assert(_EXPECTED, _MARK, _COMMENT)


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
    ExpectAux(func_link, args, kwargs).check_assert(_EXPECTED)


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
    ExpectAux(func_link, args).check_assert(_EXPECTED)


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
    ExpectAux(expression).check_assert()


# =====================================================================================================================
# @pytest.mark.parametrize(
#     argnames="args, _EXPECTED",
#     argvalues=[
#         ((1, 1),        (True, True, False)),
#         ((1, 2),        (False, False, True)),
#         ((LAMBDA_TRUE, True), (False, False, True)),
#     ]
# )
# def test__several_expected(args, _EXPECTED):
#     func_link = Valid.compare_doublesided_or_exx
#     ExpectAux(func_link, args).assert_check(_EXPECTED[0])
#
#     func_link = Valid.compare_doublesided__bool
#     ExpectAux(func_link, args).assert_check(_EXPECTED[1])
#
#     func_link = Valid.compare_doublesided__reverse
#     ExpectAux(func_link, args).assert_check(_EXPECTED[2])


# =====================================================================================================================
