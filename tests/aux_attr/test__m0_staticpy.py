import pytest

from base_aux.aux_pytester.m1_pytest_aux import PytestAux
from base_aux.aux_attr.m0_static import check_name__buildin


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="source, _EXPECTED",
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
    PytestAux(func_link).assert_check(_EXPECTED)


# =====================================================================================================================
