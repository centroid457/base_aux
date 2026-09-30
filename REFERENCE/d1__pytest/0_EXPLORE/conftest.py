def pytest_addoption(parser):
    parser.addoption(
        "--opt1",
        action="store",
        default=True,
        help="..."
    )