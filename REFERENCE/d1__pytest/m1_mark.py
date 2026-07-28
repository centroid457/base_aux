import pytest


# ======================================================================================================================
# 6. МАРКЕРЫ: skip, skipif, xfail, пользовательские
# =============================================================================
@pytest.mark.skip(reason="Этот тест пока не реализован")
def test_not_ready():
    assert False

import sys
@pytest.mark.skipif(sys.version_info < (3, 10), reason="Требуется Python 3.10+")
def test_only_recent_python():
    # match/case доступен с 3.10
    code = """
match 42:
    case 42:
        print('ok')
"""
    exec(code)  # упрощённо, просто для демонстрации

@pytest.mark.xfail(reason="Известная ошибка, исправим позже")
def test_known_bug():
    assert 1 == 2  # тест помечается как ожидаемо падающий (xfail)

# -----------------------------------------------------------------------------
# ВАЖНО: если xfail-тест внезапно начинает проходить, он будет помечен как XPASS
# (неожиданный успех). Это сигнал, что ошибка исправлена и маркер можно убрать.
# -----------------------------------------------------------------------------

# =============================================================================
# Пользовательский маркер (НУЖНО зарегистрировать в CONF!!!)
"""
если не зарегистрировать - будут WARNINGS!!! в выводе 
=========================================================== warnings summary ===========================================================
test__harvest.py:148
  C:\__STARICHENKO_Element\PROJECTS\abc=base_aux\prj_1_harvest_tests\test__harvest.py:148: PytestUnknownMarkWarning: Unknown pytest.mark.DET - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
    @pytest.mark.DET

test__harvest.py:178
  C:\__STARICHENKO_Element\PROJECTS\abc=base_aux\prj_1_harvest_tests\test__harvest.py:178: PytestUnknownMarkWarning: Unknown pytest.mark.PRE - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
    @pytest.mark.PRE
"""
@pytest.mark.slow
def test_slow_operation():
    import time
    time.sleep(0.1)  # имитация долгой операции
    assert True


# ======================================================================================================================
