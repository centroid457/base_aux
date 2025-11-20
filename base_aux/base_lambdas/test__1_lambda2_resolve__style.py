from base_aux.base_lambdas.m1_lambda import *

from base_aux.base_values.m4_primitives import *


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="source, args, _EXPECTED",
    argvalues=[
        (Exception, (), (False, True,
                         Exception, Exception, Exception, False, VALUE_SPECIAL.SKIPPED, Exception)),  # be careful here! exc in source return exc NO RAISE!!!!
        (Exception(), (), (False, True,
                Exception, Exception, Exception, False, Exception, Exception)),
        (LAMBDA_EXC, (), (False, True,
                          Exception, Exception, Exception, False, VALUE_SPECIAL.SKIPPED, Exception)),
        (LAMBDA_RAISE, (), (True, False,
                            Exception, None, Exception, False, VALUE_SPECIAL.SKIPPED, VALUE_SPECIAL.SKIPPED)),

        (LAMBDA_TRUE, (), (False, True,
                           True, True, True, True, VALUE_SPECIAL.SKIPPED, True)),
        (LAMBDA_FALSE, (), (False, True,
                            False, False, False, False, VALUE_SPECIAL.SKIPPED, False)),
        (LAMBDA_NONE, (), (False, True,
                           None, None, None, False, VALUE_SPECIAL.SKIPPED, None)),

        (True, (), (False, True,
                True, True, True, True, True, True)),
        (False, (), (False, True,
                False, False, False, False, False, False)),
        (None, (), (False, True,
                None, None, None, False, None, None)),

        (INST_CALL_TRUE, (), (False, True,
                              True, True, True, True, VALUE_SPECIAL.SKIPPED, True)),
        (INST_CALL_FALSE, (), (False, True,
                               False, False, False, False, VALUE_SPECIAL.SKIPPED, False)),
        (INST_CALL_RAISE, (), (True, False,
                               Exception, None, Exception, False, VALUE_SPECIAL.SKIPPED, VALUE_SPECIAL.SKIPPED)),

        (INST_BOOL_TRUE, (),  (False, True,
                INST_BOOL_TRUE, INST_BOOL_TRUE, INST_BOOL_TRUE, True, INST_BOOL_TRUE, INST_BOOL_TRUE)),
        (INST_BOOL_FALSE, (), (False, True,
                INST_BOOL_FALSE, INST_BOOL_FALSE, INST_BOOL_FALSE, False, INST_BOOL_FALSE, INST_BOOL_FALSE)),
        (INST_BOOL_RAISE, (), (False, True,
                INST_BOOL_RAISE, INST_BOOL_RAISE, INST_BOOL_RAISE, False, INST_BOOL_RAISE, INST_BOOL_RAISE)),

        # collections ----------
        ((), (), (False, True,
                (), (), (), False, (), ())),
        ([], (), (False, True,
                [], [], [], False, [], [])),
        (LAMBDA_LIST_KEYS, (), (False, True,
                                [], [], [], False, VALUE_SPECIAL.SKIPPED, [])),

        ([None, ], (), (False, True,
                [None, ], [None, ], [None, ], True, [None, ], [None, ])),
        ([1, ], (), (False, True,
                [1, ], [1, ], [1, ], True, [1, ], [1, ])),
    ]
)
def test__get_result(source, args, _EXPECTED):
    Lambda(Lambda(source, *args).check_raise).expect__check_assert(_EXPECTED[0])
    Lambda(Lambda(source, *args).check_no_raise).expect__check_assert(_EXPECTED[1])
    Lambda(Lambda(source, *args).resolve__raise).expect__check_assert(_EXPECTED[2])
    Lambda(Lambda(source, *args).resolve__raise_as_none).expect__check_assert(_EXPECTED[3])
    Lambda(Lambda(source, *args).resolve__exc).expect__check_assert(_EXPECTED[4])
    Lambda(Lambda(source, *args).resolve__bool).expect__check_assert(_EXPECTED[5])
    Lambda(Lambda(source, *args).resolve__skip_callables).expect__check_assert(_EXPECTED[6])
    Lambda(Lambda(source, *args).resolve__skip_raised).expect__check_assert(_EXPECTED[7])


# =====================================================================================================================
