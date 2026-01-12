from base_aux.versions.m2_version import *
from base_aux.base_lambdas.m1_lambda import *
from base_aux.base_values.m3_exceptions import *

from base_aux.tables.m1_table_obj import TableObj
from base_aux.tables.m2_table_column import TableColumn


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="table, col, _EXP_count_lines, _EXP_count_col",
    argvalues=[
        # CORRECT -------------
        (TableObj(), 0, 0),
        (TableObj(ATC=[]), 1, 0),
        (TableObj(ATC=[1,]), 1, 1),
        (TableObj(ATC=[1,2,]), 1, 2),
        (TableObj(ATC=[1,], PTB=[2,]), 2, 1),
        (TableObj(ATC=[1,], PTB=(2,)), 2, 1),
        (TableObj(ATC=[1,], PTB={2,}), 2, 1),
        (TableObj(ATC=[], PTB=[]), 2, 0),

        (TableObj(ATC="atc", PTB=[1, 2, 3]), 2, 3),
        (TableObj(ATC="atc", PTB={1:1, 2:2, 3:3}), 2, 3),
    ]
)
def test__full(table, col, _EXP_count_lines, _EXP_count_col):
    # FIXME: FINISH
    # FIXME: FINISH
    # FIXME: FINISH
    # FIXME: FINISH
    # FIXME: FINISH
    # FIXME: FINISH
    # FIXME: FINISH
    # FIXME: FINISH
    # FIXME: FINISH
    raise Exception()
    Lambda(TableColumn(table=table, column=col)).check_expected__assert(_EXP_valid)
    Lambda(lambda: TableObj(**schema)).check_raised__assert(not _EXP_valid)


# =====================================================================================================================
