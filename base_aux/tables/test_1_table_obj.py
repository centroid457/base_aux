from base_aux.versions.m2_version import *
from base_aux.base_lambdas.m1_lambda import *
from base_aux.base_values.m3_exceptions import *

from base_aux.tables.m1_table_obj import TableObj


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="schema, _EXP_valid, _EXP_count_lines, _EXP_count_col",
    argvalues=[
        # CORRECT -------------
        (dict(), True, 0, 0),
        (dict(ATC=[]), True, 1, 0),
        (dict(ATC=[1,]), True, 1, 1),
        (dict(ATC=[1,2,]), True, 1, 2),
        (dict(ATC=[1,], PTB=[2,]), True, 2, 1),
        (dict(ATC=[1,], PTB=(2,)), True, 2, 1),
        (dict(ATC=[1,], PTB={2,}), True, 2, 1),
        (dict(ATC=[], PTB=[]), True, 2, 0),

        (dict(ATC="atc", PTB=[1, 2, 3]), True, 2, 3),
        (dict(ATC="atc", PTB={1:1, 2:2, 3:3}), True, 2, 3),

        # INCORRECT -----------
        (dict(ATC=1), False, None, None),
        (dict(ATC=[1,], PTB=[]), False, None, None),
        (dict(ATC=[], PTB=0), False, None, None),
        (1, False, None, None),
        ({1:1}, False, None, None),
    ]
)
def test__full(schema, _EXP_valid, _EXP_count_lines, _EXP_count_col):
    Lambda(TableObj._validate_schema, schema=schema).check_expected__assert(_EXP_valid)
    Lambda(lambda: TableObj(**schema)).check_raised__assert(not _EXP_valid)

    if _EXP_valid:
        Lambda(TableObj(**schema).schema).check_expected__assert(schema)
        Lambda(TableObj(**schema).count_lines).check_expected__assert(_EXP_count_lines)
        Lambda(TableObj(**schema).count_columns).check_expected__assert(_EXP_count_col)

        for name, value in schema.items():
            Lambda(lambda: getattr(TableObj(**schema), name)).check_expected__assert(value)
            Lambda(lambda: TableObj(**schema)[name]).check_expected__assert(value)

        Lambda(lambda: getattr(TableObj(**schema), "NONAME")).check_expected__assert(Exception)
        Lambda(lambda: TableObj(**schema)["NONAME"]).check_expected__assert(Exception)


# =====================================================================================================================
