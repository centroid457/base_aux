from typing import *
import json
import re

from base_aux.funcs import TYPE__ELEMENTARY, args__ensure_tuple
from base_aux.objects import TypeChecker


# =====================================================================================================================
class Text:
    SOURCE: str = None

    def __init__(self, source: Optional[str] = None):
        if source is not None:
            self.SOURCE = source

    def prepare_for_json_parsing(self, source: Optional[str] = None) -> str:
        """
        GOAL
        ----
        replace pytonic values (usually created by str(Any)) before attempting to apply json.loads to get original python objects
        so it just same process as re.sub by one func for several values

        SPECIALLY CREATED FOR
        ---------------------
        try_convert_to_object
        """
        if source is None:
            source = self.SOURCE
        if isinstance(source, str):
            # convert to json expected - VALUES FOR NULL/FALSE/TRUE
            for work_pat, result in [
                [r"True", "true"],
                [r"False", "false"],
                [r"None", "null"],
            ]:
                source = self.sub__word(work_pat, result, source)
        return source

    def sub__word(self, word_pat: str, new: str = "", source: Optional[str] = None) -> str:
        """
        GOAL
        ----
        replace exact word(defined by pattern) in text.
        WORD means syntax word!

        SPECIALLY CREATED FOR
        ---------------------
        prepare_for_json_parsing
        """
        if source is None:
            source = self.SOURCE

        word_pat = r"\b" + word_pat + r"\b"
        result = re.sub(word_pat, new, source)
        return result

    # -----------------------------------------------------------------------------------------------------------------
    def try_convert_to_object(self, source: Optional[str] = None) -> TYPE__ELEMENTARY | str:
        """
        GOAL
        ----
        create an elementary object from text.
        or return source

        NOTE
        ----
        by now it works correct only with single elementary values like INT/FLOAT/BOOL/NONE
        for collections it may work but may not work correctly!!! so use it by your own risk and conscious choice!!
        """
        # FIXME: this is not work FULL and CORRECT!!!! need FIX!!!

        if source is None:
            source = self.SOURCE

        # PREPARE SOURCE ----------
        source_original = source
        source = self.prepare_for_json_parsing(source)

        # WORK --------------------
        try:
            source_elementary = json.loads(source)
            return source_elementary
        except Exception as exx:
            print(f"{exx!r}")
            return source_original

    # -----------------------------------------------------------------------------------------------------------------
    def find_by_patterns(
            self,
            patterns: list[str] | str = None,
            source: Optional[str] = None,
    ) -> list[str]:
        """
        GOAL
        ----
        find all pattern values in text

        NOTE
        ----
        if pattern have group - return group value (as usual)
        """
        if source is None:
            source = self.SOURCE

        result = []
        patterns = args__ensure_tuple(patterns)

        for pat in patterns:
            result_i = re.findall(pat, source)
            for value in result_i:
                if value not in result:
                    result.append(value)
        return result


# =====================================================================================================================
