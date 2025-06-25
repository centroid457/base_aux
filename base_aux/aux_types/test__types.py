import pytest
import sys

from base_aux.lambdas.m1_lambda import *
from base_aux.aux_types.m1_type_aux import *
from base_aux.aux_values.m4_primitives import *


# =====================================================================================================================
class Test__1:
    @pytest.mark.parametrize(
        argnames="source, _EXPECTED",
        argvalues=[
            (pytest,      (False, False, False, False, False, True, )),
            (sys,      (False, False, False, False, False, True, )),

            (None,      (True, True, True, False, False, False, )),
            (True,      (True, True, True, True, False, False, )),
            (False,     (True, True, True, True, False, False, )),
            (0,         (False, True, True, True, False, False, )),
            (111,       (False, True, True, True, False, False, )),
            (111.222,   (False, True, True, True, False, False, )),
            ("str",     (False, True, True, True, False, False, )),
            (b"bytes",  (False, True, True, True, False, False, )),

            ((111, ),        (False, True, False, False, True, False, )),
            ([111, ],        (False, True, False, False, True, False, )),
            ({111, },        (False, True, False, False, True, False, )),
            ({111: 222, },   (False, True, False, False, True, False, )),

            (int,       (False, False, False, False, False, False, )),
            (int(1),    (False, True, True, True, False, False, )),
            (str,       (False, False, False, False, False, False, )),
            (str(1),    (False, True, True, True, False, False, )),

            (Exception,     (False, False, False, False, False, False, )),
            (Exception(),   (False, False, False, False, False, False, )),
            (ClsException,  (False, False, False, False, False, False, )),
            (ClsException(), (False, False, False, False,False, False, )),

            (Cls,       (False, False, False, False, False, False, )),
            (Cls(),     (False, False, False, False, False, False, )),
            (ClsInt,    (False, False, False, False, False, False, )),
            (ClsInt(),  (False, True, True, True, False, False, )),    # int() == 0!!!

            (FUNC,                      (False, False, False, False, False, False, )),
            (LAMBDA,                    (False, False, False, False, False, False, )),
            (ClsCallNone,               (False, False, False, False, False, False, )),
            (ClsCallNone(),             (False, False, False, False, False, False, )),
            (ClsCallNone()(),           (True, True, True, False, False, False, )),
            (ClsCall().meth,            (False, False, False, False, False, False, )),
            (ClsFullTypes.attrNone,     (True, True, True, False, False, False, )),
            (ClsFullTypes().attrNone,   (True, True, True, False, False, False, )),

            *[
                (
                    class_i,
                    (False, False, False, False, False, False, )
                ) for class_i in CLASSES__AS_FUNC
            ]
        ]
    )
    def test__check__bool_none(self, source, _EXPECTED):
        victim = TypeAux(source)

        Lambda(victim.check__bool_none).expect__check_assert(_EXPECTED[0])
        Lambda(victim.check__elementary).expect__check_assert(_EXPECTED[1])
        Lambda(victim.check__elementary_single).expect__check_assert(_EXPECTED[2])
        Lambda(victim.check__elementary_single_not_none).expect__check_assert(_EXPECTED[3])
        Lambda(victim.check__elementary_collection).expect__check_assert(_EXPECTED[4])
        Lambda(victim.check__module).expect__check_assert(_EXPECTED[5])





    @pytest.mark.parametrize(
        argnames="source, _EXPECTED",
        argvalues=[
            (None, False),
            (True, False),
            (False, False),
            (0, False),
            (111, False),
            (111.222, False),
            ("str", False),
            (b"bytes", False),

            ((111, ), True),
            ([111, ], True),
            ({111, }, True),
            ({111: 222, }, False),

            (int, False),
            (int(1), False),
            (str, False),
            (str(1), False),

            (Exception, False),
            (Exception(), False),
            (ClsException, False),
            (ClsException(), False),

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
    def test__check__elementary_collection_not_dict(self, source, _EXPECTED):
        func_link = TypeAux(source).check__elementary_collection_not_dict
        Lambda(func_link).expect__check_assert(_EXPECTED)

    # -----------------------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        argnames="source, args, _EXPECTED",
        argvalues=[
            ("str", (True, True), True),
            ("str", (True, False), False),

            (b"bytes", (True, True), True),
            (b"bytes", (True, False), False),

            # -----------------------
            (None, (), False),
            (True, (), False),
            (False, (), False),
            (0, (), False),
            (111, (), False),
            (111.222, (), False),
            ("str", (), True),
            (b"bytes", (), True),

            ((111, ), (), True),
            ([111, ], (), True),
            ({111, }, (), True),
            ({111: 222, }, (), True),
            ({111: 222, }, (True, True), True),
            ({111: 222, }, (False, True), False),

            (int, (), False),
            (int(1), (), False),
            (str, (), True),        # not clear!!!
            (str(1), (), True),

            (Exception, (), False),
            (Exception(), (), False),
            (ClsException, (), False),
            (ClsException(), (), False),

            (Cls, (), False),
            (Cls(), (), False),
            (ClsInt, (), False),
            (ClsInt(), (), False),

            (FUNC, (), False),
            (LAMBDA, (), False),
            (ClsCallNone, (), False),
            (ClsCallNone(),(),  False),
            (ClsCallNone()(), (), False),
            (ClsCall.meth, (), False),
            (ClsCall().meth, (), False),
            (ClsFullTypes.attrNone, (), False),
            (ClsFullTypes().attrNone, (), False),

            # *[(class_i, False) for class_i in CLASSES__AS_FUNC]
        ]
    )
    def test__iterable(self, source, args, _EXPECTED):
        func_link = TypeAux(source).check__iterable
        Lambda(func_link, *args).expect__check_assert(_EXPECTED)

    @pytest.mark.parametrize(
        argnames="source, _EXPECTED",
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
            (ClsException, False),
            (ClsException(), False),

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
    def test__iterable_not_str(self, source, _EXPECTED):
        func_link = TypeAux(source).check__iterable_not_str
        Lambda(func_link).expect__check_assert(_EXPECTED)

    # CALLABLE --------------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        argnames="source, _EXPECTED",
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
            (ClsException, False),
            (ClsException(), False),

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
    def test__check__callable_func_meth_inst(self, source, _EXPECTED):
        func_link = TypeAux(source).check__callable_func_meth_inst
        Lambda(func_link).expect__check_assert(_EXPECTED)

    @pytest.mark.parametrize(
        argnames="source, _EXPECTED",
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
            (ClsException, False),
            (ClsException(), False),

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
    def test__check__callable_func_meth(self, source, _EXPECTED):
        func_link = TypeAux(source).check__callable_func_meth
        Lambda(func_link).expect__check_assert(_EXPECTED)

    @pytest.mark.parametrize(
        argnames="source, _EXPECTED",
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
            (ClsException, False),
            (ClsException(), False),

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
    def test__check__callable_func(self, source, _EXPECTED):
        func_link = TypeAux(source).check__callable_func
        Lambda(func_link).expect__check_assert(_EXPECTED)

    @pytest.mark.parametrize(
        argnames="source, _EXPECTED",
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
            (ClsException, False),
            (ClsException(), False),

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
    def test__check__callable_meth(self, source, _EXPECTED):
        func_link = TypeAux(source).check__callable_meth
        Lambda(func_link).expect__check_assert(_EXPECTED)

    @pytest.mark.parametrize(
        argnames="source, _EXPECTED",
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
            (ClsException, False),
            (ClsException(), False),

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
    def test__check__callable_inst(self, source, _EXPECTED):
        func_link = TypeAux(source).check__callable_inst
        Lambda(func_link).expect__check_assert(_EXPECTED)

    @pytest.mark.parametrize(
        argnames="source, _EXPECTED",
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
            (ClsException, False),
            (ClsException(), False),

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
    def test__check__callable_cls_as_func_builtin(self, source, _EXPECTED):
        func_link = TypeAux(source).check__callable_cls_as_func_builtin
        Lambda(func_link).expect__check_assert(_EXPECTED)

    # -----------------------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        argnames="source, _EXPECTED",
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
            (ClsException, True),
            (ClsException(), False),

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
    def test__check__class(self, source, _EXPECTED):
        func_link = TypeAux(source).check__class
        Lambda(func_link).expect__check_assert(_EXPECTED)

    @pytest.mark.parametrize(
        argnames="source, _EXPECTED",
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
            (ClsException, False),
            (ClsException(), True),

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
    def test__check__instance(self, source, _EXPECTED):
        func_link = TypeAux(source).check__instance
        Lambda(func_link).expect__check_assert(_EXPECTED)

    @pytest.mark.parametrize(
        argnames="source, _EXPECTED",
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
            (ClsException, False),
            (ClsException(), True),

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
    def test__check__instance_not_elementary(self, source, _EXPECTED):
        func_link = TypeAux(source).check__instance_not_elementary
        Lambda(func_link).expect__check_assert(_EXPECTED)

    # -----------------------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        argnames="source, _EXPECTED",
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
            (ClsException, True),
            (ClsException(), True),

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
    def test__check__exception(self, source, _EXPECTED):
        func_link = TypeAux(source).check__exception
        Lambda(func_link).expect__check_assert(_EXPECTED)

    # =================================================================================================================
    @pytest.mark.parametrize(
        argnames="source, parent, _EXPECTED",
        argvalues=[
            ("str", "str", [True, None]),
            ("str", str, [True, True]),
            (str, "str", [True, None]),
            (str, str, [True, True]),

            (int, str, [False, False]),
            (int, "str", [False, None]),

            (111, 111, [True, None]),
            (int, 111, [True, None]),
            (111, int, [True, True]),
            (int, int, [True, True]),

            (Exception, Exception, [True, True]),
            (Exception(), Exception, [True, True]),
            (Exception, Exception(), [True, None]),
            (Exception(), Exception(), [True, None]),

            (ClsException, Exception, [True, True]),
            (ClsException(), Exception, [True, True]),
            (ClsException, Exception(), [True, None]),
            (ClsException(), Exception(), [True, None]),

            (Exception, ClsException, [False, False]),      # REMEMBER! not clear!
            (Exception(), ClsException, [False, False]),    # REMEMBER! not clear!
            (Exception, ClsException(), [False, None]),    # REMEMBER! not clear!
            (Exception(), ClsException(), [False, None]),  # REMEMBER! not clear!

            (Cls, Cls, [True, True]),
            (Cls, Cls(), [True, None]),
            (Cls(), Cls, [True, True]),
            (Cls(), Cls(), [True, None]),

            (FUNC, Cls, [False, False]),
            (FUNC, Cls(), [False, None]),
        ]
    )
    def test__check__nested__by_cls_or_inst(self, source, parent, _EXPECTED):
        Lambda(TypeAux(source).check__nested__from_cls_or_inst, parent).expect__check_assert(_EXPECTED[0])
        Lambda(TypeAux(source).check__subclassed_or_isinst, parent).expect__check_assert(_EXPECTED[1])


# =====================================================================================================================
