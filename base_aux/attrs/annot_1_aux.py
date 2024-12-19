from typing import *

from base_aux.base_exceptions import Exx__AnnotNotDefined
from base_aux.base_objects.obj_types import TYPES

from .attr_1_aux import AttrAux


# =====================================================================================================================
@final
class AnnotsAux:
    # -----------------------------------------------------------------------------------------------------------------
    @classmethod
    def get_not_defined(cls, source: Any) -> list[str]:
        """
        GOAL
        ----
        return list of not defined annotations

        SPECIALLY CREATED FOR
        ---------------------
        annot__check_all_defined
        """

        result = []
        nested = cls.get_nested__dict_types(source)
        for key in nested:
            if not AttrAux(source).anycase__check_exists(key):
                result.append(key)
        return result

    @classmethod
    def check_all_defined(cls, source: Any) -> bool:
        """
        GOAL
        ----
        check if all annotated attrs have value!
        """
        return not cls.get_not_defined(source)

    @classmethod
    def check_all_defined_or_raise(cls, source: Any) -> None | NoReturn:
        """
        GOAL
        ----
        check if all annotated attrs have value!
        """
        not_defined = cls.get_not_defined(source)
        if not_defined:
            dict_type = cls.get_nested__dict_types(source)
            msg = f"[CRITICAL]{not_defined=} in {dict_type}"
            raise Exx__AnnotNotDefined(msg)

    # -----------------------------------------------------------------------------------------------------------------
    @classmethod
    def get_nested__dict_types(cls, source: Any) -> dict[str, type[Any]]:
        """
        GOAL
        ----
        get all annotations in correct order (nesting available)!

        RETURN
        ------
        keys - all attr names (defined and not)
        values - Types!!! not instances!!!
        """
        try:
            mro = source.__mro__
        except:
            mro = source.__class__.__mro__

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
            if cls_i in [AnnotsBase, object, *TYPES.ELEMENTARY]:
                continue

            _result_i = dict(cls_i.__annotations__)
            _result_i.update(result)
            result = _result_i
        return result

    @classmethod
    def get_nested__dict_values(cls, source: Any) -> dict[str, Any]:
        """
        GOAL
        ----
        get dict with only existed values! no raise if value not exists!
        """
        result = {}
        for key in cls.get_nested__dict_types(source):
            if hasattr(source, key):
                result.update({key: getattr(source, key)})
        return result

    @classmethod
    def iter_values(cls, source: Any) -> Iterable[Any]:
        yield from cls.get_nested__dict_values(source).values()


# =====================================================================================================================
class AnnotsBase:
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
    def __getattr__(self, name) -> Any | NoReturn:
        return AttrAux(self).anycase__getattr(name)

    def __getitem__(self, name) -> Any | NoReturn:
        return AttrAux(self).anycase__getattr(name)

    # -----------------------------------------------------------------------------------------------------------------
    def annots__print(self, source: Any = None) -> str:
        """just a pretty print for debugging or research.
        """
        if source is None:
            source = self

        result = f"{source.__class__.__name__}(Annotations):"
        annots = AnnotsAux.get_nested__dict_values(source)
        if annots:
            for key, value in annots.items():
                result += f"\n\t{key}={value}"
        else:
            result += f"\nEmpty=Empty"

        return result

    def __str__(self):
        return self.annots__print()


# =====================================================================================================================
