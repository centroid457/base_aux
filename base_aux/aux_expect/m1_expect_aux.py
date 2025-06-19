import pytest
from pytest import mark

from base_aux.aux_types.m0_static_typing import TYPING__LAMBDA_CONSTRUCTOR
from base_aux.base_nest_dunders.m1_init1_source2_kwargs import *
from base_aux.aux_eq.m2_eq_aux import *

from base_aux.aux_argskwargs.m1_argskwargs import *


# =====================================================================================================================
@final
class ExpectAux(NestInit_SourceKwArgs_Explicite):
    """
    SPECIALLY CREATED FOR
    ---------------------
    unit tests bypytest
    """
    SOURCE: TYPING__LAMBDA_CONSTRUCTOR    # if func would get Exx - instance of exx would be returned for value!

    def check_assert(
            self,
            # args: TYPING.ARGS_DRAFT = (),      # DONT USE HERE!!!
            # kwargs: TYPING.KWARGS_DRAFT = None,

            _EXPECTED: TYPING.EXPECTED = True,  # EXACT VALUE (noCallable) OR AnyCLass - to cmp as isinstanceOrSubclass!!!
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
        try:
            actual_value = CallableAux(self.SOURCE).resolve_exx(*args, **kwargs)
        except Exception as exx:
            actual_value = exx      # this is an internal value! when use incorrect ArgsKw!!!

        print(f"Expected[{self.SOURCE}/{args=}/{kwargs=}//{actual_value=}/{_EXPECTED=}]")

        # MARKS -------------------------
        # print(f"{mark.skipif(True)=}")
        if _MARK == mark.skip:
            pytest.skip("skip")
        elif isinstance(_MARK, pytest.MarkDecorator) and _MARK.name == "skipif" and all(_MARK.args):
            pytest.skip("skipIF")

        result = (
            TypeAux(actual_value).check__subclassed_or_isinst(_EXPECTED)
            or
            EqAux(actual_value).check_doubleside__bool(_EXPECTED)
        )
        if _MARK == mark.xfail:
            assert not result, f"[xfail]{comment}"
        else:
            assert result

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

def _example_TUPLE_ARGS():
    """
    use Args(otherTuple) to direct use exact tuple
    """
    class Test_EnumEq:
        class VictimEq(NestEq_Enum):
            NONE = None
            A1 = 1
            TUPLE = (1, 2)

        @pytest.mark.parametrize(
            argnames="source, other, _EXPECTED",
            argvalues=[
                # TUPLE --------
                (VictimEq, (1,2), (False, True)),
                (VictimEq, VictimEq((1,2)), (False, True)),
                (VictimEq, VictimEq.TUPLE, (False, True)),

                (VictimEq((1,2)), (1,2), (True, Exception)),
                (VictimEq((1,2)), VictimEq.TUPLE, (True, Exception)),

                (VictimEq.TUPLE, (1,2), (True, Exception)),
                (VictimEq.TUPLE, VictimEq((1,2)), (True, Exception)),
            ]
        )
        def test__eq_in(self, source, other, _EXPECTED):
            ExpectAux(source == other).check_assert(_EXPECTED[0])

            func_link = lambda x: x in source
            ExpectAux(func_link, Args(other)).check_assert(_EXPECTED[1])


# def _func_example(arg1: Any, arg2: Any) -> str:
#     return f"{arg1}{arg2}"
#
#
# # =====================================================================================================================
# @pytest.mark.parametrize(argnames="func_link", argvalues=[_func_example, ])
# @pytest.mark.parametrize(
#     argnames="args, kwargs, _EXPECTED, _MARK, _COMMENT",
#     argvalues=[
#         # TRIVIAL -------------
#         ((1, None), {}, "1None", None, "ok"),
#         ((1, 2), {}, "12", None, "ok"),
#
#         # LIST -----------------
#         ((1, []), {}, "1[]", None, "ok"),
#
#         # MARKS -----------------
#         ((1, 2), {}, None, mark.skip, "skip"),
#         ((1, 2), {}, None, mark.skipif(True), "skip"),
#         ((1, 2), {}, "12", mark.skipif(False), "ok"),
#         ((1, 2), {}, None, mark.xfail, "ok"),
#         # ((1, 2), {}, "12", mark.xfail, "SHOULD BE FAIL!"),
#     ]
# )
# def test__full_params(func_link, args, kwargs, _EXPECTED, _MARK, _COMMENT):     # NOTE: all params passed by TUPLE!!!! so you cant miss any in the middle!
#     ExpectAux(func_link, args, kwargs).check_assert(_EXPECTED, _MARK, _COMMENT)
#
#
# # =====================================================================================================================
# @pytest.mark.parametrize(argnames="func_link", argvalues=[int, ])
# @pytest.mark.parametrize(
#     argnames="args, kwargs, _EXPECTED",
#     argvalues=[
#         (("1", ), {}, 1),
#         ("1", {}, 1),                   # ARGS - direct one value acceptable
#         (("hello", ), {}, Exception),   # EXPECT - direct exceptions
#     ]
# )
# def test__short_variant(func_link, args, kwargs, _EXPECTED):
#     ExpectAux(func_link, args, kwargs).check_assert(_EXPECTED)
#
#
# # =====================================================================================================================
# @pytest.mark.parametrize(argnames="func_link", argvalues=[int, ])
# @pytest.mark.parametrize(
#     argnames="args, _EXPECTED",
#     argvalues=[
#         (("1", ), 1),
#         ("1", 1),
#         ("", ValueError),
#         (("hello", ), Exception),
#     ]
# )
# def test__shortest_variant(func_link, args, _EXPECTED):
#     ExpectAux(func_link, args).check_assert(_EXPECTED)
#
#
# # =====================================================================================================================
# @pytest.mark.parametrize(
#     argnames="expression",
#     argvalues=[
#         ("1rc2") == "1rc2",
#         ("1rc2") != "1rc1",
#
#         ("1.1rc2") > "1.0rc1",
#         ("1.1rc2") > "1.1rc0",
#         ("1.1rc2.0") > "1.1rc2",
#
#         # ("01.01rc02") > "1.1rc1",
#         ("01.01rc02") < "1.1rd1",
#     ]
# )
# def test__expressions(expression):
#     ExpectAux(expression).check_assert()
#
#
# # =====================================================================================================================
# # @pytest.mark.parametrize(
# #     argnames="args, _EXPECTED",
# #     argvalues=[
# #         ((1, 1),        (True, True, False)),
# #         ((1, 2),        (False, False, True)),
# #         ((LAMBDA_TRUE, True), (False, False, True)),
# #     ]
# # )
# # def test__several_expected(args, _EXPECTED):
# #     func_link = Valid.compare_doublesided_or_exx
# #     ExpectAux(func_link, args).assert_check(_EXPECTED[0])
# #
# #     func_link = Valid.compare_doublesided__bool
# #     ExpectAux(func_link, args).assert_check(_EXPECTED[1])
# #
# #     func_link = Valid.compare_doublesided__reverse
# #     ExpectAux(func_link, args).assert_check(_EXPECTED[2])
#
#
# # =====================================================================================================================
