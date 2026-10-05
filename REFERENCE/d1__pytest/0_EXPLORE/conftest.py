# [conftest.py]
import pytest

from base_aux.base_types.m2_info import ObjectInfo
OPT_NAME = "--ssh"



def pytest_collection_modifyitems(session, config, items):
    for item in items:
        ObjectInfo(item, max_line_len=200).print()
    pytest.exit()

def pytest_addoption(parser):
    parser.addoption("--skip-slow", action="store_true", default=False)
    parser.addoption(
        OPT_NAME,
        action="store",
        nargs="?",
        const="VALUE_CONST",
        default="VALUE_DEF",
        help="SSH-хост: без значения → harvest05",
    )

# [test.py]
def test__in_conftest(pytestconfig):
    value = pytestconfig.getoption(OPT_NAME)
    print()
    print(f"{OPT_NAME}=[{value}]")
