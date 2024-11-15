from typing import *
import json
import re

from base_aux.funcs import TYPE__ELEMENTARY
from base_aux.objects import TypeChecker


# =====================================================================================================================
class Text:
    SOURCE: str

    def __init__(self, source: Optional[str] = None):
        self.SOURCE = source

    def try_convert_to_object(self, source: Optional[Any] = None) -> TYPE__ELEMENTARY | str:
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

        # INIT source -------------
        if source is None:
            source = self.SOURCE

        # PREPARE SOURCE ----------
        source_original = source
        if isinstance(source, str):
            # convert to json expected - VALUES FOR NULL/FALSE/TRUE
            # FIXME: ref to values onlu without close chars!!!!
            source = source.replace("True", "true")
            source = source.replace("False", "false")
            source = source.replace("None", "null")

        # WORK --------------------
        try:
            source_elementary = json.loads(source)
            return source_elementary
        except Exception as exx:
            print(f"{exx!r}")
            return source_original

    def find_by_patterns(
            self,
            source: Optional[str] = None,
            patterns: list[AnyStr] | AnyStr = None,
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
        if not TypeChecker.check__iterable_not_str(patterns):
            patterns = [patterns, ]

        for pat in patterns:
            result_i = re.findall(pat, source)
            for value in result_i:
                if value not in result:
                    result.append(value)
        return result



# =====================================================================================================================
