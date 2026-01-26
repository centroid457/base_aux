from typing import *
from base_aux.loggers.m1_print import *

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
    GOAL
    ----
    print info about object (properties+methods results)

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

    :ivar MAX_ITER_ITEMS: 0 or None if not limited!
    """
    # AUX -------------------------------------------------------------------------------------------------------------
    SOURCE: Any = None
    STATE: ObjectState = None
    STATE_OLD: ObjectState | None = None

    NAMES_COUNT__ON_START: int = 0
    NAMES_COUNT__ON_FINISH: int = 0

    # SETTINGS --------------------------------------------------------------------------------------------------------
    MAX_LINE_LEN: int = 100
    MAX_ITER_ITEMS: int = 5

    SKIP__BUILD_IN: bool = True

    NAMES__USE_ONLY_PARTS: list[str] = []
    NAMES__SKIP_FULL: list[str] = []
    NAMES__SKIP_PARTS: list[str] = NAMES__SKIP_PARTS

    HIDE_NAMES__TOUCHED: bool = None
    HIDE_NAMES__BUILDIN: bool = None

    def __init__(
            self,
            source: Optional[Any] = None,

            /,
            max_line_len: Optional[int] = None,
            max_iter_items: Optional[int] = None,
            skip__build_in: Optional[bool] = None,

            hide_names__touched: bool = None,
            hide_names__buildin: bool = None,

            names__use_only_parts: Union[None, str, list[str]] = None,
            names__skip_full: Union[None, str, list[str]] = None,
            names__skip_parts: str | list[str] = None,
    ):
        if source is not None:
            self.SOURCE = source

        # SETTINGS ----------------------------------------------------------------------------------------------------
        # RAPAMS -----------------------
        if max_line_len is not None:
            self.MAX_LINE_LEN = max_line_len
        if max_iter_items is not None:
            self.MAX_ITER_ITEMS = max_iter_items
        if skip__build_in is not None:
            self.SKIP__BUILD_IN = skip__build_in

        if hide_names__touched is not None:
            self.HIDE_NAMES__TOUCHED = hide_names__touched
        if hide_names__buildin is not None:
            self.HIDE_NAMES__BUILDIN = hide_names__buildin

        # NAMES LISTS -----------------------
        if names__use_only_parts:
            if isinstance(names__use_only_parts, str):
                names__use_only_parts = [names__use_only_parts, ]
            self.NAMES__USE_ONLY_PARTS = [*self.NAMES__USE_ONLY_PARTS, *names__use_only_parts]

        if names__skip_full:
            if isinstance(names__skip_full, str):
                names__skip_full = [names__skip_full, ]
            self.NAMES__SKIP_FULL.extend(names__skip_full)
        if names__skip_parts:
            if isinstance(names__skip_parts, str):
                names__skip_parts = [names__skip_parts, ]
            self.NAMES__SKIP_PARTS = [*self.NAMES__SKIP_PARTS, *names__skip_parts]

        # WORK --------------------------------------------------------------------------------------------------------
        self.state_reload()

    # =================================================================================================================
    @property
    def SOURCE_NAMES_COUNT_WAS_CHANGED(self) -> bool:
        return self.NAMES_COUNT__ON_START != self.NAMES_COUNT__ON_FINISH

    # =================================================================================================================
    def state_clear(self) -> None:
        self.STATE_OLD = self.STATE
        self.STATE = ObjectState()

    def state_reload(self) -> None:
        self.state_clear()

        # WORK --------------------------------------
        self._print_line__group_separator(f"{self.HIDE_NAMES__TOUCHED=}")
        self.NAMES_COUNT__ON_START = len(dir(self.SOURCE))
        print(f"{self.NAMES_COUNT__ON_START=}")

        # print()
        # print(dir(self.SOURCE))
        # for dirname in dir(self.SOURCE):
        #     print(dirname)
        # print()

        for pos, name in enumerate(dir(self.SOURCE), start=1):
            if not self.HIDE_NAMES__TOUCHED:
                print(f"{pos:4d}:{name}")

            # SKIP ----------------------------------------------------------------------------------------------------
            if self.SKIP__BUILD_IN and check_name__buildin(name):
                self.STATE.SKIPPED_BUILDIN.append(name)
                continue

            if name in self.NAMES__SKIP_FULL:
                self.STATE.SKIPPED_FULLNAMES.append(name)
                continue

            if _value_search_by_list(source=name, search_list=self.NAMES__SKIP_PARTS):
                self.STATE.SKIPPED_PARTNAMES.append(name)
                continue

            # FILTER --------------------------------------------------------------------------------------------------
            if self.NAMES__USE_ONLY_PARTS:
                use_name = False
                for name_include_item in self.NAMES__USE_ONLY_PARTS:
                    if name_include_item.lower() in name.lower():
                        use_name = True
                        break
                if not use_name:
                    continue

            # PROPERTIES/METHODS + Exception---------------------------------------------------------------------------
            attr_is_method: bool = False
            try:
                value = getattr(self.SOURCE, name)
            except Exception as exc:
                self.STATE.PROPERTIES__EXC.update({name: exc})
                continue

            if callable(value):
                attr_is_method = True
                try:
                    value = value()
                except Exception as exc:
                    self.STATE.METHODS__EXC.update({name: exc})
                    continue

            # print(f"{name=}/{attr_obj=}/type={type(attr_obj)}/elementary={isinstance(attr_obj, TYPES.ELEMENTARY)}")

            # PLACE VALUE ---------------------------------------------------------------------------------------------
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

        self.NAMES_COUNT__ON_FINISH = len(dir(self.SOURCE))
        print(f"{self.NAMES_COUNT__ON_FINISH=}")

        msg = f"{self.SOURCE_NAMES_COUNT_WAS_CHANGED=}//{self.NAMES_COUNT__ON_START}/{self.NAMES_COUNT__ON_FINISH}"
        if self.SOURCE_NAMES_COUNT_WAS_CHANGED:
            Warn(msg)
        else:
            Print(msg)

    # def state_diff_last(self):
    #     # NOTE: use attrsDUMP!!! instead! cause raised values may be moved into other group! (single/collection)
    #     self.state_reload()
    #     result = ObjectState()
    #     for (name_g1, values_g1), (name_g2, values_g2) in zip(self.STATE_OLD.items(), self.STATE.items()):
    #         for

    # =================================================================================================================
    def _print_line__group_separator(self, group_name: str) -> None:
        """
        GOAL MAIN - print!
        GOAL SECONDARY - return str - just for tests!!!
        """
        result = "-" * 10 + f"{group_name:-<90}"      # here is standard MAX_LINE_LEN
        print(result)
        # return result

    def _print_line__name_type_value(self, name: Optional[str] = None, type_replace: Optional[str] = None, value: Union[None, Any, ItemKeyValue] = None, intend: Optional[int] = None) -> None:
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
        try:
            block_value = f"{value}"
        except Exception as exc:
            block_value = f"{exc!r}"

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
        try:
            if name and str(value) != repr(value) and str(value) != str(block_value) and not TypeAux(value).check__exception():
                # additional print repr()
                self._print_line__name_type_value(name=None, type_replace="__repr()", value=repr(value))
        except Exception as exc:
            print(f"{exc!r}")
            pass

        # return result

    # =================================================================================================================
    def _print_block__header(self) -> None:
        # start printing ----------------------------------
        group_name = f"{self.__class__.__name__}.print"
        self._print_line__group_separator(group_name.upper())

        try:
            print(f"str(SOURCE)={str(self.SOURCE)}")
        except Exception as exc:
            print(f"str(SOURCE)={exc!r}")

        try:
            print(f"repr(SOURCE)={repr(self.SOURCE)}")
        except Exception as exc:
            print(f"repr(SOURCE)={exc!r}")

        try:
            print(f"type(SOURCE)={type(self.SOURCE)}")
        except Exception as exc:
            print(f"type(SOURCE)={exc!r}")

        try:
            mro = self.SOURCE.__class__.__mro__
        except:
            mro = self.SOURCE.__mro__

        mro = [cls.__name__ for cls in mro]

        print(f"mro(SOURCE)={mro}")

        # SETTINGS ----------------------------------------
        group_name = "SETTINGS"
        self._print_line__group_separator(group_name)

        print(f"{self.SKIP__BUILD_IN=}")

        print(f"{self.NAMES__USE_ONLY_PARTS=}")
        print(f"{self.NAMES__SKIP_FULL=}")
        print(f"{self.NAMES__SKIP_PARTS=}")

        print(f"{self.MAX_LINE_LEN=}")
        print(f"{self.MAX_ITER_ITEMS=}")

    def _print_block__name_value(self, name, value) -> None:
        # ALWAYS ---------------------------------------------------------------------------------
        self._print_line__name_type_value(name=name, value=value)
        try:
            if len(str(value)) <= self.MAX_LINE_LEN:
                return
        except Exception as exc:
            print(f"{exc!r}")
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

        # SINGLE/EXC/OBJECTS ---------------------------------------------------------------------
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
        self._print_block__header()

        for group_name, group_values in self.STATE.__getstate__().items():
            self._print_line__group_separator(group_name)

            if group_name == "SKIPPED_BUILDIN" and self.HIDE_NAMES__BUILDIN:
                print(f"{self.HIDE_NAMES__BUILDIN=}")
                continue

            if TypeAux(group_values).check__elementary_collection_not_dict():
                for pos, name in enumerate(group_values, start=1):
                    print(f"{pos:4d}:{name}")
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
if __name__ == "__main__":
    class Victim:
        A1 = 1

        def meth1(self):
            return 1


    ObjectInfo(Victim()).print()
    assert True


# =====================================================================================================================
