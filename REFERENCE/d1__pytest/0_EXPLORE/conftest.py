# [conftest.py]
def pytest_addoption(parser):
    parser.addoption(
        "--opt1",
        action="store",
        default=True,
        help="..."
    )

# [test.py]
def test_1(pytestconfig):
    value = pytestconfig.getoption("--opt1")
    print(f"{value=}")
    assert value
