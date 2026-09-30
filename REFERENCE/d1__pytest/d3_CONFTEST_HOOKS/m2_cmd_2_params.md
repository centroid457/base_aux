# 

```python
import pytest

def pytest_addoption(parser):
    # 0=ОБЯЗАТЕЛЬНОЕ УКАЗАНИЕ
    parser.addoption(
        "--opt1",
        action="store_true",
        # default=False,
        help="обязательное указание"
    )

def test__1(config):
    assert config.getoption("--opt1")
```