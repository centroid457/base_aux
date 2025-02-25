from typing import *
import re

from base_aux.aux_eq.m0_cmp_inst import CmpInst
from base_aux.aux_text.m0_patterns import *
from base_aux.base_statics.m2_exceptions import *
from base_aux.aux_eq.m2_eq_valid3_derivatives import *
from base_aux.aux_eq.m10_types import *
from base_aux.aux_text.m1_text_aux import *


# =====================================================================================================================
TYPE__VERSION_BLOCK_ELEMENT = Union[str, int]
TYPE__VERSION_BLOCK_ELEMENTS_FINAL = tuple[TYPE__VERSION_BLOCK_ELEMENT, ...]
TYPE__VERSION_BLOCK_ELEMENTS_DRAFT = Union[str, int, list[TYPE__VERSION_BLOCK_ELEMENT],  TYPE__VERSION_BLOCK_ELEMENTS_FINAL, Any, 'VersionBlock']


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
    SOURCE: TYPE__VERSION_BLOCK_ELEMENTS_DRAFT
    ELEMENTS: TYPE__VERSION_BLOCK_ELEMENTS_FINAL = ()
    RAISE: bool = True
    EQ_VALID: TYPE__EQ_VALID = EqValidChain(
        # EqValid_RegexpAnyTrue(*PatVersionBlock.VALID),
        EqValid_RegexpAllFalse(*PatVersionBlock.VALID_REVERSE),
    )

    def __init__(
            self,
            source: TYPE__VERSION_BLOCK_ELEMENTS_DRAFT,
            eq_valid: TYPE__EQ_VALID = None,
            _raise: bool = None,
    ) -> None | NoReturn:
        if eq_valid is not None:
            self.EQ_VALID = eq_valid

        if _raise is not None:
            self.RAISE = _raise

        self.SOURCE = source
        if self.SOURCE is None:
            self.SOURCE = ""

        self._prepare_source()
        self._parse_elements()

    def _prepare_source(self) -> str:
        if isinstance(self.SOURCE, (list, tuple)):
            result = "".join([str(item) for item in self.SOURCE])
        else:
            result = str(self.SOURCE)

        # FINISH -------------------------------
        result = result.lower()
        result = result.strip()

        self.SOURCE = result
        return result

    def _parse_elements(self) -> TYPE__VERSION_BLOCK_ELEMENTS_FINAL | NoReturn:
        if self.EQ_VALID and self.EQ_VALID != self.SOURCE:
            if self.RAISE:
                raise Exx__Incompatible(f"{self.SOURCE=}/{self.EQ_VALID=}")
            else:
                return ()

        result_list = []
        for element in re.findall(PatVersionBlock.ITERATE, self.SOURCE):
            try:
                element = int(element)
            except:
                pass
            result_list.append(element)

            if len(result_list) > 1:
                if type(result_list[-1]) == type(result_list[-2]):
                    if self.RAISE:
                        raise Exx__Incompatible(f"{result_list[-1]=}/{result_list[-2]=}")
                    else:
                        result_list = ()
                        break

        result = tuple(result_list)
        self.ELEMENTS = result
        return result

    # -----------------------------------------------------------------------------------------------------------------
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self})"

    def __str__(self) -> str:
        return "".join(str(item) for item in self)

    # -----------------------------------------------------------------------------------------------------------------
    def __iter__(self):
        yield from self.ELEMENTS

    def __len__(self) -> int:
        return len(self.ELEMENTS)

    def __bool__(self) -> bool:
        """
        GOAL
        ----
        exists NOT ZERO velues,
        """
        if len(self) == 0:
            return False

        for elem in self:
            if elem:
                return True

        return False

    # CMP -------------------------------------------------------------------------------------------------------------
    def __cmp__(self, other) -> int | NoReturn:
        other = self.__class__(
            other,
            # eq_valid=self.EQ_VALID,
            _raise=False
        )

        # equel ----------------------
        if not self and not other:
            return 0

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
TYPE__VERSION_BLOCKS_FINAL = tuple[VersionBlock, ...]


# =====================================================================================================================
