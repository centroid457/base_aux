from typing import *

from base_aux.base_exceptions import Exx__AnnotNotDefined
from base_aux.base_objects.obj_types import TYPES, TypeCheck
from base_aux.base_source import *

from .attr_1_aux import AttrAux


# =====================================================================================================================
@final
class AnnotsAux(InitSource):
    """
    GOAL
    ----
    work with all __annotations__
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
    def get_not_defined(self) -> list[str]:
        """
        GOAL
        ----
        return list of not defined annotations

        SPECIALLY CREATED FOR
        ---------------------
        annot__check_all_defined
        """
        result = []
        nested = self.dump__dict_types()
        for key in nested:
            if not AttrAux(self.SOURCE).anycase__check_exists(key):
                result.append(key)
        return result

    # -----------------------------------------------------------------------------------------------------------------
    def check_all_defined(self) -> bool:
        """
        GOAL
        ----
        check if all annotated attrs have value!
        """
        return not self.get_not_defined()

    def check_all_defined_or_raise(self) -> None | NoReturn:
        """
        GOAL
        ----
        check if all annotated attrs have value!
        """
        not_defined = self.get_not_defined()
        if not_defined:
            dict_type = self.dump__dict_types()
            msg = f"[CRITICAL]{not_defined=} in {dict_type}"
            raise Exx__AnnotNotDefined(msg)

    # -----------------------------------------------------------------------------------------------------------------
    def dump__dict_types(self) -> dict[str, type[Any]]:
        """
        GOAL
        ----
        get all annotations in correct order (nesting available)!

        RETURN
        ------
        keys - all attr names (defined and not)
        values - Types!!! not instances!!!
        """
        cls = TypeCheck(self.SOURCE).ensure__class()
        mro = cls.__mro__

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

    def dump__dict_values(self) -> dict[str, Any]:
        """
        GOAL
        ----
        get dict with only existed values! no raise if value not exists!
        """
        result = {}
        for key in self.dump__dict_types():
            if hasattr(self.SOURCE, key):
                result.update({key: getattr(self.SOURCE, key)})
        return result

    # -----------------------------------------------------------------------------------------------------------------
    def iter_values(self) -> Iterable[Any]:
        yield from self.dump__dict_values().values()

    def iter_names(self) -> Iterable[Any]:
        yield from self.dump__dict_values()

    # -----------------------------------------------------------------------------------------------------------------
    def dump__pretty_str(self) -> str:
        """just a pretty string for debugging or research.
        """
        result = f"{self.SOURCE.__class__.__name__}(Annotations):"
        annots = self.dump__dict_values()
        if annots:
            for key, value in annots.items():
                result += f"\n\t{key}={value}"
        else:
            result += f"\nEmpty=Empty"

        return result

    def __str__(self):
        return self.dump__pretty_str()


# =====================================================================================================================
class AnnotsBase:
    # -----------------------------------------------------------------------------------------------------------------
    def __getattr__(self, name) -> Any | NoReturn:
        return AttrAux(self).anycase__getattr(name)

    def __getitem__(self, name) -> Any | NoReturn:
        return AttrAux(self).anycase__getattr(name)


# =====================================================================================================================
