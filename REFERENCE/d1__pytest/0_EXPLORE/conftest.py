# [conftest.py]
def pytest_addoption(parser):
    parser.addoption(
        "--opt1",
        action="store_true",
        # default=True,
        help="..."
    )

# [test.py]
def test__in_conftest(pytestconfig):
    name = "--opt1"
    value = pytestconfig.getoption(name)
    print()
    print(f"{name}=[{value}]")
