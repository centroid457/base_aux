from typing import *
from base_aux.lambdas import LambdaTrySuccess, Lambda
from base_aux.base_source import *
from base_aux.base_argskwargs import TYPE__LAMBDA_KWARGS
from base_aux.base_enums import CallablesUse


# =====================================================================================================================
@final
class AttrAux(InitSource):
    """
    NOTICE
    ------
    if there are several same attrs in different cases - you should resolve it by yourself!
    """

    # =================================================================================================================
    pass

    # ITER ------------------------------------------------------------------------------------------------------------
    def iter__not_private(self) -> Iterable[str]:
        for name in dir(self.SOURCE):
            if not name.startswith("__"):
                yield name

    def iter__not_hidden(self) -> Iterable[str]:
        for name in dir(self.SOURCE):
            if not name.startswith("_"):
                yield name

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
        for name_original in self.iter__not_private():
            if name_original.lower() == name.lower():
                return name_original

        return

    def anycase__check_exists(self, name: str) -> bool:
        return self.anycase__find(name) is not None

    # ATTR ------------------------------------------------------------------------------------------------------------
    def anycase__getattr(self, name: str) -> Any | Callable | NoReturn:
        """
        get attr value by name in any register
        no execution! return pure value as represented in object!
        """
        name_original = self.anycase__find(name)
        if name_original is None:
            raise AttributeError(name)

        return getattr(self.SOURCE, name_original)

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

    # DUMP ------------------------------------------------------------------------------------------------------------
    def dump_dict(self, callables_use: CallablesUse = CallablesUse.DIRECT) -> dict[str, Any | Callable | Exception] | NoReturn:
        """
        GOAL
        ____
        make a dict from any object from attrs (not hidden)

        SPECIALLY CREATED FOR
        ---------------------
        using any object as rules for Translator
        """
        result = {}
        for name in self.iter__not_hidden():
            if (
                    callables_use == CallablesUse.SKIP
                    and
                    LambdaTrySuccess(getattr, self.SOURCE, name)
                    and
                    callable(getattr(self.SOURCE, name))
            ):
                continue

            value = getattr(self.SOURCE, name)
            if callables_use == CallablesUse.RESOLVE_EXX:
                value = Lambda(value).get_result_or_exx()

            result.update({name: value})

        return result

    def dump_dict__callables_skip(self) -> TYPE__LAMBDA_KWARGS:
        return self.dump_dict(CallablesUse.SKIP)

    def dump_dict__callables_resolve_exx(self) -> dict[str, Any | Exception]:
        return self.dump_dict(CallablesUse.RESOLVE_EXX)

    def dump_dict__callables_resolve_raise(self) -> dict[str, Any] | NoReturn:
        return self.dump_dict(CallablesUse.RESOLVE_RAISE)

    # -----------------------------------------------------------------------------------------------------------------
    def dump__pretty_str(self) -> str:
        result = f"{self.SOURCE.__class__.__name__}(Attributes):"
        data = self.dump_dict__callables_resolve_exx()
        if data:
            for key, value in data.items():
                result += f"\n\t{key}={value}"
        else:
            result += f"\nEmpty=Empty"

        return result

    def __str__(self):
        return self.dump__pretty_str()


# =====================================================================================================================
