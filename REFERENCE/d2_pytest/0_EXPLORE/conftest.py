# [conftest.py]
import pytest
from base_aux.base_types.m2_info import ObjectInfo

# @pytest.hookimpl(hookwrapper=True)
# def pytest_runtest_makereport(item, call):
#     from _pytest.outcomes import Exit
#
#     print(f"[pytest.STAGE.pytest_runtest_makereport]START")
#
#     for obj in (item, call):
#         print()
#         print(f"{obj=}")
#         ObjectInfo(item).print()
#
#     # ПОМЕТКА выхода из тестирования pytest.exit как FAILED! если так не сделать то будет похоже на SKIPPED
#     outcome = yield
#     report = outcome.get_result()
#     if call.excinfo and isinstance(call.excinfo.value, Exit):
#         # pytest.exit() внутри теста — принудительно делаем failed
#         report.outcome = "failed"
#         report.longrepr = f"Фатальная остановка: {call.excinfo.value}"
#
#     print(f"[pytest.STAGE.pytest_runtest_makereport]FINISH")


# [test.py]
def test__in_conftest__1_ok(pytestconfig):
    pass

def test__in_conftest__2_fail(pytestconfig):
    raise Exception("raised")

def test__in_conftest__3_skip(pytestconfig):
    pytest.skip("skip")

def test__in_conftest__4_exit(pytestconfig):
    pytest.exit(f"exit")
