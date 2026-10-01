# [conftest.py]
def pytest_addoption(parser):
    parser.addoption(
        "--opt1",
        action="store_true",
        # default=True,
        help="..."
    )

# [test.py]
def test__in_congtest(pytestconfig):
    value = pytestconfig.getoption("--opt1")
    print(f"{value=}")
    assert value
