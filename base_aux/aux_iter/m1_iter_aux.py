from typing import *
from base_aux.base_inits.m1_nest_init_source import *
from base_aux.aux_types.m1_type_aux import *
from base_aux.aux_attr.m1_attr1_aux import *


# =====================================================================================================================
TYPE__ITERABLE_ORDERED = Union[dict, list, tuple, Iterable]     # "SET" - DONT USE!

TYPE__ITER_PATH_KEY = Union[Any, int]   # Any is for dict
TYPE__ITER_PATH = tuple[TYPE__ITER_PATH_KEY, ...]


# =====================================================================================================================
@final
class IterAux(NestInit_Source):
    """
    collect universal funcs which work with collections

    NOTE
    ----
    for access abilities passing with strings - resolve it by yourself

        assert self.victim("1/2", {1: 11, }) is None
        assert self.victim("1/2", {1: {2: 22}, }) == Explicit([1, 2, ])
        assert self.victim("1/2/1", {1: {2: [30, 31, 32]}, }) == Explicit([1, 2, 1])

        assert self.victim("hello", {"hello": [1]}) == Explicit(["hello", ])
        assert self.victim("hello/1", {"hello": [1]}) is None
        assert self.victim("hello/0", {"hello": [1]}) == Explicit(["hello", 0])

        assert self.victim("hello1/hello2", {"hello1": {"hello2": [1]}}) == Explicit(["hello1", "hello2"])
        assert self.victim("hello1/hello2/0", {"hello1": {"hello2": [1]}}) == Explicit(["hello1", "hello2", 0, ])
        assert self.victim("hello1/hello2/1", {"hello1": {"hello2": [1]}}) is None
    """
    SOURCE: TYPE__ITERABLE_ORDERED = dict
    # PATH: list[TYPE__ITER_PATH_KEY]   # todo: get back!!! to work with source! or make new class!

    # def init_post(self):
    #     self.PATH = []

    def item__get_original(self, item: Any) -> Any | NoValue:
        """
        get FIRST original item from any collection by comparing str(expected).lower()==str(original).lower().

        # NOTE:
        # 1. NONE RESULT__VALUE - RESOLVED!!!
        # 2. SEVERAL VALUES - not used! by now it is just FIRST matched!
        #     several items? - it is not useful!!! returning first is most expected!
        #
        # USEFUL in case-insensitive systems (like terminals or serial devices) or object structured by prefix-names:
        # 1. get key in dict
        # 2. find attribute name in aux_types
        #
        # :param item:
        # :return: actual item from collection
        #     None - if VALUE is unreachable/notFind
        """
        # if TypeAux(self.SOURCE).check__iterable_not_str():
        if isinstance(self.SOURCE, (list, tuple, dict, set)):
            values = self.SOURCE
        else:
            values = AttrAux(self.SOURCE).iter__not_private()

        for value in values:
            try:
                if value == item or str(value).lower() == str(item).lower():
                    return value
            except:
                pass

        return NoValue

    # -----------------------------------------------------------------------------------------------------------------
    def path__get_original(self, *path: TYPE__ITER_PATH_KEY) -> TYPE__ITER_PATH | None | NoReturn:
        """
        NOTES:
        1. path used as address KEY for dicts and as INDEX for other listed data
        2. separator is only simple SLASH '/'!

        :param path:
        :return:
            None - if path is unreachable/incorrect
            tuple[Any] - reachable path which could be used to get VALUE from data by chain data[i1][i2][i3]
        """
        source = self.SOURCE
        if not path:
            return None

        # work ----------------------------
        result = []
        for path_i in path:
            address_original = NoValue

            if isinstance(source, dict):
                address_original = IterAux(source).item__get_original(path_i)
                if address_original == NoValue:
                    return
                else:
                    source = source[address_original]

            elif isinstance(source, set):
                raise TypeError(f"{source=}")

            elif isinstance(source, (list, tuple)):
                try:
                    source = source[int(path_i)]
                    address_original = int(path_i)  # place last!
                except:
                    return

            else:
                address_original = AttrAux(source).anycase__name_original(str(path_i))
                if address_original is None:
                    return
                else:
                    source = getattr(source, address_original)

            # -----------------------------
            result.append(address_original)

        return tuple(result)

    # -----------------------------------------------------------------------------------------------------------------
    def value__check_exist(self, item: Any) -> bool:
        return self.item__get_original(item) is not NoValue

    # -----------------------------------------------------------------------------------------------------------------
    def value__get(self, *path: TYPE__ITER_PATH_KEY) -> Any | NoReturn:
        result = self.SOURCE
        path = self.path__get_original(*path)
        for path_i in path:
            try:
                result = result[path_i]
            except:
                result = AttrAux(result).anycase__getattr(path_i)     # raise

        return result

    def value__set(self, path: TYPE__ITER_PATH, value: Any) -> bool:
        """
        GOAL
        ----
        INLINE WORK!
        """
        source = self.SOURCE

        # work ----------------------------
        path = self.path__get_original(*path)
        try:
            length = len(path)
            for pos, path_i in enumerate(path, start=1):
                if pos == length:
                    try:
                        source[path_i] = value
                    except:
                        AttrAux(source).anycase__setattr(path_i, value)     # raise
                    return True
                else:
                    source = IterAux(source).value__get(path_i)
        except:
            return False


# =====================================================================================================================
