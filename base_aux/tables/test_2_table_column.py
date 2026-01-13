from base_aux.versions.m2_version import *
from base_aux.base_lambdas.m1_lambda import *
from base_aux.base_values.m3_exceptions import *

from base_aux.tables.m1_table_obj import TableObj
from base_aux.tables.m2_table_column import TableColumn


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="data, col, name, _EXPECTED",
    argvalues=[
        # TableObj -------------
        (dict(), 0, "ATC", Exception),

        (dict(ATC=[]), 0, "ATC", Exception),
        (dict(ATC=[]), 1, "ATC", Exception),

        (dict(ATC=[1,]), 0, "ATC", 1),
        (dict(ATC=[1,]), 1, "ATC", Exception),
        (dict(ATC=[1,]), 0, "atc", Exception),

        (dict(ATC=[1,2,]), 1, "ATC", 2),

        (dict(ATC=[1,], PTB=[2,]), 0, "PTB", 2),
        (dict(ATC=[1,], PTB=(2,)), 0, "PTB", 2),
        (dict(ATC=[1,], PTB={2,}), 0, "PTB", Exception),

        (dict(ATC="atc", PTB=[1, 2, 3]), 2, "ATC", "c"),
    ]
)
def test__full(data, col, name, _EXPECTED):
    for victim in [data, TableObj(**data)]:
        Lambda(lambda: TableColumn(table=victim, column=col)[name]).check_expected__assert(_EXPECTED)
        Lambda(lambda: getattr(TableColumn(table=victim, column=col), name)).check_expected__assert(_EXPECTED)


# =====================================================================================================================
