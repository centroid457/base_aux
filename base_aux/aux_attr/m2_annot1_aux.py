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
    # =================================================================================================================
    def annots__get_not_defined(self) -> list[str]:
        """
        GOAL
        ----
        return list of not defined annotations

        SPECIALLY CREATED FOR
        ---------------------
        annot__check_all_defined
        """
        result = []
        nested = self.dump_dict__annot_types()
        for key in nested:
            if not self.name_ic__check_exists(key):
                result.append(key)
        return result

    def annots__check_all_defined(self) -> bool:
        """
        GOAL
        ----
        check if all annotated aux_attr have value!
        """
        return not self.annots__get_not_defined()

    def annots__check_all_defined_or_raise(self) -> None | NoReturn:
        """
        GOAL
        ----
        check if all annotated aux_attr have value!
        """
        not_defined = self.annots__get_not_defined()
        if not_defined:
            dict_type = self.dump_dict__annot_types()
            msg = f"[CRITICAL]{not_defined=} in {dict_type=}"
            raise Exx__AnnotNotDefined(msg)

    # =================================================================================================================
    def dump_dict__annot_types(self) -> dict[str, type[Any]]:
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
        for cls in self._iter_mro():
            _result_i = dict(cls.__annotations__)
            _result_i.update(result)
            result = _result_i
        return result

    # =================================================================================================================
    def _iter_mro(self) -> Iterable[type]:
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

    def iter__annot_names(self) -> Iterable[str]:
        """
        iter all (with not existed)
        """
        yield from self.dump_dict__annot_types()

    def iter__annot_values(self) -> Iterable[Any]:
        """
        only existed
        """
        yield from self.dump_dict().values()

    # =================================================================================================================
    def list_annots(self) -> list[str]:
        return list(self.dump_dict__annot_types())

    def name_ic__get_original(self, name_index: str | int) -> str | None:
        # 1=annots ---------
        name_annot = IterAux(self.list_annots()).item__get_original(name_index)
        if name_annot not in [NoValue, None]:
            return name_annot

        # 2=attrs ---------
        return super().name_ic__get_original(name_index)

    def name_annot__get_by_index(self, index: int | str) -> str | None:
        """
        GOAL
        ----
        get name for annotated attr by index
        """
        try:
            return self.list_annots()[int(index)]
        except:
            return

    # INDEX ===========================================================================================================
    def index_annot__check_available(self, index: int | str) -> bool:
        return len(self.list_annots()) > int(index)

    # =================================================================================================================
    def set_annots_attrs__by_args_kwargs(self, *args: Any, **kwargs: TYPING.KWARGS_FINAL) -> None | NoReturn:
        """
        CREATED SPECIALLY FOR
        ---------------------
        NestInit_AnnotsAttrByKwArgs
        """
        self.set_annots_only__by_args(*args)
        self.set_annots_attrs__by_kwargs(**kwargs)

    def set_annots_only__by_args(self, *args: Any) -> None | NoReturn:
        """
        ARGS - ARE VALUES! not names!

        IF ARGS MORE then Annots - NoRaise! You should lnow what you do!    # FIXME: decide?
        """
        if len(args) > len(self.list_annots()):
            raise IndexError(f"{args=}/{self=}")
        return self.set_annots_attrs__by_kwargs(**dict(zip(self.iter__annot_names(), args)))

    def set_annots_attrs__by_kwargs(self, **kwargs: TYPING.KWARGS_FINAL) -> None:
        return self.values__set_by_dict(kwargs)

    # =================================================================================================================
    def annots_attr__set_by_name(self, name: str, value: Any = None) -> None:
        """
        GOAL
        ----
        set name/value by intended name from Annots or direct Attrs! or even not existsed!
        without creation new annot!
        """
        if self.name_ic__check_exists(name):
            name = self.name_ic__get_original(name)

        self.sai_ic(name, value)

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
        for name in self.iter__annot_names():
            if hasattr(self.SOURCE, name):
                setattr(self.SOURCE, name, None)

    def values__set_none__all(self) -> None:
        """
        GOAL
        ----
        set None for all annotated aux_attr! even not existed!
        """
        for name in self.iter__annot_names():
            setattr(self.SOURCE, name, None)

    # -----------------------------------------------------------------------------------------------------------------
    def values__delete(self) -> None:
        """
        GOAL
        ----
        delattr all annotated aux_attr!
        """
        for name in self.iter__annot_names():
            if hasattr(self.SOURCE, name):
                delattr(self.SOURCE, name)

    def values__reinit_by_types(self, not_existed: bool = None) -> None:
        """
        GOAL
        ----
        delattr all annotated aux_attr!
        """
        for name, value in self.dump_dict__annot_types().items():
            if not_existed and hasattr(self.SOURCE, name):
                continue

            value = TypeAux(value).type__init_value__default()
            setattr(self.SOURCE, name, value)


# =====================================================================================================================
