from typing import *
from base_aux.lambdas import LambdaTrySuccess, Lambda
from base_aux.base_source import *
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

    # ITEM ------------------------------------------------------------------------------------------------------------
    def anycase__getitem(self, name: str) -> Any | Callable | NoReturn:
        return self.anycase__getattr(name)

    def anycase__setitem(self, name: str, value: Any) -> None | NoReturn:
        self.anycase__setattr(name, value)

    # =================================================================================================================
    pass

    # DUMP ------------------------------------------------------------------------------------------------------------
    def dump_dict(self, callables_do: CallablesUse = CallablesUse.DIRECT) -> dict[str, Any | Callable | Exception]:
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
            if callables_do == CallablesUse.SKIP and LambdaTrySuccess(getattr, self.SOURCE, name) and callable(getattr(self.SOURCE, name)):
                continue

            value = getattr(self.SOURCE, name)
            if callables_do == CallablesUse.RESOLVE_EXX:
                value = Lambda(value).get_result_or_exx()

            result.update({name: value})

        return result

    def dump_dict__callables_skip(self) -> dict[str, Any]:
        return self.dump_dict(CallablesUse.SKIP)

    def dump_dict__callables_resolve(self) -> dict[str, Any]:
        return self.dump_dict(CallablesUse.RESOLVE_EXX)

    # -----------------------------------------------------------------------------------------------------------------
    def dump__pretty_str(self) -> str:
        result = f"{self.SOURCE.__class__.__name__}(Attributes):"
        data = self.dump_dict__callables_resolve()
        if data:
            for key, value in data.items():
                result += f"\n\t{key}={value}"
        else:
            result += f"\nEmpty=Empty"

        return result

    def __str__(self):
        return self.dump__pretty_str()


# =====================================================================================================================
