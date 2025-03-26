from typing import *
import copy

from base_aux.base_nest_dunders.m1_init1_source import *
from base_aux.base_statics.m4_enums import *
from base_aux.base_statics.m1_types import *


# =====================================================================================================================
# @final
class Base_DictAux(NestInit_Source):
    """
    GOAL
    ----
    collect all methods in one class
    """
    SOURCE: TYPING.DICT_ANY_ANY = dict
    SOURCE_INLINE_DEEPCOPY: Enum_SourceOrigOrCopy = Enum_SourceOrigOrCopy.COPY

    # -----------------------------------------------------------------------------------------------------------------
    def init_post(self) -> None | NoReturn:
        if self.SOURCE_INLINE_DEEPCOPY == Enum_SourceOrigOrCopy.ORIGINAL:
            pass
        if self.SOURCE_INLINE_DEEPCOPY == Enum_SourceOrigOrCopy.COPY:
            self.SOURCE = copy.deepcopy(self.SOURCE)

    # -----------------------------------------------------------------------------------------------------------------
    def values_clear(self) -> TYPING.DICT_ANY_NONE:
        for key in self.SOURCE:
            self.SOURCE[key] = None
        return self.SOURCE

    def values_change__by_func(self, func: Callable[[Any], Any], walk: bool = None) -> TYPING.DICT_ANY_ANY:
        """
        NOTE
        ----
        1/ func work with final/elementary value (not collection) - userClass or Elementary Inst
        2/ func make sure without NoReturn!!!
        3/ FILTERS - use inside func!!! and change values inline!

        GOAL
        ----
        change values by func

        SPECIALLY CREATED FOR
        ---------------------
        json prepare_serialisation - in part of make all values Elementary
        """
        # -----------------------
        for key, value in self.SOURCE.items():
            if isinstance(value, TYPES.ELEMENTARY_COLLECTION):
                if walk:
                    if isinstance(value, dict):
                        value = DictAuxInline(value).values_change__by_func(func, walk=walk)

                    elif isinstance(value, (list, tuple, set)):   # , tuple, set - too complicated!
                        result = []
                        for item in value:
                            if isinstance(item, dict):
                                item = DictAuxInline(item).values_change__by_func(func, walk=walk)
                            else:
                                item = func(item)    # NOTE: make sure no NoReturn!!!
                            result.append(item)
                        value = result
                else:
                    continue
            else:
                value = func(value)     # NOTE: make sure no NoReturn!!!

            self.SOURCE[key] = value

        return self.SOURCE

    # -----------------------------------------------------------------------------------------------------------------
    def keys_del(self, *keys: Any) -> TYPING.DICT_ANY_ANY:
        for key in keys:
            try:
                self.SOURCE.pop(key)
            except:
                pass

        return self.SOURCE

    def keys_change__by_func(self, func: Callable[[Any], Any], walk: bool = None) -> TYPING.DICT_ANY_ANY:
        """
        GOAL
        ----
        useful to rename keys by func like str.LOWER/upper
        raise on func - delete key from origin! applied like filter ---NO! keep original value!

        SPECIALLY CREATED FOR
        ---------------------
        json prepare_serialisation - in part of make all keys STR!
        """
        # -----------------------
        for key, value in dict(self.SOURCE).items():
            # value -------
            if walk:
                if isinstance(value, dict):
                    value = DictAuxInline(value).keys_change__by_func(func, walk=walk)

                elif isinstance(value, (list, tuple, set)):
                    for item in value:
                        if isinstance(item, dict):
                            item = DictAuxInline(item).keys_change__by_func(func, walk=walk)

            # name -------
            try:
                key_new = func(key)
                self.keys_del(key)
                self.SOURCE[key_new] = value
            except:
                pass

        return self.SOURCE

    # -----------------------------------------------------------------------------------------------------------------
    def key_collapse(self, key: Any) -> TYPING.DICT_ANY_ANY:
        """
        GOAL
        ----
        specially created for 2level-dicts (when values could be a dict)
        so it would replace values (if they are dicts and have special_key)

        CONSTRAINTS
        -----------
        it means that you have similar dicts with same exact keys
            {
                0: 0,
                1: {1:1, 2:2, 3:3},
                2: {1:11, 2:22, 3:33},
                3: {1:111, 2:222, 3:333},
                4: 4,
            }
        and want to get special slice like result

        SPECIALLY CREATED FOR
        ---------------------
        testplans get results for special dut from all results


        main idia to use values like dicts as variety and we can select now exact composition! remain other values without variants

        EXAMPLES
        --------
        dicts like
            {
                1: {1:1, 2:2, 3:3},
                2: {1:1, 2:None},
                3: {1:1},
                4: 4,
            }
        for key=2 return
            {
                1: 2,
                2: None,
                3: None,
                4: 4,
            }

        """
        for root_key, root_value in self.SOURCE.items():
            if isinstance(root_value, dict) and key in root_value:
                self.SOURCE[root_key] = root_value.get(key)

        return self.SOURCE

    # -----------------------------------------------------------------------------------------------------------------
    def prepare_serialisation(self) -> TYPING.DICT_STR_ELEM:
        """
        NOTE
        ----
        work not in source! return copy with ready to direct serialisation keys/values

        GOAL
        ----
        make ready for serialisation
        1/ fix keys - str
        2/ fix values - elementary
        """
        result = {}
        # TODO: FINISH
        result = {}
        for key, value in self.SOURCE.items():
            if isinstance(value, dict):
                value = DictAuxCopy(value).prepare_serialisation()

            if isinstance(value, (list)):
                value = DictAuxCopy(value).prepare_serialisation()

            result[key] = value

        return result


# =====================================================================================================================
@final
class DictAuxInline(Base_DictAux):
    SOURCE_INLINE_DEEPCOPY = Enum_SourceOrigOrCopy.ORIGINAL


@final
class DictAuxCopy(Base_DictAux):
    SOURCE_INLINE_DEEPCOPY = Enum_SourceOrigOrCopy.COPY


# =====================================================================================================================
