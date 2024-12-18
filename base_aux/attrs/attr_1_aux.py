from typing import *
from base_aux.lambdas import LambdaTrySuccess, Lambda


# =====================================================================================================================
class AttrAuxIter:
    @classmethod
    def iter__not_private(cls, source: Any) -> Iterable[str]:
        for name in dir(source):
            if not name.startswith("__"):
                yield name

    @classmethod
    def iter__not_hidden(cls, source: Any) -> Iterable[str]:
        for name in dir(source):
            if not name.startswith("_"):
                yield name


# =====================================================================================================================
class AttrAuxAnycase:
    """
    NOTICE
    ------
    if there are several same attrs in different cases - you should resolve it by yourself!
    """
    # NAME ------------------------------------------------------------------------------------------------------------
    @classmethod
    def anycase__find(cls, name: str | Any, source: Any) -> str | None:
        """
        get attr name in original register
        """
        if not isinstance(name, str):
            return

        name = name.strip()
        for name in AttrAuxIter.iter__not_private(source):
            if name.lower() == str(name).lower():
                return name

        return

    @classmethod
    def anycase__check_exists(cls, name: str | Any, source: Any) -> bool:
        return cls.anycase__find(name=name,source=source) is None

    # ATTR ------------------------------------------------------------------------------------------------------------
    @classmethod
    def anycase__getattr(cls, name: str, source: Any) -> Any | Callable | NoReturn:
        """
        get attr value by name in any register
        no execution! return pure value as represented in object!
        """
        name_original = cls.anycase__find(name, source)
        if name_original is None:
            raise AttributeError(name)

        return getattr(source, name_original)

    @classmethod
    def anycase__setattr(cls, name: str, value: Any, source: Any) -> None | NoReturn:
        """
        get attr value by name in any register
        no execution! return pure value as represented in object!

        NoReturn - in case of not accepted names when setattr
        """
        name_original = cls.anycase__find(name, source)
        if name_original is None:
            if not isinstance(name, str):
                raise AttributeError(name)

            name = name.strip()
            if name in ["", ]:
                raise AttributeError(name)
            name_original = name

        # NOTE: you still have no exx with setattr(source, "    HELLO", value) and ""
        setattr(source, name_original, value)

    # ITEM ------------------------------------------------------------------------------------------------------------
    @classmethod
    def anycase__getitem(cls, name: str, source: Any) -> Any | Callable | NoReturn:
        return cls.anycase__getattr(name, source)

    @classmethod
    def anycase__setitem(cls, name: str, value: Any, source: Any) -> None | NoReturn:
        cls.anycase__setattr(name, value, source)


# =====================================================================================================================
class AttrAuxDump:
    @classmethod
    def to_dict(cls, source: Any, callables_skip: bool = None, callables_resolve: bool = None) -> dict[str, Any | Callable | Exception]:
        """
        GOAL
        ____
        make a dict from any object from attrs (not hidden)

        SPECIALLY CREATED FOR
        ---------------------
        using any object as rules for Translator
        """
        result = {}
        for name in AttrAuxIter.iter__not_hidden(source):
            if callables_skip and LambdaTrySuccess(getattr, source, name) and callable(getattr(source, name)):
                continue

            value = getattr(source, name)
            if callables_resolve:
                value = Lambda(value).get_result_or_exx()

            result.update({name: value})

        return result

    @classmethod
    def to_dict__callables_skip(cls, source: Any) -> dict[str, Any]:
        return cls.to_dict(source=source, callables_skip=True)

    @classmethod
    def to_dict__callables_resolve(cls, source: Any) -> dict[str, Any]:
        return cls.to_dict(source=source, callables_resolve=True)


# =====================================================================================================================
@final
class AttrAux(AttrAuxIter, AttrAuxAnycase, AttrAuxDump):
    pass


# =====================================================================================================================
