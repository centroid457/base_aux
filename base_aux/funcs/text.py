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

    # -----------------------------------------------------------------------------------------------------------------
    def prepare__json_loads(self, source: Optional[str] = None) -> str:
        """
        GOAL
        ----
        replace pytonic values (usually created by str(Any)) before attempting to apply json.loads to get original python objects
        so it just same process as re.sub by one func for several values

        SPECIALLY CREATED FOR
        ---------------------
        try_convert_to_object
        """
        insource = source is None
        if insource:
            source = self.SOURCE
        result = source
        if isinstance(source, str):
            result = self.sub__words(
                rules = [
                    (r"True", "true"),
                    (r"False", "false"),
                    (r"None", "null"),
                ]
            )
        if insource:
            self.SOURCE = result
        return result

    def prepare__requirements(self, source: Optional[str] = None) -> str:
        """
        GOAL
        ----
        replace pytonic values (usually created by str(Any)) before attempting to apply json.loads to get original python objects
        so it just same process as re.sub by one func for several values

        SPECIALLY CREATED FOR
        ---------------------
        try_convert_to_object
        """
        insource = source is None
        if insource:
            source = self.SOURCE

        result = source
        result = self.clear__cmts(result)
        result = self.clear__blank_lines(result)
        if insource:
            self.SOURCE = result
        return result

    # -----------------------------------------------------------------------------------------------------------------
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
        insource = source is None
        if insource:
            source = self.SOURCE

        word_pat = r"\b" + word_pat + r"\b"
        result = re.sub(word_pat, new, source)

        if insource:
            self.SOURCE = result
        return result

    def sub__words(self, rules: list[tuple[str, str]], source: Optional[str] = None) -> str:
        insource = source is None
        if insource:
            source = self.SOURCE

        result = source
        for work_pat, new in rules:
            result = self.sub__word(work_pat, new, result)
        return result

    # =================================================================================================================
    def clear__blank_lines(
            self,
            source: Optional[str] = None,
    ) -> str:
        insource = source is None
        if insource:
            source = self.SOURCE

        result = source
        if isinstance(source, str):
            result = re.sub(pattern=r"^\s*$", repl="", string=result, flags=re.MULTILINE)

        if insource:
            self.SOURCE = result
        return result

    def clear__cmts(
            self,
            source: Optional[str] = None,
    ) -> str:
        insource = source is None
        if insource:
            source = self.SOURCE

        result = source
        if isinstance(source, str):
            result = re.sub(pattern=r"\s*\#.*$", repl="", string=result, flags=re.MULTILINE)

        if insource:
            self.SOURCE = result
        return result

    # =================================================================================================================
    def lines__split(
            self,
            source: Optional[str] = None,
    ) -> list[str]:
        insource = source is None
        if insource:
            source = self.SOURCE

        result = source.splitlines()
        return result

    def lines__strip(
            self,
            lines: list[str] = None,
    ) -> list[str]:
        insource = lines is None
        if insource:
            lines = self.lines__split()

        result = []
        for line in lines:
            result.append(line.strip())
        return result

    def lines__clear_blank(
            self,
            lines: list[str] = None,
    ) -> list[str]:
        insource = lines is None
        if insource:
            lines = self.lines__split()

        result = []
        for line in lines:
            if line:
                result.append(line)
        return result

    # =================================================================================================================
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
        insource = source is None
        if insource:
            source = self.SOURCE

        # PREPARE SOURCE ----------
        source_original = source
        source = self.prepare__json_loads(source)

        # WORK --------------------
        try:
            source_elementary = json.loads(source)
            return source_elementary
        except Exception as exx:
            print(f"{exx!r}")
            return source_original

    # -----------------------------------------------------------------------------------------------------------------
    def find_by_pats(
            self,
            patterns: list[str] | str,
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
        insource = source is None
        if insource:
            source = self.SOURCE

        result = []
        patterns = args__ensure_tuple(patterns)

        for pat in patterns:
            result_i = re.findall(pat, source)
            for value in result_i:
                value: str
                if value == "":
                    continue
                value = value.strip()
                if value not in result:
                    result.append(value)
        return result

    # -----------------------------------------------------------------------------------------------------------------
    def requirements__get_list(
            self,
            source: Optional[str] = None,
    ) -> list[str]:
        """
        GOAL
        ----
        get list of required modules (actually full lines stripped and commentsCleared)

        SPECIALLY CREATED FOR
        ---------------------
        setup.py install_requires
        """
        insource = source is None
        if insource:
            source = self.SOURCE

        result = source
        result = self.prepare__requirements(result)

        result = self.lines__split(result)
        result = self.lines__strip(result)
        result = self.lines__clear_blank(result)

        return result


# =====================================================================================================================
