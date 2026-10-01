# [conftest.py]
OPT_NAME = "--ssh"

def pytest_addoption(parser):
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
