import pytest

from base_aux.monitors.m1_imap import *
from base_aux.monitors.m2_url_tag2__derivatives import *
from base_aux.alerts.m1_alerts1_smtp import *
from base_aux.aux_callable.m1_callable_aux import *


# =====================================================================================================================
# TODO: create full auto test!


# =====================================================================================================================
@pytest.mark.skipif(CallableAux(AlertSmtp.CONN_AUTH).check_raise(), reason="no file")
class Test_UrlTag:
    def test__1(self):
        Monitor_DonorSvetofor()

    def test__2(self):
        Monitor_CbrKeyRate()

    def test__3(self):
        Monitor_ConquestS23_comments()

    def test__4(self):
        Monitor_Sportmaster_AdidasSupernova2M()

    def test__5(self):
        Monitor_AcraRaiting_GTLC()


# =====================================================================================================================
@pytest.mark.skipif(CallableAux(AlertSmtp.CONN_AUTH).check_raise(), reason="no file")
@pytest.mark.parametrize(argnames="pattern", argvalues=[None, r"\[ALERT\]test1"])
def test__imap(pattern):
    _subj_name = "test1"

    AlertSmtp(_subj_name=_subj_name)

    victim = MonitorImap
    victim.stop_flag = True
    victim.SUBJECT_REGEXP = pattern

    for i in range(3):
        victim_inst = victim()
        victim_inst.wait_cycle()
        if f"[ALERT]{_subj_name}" in victim_inst._detected:
            break

    assert f"[ALERT]{_subj_name}" in victim_inst._detected


# =====================================================================================================================
# Monitor_DonorSvetofor()
# Monitor_CbrKeyRate()
Monitor_ConquestS23_comments()
# Monitor_AcraRaiting_GTLC()
