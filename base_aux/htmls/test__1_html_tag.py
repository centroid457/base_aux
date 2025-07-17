import pytest
from base_aux.base_lambdas.m1_lambda import *

from base_aux.htmls.m1_html_tag import *


# =====================================================================================================================
# TODO: FINISH!!!
@pytest.mark.parametrize(
    argnames="source, chains, _EXPECTED",
    argvalues=[
        # (1, (lambda x: x+1, ), 2),
    ]
)
def test__chains(source, chains, _EXPECTED):
    Lambda(HtmlTagParser(source=source).resolve).expect__check_assert(_EXPECTED)


# =====================================================================================================================
