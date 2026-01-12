from base_aux.versions.m2_version import *
from base_aux.base_lambdas.m1_lambda import *
from base_aux.base_values.m3_exceptions import *

from base_aux.tables.m1_table_obj import TableObj


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="schema, _EXPECTED",
    argvalues=[
        (dict(ATC=1), False),
        (dict(ATC=[1,]), True),
        (dict(ATC=[1,], PTB=[1,]), True),
        (dict(ATC=[1,], PTB=[1,]), True),
        (dict(ATC=[1,], PTB=[]), False),
    ]
)
def test__LAMBDA_TRICK(schema, _EXPECTED):
    # INCORRECT! - too sophisticated!
    Lambda(lambda **kwargs: TableObj(**kwargs), **schema).check_raised__assert(not _EXPECTED)

    # CORRECT! - dont use any lambda params! do direct application
    Lambda(lambda: TableObj(**schema)).check_raised__assert(not _EXPECTED)


# =====================================================================================================================
