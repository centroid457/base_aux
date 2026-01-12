from base_aux.versions.m2_version import *
from base_aux.base_lambdas.m1_lambda import *
from base_aux.base_values.m3_exceptions import *

from base_aux.tables.m1_table_obj import TableObj


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="schema, _EXPECTED",
    argvalues=[
        (dict(ATC=[1,]), True),
        (dict(ATC=[1,], PTB=[2,]), True),
        (dict(ATC=[1,], PTB=[2,]), True),
        (dict(ATC=[1,], PTB=(2,)), True),
        (dict(ATC=[], PTB=[]), True),
        (dict(ATC="atc", PTB=[1, 2, 3]), True),
        (dict(ATC="atc", PTB={1:1, 2:2, 3:3}), True),

        (dict(ATC=1), False),
        (dict(ATC=[1,], PTB=[]), False),
        (dict(ATC=[], PTB=0), False),
    ]
)
def test__validate_schema__and_raise_init(schema, _EXPECTED):
    Lambda(TableObj._validate_schema, schema=schema).check_expected__assert(_EXPECTED)
    Lambda(lambda: TableObj(**schema)).check_raised__assert(not _EXPECTED)


# =====================================================================================================================
