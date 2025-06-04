from typing import *
import re

from base_aux.aux_attr.m4_dump_dumped import *
from base_aux.base_statics.m4_enums import *
from base_aux.base_statics.m1_types import *
from base_aux.aux_callable.m1_callable import CallableAux
from base_aux.aux_types.m1_type_aux import *
# from base_aux.aux_iter.m1_iter_aux import *   # dont add! import error!
from base_aux.aux_cmp_eq.m3_eq_valid1_base import Base_EqValid


# =====================================================================================================================
TYPING__NAME_FINAL = str
TYPING__NAME_DRAFT = str | int | Any


# =====================================================================================================================
# @final    # NOTE: use nesting in Annots!
class AttrAux(NestInit_Source):
    """
    NOTE
    ----
    1. if there are several same aux_attr in different cases - you should resolve it by yourself!

    ANNOTS
    ------
    names intended in annots

    DIFFERENCE from AnnotAux
    ------------------------
    1/ iter names
        - dump dict
        - cmp eq by dumped dict
    2/ AnnotAux is not listing methods! list only annots!

    FIXME: add skip methods??? seems it need!
    """
    # SOURCE: Any
    SOURCE: Any = AttrDumped
    SKIP_NAMES: tuple[str | Base_EqValid, ...] = ()

    _ATTRS_STYLE: Enum_AttrAnnotsOrExisted = Enum_AttrAnnotsOrExisted.ATTRS_EXISTED
    _ANNOTS_DEPTH: Enum_AnnotsDepthAllOrLast = Enum_AnnotsDepthAllOrLast.ALL_NESTED

    # =================================================================================================================
    def __init__(self, source: Any = NoValue, *skip_names: str | Base_EqValid) -> None:
        super().__init__(source)
        if skip_names:
            self.SKIP_NAMES = skip_names

    # =================================================================================================================
    def name__check_is_method(self, name_original: str) -> bool:
        try:
            value = getattr(self.SOURCE, name_original)
        except:
            return False

        return TypeAux(value).check__callable_meth()

    # =================================================================================================================
    def ITER_NAMES_SOURCE(self) -> Iterable[TYPING__NAME_FINAL]:
        if self._ATTRS_STYLE == Enum_AttrAnnotsOrExisted.ATTRS_EXISTED:
            yield from self.iter__attrs_external_not_builtin()
        elif self._ATTRS_STYLE == Enum_AttrAnnotsOrExisted.ANNOTS_ONLY:
            yield from self.iter__annot_names()
        else:
            raise Exx__Incompatible(f"{self._ATTRS_STYLE=}/{self._ANNOTS_DEPTH=}")

    # -----------------------------------------------------------------------------------------------------------------
    pass

    # def __contains__(self, item: str):      # IN=DONT USE IT! USE DIRECT METHOD anycase__check_exists
    #     return self.anycase__check_exists(item)

    def iter__attrs_external_not_builtin(self) -> Iterable[TYPING__NAME_FINAL]:
        """
        NOTE
        ----
        BEST WAY TO USE EXACTLY iter__not_private

        GOAL
        ----
        1/ iter ALL (without builtins)!!!
        2/ use EXT private names!

        SPECIALLY CREATED FOR
        ---------------------
        this class - all iterations!
        """
        for name in dir(self.SOURCE):
            # filter-1 skip ----------
            if name in self.SKIP_NAMES:
                continue

            # filter-2 builtin ----------
            if name.startswith("__") and name.endswith("__"):
                continue

            # filter private external ----------
            try:
                name_private_ext = self.get_name__private_external(name)
                if name_private_ext is not None:
                    name = name_private_ext
            except:
                continue

            # if self.name__check_is_method(name):    # FIXME: DONT USE HERE!!! or resolve what to do!!!
            #     continue

            # direct user attr ----------
            # print(f"{name=}")
            yield name

    # -----------------------------------------------------------------------------------------------------------------
    def iter__names(self, attr_level: Enum_AttrScope = Enum_AttrScope.NOT_PRIVATE) -> Iterable[TYPING__NAME_FINAL]:
        # -------------------------------------------------
        for name in self.ITER_NAMES_SOURCE():
            if name in self.SKIP_NAMES:
                continue

            if attr_level == Enum_AttrScope.NOT_PRIVATE:
                if not name.startswith("__"):
                    yield name

            elif attr_level == Enum_AttrScope.NOT_HIDDEN:
                if not name.startswith("_"):
                    yield name

            elif attr_level == Enum_AttrScope.PRIVATE:
                if name.startswith("__"):
                    yield name

            elif attr_level == Enum_AttrScope.ALL:
                yield name

            else:
                raise Exx__Incompatible(f"{attr_level=}")

    def iter__names_not_hidden(self) -> Iterable[TYPING__NAME_FINAL]:
        """
        NOTE
        ----
        hidden names are more simple to detect then private!
        cause of private methods(!) changes to "_<ClsName><__MethName>"
        """
        return self.iter__names(Enum_AttrScope.NOT_HIDDEN)

    def iter__names_not_private(self) -> Iterable[TYPING__NAME_FINAL]:
        """
        NOTE
        ----
        BEST WAY TO USE EXACTLY iter__not_private
        """
        return self.iter__names(Enum_AttrScope.NOT_PRIVATE)

    def iter__names_private(self) -> Iterable[TYPING__NAME_FINAL]:
        """
        BUILTIN - NOT INCLUDED!

        NOTE
        ----
        BEST WAY TO USE EXACTLY iter__not_private

        GOAL
        ----
        collect all privates in original names! without ClassName-Prefix

        BEST IDEA
        ---------
        keep list of iters
        """
        return self.iter__names(Enum_AttrScope.PRIVATE)

    # def __iter__(self):     # DONT USE IT! USE DIRECT METHODS
    #     yield from self.iter__not_hidden()

    # -----------------------------------------------------------------------------------------------------------------
    def _iter_mro(self) -> Iterable[type]:
        """
        GOAL
        ----
        iter only important user classes from mro
        """
        yield from TypeAux(self.SOURCE).iter_mro_user(
            # NestGAI_AnnotAttrIC,
            # NestGSAI_AttrAnycase,
            # NestGA_AnnotAttrIC, NestGI_AnnotAttrIC,
            # NestSA_AttrAnycase, NestSI_AttrAnycase,
        )

    def iter__annot_names(self) -> Iterable[TYPING__NAME_FINAL]:
        """
        iter all (with not existed)
        """
        yield from self.dump_dict__annot_types()

    def iter__annot_values(self) -> Iterable[Any]:
        """
        only existed
        """
        for name in self.list__annots():
            try:
                yield self.gai_ic(name)
            except:
                pass

    # -----------------------------------------------------------------------------------------------------------------
    def list__annots(self) -> list[TYPING__NAME_FINAL]:
        return list(self.dump_dict__annot_types())

    # =================================================================================================================
    def reinit__mutable_values(self) -> None:
        """
        GOAL
        ----
        reinit default mutable values from class dicts/lists on instantiation.
        usually intended blank values.

        REASON
        ------
        for dataclasses you should use field(dict) but i think it is complicated (but of cause more clear)

        SPECIALLY CREATED FOR
        ---------------------
        Nest_AttrKit
        """
        for attr in self.iter__names_not_private():
            try:
                value = getattr(self.SOURCE, attr)
            except:
                continue

            if isinstance(value, dict):
                setattr(self.SOURCE, attr, dict(value))
            elif isinstance(value, list):
                setattr(self.SOURCE, attr, list(value))
            elif isinstance(value, set):
                setattr(self.SOURCE, attr, set(value))

    def reinit__annots_by_None(self) -> None:
        """
        GOAL
        ----
        set None for all annotated aux_attr! even not existed!
        """
        for name in self.iter__annot_names():
            self.sai_ic(name, None)

    def reinit__annots_by_types(self, not_existed: bool = None) -> None:
        """
        GOAL
        ----
        delattr all annotated aux_attr!
        """
        for name, value in self.dump_dict__annot_types().items():
            if not_existed and hasattr(self.SOURCE, name):
                continue

            value = TypeAux(value).type__init_value__default()
            self.sai_ic(name, value)

    # =================================================================================================================
    def get_name__private_external(self, dirname: str) -> TYPING__NAME_FINAL | None:
        """
        typically BUILTIN - NOT INCLUDED!

        NOTE
        ----
        BEST WAY TO USE EXACTLY iter__not_private

        GOAL
        ----
        using name (from dir(obj)) return user-friendly name! external name!

        REASON
        ------
        here in example - "__hello" will never appear directly!!!
        class Cls:
            ATTR1 = 1
            def __hello(self, *args) -> None:
                kwargs = dict.fromkeys(args)
                self.__init_kwargs(**kwargs)

        name='_Cls__hello' hasattr(self.SOURCE, name)=True
        name='__class__' hasattr(self.SOURCE, name)=True
        name='__delattr__' hasattr(self.SOURCE, name)=True
        name='__dict__' hasattr(self.SOURCE, name)=True
        name='__dir__' hasattr(self.SOURCE, name)=True
        name='__doc__' hasattr(self.SOURCE, name)=True
        ///
        name='ATTR1' hasattr(self.SOURCE, name)=True
        """
        # filter not hidden -------
        if not dirname.startswith("_"):
            return

        # filter private builtin -------
        if dirname.startswith("__"):
            return

        # parse private user -------
        if re.fullmatch(r"_.+__.+", dirname):
            # print(f"{dirname=}")
            # print(f"{self.SOURCE=}")
            try:
                # print(11)
                mro = self.SOURCE.__mro__
            except:
                # print(111)
                mro = self.SOURCE.__class__.__mro__
                # print(f"{mro=}")

            # fixme: cant solve problem for NestGa_Prefix_RaiseIf! in case of _GETATTR__PREFIXES!!!
            for cls in mro:
                if dirname.startswith(f"_{cls.__name__}__"):
                    name_external = dirname.replace(f"_{cls.__name__}", "")
                    return name_external

    # -----------------------------------------------------------------------------------------------------------------
    def name_ic__get_original(self, name_index: TYPING__NAME_DRAFT) -> TYPING__NAME_FINAL | None:
        """
        get attr name_index in original register
        """
        name_index = str(name_index)

        # name as index for annots -------
        index = None
        try:
            index = int(name_index)
        except:
            pass

        if index is not None:
            return self.list__annots()[index]  # dont place in try sentence

        # name as str for annots/attrs ------
        name_index = str(name_index).strip()

        if not name_index:
            return

        for name_original in self.iter__attrs_external_not_builtin():
            if name_original.lower() == name_index.lower():
                return name_original

        return

    def name_ic__check_exists(self, name_index: TYPING__NAME_DRAFT) -> bool:
        return self.name_ic__get_original(name_index) is not None

    def name__check_have_value(self, name_index: TYPING__NAME_DRAFT) -> bool:
        """
        GOAL
        ----
        check attr really existed!
        separate exx on getattr (like for property) and name-not-existed.
        used only due to annots!

        SPECIALLY CREATED FOR
        ---------------------
        dump_dict - because in there if not value exists - logic is differ from base logic! (here we need to pass!)
        """
        name_final = self.name_ic__get_original(name_index)
        if name_final:
            return hasattr(self.SOURCE, name_final)
        else:
            return False

    # -----------------------------------------------------------------------------------------------------------------
    def annots__ensure(self) -> None:
        """
        GOAL
        ----
        unsure access to __annotations__ if it was not created on class!

        REASON
        ------
        if class have not any annotations and you will access them over instance - raise!
        but if you will first access annotations over class - no raise!

            AttributeError: 'AttrDumped' object has no attribute '__annotations__'

        SPECIALLY CREATED FOR
        ---------------------
        annots__append
        """
        try:
            self.SOURCE.__class__.__annotations__
        except:
            pass

        try:
            self.SOURCE.__annotations__
        except:
            pass

    def annots__append(self, **kwargs: type | Any) -> AttrDumped | Any:
        """
        GOAL
        ----
        add new annot in last position

        BEST USAGE
        ----------
        create NEW OBJECT

        SPECIALLY CREATED FOR
        ---------------------
        TextFormatted
        """
        self.annots__ensure()
        annots: dict[str, type] = self.SOURCE.__annotations__
        for key, value in kwargs.items():
            if value is None:
                value_type = Any
            elif not TypeAux(value).check__class():
                value_type = type(value)
            else:
                value_type = value

            # set type
            if key.lower() not in [key_orig.lower() for key_orig in annots]:
                annots.update({key: value_type})

            # set value
            if value != value_type:
                self.sai_ic(key, value)

        return self.SOURCE

    def annots__get_not_defined(self) -> list[TYPING__NAME_FINAL]:
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

    def annots__check_all_defined_or_raise(self) -> bool | NoReturn:
        """
        GOAL
        ----
        check if all annotated aux_attr have value!
        """
        not_defined = self.annots__get_not_defined()
        if not_defined:
            dict_type = self.dump_dict__annot_types()
            msg = f"[CRITICAL]{not_defined=} in {dict_type=}"
            raise Exx__NotExistsNotFoundNotCreated(msg)

        return True

    # =================================================================================================================
    def gai_ic(self, name_index: TYPING__NAME_DRAFT) -> Any | Callable | NoReturn:
        """
        GOAL
        ----
        get attr value by name_index in any register
        no execution/resolving! return pure value as represented in object!
        """
        name_original = self.name_ic__get_original(name_index)

        if name_index == "__name__":        # this is a crutch! костыль!!!!
            result = "ATTRS"
            result = self.SOURCE.__class__.__name__
            return result

        if name_original is None:
            raise IndexError(f"{name_index=}/{self=}")

        return getattr(self.SOURCE, name_original)

    def sai_ic(self, name_index: TYPING__NAME_DRAFT, value: Any) -> None | NoReturn:
        """
        get attr value by name_index in any register
        no execution! return pure value as represented in object!

        NoReturn - in case of not accepted names when setattr
        """
        name_original: str = self.name_ic__get_original(name_index)
        if name_original is None:
            name_original = name_index

        if not name_original:
            raise IndexError(f"{name_index=}/{self=}")

        # NOTE: you still have no exx with setattr(self.SOURCE, "    HELLO", value) and ""
        setattr(self.SOURCE, name_original, value)
        pass

    def dai_ic(self, name_index: TYPING__NAME_DRAFT) -> None:
        name_original = self.name_ic__get_original(name_index)
        if name_original is None:
            return      # already not exists

        delattr(self.SOURCE, name_original)

    # -----------------------------------------------------------------------------------------------------------------
    def gai_ic__callable_resolve(self, name_index: TYPING__NAME_DRAFT, callables_resolve: Enum_CallResolve = Enum_CallResolve.DIRECT) -> Any | Callable | Enum_CallResolve | NoReturn:
        """
        SAME AS
        -------
        CallableAux(*).resolve_*

        WHY NOT-1=CallableAux(*).resolve_*
        ----------------------------------
        it is really the same, BUT
        1. additional try for properties (could be raised without calling)
        2. cant use here cause of Circular import accused
        """
        # resolve property --------------
        # result_property = CallableAux(getattr).resolve(callables_resolve, self.SOURCE, realname)
        # TypeAux

        try:
            value = self.gai_ic(name_index)
        except Exception as exx:
            if callables_resolve == Enum_CallResolve.SKIP_RAISED:
                return Enum_ProcessResult.SKIPPED
            elif callables_resolve == Enum_CallResolve.EXX:
                return exx
            elif callables_resolve == Enum_CallResolve.RAISE_AS_NONE:
                return None
            elif callables_resolve == Enum_CallResolve.RAISE:
                raise exx
            elif callables_resolve == Enum_CallResolve.BOOL:
                return False
            else:
                raise exx

        # resolve callables ------------------
        result = CallableAux(value).resolve(callables_resolve)
        return result

    # -----------------------------------------------------------------------------------------------------------------
    def sai__by_args_kwargs(self, *args: Any, **kwargs: dict[str, Any]) -> Any | NoReturn:
        """
        MAIN ITEA
        ----------
        LOAD MEANS basically setup final values for final not callables values!
        but you can use any types for your own!
        expected you know what you do and do exactly ready to use final values/not callables in otherObj!
        """
        self.sai__by_args(*args)
        self.sai__by_kwargs(**kwargs)

        return self.SOURCE

    def sai__by_args(self, *args: Any) -> Any | NoReturn:
        for index, value in enumerate(args):
            self.sai_ic(index, value)

        return self.SOURCE

    def sai__by_kwargs(self, **kwargs: dict[str, Any]) -> Any | NoReturn:
        for name, value in kwargs.items():
            self.sai_ic(name, value)

        return self.SOURCE

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
        if self._ANNOTS_DEPTH == Enum_AnnotsDepthAllOrLast.ALL_NESTED:
            for cls in self._iter_mro():
                _result_i = dict(cls.__annotations__)
                _result_i.update(result)
                result = _result_i
        elif self._ANNOTS_DEPTH == Enum_AnnotsDepthAllOrLast.LAST_CHILD:
            result = dict(self.__annotations__)

        else:
            raise Exx__Incompatible(f"{self._ANNOTS_DEPTH=}")

        return result

    # -----------------------------------------------------------------------------------------------------------------
    def dump_dict(
            self,
            *skip_names: str | Base_EqValid,
            callables_resolve: Enum_CallResolve = Enum_CallResolve.EXX,
    ) -> dict[str, Any | Callable | Exception] | NoReturn:
        """
        MAIN IDEA
        ----------
        BUMPS MEANS basically save final values for all (even any dynamic/callables) values! or only not callables!
        SKIP NOT EXISTED ANNOTS!!!

        NOTE
        ----
        DUMP WITHOUT PRIVATE NAMES

        GOAL
        ----
        make a dict from any object from aux_attr (not hidden)

        SPECIALLY CREATED FOR
        ---------------------
        using any object as rules for Translator
        """
        skip_names = skip_names or []
        result = {}
        for name in self.iter__names_not_private():
            # skip is attr not exist
            if not self.name__check_have_value(name):
                continue
            if name in skip_names:
                continue

            value = self.gai_ic__callable_resolve(name_index=name, callables_resolve=callables_resolve)
            if value is Enum_ProcessResult.SKIPPED:
                continue
            result.update({name: value})

        return result

    def dump_dict__resolve_exx(self, *skip_names: str | Base_EqValid) -> dict[str, Any | Exception]:
        """
        MAIN DERIVATIVE!
        """
        return self.dump_dict(*skip_names, callables_resolve=Enum_CallResolve.EXX)

    def dump_dict__direct(self, *skip_names: str | Base_EqValid) -> TYPING.KWARGS_FINAL:
        return self.dump_dict(*skip_names, callables_resolve=Enum_CallResolve.DIRECT)

    def dump_dict__skip_callables(self, *skip_names: str | Base_EqValid) -> TYPING.KWARGS_FINAL:
        return self.dump_dict(*skip_names, callables_resolve=Enum_CallResolve.SKIP_CALLABLE)

    def dump_dict__skip_raised(self, *skip_names: str | Base_EqValid) -> dict[str, Any] | NoReturn:
        return self.dump_dict(*skip_names, callables_resolve=Enum_CallResolve.RAISE)

    # -----------------------------------------------------------------------------------------------------------------
    def dump_obj(
            self,
            *skip_names: str | Base_EqValid,
            callables_resolve: Enum_CallResolve = Enum_CallResolve.EXX,
    ) -> AttrDumped | NoReturn:
        data = self.dump_dict(*skip_names, callables_resolve=callables_resolve)
        obj = AttrAux(AttrDumped()).sai__by_args_kwargs(**data)
        return obj

    def dump_obj__resolve_exx(self, *skip_names: str | Base_EqValid) -> dict[str, Any | Exception]:
        """
        MAIN DERIVATIVE!
        """
        return self.dump_obj(*skip_names, callables_resolve=Enum_CallResolve.EXX)

    def dump_obj__direct(self, *skip_names: str | Base_EqValid) -> TYPING.KWARGS_FINAL:
        return self.dump_obj(*skip_names, callables_resolve=Enum_CallResolve.DIRECT)

    def dump_obj__skip_callables(self, *skip_names: str | Base_EqValid) -> TYPING.KWARGS_FINAL:
        return self.dump_obj(*skip_names, callables_resolve=Enum_CallResolve.SKIP_CALLABLE)

    def dump_obj__skip_raised(self, *skip_names: str | Base_EqValid) -> dict[str, Any] | NoReturn:
        return self.dump_obj(*skip_names, callables_resolve=Enum_CallResolve.RAISE)

    # -----------------------------------------------------------------------------------------------------------------
    def dump_str__pretty(
            self,
            *skip_names: str | Base_EqValid,
            callables_resolve: Enum_CallResolve = Enum_CallResolve.EXX,
    ) -> str:
        try:
            result = f"{self.SOURCE.__class__.__name__}(Attributes):"
        except:
            result = f"{self.SOURCE.__name__}(Attributes):"

        for key, value in self.dump_dict(*skip_names, callables_resolve=callables_resolve).items():
            result += f"\n    {key}={value}"
        else:
            result += f"\nEmpty=Empty"

        return result


# =====================================================================================================================
@final
class AnnotsAllAux(AttrAux):
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
    _ATTRS_STYLE: Enum_AttrAnnotsOrExisted = Enum_AttrAnnotsOrExisted.ANNOTS_ONLY
    _ANNOTS_DEPTH: Enum_AnnotsDepthAllOrLast = Enum_AnnotsDepthAllOrLast.ALL_NESTED


# ---------------------------------------------------------------------------------------------------------------------
@final
class AnnotsLastAux(AttrAux):
    """
    GOAL
    ----
    separate last/all nesting parents annotations
    """
    _ATTRS_STYLE: Enum_AttrAnnotsOrExisted = Enum_AttrAnnotsOrExisted.ANNOTS_ONLY
    _ANNOTS_DEPTH: Enum_AnnotsDepthAllOrLast = Enum_AnnotsDepthAllOrLast.LAST_CHILD


# =====================================================================================================================
