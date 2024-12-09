from typing import *
import pytest

from base_aux.pytester import *
from base_aux.objects import *


# =====================================================================================================================
values_elementary_single = [None, True, False, 0, 11, 11.22]
CLASSES__AS_FUNC: list = [ClsInt, ClsStr, ClsList, ClsSet, ClsDict, ]   # actually this is keep all buildIn


# =====================================================================================================================
class Test__1:
    @classmethod
    def setup_class(cls):
        pass
        cls.Victim = TypeChecker

    # @classmethod
    # def teardown_class(cls):
    #     pass
    #
    # def setup_method(self, method):
    #     pass
    #
    # def teardown_method(self, method):
    #     pass

    # -----------------------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        argnames="args, _EXPECTED",
        argvalues=[
            ("_", False),
            ("__", False),
            ("____", False),

            ("___abc___", True),
            ("__abc__", True),
            ("__abc_", False),
            ("__abc", False),

            ("_abc__", False),
            ("_abc_", False),
            ("_abc", False),

            ("abc__", False),
            ("abc_", False),
            ("abc", False),
        ]
    )
    def test__name_is_build_in(self, args, _EXPECTED):
        victim = self.Victim.check__name_is_build_in
        pytest_func_tester__no_kwargs(victim, args, _EXPECTED)

    # =================================================================================================================
    @pytest.mark.parametrize(
        argnames="args, _EXPECTED",
        argvalues=[
            (None, True),
            (True, True),
            (False, True),
            (0, False),
            (111, False),
            (111.222, False),
            ("str", False),
            (b"bytes", False),

            (((111, ),), False),
            (([111, ],), False),
            (({111, },), False),
            (({111: 222, },), False),

            (int, False),
            (int(1), False),
            (str, False),
            (str(1), False),

            (Exception, False),
            (Exception(), False),
            (Exx, False),
            (Exx(), False),

            (Cls, False),
            (Cls(), False),
            (ClsInt, False),
            (ClsInt(), False),    # int() == 0!!!

            (FUNC, False),
            (LAMBDA, False),
            (ClsCallNone, False),
            (ClsCallNone(), False),
            (ClsCallNone()(), True),
            (ClsCall().meth, False),
            (ClsFullTypes.attrNone, True),
            (ClsFullTypes().attrNone, True),

            *[(class_i, False) for class_i in CLASSES__AS_FUNC]
        ]
    )
    def test__check__bool_none(self, args, _EXPECTED):
        victim = self.Victim.check__bool_none
        pytest_func_tester__no_kwargs(victim, args, _EXPECTED)

    @pytest.mark.parametrize(
        argnames="args, _EXPECTED",
        argvalues=[
            (None, True),
            (True, True),
            (False, True),
            (0, True),
            (111, True),
            (111.222, True),
            ("str", True),
            (b"bytes", True),

            (((111, ),), True),
            (([111, ],), True),
            (({111, },), True),
            (({111: 222, },), True),

            (int, False),
            (int(1), True),
            (str, False),
            (str(1), True),

            (Exception, False),
            (Exception(), False),
            (Exx, False),
            (Exx(), False),

            (Cls, False),
            (Cls(), False),
            (ClsInt, False),
            (ClsInt(), True),    # int() == 0!!!

            (FUNC, False),
            (LAMBDA, False),
            (ClsCallNone, False),
            (ClsCallNone(), False),
            (ClsCallNone()(), True),
            (ClsCall().meth, False),
            (ClsFullTypes.attrNone, True),
            (ClsFullTypes().attrNone, True),

            *[(class_i, False) for class_i in CLASSES__AS_FUNC]
        ]
    )
    def test__check__elementary(self, args, _EXPECTED):
        victim = self.Victim.check__elementary
        pytest_func_tester__no_kwargs(victim, args, _EXPECTED)

    @pytest.mark.parametrize(
        argnames="args, _EXPECTED",
        argvalues=[
            (None, True),
            (True, True),
            (False, True),
            (0, True),
            (111, True),
            (111.222, True),
            ("str", True),
            (b"bytes", True),

            (((111, ),), False),
            (([111, ],), False),
            (({111, },), False),
            (({111: 222, },), False),

            (int, False),
            (int(1), True),
            (str, False),
            (str(1), True),

            (Exception, False),
            (Exception(), False),
            (Exx, False),
            (Exx(), False),

            (Cls, False),
            (Cls(), False),
            (ClsInt, False),
            (ClsInt(), True),    # int() == 0!!!

            (FUNC, False),
            (LAMBDA, False),
            (ClsCallNone, False),
            (ClsCallNone(), False),
            (ClsCallNone()(), True),
            (ClsCall.meth, False),
            (ClsCall().meth, False),
            (ClsFullTypes.attrNone, True),
            (ClsFullTypes().attrNone, True),

            *[(class_i, False) for class_i in CLASSES__AS_FUNC]
        ]
    )
    def test__check__elementary_single(self, args, _EXPECTED):
        victim = self.Victim.check__elementary_single
        pytest_func_tester__no_kwargs(victim, args, _EXPECTED)

    @pytest.mark.parametrize(
        argnames="args, _EXPECTED",
        argvalues=[
            (None, False),
            (True, True),
            (False, True),
            (0, True),
            (111, True),
            (111.222, True),
            ("str", True),
            (b"bytes", True),

            (((111, ),), False),
            (([111, ],), False),
            (({111, },), False),
            (({111: 222, },), False),

            (int, False),
            (int(1), True),
            (str, False),
            (str(1), True),

            (Exception, False),
            (Exception(), False),
            (Exx, False),
            (Exx(), False),

            (Cls, False),
            (Cls(), False),
            (ClsInt, False),
            (ClsInt(), True),    # int() == 0!!!

            (FUNC, False),
            (LAMBDA, False),
            (ClsCallNone, False),
            (ClsCallNone(), False),
            (ClsCallNone()(), False),
            (ClsCall.meth, False),
            (ClsCall().meth, False),
            (ClsFullTypes.attrNone, False),
            (ClsFullTypes().attrNone, False),

            *[(class_i, False) for class_i in CLASSES__AS_FUNC]
        ]
    )
    def test__check__elementary_single_not_none(self, args, _EXPECTED):
        victim = self.Victim.check__elementary_single_not_none
        pytest_func_tester__no_kwargs(victim, args, _EXPECTED)

    @pytest.mark.parametrize(
        argnames="args, _EXPECTED",
        argvalues=[
            (None, False),
            (True, False),
            (False, False),
            (0, False),
            (111, False),
            (111.222, False),
            ("str", False),
            (b"bytes", False),

            (((111, ),), True),
            (([111, ],), True),
            (({111, },), True),
            (({111: 222, },), True),

            (int, False),
            (int(1), False),
            (str, False),
            (str(1), False),

            (Exception, False),
            (Exception(), False),
            (Exx, False),
            (Exx(), False),

            (Cls, False),
            (Cls(), False),
            (ClsInt, False),
            (ClsInt(), False),    # int() == 0!!!

            (FUNC, False),
            (LAMBDA, False),
            (ClsCallNone, False),
            (ClsCallNone(), False),
            (ClsCallNone()(), False),
            (ClsCall.meth, False),
            (ClsCall().meth, False),
            (ClsFullTypes.attrNone, False),
            (ClsFullTypes().attrNone, False),

            *[(class_i, False) for class_i in CLASSES__AS_FUNC]
        ]
    )
    def test__check__elementary_collection(self, args, _EXPECTED):
        victim = self.Victim.check__elementary_collection
        pytest_func_tester__no_kwargs(victim, args, _EXPECTED)

    @pytest.mark.parametrize(
        argnames="args, _EXPECTED",
        argvalues=[
            (None, False),
            (True, False),
            (False, False),
            (0, False),
            (111, False),
            (111.222, False),
            ("str", False),
            (b"bytes", False),

            (((111, ),), True),
            (([111, ],), True),
            (({111, },), True),
            (({111: 222, },), False),

            (int, False),
            (int(1), False),
            (str, False),
            (str(1), False),

            (Exception, False),
            (Exception(), False),
            (Exx, False),
            (Exx(), False),

            (Cls, False),
            (Cls(), False),
            (ClsInt, False),
            (ClsInt(), False),    # int() == 0!!!

            (FUNC, False),
            (LAMBDA, False),
            (ClsCallNone, False),
            (ClsCallNone(), False),
            (ClsCallNone()(), False),
            (ClsCall.meth, False),
            (ClsCall().meth, False),
            (ClsFullTypes.attrNone, False),
            (ClsFullTypes().attrNone, False),

            *[(class_i, False) for class_i in CLASSES__AS_FUNC]
        ]
    )
    def test__check__elementary_collection_not_dict(self, args, _EXPECTED):
        victim = self.Victim.check__elementary_collection_not_dict
        pytest_func_tester__no_kwargs(victim, args, _EXPECTED)

    # -----------------------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        argnames="args, _EXPECTED",
        argvalues=[
            (("str", True, True), True),
            (("str", True, False), False),

            ((b"bytes", True, True), True),
            ((b"bytes", True, False), False),

            # -----------------------
            (None, False),
            (True, False),
            (False, False),
            (0, False),
            (111, False),
            (111.222, False),
            ("str", True),
            (b"bytes", True),

            (((111, ),), True),
            (([111, ],), True),
            (({111, },), True),
            (({111: 222, },), True),
            (({111: 222, }, True, True), True),
            (({111: 222, }, False, True), False),

            (int, False),
            (int(1), False),
            (str, True),        # not clear!!!
            (str(1), True),

            (Exception, False),
            (Exception(), False),
            (Exx, False),
            (Exx(), False),

            (Cls, False),
            (Cls(), False),
            (ClsInt, False),
            (ClsInt(), False),

            (FUNC, False),
            (LAMBDA, False),
            (ClsCallNone, False),
            (ClsCallNone(), False),
            (ClsCallNone()(), False),
            (ClsCall.meth, False),
            (ClsCall().meth, False),
            (ClsFullTypes.attrNone, False),
            (ClsFullTypes().attrNone, False),

            # *[(class_i, False) for class_i in CLASSES__AS_FUNC]
        ]
    )
    def test__iterable(self, args, _EXPECTED):
        victim = self.Victim.check__iterable
        pytest_func_tester__no_kwargs(victim, args, _EXPECTED)

    @pytest.mark.parametrize(
        argnames="args, _EXPECTED",
        argvalues=[
            (None, False),
            (True, False),
            (False, False),
            (0, False),
            (111, False),
            (111.222, False),
            ("str", False),
            (b"bytes", False),

            (((111, ),), True),
            (([111, ],), True),
            (({111, },), True),
            (({111: 222, },), True),

            (int, False),
            (int(1), False),
            (str, True),        # not clear!!!
            (str(1), False),

            (Exception, False),
            (Exception(), False),
            (Exx, False),
            (Exx(), False),

            (Cls, False),
            (Cls(), False),
            (ClsInt, False),
            (ClsInt(), False),

            (FUNC, False),
            (LAMBDA, False),
            (ClsCallNone, False),
            (ClsCallNone(), False),
            (ClsCallNone()(), False),
            (ClsCall.meth, False),
            (ClsCall().meth, False),
            (ClsFullTypes.attrNone, False),
            (ClsFullTypes().attrNone, False),

            # *[(class_i, False) for class_i in CLASSES__AS_FUNC]
        ]
    )
    def test__iterable_not_str(self, args, _EXPECTED):
        victim = self.Victim.check__iterable_not_str
        pytest_func_tester__no_kwargs(victim, args, _EXPECTED)

    # CALLABLE --------------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        argnames="args, _EXPECTED",
        argvalues=[
            (None, False),
            (True, False),
            (False, False),
            (0, False),
            (111, False),
            (111.222, False),
            ("str", False),
            (b"bytes", False),

            (((111, ),), False),
            (([111, ],), False),
            (({111, },), False),
            (({111: 222, },), False),

            (int, True),
            (int(1), False),
            (str, True),
            (str(1), False),

            (Exception, False),
            (Exception(), False),
            (Exx, False),
            (Exx(), False),

            (Cls, False),
            (Cls(), False),
            (ClsInt, True),
            (ClsInt(), False),    # int() == 0!!!

            (FUNC, True),
            (LAMBDA, True),
            (ClsCallNone, False),
            (ClsCallNone(), True),
            (ClsCallNone()(), False),
            (ClsCall.meth, True),
            (ClsCall().meth, True),
            (ClsFullTypes.attrNone, False),
            (ClsFullTypes().attrNone, False),

            *[(class_i, True) for class_i in CLASSES__AS_FUNC]
        ]
    )
    def test__check__callable_func_meth_inst(self, args, _EXPECTED):
        victim = self.Victim.check__callable_func_meth_inst
        pytest_func_tester__no_kwargs(victim, args, _EXPECTED)

    @pytest.mark.parametrize(
        argnames="args, _EXPECTED",
        argvalues=[
            (None, False),
            (True, False),
            (False, False),
            (0, False),
            (111, False),
            (111.222, False),
            ("str", False),
            (b"bytes", False),

            (((111, ),), False),
            (([111, ],), False),
            (({111, },), False),
            (({111: 222, },), False),

            (int, True),
            (int(1), False),
            (str, True),
            (str(1), False),

            (Exception, False),
            (Exception(), False),
            (Exx, False),
            (Exx(), False),

            (Cls, False),
            (Cls(), False),
            (ClsInt, True),
            (ClsInt(), False),    # int() == 0!!!

            (FUNC, True),
            (LAMBDA, True),
            (ClsCallNone, False),
            (ClsCallNone(), False),
            (ClsCallNone()(), False),
            (ClsCall.meth, True),
            (ClsCall().meth, True),
            (ClsFullTypes.attrNone, False),
            (ClsFullTypes().attrNone, False),

            *[(class_i, True) for class_i in CLASSES__AS_FUNC]
        ]
    )
    def test__check__callable_func_meth(self, args, _EXPECTED):
        victim = self.Victim.check__callable_func_meth
        pytest_func_tester__no_kwargs(victim, args, _EXPECTED)

    @pytest.mark.parametrize(
        argnames="args, _EXPECTED",
        argvalues=[
            (None, False),
            (True, False),
            (False, False),
            (0, False),
            (111, False),
            (111.222, False),
            ("str", False),
            (b"bytes", False),

            (((111, ),), False),
            (([111, ],), False),
            (({111, },), False),
            (({111: 222, },), False),

            (int, True),
            (int(1), False),
            (str, True),
            (str(1), False),

            (Exception, False),
            (Exception(), False),
            (Exx, False),
            (Exx(), False),

            (Cls, False),
            (Cls(), False),
            (ClsInt, True),
            (ClsInt(), False),    # int() == 0!!!

            (FUNC, True),
            (LAMBDA, True),
            (ClsCallNone, False),
            (ClsCallNone(), False),
            (ClsCallNone()(), False),
            (ClsCall.meth, True),
            (ClsCall().meth, False),
            (ClsFullTypes.attrNone, False),
            (ClsFullTypes().attrNone, False),

            *[(class_i, True) for class_i in CLASSES__AS_FUNC]
        ]
    )
    def test__check__callable_func(self, args, _EXPECTED):
        victim = self.Victim.check__callable_func
        pytest_func_tester__no_kwargs(victim, args, _EXPECTED)

    @pytest.mark.parametrize(
        argnames="args, _EXPECTED",
        argvalues=[
            (None, False),
            (True, False),
            (False, False),
            (0, False),
            (111, False),
            (111.222, False),
            ("str", False),
            (b"bytes", False),

            (((111, ),), False),
            (([111, ],), False),
            (({111, },), False),
            (({111: 222, },), False),

            (int, False),
            (int(1), False),
            (str, False),
            (str(1), False),

            (Exception, False),
            (Exception(), False),
            (Exx, False),
            (Exx(), False),

            (Cls, False),
            (Cls(), False),
            (ClsInt, False),
            (ClsInt(), False),    # int() == 0!!!

            (FUNC, False),
            (LAMBDA, False),
            (ClsCallNone, False),
            (ClsCallNone(), False),
            (ClsCallNone()(), False),
            (ClsCall.meth, False),
            (ClsCall().meth, True),
            (ClsFullTypes.attrNone, False),
            (ClsFullTypes().attrNone, False),

            *[(class_i, False) for class_i in CLASSES__AS_FUNC]
        ]
    )
    def test__check__callable_meth(self, args, _EXPECTED):
        victim = self.Victim.check__callable_meth
        pytest_func_tester__no_kwargs(victim, args, _EXPECTED)

    @pytest.mark.parametrize(
        argnames="args, _EXPECTED",
        argvalues=[
            (None, False),
            (True, False),
            (False, False),
            (0, False),
            (111, False),
            (111.222, False),
            ("str", False),
            (b"bytes", False),

            (((111, ),), False),
            (([111, ],), False),
            (({111, },), False),
            (({111: 222, },), False),

            (int, False),
            (int(1), False),
            (str, False),
            (str(1), False),

            (Exception, False),
            (Exception(), False),
            (Exx, False),
            (Exx(), False),

            (Cls, False),
            (Cls(), False),
            (ClsInt, False),
            (ClsInt(), False),    # int() == 0!!!

            (FUNC, False),
            (LAMBDA, False),
            (ClsCallNone, False),
            (ClsCallNone(), True),
            (ClsCallNone()(), False),
            (ClsCall.meth, False),
            (ClsCall().meth, False),
            (ClsFullTypes.attrNone, False),
            (ClsFullTypes().attrNone, False),

            *[(class_i, False) for class_i in CLASSES__AS_FUNC]
        ]
    )
    def test__check__callable_inst(self, args, _EXPECTED):
        victim = self.Victim.check__callable_inst
        pytest_func_tester__no_kwargs(victim, args, _EXPECTED)

    @pytest.mark.parametrize(
        argnames="args, _EXPECTED",
        argvalues=[
            (None, False),
            (True, False),
            (False, False),
            (0, False),
            (111, False),
            (111.222, False),
            ("str", False),
            (b"bytes", False),

            (((111, ),), False),
            (([111, ],), False),
            (({111, },), False),
            (({111: 222, },), False),

            (int, True),
            (int(1), False),
            (str, True),
            (str(1), False),

            (Exception, False),
            (Exception(), False),
            (Exx, False),
            (Exx(), False),

            (Cls, False),
            (Cls(), False),
            (ClsInt, True),
            (ClsInt(), False),    # int() == 0!!!

            (FUNC, False),
            (LAMBDA, False),
            (ClsCallNone, False),
            (ClsCallNone(), False),
            (ClsCallNone()(), False),
            (ClsCall.meth, False),
            (ClsCall().meth, False),
            (ClsFullTypes.attrNone, False),
            (ClsFullTypes().attrNone, False),

            *[(class_i, True) for class_i in CLASSES__AS_FUNC]
        ]
    )
    def test__check__callable_cls_as_func_builtin(self, args, _EXPECTED):
        victim = self.Victim.check__callable_cls_as_func_builtin
        pytest_func_tester__no_kwargs(victim, args, _EXPECTED)

    # -----------------------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        argnames="args, _EXPECTED",
        argvalues=[
            (None, False),
            (True, False),
            (False, False),
            (0, False),
            (111, False),
            (111.222, False),
            ("str", False),
            (b"bytes", False),

            (((111, ),), False),
            (([111, ],), False),
            (({111, },), False),
            (({111: 222, },), False),

            (int, True),
            (int(1), False),
            (str, True),
            (str(1), False),

            (Exception, True),
            (Exception(), False),
            (Exx, True),
            (Exx(), False),

            (Cls, True),
            (Cls(), False),
            (ClsInt, True),
            (ClsInt(), False),    # int() == 0!!!

            (FUNC, False),
            (LAMBDA, False),
            (ClsCallNone, True),
            (ClsCallNone(), False),
            (ClsCallNone()(), False),
            (ClsCall.meth, False),
            (ClsCall().meth, False),
            (ClsFullTypes.attrNone, False),
            (ClsFullTypes().attrNone, False),

            *[(class_i, True) for class_i in CLASSES__AS_FUNC]
        ]
    )
    def test__check__class(self, args, _EXPECTED):
        victim = self.Victim.check__class
        pytest_func_tester__no_kwargs(victim, args, _EXPECTED)

    @pytest.mark.parametrize(
        argnames="args, _EXPECTED",
        argvalues=[
            (None, True),
            (True, True),
            (False, True),
            (0, True),
            (111, True),
            (111.222, True),
            ("str", True),
            (b"bytes", True),

            (((111, ),), True),
            (([111, ],), True),
            (({111, },), True),
            (({111: 222, },), True),

            (int, False),
            (int(1), True),
            (str, False),
            (str(1), True),

            (Exception, False),
            (Exception(), True),
            (Exx, False),
            (Exx(), True),

            (Cls, False),
            (Cls(), True),
            (ClsInt, False),
            (ClsInt(), True),    # int() == 0!!!

            (FUNC, False),
            (LAMBDA, False),
            (ClsCallNone, False),
            (ClsCallNone(), True),
            (ClsCallNone()(), True),
            (ClsCall.meth, False),
            (ClsCall().meth, False),
            (ClsFullTypes.attrNone, True),
            (ClsFullTypes().attrNone, True),

            *[(class_i, False) for class_i in CLASSES__AS_FUNC]
        ]
    )
    def test__check__instance(self, args, _EXPECTED):
        victim = self.Victim.check__instance
        pytest_func_tester__no_kwargs(victim, args, _EXPECTED)

    @pytest.mark.parametrize(
        argnames="args, _EXPECTED",
        argvalues=[
            (None, False),
            (True, False),
            (False, False),
            (0, False),
            (111, False),
            (111.222, False),
            ("str", False),
            (b"bytes", False),

            (((111, ),), False),
            (([111, ],), False),
            (({111, },), False),
            (({111: 222, },), False),

            (int, False),
            (int(1), False),
            (str, False),
            (str(1), False),

            (Exception, False),
            (Exception(), True),
            (Exx, False),
            (Exx(), True),

            (Cls, False),
            (Cls(), True),
            (ClsInt, False),
            (ClsInt(), False),    # int() == 0!!!

            (FUNC, False),
            (LAMBDA, False),
            (ClsCallNone, False),
            (ClsCallNone(), True),
            (ClsCallNone()(), False),
            (ClsCall.meth, False),
            (ClsCall().meth, False),
            (ClsFullTypes.attrNone, False),
            (ClsFullTypes().attrNone, False),

            *[(class_i, False) for class_i in CLASSES__AS_FUNC]
        ]
    )
    def test__check__instance_not_elementary(self, args, _EXPECTED):
        victim = self.Victim.check__instance_not_elementary
        pytest_func_tester__no_kwargs(victim, args, _EXPECTED)

    # -----------------------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        argnames="args, _EXPECTED",
        argvalues=[
            (None, False),
            (True, False),
            (False, False),
            (0, False),
            (111, False),
            (111.222, False),
            ("str", False),
            (b"bytes", False),

            (((111, ),), False),
            (([111, ],), False),
            (({111, },), False),
            (({111: 222, },), False),

            (int, False),
            (int(1), False),
            (str, False),
            (str(1), False),

            (Exception, True),
            (Exception(), True),
            (Exx, True),
            (Exx(), True),

            (Cls, False),
            (Cls(), False),
            (ClsInt, False),
            (ClsInt(), False),    # int() == 0!!!

            (FUNC, False),
            (LAMBDA, False),
            (ClsCallNone, False),
            (ClsCallNone(), False),
            (ClsCallNone()(), False),
            (ClsCall.meth, False),
            (ClsCall().meth, False),
            (ClsFullTypes.attrNone, False),
            (ClsFullTypes().attrNone, False),

            *[(class_i, False) for class_i in CLASSES__AS_FUNC]
        ]
    )
    def test__check__exception(self, args, _EXPECTED):
        victim = self.Victim.check__exception
        pytest_func_tester__no_kwargs(victim, args, _EXPECTED)

    # =================================================================================================================
    @pytest.mark.parametrize(
        argnames="args, _EXPECTED",
        argvalues=[
            (("str", "str"), True),
            (("str", str), True),
            ((str, "str"), True),
            ((str, str), True),

            ((int, str), False),
            ((int, "str"), False),

            ((111, 111), True),
            ((int, 111), True),
            ((111, int), True),
            ((int, int), True),

            ((Exception, Exception), True),
            ((Exception(), Exception), True),
            ((Exception, Exception()), True),
            ((Exception(), Exception()), True),

            ((Exx, Exception), True),
            ((Exx(), Exception), True),
            ((Exx, Exception()), True),
            ((Exx(), Exception()), True),

            ((Exception, Exx), False),      # REMEMBER! not clear!
            ((Exception(), Exx), False),    # REMEMBER! not clear!
            ((Exception, Exx()), False),    # REMEMBER! not clear!
            ((Exception(), Exx()), False),  # REMEMBER! not clear!

            ((Cls, Cls), True),
            ((Cls, Cls()), True),
            ((Cls(), Cls), True),
            ((Cls(), Cls()), True),

            ((FUNC, Cls), None),
            ((FUNC, Cls()), None),
        ]
    )
    def test__check__nested__by_cls_or_inst(self, args, _EXPECTED):
        victim = self.Victim.check__nested__by_cls_or_inst
        pytest_func_tester__no_kwargs(victim, args, _EXPECTED)


# =====================================================================================================================
