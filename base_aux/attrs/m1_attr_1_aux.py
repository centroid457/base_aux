from typing import *
import re

from base_aux.base_source.source import InitSource
from base_aux.base_argskwargs.argskwargs import TYPE__LAMBDA_KWARGS
from base_aux.base_enums.enums import CallablesUse

from base_aux.attrs.m0_static import AttrsDump, AnnotsTemplate

# from base_aux.lambdas.lambdas import Lambda   # CIRCULAR_IMPORT=TRY USE IT ONLY ON OUT CODE! not inside base_aux!


# =====================================================================================================================
@final
class AttrAux(InitSource):
    """
    NOTICE
    ------
    if there are several same attrs in different cases - you should resolve it by yourself!
    """
    # SOURCE = Lambda(AttrsDump)
    SOURCE = AttrsDump

    # =================================================================================================================
    def get_name__private_external(self, dirname: str) -> str | None:
        """
        typically BUILTIN - NOT INCLUDED!

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

            # fixme: cant solve problem for GetattrPrefixInst_RaiseIf! in case of _GETATTR__PREFIXES!!!
            for cls in mro:
                if dirname.startswith(f"_{cls.__name__}__"):
                    name_external = dirname.replace(f"_{cls.__name__}", "")
                    return name_external

    # =================================================================================================================
    # def __contains__(self, item: str):      # IN=DONT USE IT! USE DIRECT METHOD anycase__check_exists
    #     return self.anycase__check_exists(item)

    # ITER ------------------------------------------------------------------------------------------------------------
    def iter__external_not_builtin(self) -> Iterable[str]:
        """
        GOAL
        ----
        1/ iter only without builtins!!!
        2/ use EXT private names!

        SPECIALLY CREATED FOR
        ---------------------
        this class - all iterations!
        """
        for name in dir(self.SOURCE):
            # filter builtin ----------
            if name.startswith("__"):
                continue

            # filter private external ----------
            name_private_ext = self.get_name__private_external(name)
            if name_private_ext:
                yield name_private_ext
                continue

            # direct user attr ----------
            # print(f"{name=}")
            yield name

    # -----------------------------------------------------------------------------------------------------------------
    def iter__not_hidden(self) -> Iterable[str]:
        """
        NOTE
        ----
        hidden names are more simple to detect then private!
        cause of private methods(!) changes to "_<ClsName><__MethName>"

        """
        for name in self.iter__external_not_builtin():
            if not name.startswith("_"):
                yield name

    def iter__not_private(self) -> Iterable[str]:
        for name in self.iter__external_not_builtin():
            if not name.startswith("__"):
                yield name

    def iter__private(self) -> Iterable[str]:
        """
        BUILTIN - NOT INCLUDED!

        GOAL
        ----
        collect all privates in original names! without ClassName-Prefix

        BEST IDEA
        ---------
        keep list of iters
        """
        for name in self.iter__external_not_builtin():
            if name.startswith("__"):
                yield name

    # def __iter__(self):     # DONT USE IT! USE DIRECT METHODS
    #     yield from self.iter__not_hidden()

    # =================================================================================================================
    pass

    # NAME ------------------------------------------------------------------------------------------------------------
    def anycase__find(self, name: str) -> str | None:
        """
        get attr name in original register
        """
        if not isinstance(name, str):
            return

        name = str(name).strip()
        if not name:
            return

        for name_original in self.iter__external_not_builtin():
            if name_original.lower() == name.lower():
                return name_original

        return

    def anycase__check_exists(self, name: str) -> bool:
        return self.anycase__find(name) is not None

    # ATTR ------------------------------------------------------------------------------------------------------------
    def anycase__getattr(self, name: str) -> Any | Callable | NoReturn:
        """
        GOAL
        ----
        get attr value by name in any register
        no execution/resolving! return pure value as represented in object!
        """
        name_original = self.anycase__find(name)
        if name_original is None:
            raise AttributeError(name)

        value = getattr(self.SOURCE, name_original)
        return value

    def anycase__setattr(self, name: str, value: Any) -> None | NoReturn:
        """
        get attr value by name in any register
        no execution! return pure value as represented in object!

        NoReturn - in case of not accepted names when setattr
        """
        if not isinstance(name, str):
            raise AttributeError(name)

        name = name.strip()
        if name in ["", ]:
            raise AttributeError(name)

        name_original = self.anycase__find(name)
        if name_original is None:
            name_original = name

        # NOTE: you still have no exx with setattr(self.SOURCE, "    HELLO", value) and ""
        setattr(self.SOURCE, name_original, value)

    def anycase__delattr(self, name: str) -> None:
        name_original = self.anycase__find(name)
        if name_original is None:
            return      # already not exists

        delattr(self.SOURCE, name_original)

    # ITEM ------------------------------------------------------------------------------------------------------------
    def anycase__getitem(self, name: str) -> Any | Callable | NoReturn:
        return self.anycase__getattr(name)

    def anycase__setitem(self, name: str, value: Any) -> None | NoReturn:
        self.anycase__setattr(name, value)

    def anycase__delitem(self, name: str) -> None:
        self.anycase__delattr(name)

    # =================================================================================================================
    pass

    # LOAD ------------------------------------------------------------------------------------------------------------
    def load(self, other: dict | Any, callables_use: CallablesUse = CallablesUse.DIRECT, template: dict | type[AnnotsTemplate] = None) -> Any | AttrsDump:
        """
        GOAL
        ----
        load attrs by dict/attrs in other object
        """
        if isinstance(other, dict):
            return self.load__by_dict(other, template=template)
        else:
            return self.load__by_obj(other, callables_use=callables_use, template=template)

    def load__by_dict(self, other: dict, template: dict | type[AnnotsTemplate] = None) -> Any | AttrsDump:
        """
        MAIN ITEA
        ----------
        LOAD MEANS basically setup final values for final not callables values!
        but you can use any types for your own!
        expected you know what you do and do exactly ready to use final values/not callables in otherObj!

        NOTE
        ----
        dont use callables_use


        :param template: used as filter!
            if you have callables and dont want to use them (raise acceptable) or not need some attrs - just use it as filter!
        """
        # template ----------
        if not isinstance(template, dict):
            template = template.__annotations__
        template_dump = AttrAux().load(template)

        # work ----------
        for key, value in other.items():
            if template:
                if AttrAux(template_dump).anycase__check_exists(key):
                    key = AttrAux(template_dump).anycase__find(key)
                    self.anycase__setattr(key, value)
            else:
                self.anycase__setattr(key, value)
        return self.SOURCE

    def load__by_obj(self, other: Any, callables_use: CallablesUse = CallablesUse.DIRECT, template: dict | type[AnnotsTemplate] = None) -> Any | AttrsDump:
        """
        its a derivative additional meth for load__by_dict
        NOTE
        ----
        return AttrsDump in case of using directly without source AttrsAux().load__by_obj(other) -> AttrsDump()
        """
        other = AttrAux(other).dump_dict(callables_use=callables_use, template=template)
        return self.load__by_dict(other)     # here must be DIRECT

    # =================================================================================================================
    pass

    # DUMP ------------------------------------------------------------------------------------------------------------
    def dump_obj(self, callables_use: CallablesUse = CallablesUse.DIRECT, template: dict | Any = None) -> AttrsDump | NoReturn:
        pass
        # TODO: finish

    def dump_dict(self, callables_use: CallablesUse = CallablesUse.RESOLVE_EXX, template: dict | Any = None) -> dict[str, Any | Callable | Exception] | NoReturn:
        """
        MAIN ITEA
        ----------
        BUMPS MEANS basically save final values for all (even any dynamic/callables) values! or only not callables!

        GOAL
        ----
        make a dict from any object from attrs (not hidden)

        SPECIALLY CREATED FOR
        ---------------------
        using any object as rules for Translator
        """
        result = {}
        # TODO: add template!
        # if template is not None:
        #     template: AttrsDump = AttrAux().load(template)

        for name in self.iter__not_hidden():

            value = None
            # resolve properties --------------
            try:
                value = getattr(self.SOURCE, name)
            except Exception as exx:
                if callables_use == CallablesUse.SKIP or callables_use == CallablesUse.RESOLVE_RAISE_SKIP:
                    continue
                elif callables_use == CallablesUse.RESOLVE_EXX:
                    value = exx

            # resolve callables ------------------
            if callable(value):
                if callables_use == CallablesUse.SKIP:
                    continue

                try:
                    value = value()
                except Exception as exx:
                    if callables_use == CallablesUse.RESOLVE_EXX:
                        value = exx
                    elif callables_use == CallablesUse.RESOLVE_RAISE_SKIP:
                        continue
                    elif callables_use == CallablesUse.RESOLVE_RAISE:
                        raise exx

            result.update({name: value})

        return result

    def dump_dict__callables_resolve_exx(self) -> dict[str, Any | Exception]:
        """
        MAIN DERIVATIVE!
        """
        return self.dump_dict(CallablesUse.RESOLVE_EXX)

    def dump_dict__direct(self) -> TYPE__LAMBDA_KWARGS:
        return self.dump_dict(CallablesUse.DIRECT)

    def dump_dict__callables_skip(self) -> TYPE__LAMBDA_KWARGS:
        return self.dump_dict(CallablesUse.SKIP)

    def dump_dict__callables_resolve_raise(self) -> dict[str, Any] | NoReturn:
        return self.dump_dict(CallablesUse.RESOLVE_RAISE)

    # -----------------------------------------------------------------------------------------------------------------
    def dump__pretty_str(self) -> str:
        result = f"{self.SOURCE.__class__.__name__}(Attributes):"
        data = self.dump_dict(CallablesUse.RESOLVE_EXX)
        if data:
            for key, value in data.items():
                result += f"\n\t{key}={value}"
        else:
            result += f"\nEmpty=Empty"

        return result


# =====================================================================================================================
