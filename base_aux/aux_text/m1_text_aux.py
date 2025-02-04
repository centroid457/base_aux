from typing import *
import json
import re

from base_aux.base_enums.m0_enums import *
from base_aux.aux_argskwargs.m2_argskwargs_aux import *
from base_aux.base_inits.m1_source import *

from base_aux.aux_types.m0_types import TYPE__ELEMENTARY


# =====================================================================================================================
# @final      # dont use final here! expect nesting for fileWork! or FIXME: nest File here!????
class TextAux(InitSource):
    SOURCE: str

    def init_post(self) -> None | NoReturn:
        if self.SOURCE is NoValue:
            self.SOURCE = ""
        else:
            self.SOURCE = str(self.SOURCE)

    # =================================================================================================================
    def sub__regexp(self, pat: str, new: str | None = None, flags: re.RegexFlag = None, *, as_word: bool = None) -> str:
        if new is None:
            new = ""

        flags = flags or 0

        if as_word:
            pat = r"\b" + pat + r"\b"

        self.SOURCE = re.sub(pat, new, self.SOURCE, flags=flags)
        return self.SOURCE

    def sub__regexps(self, *rules: Union[tuple[str], tuple[str, str | None], tuple[str, str | None, re.RegexFlag]], as_word: bool = None) -> str:
        """
        GOAL
        ----


        SPECIALLY CREATED FOR
        ---------------------
        as_word - for prepare_for_json_parsing
        WORD means syntax word!
        """
        for rule in rules:
            self.sub__regexp(*rule, as_word=as_word)

        return self.SOURCE

    def sub__words(self, *rules) -> str:
        """
        GOAL
        ----
        replace exact word(defined by pattern) in text.
        """
        return self.sub__regexps(*rules, as_word=True)

    # EDIT ============================================================================================================
    def clear__spaces_all(self) -> str:
        """
        GOAL
        ----
        make a shortest string for like a str() from any container!
        assert str([1,2]) == "[1, 2]"
        assert func(str([1,2])) == "[1,2]"
        """
        return self.sub__regexp(r" ", "")

    def clear__spaces_double(self) -> str:
        """
        GOAL
        ----
        replace repetitive spaces by single one
        """
        return self.sub__regexps((r" {2,}", " "))

    def clear__blank_lines(self) -> str:
        self.sub__regexp(r"^\s*\n", "", re.MULTILINE)
        self.sub__regexp(r"\n\s*$", "", re.MULTILINE)
        self.sub__regexp(r"^\s*$", "", re.MULTILINE)  # not enough!
        return self.SOURCE

    def clear__cmts(self) -> str:
        """
        NOTE
        ----
        if oneline cmt - full line would be deleted!
        """
        self.sub__regexp(r"\s*\#.*$", "", re.MULTILINE)
        return self.SOURCE

    # -----------------------------------------------------------------------------------------------------------------
    def strip__lines(self) -> str:
        self.lstrip__lines()
        self.rstrip__lines()
        return self.SOURCE

    def rstrip__lines(self) -> str:
        """
        GOAL
        ----
        keep indents! strip right!
            " line1 \n line2 " --> " line1\n line2"

        NOTE
        ----
        it can strip blank lines!
            " line1 \n \n  line2 " --> " line1\nline2"
        """
        return self.sub__regexp(r"\s*$", "", re.MULTILINE)

    def lstrip__lines(self) -> str:
        """
        NOTE
        ----
        less usefull as lstrip__lines
        but for the company)
        """
        return self.sub__regexp(r"^\s*", "", re.MULTILINE)

    # -----------------------------------------------------------------------------------------------------------------
    def prepare__json_loads(self) -> str:
        """
        GOAL
        ----
        replace pytonic values (usually created by str(Any)) before attempting to apply json.loads to get original python aux_types
        so it just same process as re.sub by one func for several values

        SPECIALLY CREATED FOR
        ---------------------
        try_convert_to_object
        """
        self.sub__regexps(
                (r"True", "true"),
                (r"False", "false"),
                (r"None", "null"),
                as_word=True,
        )
        # FIXME: apply work with int-keys in dicts!!! its difficalt to walk and edit result dict-objects in all tree!!!!
        return self.sub__regexp("\'", "\"")

    def prepare__requirements(self) -> str:
        """
        GOAL
        ----
        replace pytonic values (usually created by str(Any)) before attempting to apply json.loads to get original python aux_types
        so it just same process as re.sub by one func for several values

        SPECIALLY CREATED FOR
        ---------------------
        try_convert_to_object
        """
        self.clear__cmts()
        self.clear__blank_lines()
        return self.SOURCE

    # =================================================================================================================
    def iter_numbers(self, float_sep: str = ".") -> Iterable[int | float]:
        pass

    def parse__single_int(self) -> int | None:
        """
        GOAL
        ----
        get value from value with unit from UART

        :returns: None if no value/value is not single/value is not exact type
        if need INT and parsed FLOAT??? - BAD!!!
        """

    def parse__single_float(self) -> float | None:
        pass

    def parse__single_int_float(self) -> int | float | None:
        pass

    # =================================================================================================================
    def split_lines(self, skip_blanks: bool = None) -> list[str]:
        lines_all = self.SOURCE.splitlines()
        if skip_blanks:
            result_no_blanks = []
            for line in lines_all:
                if line:
                    result_no_blanks.append(line)
            return result_no_blanks

        else:
            return lines_all

    # =================================================================================================================
    def make__shortcut(
            self,
            maxlen: int = 15,
            where: Where3 = Where3.LAST,
            sub: str | None = "...",
    ) -> str:
        """
        MAIN IDEA-1=for SUB
        -------------------
        if sub is exists in result - means it was SHORTED!
        if not exists - was not shorted!
        """
        sub = sub or ""
        sub_len = len(sub)

        source = self.SOURCE
        source_len = len(source)

        if source_len > maxlen:
            if maxlen <= sub_len:
                return sub[0:maxlen]

            if where == Where3.FIRST:
                result = sub + source[-(maxlen - sub_len):]
            elif where == Where3.LAST:
                result = source[0:maxlen - sub_len] + sub
            elif where == Where3.MIDDLE:
                len_start = maxlen // 2 - sub_len // 2
                len_finish = maxlen - len_start - sub_len
                result = source[0:len_start] + sub + source[-len_finish:]
            else:
                result = source
            return result

        return source

    def make__shortcut_nosub(
            self,
            maxlen: int = 15,
            where: Where3 = Where3.LAST,
    ) -> str:
        """
        GOAL
        ----
        derivative-link for shortcut but no using subs!
        so it same as common slice
        """
        return self.make__shortcut(maxlen=maxlen, where=where, sub=None)

    # -----------------------------------------------------------------------------------------------------------------
    def make__object_try(self) -> TYPE__ELEMENTARY | str:
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
        # PREPARE SOURCE ----------
        source_original = self.SOURCE

        # WORK --------------------
        try:
            result = self.prepare__json_loads()
            result = json.loads(result)
            return result
        except Exception as exx:
            print(f"{exx!r}")
            return source_original

    # =================================================================================================================
    def find__by_pats(self, *pats: str) -> list[str]:
        """
        GOAL
        ----
        find all pattern values in text

        NOTE
        ----
        if pattern have group - return group value (as usual)
        """
        result = []
        for pat in pats:
            result_i = re.findall(pat, self.SOURCE)
            for value in result_i:
                value: str
                if value == "":
                    continue
                value = value.strip()
                if value not in result:
                    result.append(value)
        return result

    # -----------------------------------------------------------------------------------------------------------------
    def requirements__get_list(self) -> list[str]:
        """
        GOAL
        ----
        get list of required modules (actually full lines stripped and commentsCleared)

        SPECIALLY CREATED FOR
        ---------------------
        setup.py install_requires
        """
        self.prepare__requirements()
        self.clear__blank_lines()
        self.strip__lines()
        result = self.split_lines()
        return result


# =====================================================================================================================
