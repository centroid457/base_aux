from base_aux.lambdas.m1_lambda import *

from base_aux.aux_values.m4_primitives import *
from base_aux.aux_values.m5_enums import *


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="source, args, _EXPECTED",
    argvalues=[
        (Exception, (), (False, True,
                         Exception, Exception, Exception, False, Enum_ProcessResult.SKIPPED, Exception)),  # be careful here! exx in source return exx NO RAISE!!!!
        (Exception(), (), (False, True,
                Exception, Exception, Exception, False, Exception, Exception)),
        (LAMBDA_EXX, (), (False, True,
                          Exception, Exception, Exception, False, Enum_ProcessResult.SKIPPED, Exception)),
        (LAMBDA_RAISE, (), (True, False,
                            Exception, None, Exception, False, Enum_ProcessResult.SKIPPED, Enum_ProcessResult.SKIPPED)),

        (LAMBDA_TRUE, (), (False, True,
                           True, True, True, True, Enum_ProcessResult.SKIPPED, True)),
        (LAMBDA_FALSE, (), (False, True,
                            False, False, False, False, Enum_ProcessResult.SKIPPED, False)),
        (LAMBDA_NONE, (), (False, True,
                           None, None, None, False, Enum_ProcessResult.SKIPPED, None)),

        (True, (), (False, True,
                True, True, True, True, True, True)),
        (False, (), (False, True,
                False, False, False, False, False, False)),
        (None, (), (False, True,
                None, None, None, False, None, None)),

        (INST_CALL_TRUE, (), (False, True,
                              True, True, True, True, Enum_ProcessResult.SKIPPED, True)),
        (INST_CALL_FALSE, (), (False, True,
                               False, False, False, False, Enum_ProcessResult.SKIPPED, False)),
        (INST_CALL_RAISE, (), (True, False,
                               Exception, None, Exception, False, Enum_ProcessResult.SKIPPED, Enum_ProcessResult.SKIPPED)),

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
        (LAMBDA_LIST_DIRECT, (), (False, True,
                                  [], [], [], False, Enum_ProcessResult.SKIPPED, [])),

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
    Lambda(Lambda(source, *args).resolve__exx).expect__check_assert(_EXPECTED[4])
    Lambda(Lambda(source, *args).resolve__bool).expect__check_assert(_EXPECTED[5])
    Lambda(Lambda(source, *args).resolve__skip_callables).expect__check_assert(_EXPECTED[6])
    Lambda(Lambda(source, *args).resolve__skip_raised).expect__check_assert(_EXPECTED[7])


# =====================================================================================================================
