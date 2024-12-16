from typing import *
from base_aux.base_argskwargs.novalue import NoValue
from base_aux.lambdas import LambdaTrySuccess


# =====================================================================================================================
class AttrAuxIter:
    @classmethod
    def attrs__iter_not_private(cls, source: Any) -> Iterable[str]:
        for name in dir(source):
            if not name.startswith("__"):
                yield name

    @classmethod
    def attrs__iter_not_hidden(cls, source: Any) -> Iterable[str]:
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
    def attr_anycase__find(cls, item: str | Any, source: Any = NoValue) -> str | None:
        """
        get attr name in original register
        """
        if not isinstance(item, str):
            return

        item = item.strip()
        if source == NoValue:
            source = cls  # seems it is not good idea!!!

        for name in AttrAuxIter.attrs__iter_not_private(source):
            if name.lower() == str(item).lower():
                return name

        return

    # ATTR ------------------------------------------------------------------------------------------------------------
    @classmethod
    def getattr_anycase(cls, item: str, obj: Any) -> Any | Callable | NoReturn:
        """
        get attr value by name in any register
        no execution! return pure value as represented in object!
        """
        name_original = cls.attr_anycase__find(item, obj)
        if name_original is None:
            raise AttributeError(item)

        return getattr(obj, name_original)

    @classmethod
    def setattr_anycase(cls, item: str, value: Any, obj: Any) -> None | NoReturn:
        """
        get attr value by name in any register
        no execution! return pure value as represented in object!

        NoReturn - in case of not accepted names when setattr
        """
        name_original = cls.attr_anycase__find(item, obj)
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
    def getitem_anycase(cls, item: str, obj: Any) -> Any | Callable | NoReturn:
        return cls.getattr_anycase(item, obj)

    @classmethod
    def setitem_anycase(cls, item: str, value: Any, obj: Any) -> None | NoReturn:
        cls.setattr_anycase(item, value, obj)


# =====================================================================================================================
class AttrAuxDump:
    @classmethod
    def to_dict__direct(cls, source: Any, callables_drop: bool = None) -> dict[str, Any]:
        """
        GOAL
        ____
        make a dict from any object from attrs (not hidden)

        SPECIALLY CREATED FOR
        ---------------------
        using any object as rules for Translator
        """
        result = {}
        for name in AttrAuxIter.attrs__iter_not_hidden(source):
            result.update({name: getattr(source, name)})
            # TODO: finish!!!


            if callables_drop and LambdaTrySuccess(getattr, source, name) and callable(getattr(source, name)):
                continue


        return result

    @classmethod
    def to_dict__not_callable(cls, source: Any) -> dict[str, Any]:
        pass


# =====================================================================================================================
class AttrAux(AttrAuxIter, AttrAuxAnycase, AttrAuxDump):
    pass


# =====================================================================================================================
