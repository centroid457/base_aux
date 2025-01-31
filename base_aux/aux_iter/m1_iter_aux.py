from typing import *
from base_aux.base_inits.m1_source import *


# =====================================================================================================================
TYPE__ITERABLE = Union[dict, list, tuple, set, Iterable]    # FIXME: add Iterable!!!

TYPE__ITER_PATH_KEY = Union[Any, int]
TYPE__ITER_PATH = tuple[TYPE__ITER_PATH_KEY, ...]


# =====================================================================================================================
@final
class IterAux(InitSource):
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
    SOURCE: TYPE__ITERABLE = dict
    # PATH: list[TYPE__ITER_PATH_KEY]   # todo: get back!!! to work with source! or make new class!

    # def init_post(self):
    #     self.PATH = []

    def item__get_original(self, item: Any) -> Any | None:
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
        for value in self.SOURCE:
            if value == item or str(value).lower() == str(item).lower():
                return value

    # -----------------------------------------------------------------------------------------------------------------
    def path__get_original(self, *path: TYPE__ITER_PATH_KEY) -> TYPE__ITER_PATH | None:
        """
        NOTES:
        1. path used as address KEY for dicts and as INDEX for other listed data
        2. separator is only simple SLASH '/'!

        :param path:
        :return:
            None - if path is unreachable/incorrect
            tuple[Any] - reachable path which could be used to get VALUE from data by chain data[i1][i2][i3]
        """

        # TODO: add attribute acceptable in path! and separate as Extruder?
        source = self.SOURCE
        if not path:
            return ()

        # work ----------------------------
        result = []
        for path_i in path:
            if isinstance(source, dict):
                address_original = IterAux(source).item__get_original(path_i)
                if not address_original:
                    return
                source = source[address_original]

            elif isinstance(source, set):
                msg = f"{source=},inconvenient type SET"
                raise TypeError(msg)

            else:
                # elif isinstance(source, (list, tuple)) or True:
                try:
                    address_original = int(path_i)
                    source = source[address_original]
                except:
                    return

            result.append(address_original)

        return tuple(result)

    # -----------------------------------------------------------------------------------------------------------------
    def value__get(self, *path: TYPE__ITER_PATH_KEY) -> Any | NoReturn:
        result = self.SOURCE
        path = self.path__get_original(*path)
        for path_i in path:
            result = result[path_i]
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
                    source[path_i] = value
                else:
                    source = source[path_i]
        except:
            return False

        return True


# =====================================================================================================================
