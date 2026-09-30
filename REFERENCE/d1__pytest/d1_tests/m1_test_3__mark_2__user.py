import pytest


# ======================================================================================================================
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
