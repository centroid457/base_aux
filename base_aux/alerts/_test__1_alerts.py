from base_aux.alerts.m1_alerts1_smtp import *
from base_aux.alerts.m1_alerts2_telegram import *
from base_aux.lambdas.m1_lambda import *


# =====================================================================================================================
# TODO: separate by base class and use victimCls as attr!

@pytest.mark.skip
@pytest.mark.skipif(Lambda(AlertSmtp.CONN_AUTH).check_raise(), reason="no file")
class Test__1:
    @pytest.mark.parametrize(argnames="cls", argvalues=[
        AlertSmtp,
        AlertTelegram,
    ])
    def test__send_single(self, cls):
        victim = cls()
        victim.send_msg("single")
        assert victim.wait()

    @pytest.mark.parametrize(argnames="victim", argvalues=[
        # AlertSmtp,
        # AlertTelegram,
    ])
    @pytest.mark.parametrize(argnames="subject, msg, _subtype", argvalues=[
        (None, "zero", None),
        ("", "plain123", "plain123"),
        ("plain", "plain", "plain"),
        ("html", "<p><font color='red'>html(red)</font></p>", "html")
    ])
    def test__send_single__parametrized(self, victim, subject, msg, _subtype):
        victim = victim()
        victim.send_msg(subject=subject, body=msg, _subtype=_subtype)
        assert victim.result_sent_all is not True
        victim.wait()
        assert victim.result_sent_all is True

    @pytest.mark.parametrize(argnames="victim", argvalues=[
        AlertSmtp,
        # AlertTelegram
    ])
    def test__send_multy__result_wait(self, victim):
        pass
        # assert victim("multy1").wait() is True
        # assert victim("multy2").wait() is True

    @pytest.mark.parametrize(argnames="victim", argvalues=[
        AlertSmtp,
        # AlertTelegram
    ])
    def test__send_multy__wait_join(self, victim):
        return

        thread1 = victim("thread1")
        thread2 = victim("thread2")

        thread1.wait()
        thread2.wait()

        assert thread1._result is True
        assert thread2._result is True


# =====================================================================================================================
# class Test_AlertHttp:
#     Victim = AlertHttp
#     def test__send_single(self, victim):
#         assert self.Victim({}).result_wait() is True


# =====================================================================================================================
