from typing import *
from base_aux.base_exceptions import Exx__AnnotNotDefined

from .attr_1_aux import AttrAux
from base_aux.objects.obj_types import TypeChecker


# =====================================================================================================================
class AnnotAux:
    """
    access to all __annotations__
        from all nested classes
        in correct order

    RULES
    -----
    4. nesting available with correct order!
        class ClsFirst(BreederStrStack):
            atr1: int
            atr3: int = None

        class ClsLast(BreederStrStack):
            atr2: int = None
            atr4: int

        for key, value in ClsLast.annotations__get_nested().items():
            print(f"{key}:{value}")

        # atr1:<class 'int'>
        # atr3:<class 'int'>
        # atr2:<class 'int'>
        # atr4:<class 'int'>
    """
    # -----------------------------------------------------------------------------------------------------------------
    def __getattr__(self, item) -> Any | NoReturn:
        return AttrAux._getattr_anycase(item, self)

    def __getitem__(self, item) -> Any | NoReturn:
        return AttrAux._getattr_anycase(item, self)

    # -----------------------------------------------------------------------------------------------------------------
    @classmethod
    def annot__get_nested__dict_types(cls, obj: Any | None = None) -> dict[str, type[Any]]:
        """
        GOAL
        ----
        get all annotations in correct order (nesting available)!

        RETURN
        ------
        keys - all attr names (defined and not)
        values - Types!!! not instances!!!
        """
        if obj is None:
            obj = cls

        try:
            mro = obj.__mro__
        except:
            mro = obj.__class__.__mro__

        if not mro:
            """
            created specially for
            ---------------------
            DictDotsAnnotRequired(dict)
            it is not working without it!!!
            """
            return {}

        result = {}
        for cls_i in mro:
            if cls_i in [AnnotAux, object, type(None), dict, *TypeChecker.TYPES__ELEMENTARY]:
                continue

            _result_i = dict(cls_i.__annotations__)
            _result_i.update(result)
            result = _result_i
        return result

    def annot__get_nested__dict_values(self, obj: Any | None = None) -> dict[str, Any]:
        """
        GOAL
        ----
        get dict with only existed values! no raise if value not exists!
        """
        if obj is None:
            obj = self

        result = {}
        for key in self.annot__get_nested__dict_types(obj):
            if hasattr(obj, key):
                result.update({key: getattr(obj, key)})
        return result

    def annot__iter_values(self, obj: Any = None):
        yield from self.annot__get_nested__dict_values(obj).values()

    # -----------------------------------------------------------------------------------------------------------------
    def annot__get_not_defined(self, obj: Any | None = None) -> list[str]:
        """
        GOAL
        ----
        return list of not defined annotations

        SPECIALLY CREATED FOR
        ---------------------
        annot__check_all_defined
        """
        if obj is None:
            obj = self

        result = []
        nested = self.annot__get_nested__dict_types(obj)
        for key in nested:
            if not self.attr__check_defined(key, obj):
                result.append(key)
        return result

    def attr__check_defined(self, item: str, obj: Any | None = None) -> bool:
        if obj is None:
            obj = self

        return hasattr(obj, item)

    def annot__check_all_defined(self, obj: Any | None = None) -> bool:
        """
        GOAL
        ----
        check if all annotated attrs have value!
        """
        return not self.annot__get_not_defined(obj)

    def annot__raise_if_not_defined(self, obj: Any | None = None) -> None | NoReturn:
        """
        GOAL
        ----
        check if all annotated attrs have value!
        """
        not_defined = self.annot__get_not_defined(obj)
        if not_defined:
            dict_type = self.annot__get_nested__dict_types(obj)
            msg = f"[CRITICAL]{not_defined=} in {dict_type}"
            raise Exx__AnnotNotDefined(msg)

    # -----------------------------------------------------------------------------------------------------------------
    def annot__print(self, obj: Any = None) -> str:
        """just a pretty print for debugging or research.
        """
        if obj is None:
            obj = self

        result = f"{obj.__class__.__name__}(Annotations):"
        annots = self.annot__get_nested__dict_values(obj)
        if annots:
            for key, value in annots.items():
                result += f"\n\t{key}={value}"
        else:
            result += f"\nEmpty=Empty"

        return result

    def __str__(self):
        return self.annot__print()


# =====================================================================================================================
