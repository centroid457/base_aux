import pytest

from base_aux.aux_pytester import *
from base_aux.aux_attr import check_name__buildin


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="source, EXPECTED",
    argvalues=[
        ("_", False),
        ("__", False),
        ("____", False),

        ("___abc___", True),
        ("__abc__", True),
        ("__abc_", False),
        ("__abc", False),

        ("_abc__", False),
        ("_abc_", False),
        ("_abc", False),

        ("abc__", False),
        ("abc_", False),
        ("abc", False),
    ]
)
def test__name_is_build_in(source, _EXPECTED):
    func_link = check_name__buildin(source)
    pytest_func_tester__no_args_kwargs(func_link, _EXPECTED)


# =====================================================================================================================
