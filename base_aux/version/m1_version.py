import re

from base_aux.aux_eq.m0_cmp_inst import CmpInst
from base_aux.aux_types.m2_info import *


# =====================================================================================================================
def _explore():
    # EXPLORE VARIANTS ----------------------------------------------
    # 1=PACKAGING.version ---------
    from packaging import version
    ObjectInfo(version.parse(str((1,2,3)))).print()

    result = version.parse("2.3.1") < version.parse("10.1.2")

    ObjectInfo(version.parse("1.2.3")).print()
    print(result)
    print()

    # 2=PKG_RESOURCES.parse_version ---------
    from pkg_resources import parse_version         # DEPRECATED!!!
    parse_version("1.9.a.dev") == parse_version("1.9a0dev")


    import sys
    print(sys.winver)
    print(sys.version_info)
    print(tuple(sys.version_info))

    result = sys.version_info > (2, 7)
    print(result)


# =====================================================================================================================
class Exx__VersionIncompatibleBlock(Exception):
    """
    """


class Exx__VersionIncompatible(Exception):
    """
    """


# ---------------------------------------------------------------------------------------------------------------------
TYPE__VERSION_BLOCK_ELEMENT = Union[str, int]
TYPE__VERSION_BLOCK_FINAL = tuple[TYPE__VERSION_BLOCK_ELEMENT, ...]
TYPE__VERSION_BLOCK_DRAFT = Union[str, int, list[TYPE__VERSION_BLOCK_ELEMENT],  TYPE__VERSION_BLOCK_FINAL, Any, 'VersionBlock']


# =====================================================================================================================
class PatternsBlock:
    CLEAR = r"[\"' -]*"
    VALIDATE_SOURCE_NEGATIVE = r"\d+[^0-9a-z]+\d+"
    VALIDATE_CLEANED = r"(\d|[a-z])+"
    ITERATE = r"\d+|[a-z]+"


# =====================================================================================================================
class VersionBlock(CmpInst):
    """
    this is exact block in version string separated by dots!!!

    PATTERN for blocks
    ------------------
        block1.block2.block3

    EXAMPLES for block
    ------------------
        1rc2
        1-rc2
        1 rc 2

    RULES
    -----
    1.
    """
    _SOURCE: Any
    ELEMENTS: TYPE__VERSION_BLOCK_FINAL

    def __init__(self, source: TYPE__VERSION_BLOCK_DRAFT):
        self._SOURCE = source
        if not self._validate_source(source):
            raise Exx__VersionIncompatibleBlock()

        string = self._prepare_string(source)
        if not self._validate_string(string):
            raise Exx__VersionIncompatibleBlock()

        self.ELEMENTS = self._parse_elements(string)

    @classmethod
    def _validate_source(cls, source: TYPE__VERSION_BLOCK_DRAFT) -> bool:
        source = str(source).lower()
        match = re.search(PatternsBlock.VALIDATE_SOURCE_NEGATIVE, source)
        return not bool(match)

    @classmethod
    def _prepare_string(cls, source: TYPE__VERSION_BLOCK_DRAFT) -> str:
        if isinstance(source, (list, tuple)):
            result = "".join([str(item) for item in source])
        else:
            result = str(source)

        # FINISH -------------------------------
        result = re.sub(PatternsBlock.CLEAR, "", result)
        result = result.lower()
        result = result.strip()
        return result

    @classmethod
    def _validate_string(cls, string: str) -> bool:
        if not isinstance(string, str):
            return False
        match = re.fullmatch(PatternsBlock.VALIDATE_CLEANED, string)
        return bool(match)

    @classmethod
    def _parse_elements(cls, string: str) -> TYPE__VERSION_BLOCK_FINAL:
        if not isinstance(string, str):
            return ()

        result_list = []
        for element in re.findall(PatternsBlock.ITERATE, string):
            try:
                element = int(element)
            except:
                pass
            result_list.append(element)

        return tuple(result_list)

    def __iter__(self):
        yield from self.ELEMENTS

    def __len__(self) -> int:
        return len(self.ELEMENTS)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self})"

    def __str__(self) -> str:
        return "".join(str(item) for item in self.ELEMENTS)

    # CMP -------------------------------------------------------------------------------------------------------------
    def __cmp__(self, other) -> int | NoReturn:
        other = self.__class__(other)

        # equel ----------------------
        if str(self) == str(other):
            return 0

        # by elements ----------------
        for elem_1, elem_2 in zip(self, other):
            if elem_1 == elem_2:
                continue

            if isinstance(elem_1, int):
                if isinstance(elem_2, int):
                    return elem_1 - elem_2
                else:
                    return 1
            else:
                if isinstance(elem_2, int):
                    return -1
                else:
                    return int(elem_1 > elem_2) or -1

        # final - longest ------------
        return int(len(self) > len(other)) or -1


# =====================================================================================================================
pass    # -------------------------------------------------------------------------------------------------------------
pass    # -------------------------------------------------------------------------------------------------------------
pass    # -------------------------------------------------------------------------------------------------------------
pass    # -------------------------------------------------------------------------------------------------------------
pass    # -------------------------------------------------------------------------------------------------------------
pass    # -------------------------------------------------------------------------------------------------------------
pass    # -------------------------------------------------------------------------------------------------------------
pass    # -------------------------------------------------------------------------------------------------------------

TYPE__VERSION_FINAL = tuple[VersionBlock, ...]
TYPE__VERSION_DRAFT = Union[TYPE__VERSION_BLOCK_DRAFT,  TYPE__VERSION_FINAL, 'Version', Any]


class PatternsVer:
    # VERSION_TUPLE = r"\((\d+\.+(\w+\.?)+)\)"
    # VERSION_LIST = r"\[(\d+\.+(\w+\.?)+)\]"
    VERSION_IN_BRACKETS: list = [r"\((.*)\)", r"\[(.*)\]"]  # get first bracket!!!
    VALID_BRACKETS: list = [r"[^\[].*\]", r"\[.*[^\]]", r"[^\(].*\)", r"\(.*[^\)]"]


# =====================================================================================================================
class Version(CmpInst):
    """
    :ivar _SOURCE: try to pass parsed value! it will try to self-parse in _prepare_string, but make it ensured on your own!
    """
    _SOURCE: Any
    BLOCKS: TYPE__VERSION_FINAL = ()

    MIN_BLOCKS_COUNT: int = 1
    RAISE: bool = True

    def __init__(self, source: Any, min_blocks_count: int = None):
        if min_blocks_count is not None:
            self.MIN_BLOCKS_COUNT = min_blocks_count

        self._SOURCE = source
        string = self._prepare_string(source)
        self.BLOCKS = self._parse_blocks(string)
        if not self.check_blocks_enough() and self.RAISE:
            raise Exx__VersionIncompatible()

    def check_blocks_enough(self, count: int = None) -> bool:
        if count is None:
            count = self.MIN_BLOCKS_COUNT
        return len(self.BLOCKS) >= count

    # -----------------------------------------------------------------------------------------------------------------
    @classmethod
    def _prepare_string(cls, source: Any) -> str:
        """
        ONLY PREPARE STRING FOR CORRECT SPLITTING BLOCKS - parsing blocks would inside VersionBlock
        """
        if isinstance(source, (list, tuple)):
            result = ".".join([str(item) for item in source])
        else:
            result = str(source)

        result = result.lower()

        # CUT ---------
        for pattern in PatternsVer.VERSION_IN_BRACKETS:
            match = re.search(pattern, result)
            if match:
                result = match[1]
                break

        if "," in result and "." in result:
            raise Exx__VersionIncompatible()

        for pattern in PatternsVer.VALID_BRACKETS:
            if re.search(pattern, result):
                raise Exx__VersionIncompatible()

        result = re.sub(r"\A\D+", "", result)   # ver/version
        result = re.sub(r",+", ".", result)
        result = re.sub(r"\.+", ".", result)
        result = result.strip(".")

        return result

    @staticmethod
    def _parse_blocks(source: str) -> TYPE__VERSION_FINAL:
        blocks_list__str = source.split(".")

        # RESULT -----------
        result = []
        for item in blocks_list__str:
            if not item:
                continue

            block = VersionBlock(item)
            result.append(block)

        return tuple(result)

    # -----------------------------------------------------------------------------------------------------------------
    def __len__(self) -> int:
        return len(self.BLOCKS)

    def __getitem__(self, item: int) -> VersionBlock | None:
        try:
            return self.BLOCKS[item]
        except:
            return

    def __iter__(self):
        yield from self.BLOCKS

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self})"

    def __str__(self):
        return ".".join([str(block) for block in self.BLOCKS])

    # -----------------------------------------------------------------------------------------------------------------
    @property
    def major(self) -> VersionBlock | None:
        return self[0]

    @property
    def minor(self) -> VersionBlock | None:
        return self[1]

    @property
    def micro(self) -> VersionBlock | None:
        return self[2]

    # -----------------------------------------------------------------------------------------------------------------
    def __cmp__(self, other: TYPE__VERSION_DRAFT) -> int | NoReturn:
        other = self.__class__(other)

        # equel ----------------------
        if str(self) == str(other):
            return 0

        # by elements ----------------
        for block_1, block_2 in zip(self, other):
            if block_1 == block_2:
                continue
            else:
                return int(block_1 > block_2) or -1

        # final - longest ------------
        return int(len(self) > len(other)) or -1


# =====================================================================================================================
