from typing import *

from base_aux.base_exceptions import Exx__AnnotNotDefined
from base_aux.base_objects.m1_obj_types import TYPES, TypeCheck
from base_aux.base_source import InitSource

from base_aux.aux_argskwargs import *

from .m1_attr_1_aux import AttrAux


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

    # =================================================================================================================
    def check_all_defined(self) -> bool:
        """
        GOAL
        ----
        check if all annotated aux_attr have value!
        """
        return not self.get_not_defined()

    def check_all_defined_or_raise(self) -> None | NoReturn:
        """
        GOAL
        ----
        check if all annotated aux_attr have value!
        """
        not_defined = self.get_not_defined()
        if not_defined:
            dict_type = self.dump__dict_types()
            msg = f"[CRITICAL]{not_defined=} in {dict_type}"
            raise Exx__AnnotNotDefined(msg)

    # =================================================================================================================
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

        result = {}
        for cls in self.iter_mro():
            _result_i = dict(cls.__annotations__)
            _result_i.update(result)
            result = _result_i
        return result

    def dump__dict_values(self) -> TYPE__KWARGS_FINAL:
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

    # =================================================================================================================
    def iter_mro(self) -> Iterable[type]:
        """
        GOAL
        ----
        iter only important user classes from mro
        """
        yield from TypeCheck(self.SOURCE).iter_mro_user(AnnotsBase)

    def iter_names(self) -> Iterable[str]:
        """
        iter all (with not existed)
        """
        yield from self.dump__dict_types()

    def iter_values(self) -> Iterable[Any]:
        """
        only existed
        """
        yield from self.dump__dict_values().values()

    # =================================================================================================================
    def values__set_none__existed(self) -> None:
        """
        GOAL
        ----
        set None for all annotated aux_attr! only existed!
        """
        for name in self.iter_names():
            if hasattr(self.SOURCE, name):
                setattr(self.SOURCE, name, None)

    def values__set_none__all(self) -> None:
        """
        GOAL
        ----
        set None for all annotated aux_attr! even not existed!
        """
        for name in self.iter_names():
            setattr(self.SOURCE, name, None)

    def values__delete(self) -> None:
        """
        GOAL
        ----
        delattr all annotated aux_attr!
        """
        for name in self.iter_names():
            if hasattr(self.SOURCE, name):
                delattr(self.SOURCE, name)

    # -----------------------------------------------------------------------------------------------------------------
    def names__delete(self, *names: str) -> None:
        """
        ATTENTION
        ---------
        its not good idea!!! dont use it! yoг will change real CLASS parameters|

        GOAL
        ----
        del names from annots! if existed
        """
        if not names:
            names = self.iter_names()

        for name in names:
            for cls in self.iter_mro():
                if name in cls.__annotations__:
                    cls.__annotations__.pop(name)

    def names__add(self, *names: str) -> None:
        """
        ATTENTION
        ---------
        its not good idea!!! dont use it! yoг will change real CLASS parameters|

        GOAL
        ----
        add names into annots!
        """
        cls = TypeCheck(self).get__class()

        for name in names:
            annots = cls.__annotations__
            if name not in annots:
                cls.__annotations__.update({name: Any})


# =====================================================================================================================
class AnnotsBase:
    # -----------------------------------------------------------------------------------------------------------------
    def __getattr__(self, name) -> Any | NoReturn:
        return AttrAux(self).anycase__getattr(name)

    def __getitem__(self, name) -> Any | NoReturn:
        return AttrAux(self).anycase__getattr(name)


# =====================================================================================================================
