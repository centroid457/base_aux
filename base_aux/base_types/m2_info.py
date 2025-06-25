"""
Designed to print info about object (properties+methods results)

But why? if we can use debugger directly?
Reason:
1. to get and save standard text info,
it useful to keep this info for future quick eye sight without exact condition like other OS or device/devlist/configuration
2. in debugger we cant see result of methods!
try to see for example information from platform module! it have only methods and no one in object tree in debugger!
```python
import platform

obj = platform
print(platform.platform())
pass    # place debug point here
```
3. Useful if you wish to see info from remote SOURCE if connecting directly over ssh for example

FEATURES
    "print all properties/methods results",
    "show exceptions on methods/properties",
    "skip names by full/part names and use only by partnames",
    "separated collections by groups",


TODO:
    "add TIMEOUT (use start in thread!) for print! use timeout for GETATTR!!!",
    [
        "realise PRINT_DIFFS=CHANGE_state/COMPARE_objects (one from different states like thread before and after start)!",
        "this is about to save object STATE!",
        "add parameter show only diffs or show all",
        "add TESTS after this step!",
    ],
    "apply asyncio.run for coroutine?",
    "merge items Property/Meth? - cause it does not matter callable or not (just add type info block)",
    "add check__instance_of_user_class",
"""
from typing import *

from base_aux.base_types.m0_static_aux import *
from base_aux.base_types.m1_type_aux import TypeAux
from base_aux.aux_attr.m0_static import check_name__buildin, NAMES__SKIP_PARTS


# =====================================================================================================================
def _value_search_by_list(source: Any, search_list: list[Any]) -> Any | None:
    search_list = search_list or []
    for search_item in search_list:
        try:
            if search_item in source:
                return search_item
        except:
            pass

        try:
            if search_item == source:
                return search_item
        except:
            pass


# =====================================================================================================================
class ObjectInfo:
    """
    :ivar MAX_ITER_ITEMS: 0 or None if not limited!
    """
    # SETTINGS --------------------------------------------
    MAX_LINE_LEN: int = 100
    MAX_ITER_ITEMS: int = 5
    HIDE_BUILD_IN: bool = None
    LOG_ITER: bool = None

    NAMES__USE_ONLY_PARTS: list[str] = []
    NAMES__SKIP_FULL: list[str] = []
    NAMES__SKIP_PARTS: list[str] = NAMES__SKIP_PARTS

    # AUX --------------------------------------------------
    SOURCE: Any = None
    STATE: ObjectState = None
    STATE_OLD: ObjectState | None = None

    def __init__(
            self,
            source: Optional[Any] = None,

            max_line_len: Optional[int] = None,
            max_iter_items: Optional[int] = None,
            hide_build_in: Optional[bool] = None,
            log_iter: Optional[bool] = None,

            names__use_only_parts: Union[None, str, list[str]] = None,
            names__skip_full: Union[None, str, list[str]] = None,
            names__skip_parts: str | list[str] = None,
    ):
        # SETTINGS -----------------------------------------------------------
        # RAPAMS -----------------------
        if max_line_len is not None:
            self.MAX_LINE_LEN = max_line_len
        if max_iter_items is not None:
            self.MAX_ITER_ITEMS = max_iter_items
        if hide_build_in is not None:
            self.HIDE_BUILD_IN = hide_build_in
        if log_iter is not None:
            self.LOG_ITER = log_iter

        # LISTS -----------------------
        if names__use_only_parts:
            if isinstance(names__use_only_parts, str):
                names__use_only_parts = [names__use_only_parts, ]
            self.NAMES__USE_ONLY_PARTS = names__use_only_parts
        if names__skip_full:
            if isinstance(names__skip_full, str):
                names__skip_full = [names__skip_full, ]
            self.NAMES__SKIP_FULL.extend(names__skip_full)
        if names__skip_parts:
            if isinstance(names__skip_parts, str):
                names__skip_parts = [names__skip_parts, ]
            self.NAMES__SKIP_PARTS = [*self.NAMES__SKIP_PARTS, *names__skip_parts]

        # WORK -----------------------------------------------------------
        self.state_reload()

        if source is not None:
            self.SOURCE = source

    # =================================================================================================================
    def state_clear(self) -> None:
        self.STATE_OLD = self.STATE
        self.STATE = ObjectState()

    def state_reload(self) -> None:
        self.state_clear()

        # WORK --------------------------------------
        group_name = f"log_iter={self.LOG_ITER}(wait last touched)"
        self._print_line__group_separator(group_name)

        for pos, name in enumerate(dir(self.SOURCE), start=1):
            if self.LOG_ITER:
                print(f"{pos}:\t{name}")

            # FILTER -----------------------------------------------------------------------
            if self.HIDE_BUILD_IN and check_name__buildin(name):
                continue

            if self.NAMES__USE_ONLY_PARTS:
                use_name = False
                for name_include_item in self.NAMES__USE_ONLY_PARTS:
                    if name_include_item.lower() in name.lower():
                        use_name = True
                        break
                if not use_name:
                    continue

            # SKIP ------------------------------------------------------------------------
            SKIP_FULLNAMES = []
            if self.NAMES__SKIP_FULL:
                SKIP_FULLNAMES.extend(self.NAMES__SKIP_FULL)
            if SKIP_FULLNAMES:
                SKIP_FULLNAMES.extend(SKIP_FULLNAMES)
            if name in SKIP_FULLNAMES:
                self.STATE.SKIPPED_FULLNAMES.append(name)
                continue

            SKIP_PARTNAMES = []
            if self.NAMES__SKIP_PARTS:
                SKIP_PARTNAMES.extend(self.NAMES__SKIP_PARTS)
            if SKIP_PARTNAMES:
                SKIP_PARTNAMES.extend(SKIP_PARTNAMES)
            if _value_search_by_list(source=name, search_list=SKIP_PARTNAMES):
                self.STATE.SKIPPED_PARTNAMES.append(name)
                continue

            # PROPERTIES/METHODS + Exception--------------------------------------------------
            attr_is_method: bool = False
            try:
                value = getattr(self.SOURCE, name)
            except Exception as exx:
                self.STATE.PROPERTIES__EXX.update({name: exx})
                continue

            if callable(value):
                attr_is_method = True
                try:
                    value = value()
                except Exception as exx:
                    self.STATE.METHODS__EXX.update({name: exx})
                    continue

            # print(f"{name=}/{attr_obj=}/type={type(attr_obj)}/elementary={isinstance(attr_obj, TYPES.ELEMENTARY)}")

            # PLACE VALUE ---------------------------------------------------------------------
            if TypeAux(value).check__elementary_single():
                if attr_is_method:
                    self.STATE.METHODS__ELEMENTARY_SINGLE.update({name: value})
                else:
                    self.STATE.PROPERTIES__ELEMENTARY_SINGLE.update({name: value})

            elif TypeAux(value).check__elementary_collection():
                if attr_is_method:
                    self.STATE.METHODS__ELEMENTARY_COLLECTION.update({name: value})
                else:
                    self.STATE.PROPERTIES__ELEMENTARY_COLLECTION.update({name: value})

            else:
                if attr_is_method:
                    self.STATE.METHODS__OBJECTS.update({name: value})
                else:
                    self.STATE.PROPERTIES__OBJECTS.update({name: value})

    # def state_diff_last(self):
    #     # NOTE: use attrsDUMP!!! instead! cause raised values may be moved into other group! (single/collection)
    #     self.state_reload()
    #     result = ObjectState()
    #     for (name_g1, values_g1), (name_g2, values_g2) in zip(self.STATE_OLD.items(), self.STATE.items()):
    #         for

    # =================================================================================================================
    def _print_line__group_separator(self, group_name: str) -> str:
        """
        GOAL MAIN - print!
        GOAL SECONDARY - return str - just for tests!!!
        """
        result = "-" * 10 + f"{group_name:-<90}"      # here is standard MAX_LINE_LEN
        print(result)
        return result

    def _print_line__name_type_value(self, name: Optional[str] = None, type_replace: Optional[str] = None, value: Union[None, Any, ItemKeyValue] = None, intend: Optional[int] = None) -> str:
        # -------------------------------
        name = name or ""
        if isinstance(value, ItemKeyValue):
            name = ""
        block_name = f"{name}"

        # -------------------------------
        block_type = f"{value.__class__.__name__}"
        if isinstance(value, ItemKeyValue):
            block_type = f"{value.KEY.__class__.__name__}:{value.VALUE.__class__.__name__}"
        if type_replace is not None:
            block_type = type_replace

        # -------------------------------
        intend = intend or 0
        if isinstance(value, ItemKeyValue):
            intend = 1

        _block_intend = "\t" * intend

        # -------------------------------
        block_value = f"{value}"
        if isinstance(value, ItemKeyValue):
            block_type = f"{value.KEY}:{value.VALUE}"
        elif TypeAux(value).check__exception():
            block_value = f"{value!r}"

        # -------------------------------
        result = f"{block_name:20}\t{block_type:12}:{_block_intend}{block_value}"

        if self.MAX_LINE_LEN and len(result) > self.MAX_LINE_LEN:
            result = result[:self.MAX_LINE_LEN - 3*2] + "..."

        # --------------------------------------------------------------------------------------
        print(result)

        # -------------------------------
        if name and str(value) != repr(value) and str(value) != str(block_value) and not TypeAux(value).check__exception():
            # additional print repr()
            self._print_line__name_type_value(name=None, type_replace="__repr()", value=repr(value))

        return result

    # =================================================================================================================
    def _print_block__head(self) -> None:
        # start printing ----------------------------------
        group_name = f"{self.__class__.__name__}.print"
        self._print_line__group_separator(group_name.upper())

        print(f"str(SOURCE)={str(self.SOURCE)}")
        print(f"repr(SOURCE)={repr(self.SOURCE)}")
        print(f"type(SOURCE)={type(self.SOURCE)}")

        try:
            mro = self.SOURCE.__class__.__mro__
        except:
            mro = self.SOURCE.__mro__

        mro = [cls.__name__ for cls in mro]

        print(f"mro(SOURCE)={mro}")

        # SETTINGS ----------------------------------------
        group_name = "SETTINGS"
        self._print_line__group_separator(group_name)

        print(f"{self.NAMES__USE_ONLY_PARTS=}")
        print(f"{self.NAMES__SKIP_FULL=}")
        print(f"{self.NAMES__SKIP_PARTS=}")

        print(f"{self.HIDE_BUILD_IN=}")
        print(f"{self.LOG_ITER=}")

        print(f"{self.MAX_LINE_LEN=}")
        print(f"{self.MAX_ITER_ITEMS=}")

    def _print_block__name_value(self, name, value) -> None:
        # ALWAYS ---------------------------------------------------------------------------------
        self._print_line__name_type_value(name=name, value=value)
        if len(str(value)) <= self.MAX_LINE_LEN:
            return

        # COLLECTION -----------------------------------------------------------------------------
        if TypeAux(value).check__elementary_collection():
            # start some pretty style -------------------------------------
            if not isinstance(value, dict):
                _index = 0
                for item in value:
                    _index += 1
                    if self.MAX_ITER_ITEMS and _index > self.MAX_ITER_ITEMS:
                        self._print_line__name_type_value(name=None, type_replace="", value="...", intend=1)
                        break
                    self._print_line__name_type_value(name=None, value=item, intend=1)

            elif isinstance(value, dict):
                _index = 0
                for item_key, item_value in value.items():
                    _index += 1
                    if self.MAX_ITER_ITEMS and _index > self.MAX_ITER_ITEMS:
                        self._print_line__name_type_value(name=None, type_replace="", value="...", intend=1)
                        break
                    self._print_line__name_type_value(name=None, value=ItemKeyValue(item_key, item_value))

        # SINGLE/EXX/OBJECTS ---------------------------------------------------------------------
        if any([
            TypeAux(value).check__elementary_single(),
            TypeAux(value).check__exception(),
            TypeAux(value).check__instance(),
        ]):
            pass    # DONT USE RETURN HERE OR ELIF IN NEXT LINE!!!

    # =================================================================================================================
    def print(self) -> None:
        """print all params from object
        if callable - try to call it!
        """
        WRAPPER_MAIN_LINE = "="*min(90, self.MAX_LINE_LEN)  # here we need use less then

        print(WRAPPER_MAIN_LINE)
        self._print_block__head()

        for group_name, group_values in self.STATE.__getstate__().items():
            self._print_line__group_separator(group_name)

            if TypeAux(group_values).check__elementary_collection_not_dict():
                for pos, name in enumerate(group_values, start=1):
                    print(f"{pos}:\t{name}")
            else:
                for name, value in group_values.items():
                    self._print_block__name_value(name, value)

        print(WRAPPER_MAIN_LINE)

    # =================================================================================================================
    @classmethod
    def print_diffs(cls, *state: ObjectState) -> None:
        pass
        # TODO: FINISH!


# =====================================================================================================================
