from typing import *

from base_aux.base_statics.m2_exceptions import *
from base_aux.base_statics.m1_types import *
from base_aux.aux_iter.m1_iter_aux import *
from base_aux.aux_argskwargs.m1_argskwargs import *
from base_aux.aux_types.m1_type_aux import *

from base_aux.base_inits.m1_nest_init_source import *
from base_aux.aux_attr.m1_attr1_aux import *


# =====================================================================================================================
@final
class AnnotAttrAux(AttrAux):
    """
    GOAL
    ----
    work with all __annotations__
        from all nested classes
        in correct order

    RULES
    -----
    1. nesting available with correct order!
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
        nested = self.annot_only__dict_types()
        for key in nested:
            if not AttrAux(self.SOURCE).name_ic__check_exists(key):
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
            dict_type = self.annot_only__dict_types()
            msg = f"[CRITICAL]{not_defined=} in {dict_type=}"
            raise Exx__AnnotNotDefined(msg)

    # =================================================================================================================
    def annot_only__dict_types(self) -> dict[str, type[Any]]:
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

    def annot_only__dict_values(self) -> TYPING.KWARGS_FINAL:
        """
        GOAL
        ----
        get dict with only existed values! no raise if value not exists!
        """
        result = {}
        for key in self.annot_only__dict_types():
            if hasattr(self.SOURCE, key):
                result.update({key: getattr(self.SOURCE, key)})
        return result

    # -----------------------------------------------------------------------------------------------------------------
    def annot_only__str_pretty(self) -> str:
        """just a pretty string for debugging or research.
        """
        result = f"{self.SOURCE.__class__.__name__}(Annotations):"
        annots = self.annot_only__dict_values()
        if annots:
            for key, value in annots.items():
                result += f"\n\t{key}={value}"
        else:
            result += f"\nEmpty=Empty"

        print(result)
        return result

    # =================================================================================================================
    def iter_mro(self) -> Iterable[type]:
        """
        GOAL
        ----
        iter only important user classes from mro
        """
        yield from TypeAux(self.SOURCE).iter_mro_user(
            # NestGAI_AttrIC,
            # NestGSAI_AttrAnycase,
            # NestGA_AttrIC, NestGI_AttrIC,
            # NestSA_AttrAnycase, NestSI_AttrAnycase,
        )

    def iter_names(self) -> Iterable[str]:
        """
        iter all (with not existed)
        """
        yield from self.annot_only__dict_types()

    def iter_values(self) -> Iterable[Any]:
        """
        only existed
        """
        yield from self.annot_only__dict_values().values()

    # =================================================================================================================
    def set_annots_only__by_args(self, *args: Any) -> None | NoReturn:
        """
        ARGS - ARE VALUES! not names!

        IF ARGS MORE then Annots - NoRaise! You should lnow what you do!    # FIXME: decide?
        """
        if len(args) > len(self.list_annots()):
            raise IndexError(f"{args=}/{self=}")
        return self.set_annots_attrs__by_kwargs(**dict(zip(self.iter_names(), args)))

    def set_annots_attrs__by_args_kwargs(self, *args: Any, **kwargs: TYPING.KWARGS_FINAL) -> None | NoReturn:
        """
        CREATED SPECIALLY FOR
        ---------------------
        NestInit_AnnotsAttrByKwArgs
        """
        self.set_annots_only__by_args(*args)
        self.set_annots_attrs__by_kwargs(**kwargs)

    def set_annots_attrs__by_kwargs(self, **kwargs: TYPING.KWARGS_FINAL) -> None:
        return self.values__set_by_dict(kwargs)

    # =================================================================================================================
    def getitem(self, item: str | int) -> Any | NoReturn:
        try:
            index = int(item)
            return self.value_annot__get_by_index(index)
        except:
            name = str(item)
            return self.value_attr__get_by_name(name)

    def setitem(self, item: str | int, value: Any) -> None | NoReturn:
        try:
            index = int(item)
            return self.annot__set_by_index(index, value)
        except:
            name = str(item)
            return self.annots_attr__set_by_name(name, value)

    # =================================================================================================================
    def value_annot__get_by_index(self, index: int | str) -> Any | NoReturn:
        name = self.name__get_by_index(index)
        if name:
            return self.value_attr__get_by_name(name)
        else:
            raise IndexError(f"{index=}/{self=}")

    def value_attr__get_by_name(self, name: str) -> Any | NoReturn:
        return AttrAux(self.SOURCE).getattr_ic(name)

    # -----------------------------------------------------------------------------------------------------------------
    def annots_attr__set_by_name(self, name: str, value: Any = None) -> None:
        """
        GOAL
        ----
        set name/value by intended name from Annots or direct Attrs! or even not existsed!
        without creation new annot!
        """
        if self.name__check_exists(name):
            name = self.name__get_original(name)

        AttrAux(self.SOURCE).setattr_ic(name, value)

    def annot__set_by_index(self, index: int | str, value: Any = None) -> bool | NoReturn:
        """
        GOAL
        ----
        set value for existed annot
        """
        name = self.name__get_by_index(index)
        if name:
            self.annots_attr__set_by_name(name, value)
            return True
        else:
            raise IndexError(f"{index=}/{self=}")

    # -----------------------------------------------------------------------------------------------------------------
    def values__set_by_dict(self, data: TYPING.KWARGS_FINAL) -> None:
        """
        GOAL
        ----
        SAME AS AttrAux.SetValues but assume names from annots!
        # set attrs for annotated names (fixme: ???? AND STD ATTRS! - it seems OK!
        # so annots+attrs used like filter

        SPECIALLY CREATED FOR
        ---------------------
        load into AnnotTemplate
        """
        for key, value in data.items():
            self.annots_attr__set_by_name(key, value)

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

    # -----------------------------------------------------------------------------------------------------------------
    def values__delete(self) -> None:
        """
        GOAL
        ----
        delattr all annotated aux_attr!
        """
        for name in self.iter_names():
            if hasattr(self.SOURCE, name):
                delattr(self.SOURCE, name)

    def values__reinit_by_types(self, not_existed: bool = None) -> None:
        """
        GOAL
        ----
        delattr all annotated aux_attr!
        """
        for name, value in self.annot_only__dict_types().items():
            if not_existed and hasattr(self.SOURCE, name):
                continue

            value = TypeAux(value).type__init_value__default()
            setattr(self.SOURCE, name, value)

    # =================================================================================================================
    def list_annots(self) -> list[str]:
        return list(self.annot_only__dict_types())

    def index_check_available(self, index: int | str) -> bool:
        return len(self.list_annots()) > index

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

        for cls in self.iter_mro():
            for name in names:
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
        cls = TypeAux(self.SOURCE).get__class()

        for name in names:
            annots = cls.__annotations__
            if name not in annots:
                cls.__annotations__.update({name: Any})

    def name__get_original(self, name: str) -> str | None:
        """
        GOAL
        ----
        check name exists in annots ONLY!
        """
        annots = self.annot_only__dict_types()
        name = IterAux(annots).item__get_original(name)
        if name == NoValue:
            name = None
        return name

    def name__get_by_index(self, index: int | str) -> str | None:
        """
        GOAL
        ----
        get name for annotated attr by index
        """
        try:
            return self.list_annots()[int(index)]
        except:
            return

    def name__check_exists(self, name: str) -> bool:
        """
        GOAL
        ----
        check name exists in annots ONLY!
        """
        return self.name__get_original(name) is not None


# =====================================================================================================================
