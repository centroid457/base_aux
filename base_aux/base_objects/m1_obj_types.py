from typing import *

from base_aux.base_source.m1_source import InitSource


# =====================================================================================================================
class _Cls:
    def meth(self):
        pass


# =====================================================================================================================
@final
class TYPES:
    """
    GOAL
    ----
    collect all types variants
    """

    # SINGLE ---------------------------
    NONE: type = type(None)
    FUNCTION: type = type(lambda: True)
    METHOD: type = type(_Cls().meth)

    # COLLECTIONS ---------------------------
    ELEMENTARY_SINGLE: tuple[type, ...] = (
        type(None),
        bool,
        str, bytes,
        int, float,
    )
    ELEMENTARY_COLLECTION: tuple[type, ...] = (
        tuple, list,
        set, dict,
    )
    ELEMENTARY: tuple[type, ...] = (
        *ELEMENTARY_SINGLE,
        *ELEMENTARY_COLLECTION,
    )


# =====================================================================================================================
@final
class TypeCheck(InitSource):
    # -----------------------------------------------------------------------------------------------------------------
    def check__bool_none(self) -> bool:
        """
        GOAL
        ----
        help in case of
            assert 0 == False
            assert 1 == True
            assert 2 == False   # unclear!!!

        CREATED SPECIALLY FOR
        ---------------------
        funcs.Valid.compare_doublesided
        """
        return isinstance(self.SOURCE, (bool, type(None)))

    def check__elementary(self) -> bool:
        if callable(self.SOURCE):
            return False
        return isinstance(self.SOURCE, TYPES.ELEMENTARY)

    def check__elementary_single(self) -> bool:
        return isinstance(self.SOURCE, TYPES.ELEMENTARY_SINGLE)

    def check__elementary_single_not_none(self) -> bool:
        """
        its just an Idea!!!

        GOAL
        ----
        prepare to work with ensure_collection
        None assumed as not Passed value! so we can ensure to return None -> ()

        SPECIALLY CREATED FOR
        ---------------------
        ensure_collection somewhere!
        """
        return self.check__elementary_single() and self.SOURCE is not None

    def check__elementary_collection(self) -> bool:
        """
        GOAL
        ----
        MOST PREFERRED to use for ensure_collection! and apply for Args!
        all other base_objects (ClsInst) will covered by brackets!
        """
        return isinstance(self.SOURCE, TYPES.ELEMENTARY_COLLECTION)

    def check__elementary_collection_not_dict(self) -> bool:
        return isinstance(self.SOURCE, TYPES.ELEMENTARY_COLLECTION) and not isinstance(self.SOURCE, dict)

    # -----------------------------------------------------------------------------------------------------------------
    def check__iterable(
            self,
            dict_as_iterable: bool = True,
            str_and_bytes_as_iterable: bool = True,
    ) -> bool:
        """checks if SOURCE is iterable.

        :param source: SOURCE data
        :param dict_as_iterable: if you dont want to use dict in your selecting,
            becouse maybe you need flatten all elements in list/set/tuple into one sequence
            and dict (as extended list) will be irrelevant!
        :param str_and_bytes_as_iterable: usually in data processing you need to work with str-type elements as OneSolid element
            but not iterating through chars!
        """
        if isinstance(self.SOURCE, dict):
            return dict_as_iterable
        elif isinstance(self.SOURCE, (str, bytes)):
            return str_and_bytes_as_iterable
        elif isinstance(self.SOURCE, (tuple, list, set,)):  # need to get it explicitly!!!
            return True
        elif hasattr(self.SOURCE, '__iter__') or hasattr(self.SOURCE, '__getitem__'):
            return True

        # FINAL ---------------------
        return False

    def check__iterable_not_str(self) -> bool:
        """
        GOAL
        ----
        checks if SOURCE is iterable, but not exactly str!!!
        """
        return self.check__iterable(str_and_bytes_as_iterable=False)

    # CALLABLE --------------------------------------------------------------------------------------------------------
    def check__callable_func_meth_inst_cls(self) -> bool:
        """
        GOAL
        ----
        just any callable or CLASS!!! - so it is actually all CALLABLE!


        CREATES SPECIALLY FOR
        ---------------------
        just to see difference and clearly using by name!!!
        """
        return callable(self.SOURCE)

    def check__callable_func_meth_inst(self) -> bool:
        """
        GOAL
        ----
        just any callable but NO CLASS!!!


        CREATES SPECIALLY FOR
        ---------------------
        detect all funcs like func/meth/or even DescriptedClasses (it is class but actually used like func!)
        recommended using instead of just Callable! cause Callable keeps additionally every class instead of just simple func/method!
        """
        if self.check__class():
            result = issubclass(self.SOURCE, TYPES.ELEMENTARY)
        else:
            result = callable(self.SOURCE)
        return result

    def check__callable_func_meth(self) -> bool:
        return self.check__callable_func() or self.check__callable_meth()

    def check__callable_func(self) -> bool:
        """
        if only the exact generic function! no class method!
        Lambda included!
        Classmethod included!

        CREATED SPECIALLY FOR
        ---------------------
        not special! just as ones found ability to!
        """
        if self.check__callable_cls_as_func_builtin():
            result = True
        else:
            result = TYPES.FUNCTION in self.SOURCE.__class__.__mro__
        return result

    def check__callable_meth(self) -> bool:
        """
        if only the exact instance method!
        no generic funcs!
        no CALLABLE INSTANCE!
        no callable classes!

        CREATED SPECIALLY FOR
        ---------------------
        not special! just as ones found ability to!
        """
        result = not self.check__class() and type(_Cls().meth) in self.SOURCE.__class__.__mro__
        return result

    def check__callable_inst(self) -> bool:
        """
        CREATED SPECIALLY FOR
        ---------------------
        not special! just as ones found ability to!
        """
        result = self.check__instance() and hasattr(self.SOURCE, "__call__")
        return result

    def check__callable_cls_as_func_builtin(self) -> bool:
        """
        if class and class is as func like int/str/*  or nested
        """
        return self.check__class() and issubclass(self.SOURCE, TYPES.ELEMENTARY)

    # CLS/INST --------------------------------------------------------------------------------------------------------
    def check__class(self) -> bool:
        """
        works both for funcs/meths for any Сды/Штые1 see tests test__check__class
        """
        # 1 -----------------
        # return hasattr(self.SOURCE, "__class__")     # this is incorrect!!! tests get fail!

        # 2 -----------------
        # INCORRECT! metaclasses have middle class(MetaType)!
        # if self.SOURCE.__class__ is type:
        #     return True

        # 3 -----------------
        # CORRECT! only Class can be subclass!!! otherwise Raise!
        try:
            return issubclass(self.SOURCE, object)
        except:
            return False

        # 4 -----------------
        # CORRECT! only Class have __mro__!!! otherwise Raise!
        # try:
        #     _ = self.SOURCE.__mro__
        #     return True
        # except:
        #     return False

    def check_metaclassed(self) -> bool:
        """
        just an idea to show that class crates by metaclass!
        no idea how and where to use! just a toy for playing and deeper understanding
        """
        # todo: finish

    def check__instance(self) -> bool:
        return not self.check__class() and not self.check__callable_func() and not self.check__callable_meth()

    def check__instance_not_elementary(self) -> bool:
        return self.check__instance() and not self.check__elementary()

    def check__exception(self) -> bool:
        """
        any of both variant (Instance/Class) of any Exception!
        """
        try:
            return issubclass(self.SOURCE, Exception)   # check it first!!! in try cover
        except:
            return isinstance(self.SOURCE, Exception)

        # if isinstance(self.SOURCE, Exception):
        #     return True
        # try:
        #     return issubclass(self.SOURCE, Exception)
        # except:
        #     pass
        # return False

    def check__nested__by_cls_or_inst(self, parent: Any) -> bool | None:
        """
        any of both variant (Instance/Class) comparing with TARGET of both variant (Instance/Class)

        specially created for pytest_aux for comparing with Exception!
        """
        source_cls = self.get__class()
        parent_cls = TypeCheck(parent).get__class()
        return issubclass(source_cls, parent_cls)

    # =================================================================================================================
    def get__class(self) -> type:
        """
        GOAL
        ----
        get class from any object

        CREATED SPECIALLY FOR
        ---------------------
        classes.ClsMiddleGroup
        """
        if self.check__class():
            return self.SOURCE
        else:
            return self.SOURCE.__class__

    def get_mro(self) -> tuple[type, ...]:
        """
        GAOL
        ----
        get DIRECT mro for instance/class!
        """
        cls = self.get__class()
        mro = cls.__mro__
        return mro

    def iter_mro_user(self, *exclude: type) -> Iterable[type]:
        """
        GAOL
        ----
        iter only user classes
        """
        mro = self.get_mro()
        if not mro:
            """
            created specially for
            ---------------------
            DictDotsAnnotRequired(dict)
            it is not working without it!!!
            """
            mro = ()

        for cls in mro:
            if cls not in [*exclude, object, *TYPES.ELEMENTARY]:
                yield cls


# =====================================================================================================================
