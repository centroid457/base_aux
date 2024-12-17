from typing import *
from base_aux.base_argskwargs.novalue import NoValue
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
    def anycase__find(cls, item: str | Any, source: Any = NoValue) -> str | None:
        """
        get attr name in original register
        """
        if not isinstance(item, str):
            return

        item = item.strip()
        if source == NoValue:
            source = cls  # seems it is not good idea!!!

        for name in AttrAuxIter.iter__not_private(source):
            if name.lower() == str(item).lower():
                return name

        return

    # ATTR ------------------------------------------------------------------------------------------------------------
    @classmethod
    def anycase__getattr(cls, item: str, obj: Any) -> Any | Callable | NoReturn:
        """
        get attr value by name in any register
        no execution! return pure value as represented in object!
        """
        name_original = cls.anycase__find(item, obj)
        if name_original is None:
            raise AttributeError(item)

        return getattr(obj, name_original)

    @classmethod
    def anycase__setattr(cls, item: str, value: Any, obj: Any) -> None | NoReturn:
        """
        get attr value by name in any register
        no execution! return pure value as represented in object!

        NoReturn - in case of not accepted names when setattr
        """
        name_original = cls.anycase__find(item, obj)
        if name_original is None:
            if not isinstance(item, str):
                raise AttributeError(item)

            item = item.strip()
            if item in ["", ]:
                raise AttributeError(item)
            name_original = item

        # NOTE: you still have no exx with setattr(obj, "    HELLO", value) and ""
        setattr(obj, name_original, value)

    # ITEM ------------------------------------------------------------------------------------------------------------
    @classmethod
    def anycase__getitem(cls, item: str, obj: Any) -> Any | Callable | NoReturn:
        return cls.anycase__getattr(item, obj)

    @classmethod
    def anycase__setitem(cls, item: str, value: Any, obj: Any) -> None | NoReturn:
        cls.anycase__setattr(item, value, obj)


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
class AttrAux(AttrAuxIter, AttrAuxAnycase, AttrAuxDump):
    pass


# =====================================================================================================================
