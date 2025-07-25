import pytest
from base_aux.buses.m1_serial3_server import *
from base_aux.buses.m1_serial1_client import *
from base_aux.base_values.m5_value_valid2_variants import *
from base_aux.base_values.m5_value_valid3_unit import *
from base_aux.aux_text.m3_parser1_cmd_args_kwargs import *


# =====================================================================================================================
@pytest.mark.xfail  # FIXME: BROKEN
class Test__SerialServer_NoConnection:
    # @classmethod
    # def setup_class(cls):
    #     pass
    #
    # @classmethod
    # def teardown_class(cls):
    #     pass
    #
    def setup_method(self, method):
        pass
        self.Victim = type("Victim", (SerialServer_Example,), {})
    #
    # def teardown_method(self, method):
    #     pass

    # -----------------------------------------------------------------------------------------------------------------
    def test__cmd__script(self):
        victim = self.Victim()
        assert victim._cmd__(CmdArgsKwargsParser("script1")) == AnswerVariants.ERR__NAME_CMD_OR_PARAM
        assert victim._cmd__(CmdArgsKwargsParser("script script1")) == AnswerVariants.SUCCESS

    def test__LISTS(self):
        victim = self.Victim()
        assert set(victim._LIST__CMDS) == {
            "set", "get",
            "hello", "help", "echo",
            "upper", "lower",

            "cmd", "cmd_no_line",

            "script",
        }
        assert set(victim._LIST__SCRIPTS) == {
            "script1",
        }

    def test__cmd__cmd(self):
        victim = self.Victim()
        assert victim._cmd__(CmdArgsKwargsParser("cmd")) == AnswerVariants.SUCCESS
        assert victim._cmd__(CmdArgsKwargsParser("cmd_no_line")) == AnswerVariants.SUCCESS

    def test__cmd__echo(self):
        victim = self.Victim()
        assert victim._cmd__(CmdArgsKwargsParser("echo 123")) == "echo 123"
        assert victim._cmd__(CmdArgsKwargsParser("echo HELLO")) == "echo HELLO"

    def test__cmd__upper_lower(self):
        victim = self.Victim()
        assert victim._cmd__(CmdArgsKwargsParser("upper HELLO")) == "UPPER HELLO"
        assert victim._cmd__(CmdArgsKwargsParser("lower HELLO")) == "lower hello"

    def test__GET__single(self):
        victim = self.Victim()
        assert victim._cmd__(CmdArgsKwargsParser("hello123")) == AnswerVariants.ERR__NAME_CMD_OR_PARAM

        assert victim._cmd__(CmdArgsKwargsParser("get str")) == "str"
        assert victim._cmd__(CmdArgsKwargsParser("str")) == "str"
        assert victim._cmd__(CmdArgsKwargsParser("blanc")) == ""
        assert victim._cmd__(CmdArgsKwargsParser("zero")) == '0'

        assert victim._cmd__(CmdArgsKwargsParser("int")) == '1'
        assert victim._cmd__(CmdArgsKwargsParser("float")) == '1.1'

        assert victim._cmd__(CmdArgsKwargsParser("none")) == "None"
        assert victim._cmd__(CmdArgsKwargsParser("true")) == "True"
        assert victim._cmd__(CmdArgsKwargsParser("false")) == "False"

        try:
            float(victim._cmd__(CmdArgsKwargsParser("call")))
        except:
            assert False
        assert victim._cmd__(CmdArgsKwargsParser("exx")) == AnswerVariants.ERR__PARAM_CALLING

        assert victim._cmd__(CmdArgsKwargsParser("list")) == "[0, 1, 2]"
        assert victim._cmd__(CmdArgsKwargsParser("_set")) == "{0, 1, 2}"
        assert victim._cmd__(CmdArgsKwargsParser("get _set")) == "{0, 1, 2}"
        assert victim._cmd__(CmdArgsKwargsParser("dict_short")) == "{1: 11}"

    def test__GET__nested__list(self):
        victim = self.Victim()
        assert victim._cmd__(CmdArgsKwargsParser("list")) == "[0, 1, 2]"

        assert victim._cmd__(CmdArgsKwargsParser("list 1")) == "1"
        assert victim._cmd__(CmdArgsKwargsParser("list/1")) == "1"

        assert victim._cmd__(CmdArgsKwargsParser("get list 1")) == "1"
        assert victim._cmd__(CmdArgsKwargsParser("get list/1")) == "1"

        assert victim._cmd__(CmdArgsKwargsParser("list/10")) == AnswerVariants.ERR__NAME_CMD_OR_PARAM

        # -----
        assert victim._cmd__(CmdArgsKwargsParser("list_2")) == "[[11]]"
        assert victim._cmd__(CmdArgsKwargsParser("list_2/0")) == "[11]"
        assert victim._cmd__(CmdArgsKwargsParser("list_2/0/0")) == "11"

        assert victim._cmd__(CmdArgsKwargsParser("list_2 0 0")) == "11"
        assert victim._cmd__(CmdArgsKwargsParser("get list_2 0 0")) == "11"

    def test__GET__dict(self):
        # TODO: add BOOL/NONE
        victim = self.Victim()
        assert victim._cmd__(CmdArgsKwargsParser("dict_short_2")) == "{'HEllo': {1: 11}}"
        assert victim._cmd__(CmdArgsKwargsParser("get dict_short_2")) == "{'HEllo': {1: 11}}"

        assert victim._cmd__(CmdArgsKwargsParser("dict_short_2/hello")) == "{1: 11}"
        assert victim._cmd__(CmdArgsKwargsParser("dict_short_2 hello")) == "{1: 11}"
        assert victim._cmd__(CmdArgsKwargsParser("get dict_short_2 hello")) == "{1: 11}"
        assert victim._cmd__(CmdArgsKwargsParser("dict_short_2/hello11111")) == AnswerVariants.ERR__NAME_CMD_OR_PARAM

        assert victim._cmd__(CmdArgsKwargsParser("dict_short_2/hello/1")) == "11"
        assert victim._cmd__(CmdArgsKwargsParser("get dict_short_2/hello/1")) == "11"
        assert victim._cmd__(CmdArgsKwargsParser("dict_short_2 hello/1")) == "11"
        assert victim._cmd__(CmdArgsKwargsParser("get dict_short_2 hello/1")) == "11"
        assert victim._cmd__(CmdArgsKwargsParser("dict_short_2 hello 1")) == "11"
        assert victim._cmd__(CmdArgsKwargsParser("get dict_short_2 hello 1")) == "11"
        assert victim._cmd__(CmdArgsKwargsParser("dict_short_2/hello/11111")) == AnswerVariants.ERR__NAME_CMD_OR_PARAM

        assert victim._cmd__(CmdArgsKwargsParser("dict_short_2/hello/1/9/9/9/9/")) == AnswerVariants.ERR__NAME_CMD_OR_PARAM

    @pytest.mark.xfail   # FIXME: BROKEN
    def test__SET__level_first__type(self):
        victim = self.Victim()
        assert victim.PARAMS["VAR"] == ""

        # line_parsed = CmdArgsKwargsParser("var=True")
        # result = victim._cmd__(line_parsed)
        assert victim._cmd__(CmdArgsKwargsParser("var=True")) == AnswerVariants.SUCCESS
        assert victim.PARAMS["VAR"] is True

        assert victim._cmd__(CmdArgsKwargsParser("var=false")) == AnswerVariants.SUCCESS
        assert victim.PARAMS["VAR"] is False

        assert victim._cmd__(CmdArgsKwargsParser("var=null")) == AnswerVariants.SUCCESS
        assert victim.PARAMS["VAR"] is None

        assert victim._cmd__(CmdArgsKwargsParser("var=")) == AnswerVariants.SUCCESS
        assert victim.PARAMS["VAR"] == ""

        # assert victim._cmd__(CmdArgsKwargsParser("var=''")) == AnswerVariants.SUCCESS
        # assert victim.PARAMS["VAR"] == "''"                             # TODO: convert to expected!!!

        assert victim._cmd__(CmdArgsKwargsParser("var=0")) == AnswerVariants.SUCCESS
        assert victim.PARAMS["VAR"] == 0

        assert victim._cmd__(CmdArgsKwargsParser("var=123")) == AnswerVariants.SUCCESS
        assert victim.PARAMS["VAR"] == 123

        assert victim._cmd__(CmdArgsKwargsParser("var=1.1")) == AnswerVariants.SUCCESS
        assert victim.PARAMS["VAR"] == 1.1
        assert victim._cmd__(CmdArgsKwargsParser("var=1,1")) == AnswerVariants.SUCCESS
        assert victim.PARAMS["VAR"] != 1.1

        # ITERABLES --------------------
        assert victim._cmd__(CmdArgsKwargsParser("var=[]")) == AnswerVariants.SUCCESS
        assert victim.PARAMS["VAR"] == []

        # assert victim._cmd__(CmdArgsKwargsParser("var=[1, 2]")) == AnswerVariants.SUCCESS  # TODO: CLEAR ALL INTERNAL SPACES!!!
        assert victim._cmd__(CmdArgsKwargsParser("var=[1,2]")) == AnswerVariants.SUCCESS
        assert victim.PARAMS["VAR"] == [1, 2]

    @pytest.mark.xfail   # FIXME: BROKEN
    def test__SET__level_first__syntax(self):
        victim = self.Victim()
        assert victim.PARAMS["INT"] == 1

        assert victim._cmd__(CmdArgsKwargsParser("set int=10")) == AnswerVariants.SUCCESS
        assert victim.PARAMS["INT"] == 10

        assert victim._cmd__(CmdArgsKwargsParser("int=11")) == AnswerVariants.SUCCESS
        assert victim.PARAMS["INT"] == 11

        assert victim._cmd__(CmdArgsKwargsParser("int    =12")) == AnswerVariants.SUCCESS
        assert victim.PARAMS["INT"] == 12

        assert victim._cmd__(CmdArgsKwargsParser("int=     13")) == AnswerVariants.SUCCESS
        assert victim.PARAMS["INT"] == 13

        assert victim._cmd__(CmdArgsKwargsParser("   int       =     14   ")) == AnswerVariants.SUCCESS
        assert victim.PARAMS["INT"] == 14

        assert victim._cmd__(CmdArgsKwargsParser("   int =======     15   ")) == AnswerVariants.SUCCESS
        assert victim.PARAMS["INT"] == 15

        # several
        assert victim._cmd__(CmdArgsKwargsParser("var 1 int=16")) == AnswerVariants.ERR__ARGS_VALIDATION
        assert victim.PARAMS["INT"] == 15

        victim.PARAMS["VAR"] = 1
        assert victim.PARAMS["VAR"] == 1
        assert victim._cmd__(CmdArgsKwargsParser("var=11 int=16")) == AnswerVariants.SUCCESS
        assert victim.PARAMS["VAR"] == 11
        assert victim.PARAMS["INT"] == 16

        # NOCHANGES if wrong name exists
        assert victim._cmd__(CmdArgsKwargsParser("var=110 int123=160")) == AnswerVariants.ERR__NAME_CMD_OR_PARAM
        assert victim.PARAMS["VAR"] == 11
        assert victim.PARAMS["INT"] == 16

    @pytest.mark.xfail   # FIXME: BROKEN
    def test__ValueUnit(self):
        victim = self.Victim()
        victim.PARAMS["UNIT123"] = ValueUnit(1, unit="V")
        assert victim.PARAMS["UNIT123"] == ValueUnit(1, unit="V")
        assert victim._cmd__(CmdArgsKwargsParser("unit123")) == "1V"

        assert victim._cmd__(CmdArgsKwargsParser("unit123=11")) == AnswerVariants.SUCCESS
        assert victim._cmd__(CmdArgsKwargsParser("unit123")) == "11V"

        assert victim._cmd__(CmdArgsKwargsParser("unit123=1.00")) == AnswerVariants.SUCCESS
        assert victim._cmd__(CmdArgsKwargsParser("unit123")) == "1.0V"

        assert victim.PARAMS["UNIT123"] == ValueUnit(1.0, unit="V")

    @pytest.mark.xfail   # FIXME: BROKEN
    def test__ValueVariants(self):
        victim = self.Victim()

        victim.PARAMS["VARIANT"] = ValueVariants(220, variants=[220, 380])
        assert victim._cmd__(CmdArgsKwargsParser("variant")) == "220"

        assert victim._cmd__(CmdArgsKwargsParser("variant=11")) == AnswerVariants.ERR__VALUE_INCOMPATIBLE
        assert victim._cmd__(CmdArgsKwargsParser("variant")) == "220"

        assert victim._cmd__(CmdArgsKwargsParser("variant=380")) == AnswerVariants.SUCCESS
        assert victim._cmd__(CmdArgsKwargsParser("variant")) == "380"

        assert victim.PARAMS["VARIANT"] == ValueVariants(380, variants=[220, 380])

    def test__list_results(self):
        victim = self.Victim()
        victim.PARAMS["VARIANT"] = ValueVariants(220, variants=[220, 380])
        victim.PARAMS["UNIT123"] = ValueUnit(1, unit="V")

        assert victim.list_param_results(["VARIANT", "UNIT123"]) == ["VARIANT=220", "UNIT123=1V"]
        assert victim.list_param_results(["cmd", "unit123"]) == [f"cmd={AnswerVariants.SUCCESS}", "unit123=1V"]


# =====================================================================================================================
@pytest.mark.xfail  # FIXME: BROKEN
class Test_SerialServer_WithConnection:
    Victim: type[SerialClient] = type("Victim", (SerialClient,), {})
    victim: SerialClient = None

    @classmethod
    def setup_class(cls):
        if cls.Victim.addresses_paired__count() < 1:
            msg = f"[ERROR] need connect TWO SerialPorts"
            print(msg)
            raise Exception(msg)

    @classmethod
    def teardown_class(cls):
        pass
        if cls.victim:
            cls.victim.disconnect()

    # def setup_method(self, method):
    #     pass
    #
    # def teardown_method(self, method):
    #     pass

    # -----------------------------------------------------------------------------------------------------------------
    def test__1(self):
        # server start
        server = SerialServer_Example()
        server.connect()

        class Victim(SerialClient):
            _ADDRESS = Enum__AddressAutoAcceptVariant.FIRST_FREE__ANSWER_VALID

            def address__validate(self) -> bool | None | NoReturn:
                return server.HELLO_MSG[0] in self.write_read("hello").list_output()

        victim = Victim()
        assert victim.connect()

        assert victim.write_read__last("echo 123") == "echo 123"
        assert victim.write_read__last("CMD_NOT_ESISTS") == server.ANSWER.ERR__NAME_CMD_OR_PARAM
        assert victim.write_read__last("upper hello") == "UPPER HELLO"


# =====================================================================================================================
