import json
import re

from base_aux.base_statics.m4_enums import *
from base_aux.base_inits.m1_source import *

from base_aux.base_statics.m1_types import TYPE__ELEMENTARY
from base_aux.base_statics.m5_patterns1_nums import *


# =====================================================================================================================
# @final      # dont use final here! expect nesting for fileWork! or FIXME: nest File here!????
class TextAux(Init_Source):
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

    def sub__word(self, *rule) -> str:
        """
        GOAL
        ----
        replace exact word(defined by pattern) in text.
        """
        return self.sub__regexp(*rule, as_word=True)

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
    def shortcut(
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

    def shortcut_nosub(
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
        return self.shortcut(maxlen=maxlen, where=where, sub=None)

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

    # =================================================================================================================
    def parse__single_number(self, fpoint: TYPE__FPOINT_DRAFT = FPoint.AUTO, num_type: NumType = NumType.BOTH) -> int | float | None:
        """
        GOAL
        ----
        parce single float value (unit available) from text.

        SPECIALLY CREATED FOR
        ---------------------
        UART terminal data validation

        :returns:
            noraise in any case!
            None - no value
            None - value is not single
            None - value is not exact type
        """
        result = None
        if fpoint is not NoValue:
            fpoint = FPoint(fpoint)
        num_type = NumType(num_type)

        # get PAT ---------
        if num_type == NumType.INT:
            pat = PatNumberSingle(fpoint).INT_COVERED
        elif num_type == NumType.FLOAT:
            pat = PatNumberSingle(fpoint).FLOAT_COVERED
        elif num_type == NumType.BOTH:
            pat = PatNumberSingle(fpoint).BOTH_COVERED
        else:
            raise TypeError(f"{num_type=}")

        # FIND STR --------
        match = re.fullmatch(pat, self.SOURCE)
        value: str | None = match and match[1]

        # get num ---------
        if value:
            value: str = value.replace(",", ".")

            if num_type == NumType.INT:
                result = int(value)
            elif num_type == NumType.FLOAT:
                result = float(value)
            elif num_type == NumType.BOTH:
                if "." in value:
                    result = float(value)
                else:
                    result = int(value)
        # FINISH ----------
        return result

    def parse__single_int(self) -> int | None:
        return self.parse__single_number(num_type=NumType.INT)

    def parse__single_float(self, fpoint: TYPE__FPOINT_DRAFT = FPoint.AUTO) -> float | None:
        return self.parse__single_number(fpoint=fpoint, num_type=NumType.FLOAT)

    # -----------------------------------------------------------------------------------------------------------------
    def parse__object(self) -> TYPE__ELEMENTARY | str:
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

        # PREPARE__JSON_LOADS ---
        # replace pytonic values (usually created by str(Any)) before attempting to apply json.loads to get original python aux_types
        # so it just same process as re.sub by one func for several values
        self.sub__word(r"True", "true")
        self.sub__word(r"False", "false")
        self.sub__word(r"None", "null")
        self.sub__regexp("\'", "\"")
        # FIXME: apply work with int-keys in dicts!!! its difficalt to walk and edit result dict-objects in all tree!!!!

        # WORK --------------------
        try:
            result = json.loads(self.SOURCE)
            return result
        except Exception as exx:
            print(f"{exx!r}")
            return source_original

    def parse__json(self) -> TYPE__ELEMENTARY | str:
        """
        just a link
        """
        return self.parse__object()

    # -----------------------------------------------------------------------------------------------------------------
    def parse__requirements(self) -> list[str]:
        """
        GOAL
        ----
        get list of required modules (actually full lines stripped and commentsCleared)

        SPECIALLY CREATED FOR
        ---------------------
        setup.py install_requires
        """
        self.clear__cmts()
        self.clear__blank_lines()
        self.strip__lines()
        result = self.split_lines()
        return result


# =====================================================================================================================
