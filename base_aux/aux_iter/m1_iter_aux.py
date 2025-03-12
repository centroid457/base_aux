from typing import *

from base_aux.aux_attr.m1_annot_attr1_aux import *
from base_aux.base_nest_dunders.m1_init1_source import *
from base_aux.aux_types.m1_type_aux import *
from base_aux.base_statics.m1_types import *


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
    SOURCE: TYPING.ORDERED_ITERABLE = dict
    # PATH: list[TYPING.ITERPATH_KEY]   # todo: get back!!! to work with source! or make new class!

    # def init_post(self):
    #     self.PATH = []

    # -----------------------------------------------------------------------------------------------------------------
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
            values = AttrAux(self.SOURCE).iter__names_not_private()

        for value in values:
            try:
                if value == item or str(value).lower() == str(item).lower():
                    return value
            except:
                pass

        return NoValue

    # -----------------------------------------------------------------------------------------------------------------
    def item__check_exist(self, item: Any) -> bool:
        return self.item__get_original(item) is not NoValue

    # -----------------------------------------------------------------------------------------------------------------
    def keypath__get_original(self, *keypath: TYPING.ITERPATH_KEY) -> TYPING.ITERPATH | None | NoReturn:
        """
        NOTES:
        1. keypath used as address KEY for dicts and as INDEX for other listed data
        2. separator is only simple SLASH '/'!

        :param keypath:
        :return:
            None - if keypath is unreachable/incorrect
            tuple[Any] - reachable keypath which could be used to get VALUE from data by chain data[i1][i2][i3]
        """
        source = self.SOURCE
        if not keypath:
            return ()   # ROOT is OK!

        # work ----------------------------
        result = []
        for key_i in keypath:
            key_original = NoValue

            if isinstance(source, dict):
                key_original = IterAux(source).item__get_original(key_i)
                if key_original == NoValue:
                    return
                else:
                    source = source[key_original]

            elif isinstance(source, set):
                raise TypeError(f"{source=}")

            elif isinstance(source, (list, tuple)):
                try:
                    source = source[int(key_i)]
                    key_original = int(key_i)  # place last!
                except:
                    return

            else:
                key_original = AttrAux(source).name_ic__get_original(str(key_i))
                if key_original is None:
                    return
                else:
                    source = getattr(source, key_original)

            # -----------------------------
            result.append(key_original)

        return tuple(result)

    # -----------------------------------------------------------------------------------------------------------------
    def value__get(self, *keypath: TYPING.ITERPATH_KEY) -> Any | NoReturn:
        result = self.SOURCE
        keypath = self.keypath__get_original(*keypath)
        for key_i in keypath:
            try:
                result = result[key_i]
            except:
                result = AttrAux(result).gai_ic(key_i)     # raise

        return result

    def value__set(self, keypath: TYPING.ITERPATH, value: Any) -> bool:
        """
        GOAL
        ----
        INLINE WORK!
        """
        source = self.SOURCE

        # work ----------------------------
        keypath = self.keypath__get_original(*keypath)
        try:
            length = len(keypath)
            for pos, key_i in enumerate(keypath, start=1):
                if pos == length:
                    try:
                        source[key_i] = value
                    except:
                        AttrAux(source).sai_ic(key_i, value)     # raise
                    return True
                else:
                    source = IterAux(source).value__get(key_i)
        except:
            return False

    # -----------------------------------------------------------------------------------------------------------------
    def get_first_is_not(self, *variants: Any) -> Any | None:
        """
        GOAL
        ----
        from iterable get first is not None value!
        typically get value from params active/sub_default/default

        SPECIALY CREATED FOR
        --------------------
        Base_ReAttempts to get flags
        """
        for item in self.SOURCE:
            if not variants:
                return item

            if any([item is variant for variant in variants]):    # CMP ONLY BY IS_NOT_NONE!!! dont use '==' cause of __EQ__!
                continue
            else:
                return item

    def get_first_is_not_none(self) -> Any | None:
        return self.get_first_is_not(None)


# =====================================================================================================================
