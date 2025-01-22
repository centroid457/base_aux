from typing import *
from dataclasses import dataclass, field

from .m1_type_aux import TypeAux
from base_aux.aux_attr.m0_static import check_name__buildin


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
class ItemInternal(NamedTuple):
    KEY: str
    VALUE: str


# =====================================================================================================================

@dataclass
class ObjectState:
    """
    class for keeping results
    """
    # TODO: add sort method!!!
    SKIPPED_FULLNAMES: list[str] = field(default_factory=list)
    SKIPPED_PARTNAMES: list[str] = field(default_factory=list)

    PROPERTIES__ELEMENTARY_SINGLE: dict[str, Any] = field(default_factory=dict)
    PROPERTIES__ELEMENTARY_COLLECTION: dict[str, Any] = field(default_factory=dict)
    PROPERTIES__OBJECTS: dict[str, Any] = field(default_factory=dict)
    PROPERTIES__EXX: dict[str, Exception] = field(default_factory=dict)

    METHODS__ELEMENTARY_SINGLE: dict[str, Any] = field(default_factory=dict)
    METHODS__ELEMENTARY_COLLECTION: dict[str, Any] = field(default_factory=dict)
    METHODS__OBJECTS: dict[str, Any] = field(default_factory=dict)
    METHODS__EXX: dict[str, Exception] = field(default_factory=dict)


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
    NAMES__SKIP_FULL: list[str] = [
    ]
    NAMES__SKIP_PARTS: list[str] = [
        # DANGER
        "init", "new", "create", "enter", "install",
        "set",
        "clone", "copy", "move",
        "next",
        "clear", "reduce",
        "close", "del", "exit", "kill", "abort",

        # PyQt5 Qthread
        "exec", "exec_", "pyqtConfigure",
        "dump",     # 'dumpObjectInfo' from PyQt5.QMenu

        # GIT
        "checkout", "detach",
        # threads
        "run", "start", "wait", "join", "terminate", "quit", "disconnect",

        # change collection content/count/order
        "pop", "popleft",
        "append", "appendleft",
        "extend", "extendleft",
        "add", "insert",
        "reverse", "rotate", "sort",
    ]

    # AUX --------------------------------------------------
    ITEM_CLS: type[ObjectState] = ObjectState
    ITEM: ObjectState = ITEM_CLS()
    SOURCE: Any = None

    def __init__(
            self,
            source: Optional[Any] = None,

            max_line_len: Optional[int] = None,
            max_iter_items: Optional[int] = None,
            hide_build_in: Optional[bool] = None,
            log_iter: Optional[bool] = None,

            names__use_only_parts: Union[None, str, list[str]] = None,
            names__skip_full: Union[None, str, list[str]] = None,
            names__skip_parts: Union[None, str, list[str]] = None,
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
                names__skip_full = [names__skip_parts, ]
            self.NAMES__SKIP_PARTS.extend(names__skip_parts)

        # WORK -----------------------------------------------------------
        self._item_clear()

        if source is not None:
            self.SOURCE = source

    # =================================================================================================================
    def _item_clear(self) -> None:
        self.ITEM = self.ITEM_CLS()

    def _item_reload(self) -> None:
        self._item_clear()

        # WORK --------------------------------------
        name = "log_iter(wait last touched)"
        self._print_line__group_separator(name)

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
                self.ITEM.SKIPPED_FULLNAMES.append(name)
                continue

            SKIP_PARTNAMES = []
            if self.NAMES__SKIP_PARTS:
                SKIP_PARTNAMES.extend(self.NAMES__SKIP_PARTS)
            if SKIP_PARTNAMES:
                SKIP_PARTNAMES.extend(SKIP_PARTNAMES)
            if _value_search_by_list(source=name, search_list=SKIP_PARTNAMES):
                self.ITEM.SKIPPED_PARTNAMES.append(name)
                continue

            # PROPERTIES/METHODS + Exception--------------------------------------------------
            attr_is_method: bool = False
            try:
                value = getattr(self.SOURCE, name)
            except Exception as exx:
                self.ITEM.PROPERTIES__EXX.update({name: exx})
                continue

            if callable(value):
                attr_is_method = True
                try:
                    value = value()
                except Exception as exx:
                    self.ITEM.METHODS__EXX.update({name: exx})
                    continue

            # print(f"{name=}/{attr_obj=}/type={type(attr_obj)}/elementary={isinstance(attr_obj, TYPES.ELEMENTARY)}")

            # PLACE VALUE ---------------------------------------------------------------------
            if TypeAux(value).check__elementary_single():
                if attr_is_method:
                    self.ITEM.METHODS__ELEMENTARY_SINGLE.update({name: value})
                else:
                    self.ITEM.PROPERTIES__ELEMENTARY_SINGLE.update({name: value})

            elif TypeAux(value).check__elementary_collection():
                if attr_is_method:
                    self.ITEM.METHODS__ELEMENTARY_COLLECTION.update({name: value})
                else:
                    self.ITEM.PROPERTIES__ELEMENTARY_COLLECTION.update({name: value})

            else:
                if attr_is_method:
                    self.ITEM.METHODS__OBJECTS.update({name: value})
                else:
                    self.ITEM.PROPERTIES__OBJECTS.update({name: value})

    # =================================================================================================================
    def _print_line__group_separator(self, name: str) -> str:
        """
        GOAL MAIN - print!
        GOAL SECONDARY - return str - just for tests!!!
        """
        result = "-" * 10 + f"{name:-<90}"      # here is standard MAX_LINE_LEN
        print(result)
        return result

    def _print_line__name_type_value(self, name: Optional[str] = None, type_replace: Optional[str] = None, value: Union[None, Any, ItemInternal] = None, intend: Optional[int] = None) -> str:
        # -------------------------------
        name = name or ""
        if isinstance(value, ItemInternal):
            name = ""
        block_name = f"{name}"

        # -------------------------------
        block_type = f"{value.__class__.__name__}"
        if isinstance(value, ItemInternal):
            block_type = f"{value.KEY.__class__.__name__}:{value.VALUE.__class__.__name__}"
        if type_replace is not None:
            block_type = type_replace

        # -------------------------------
        intend = intend or 0
        if isinstance(value, ItemInternal):
            intend = 1

        _block_intend = "\t" * intend

        # -------------------------------
        block_value = f"{value}"
        if isinstance(value, ItemInternal):
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
        name = f"{self.__class__.__name__}.print"
        self._print_line__group_separator(name.upper())

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
        name = "SETTINGS"
        self._print_line__group_separator(name)

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
                    self._print_line__name_type_value(name=None, value=ItemInternal(item_key, item_value))

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
        self._item_reload()

        for group_name, group_values in self.ITEM.__getstate__().items():
            self._print_line__group_separator(group_name)

            if TypeAux(group_values).check__elementary_collection_not_dict():
                for pos, name in enumerate(group_values, start=1):
                    print(f"{pos}:\t{name}")
            else:
                for name, value in group_values.items():
                    self._print_block__name_value(name, value)
        print(WRAPPER_MAIN_LINE)

    # =================================================================================================================
    def print_diffs(self) -> None:
        pass
        # TODO: FINISH!


# =====================================================================================================================
