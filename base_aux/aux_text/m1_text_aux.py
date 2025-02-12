import json
import re

from base_aux.base_statics.m1_types import *
from base_aux.aux_text.m0_patterns import *


# =====================================================================================================================
# @final      # dont use final here! expect nesting for fileWork! or FIXME: nest FileAux here!????
class TextAux:
    TEXT: TYPING.STR_FINAL = ""

    def __init__(self, text: TYPING.STR_DRAFT = "", *args, **kwargs) -> None | NoReturn:
        self.TEXT = str(text)
        super().__init__(*args, **kwargs)

    # =================================================================================================================
    def sub__regexp(self, pat: str, new: str | None = None, flags: re.RegexFlag = 0, *, cover_type: PatCoverType = PatCoverType.DIRECT) -> str:
        if new is None:
            new = ""

        flags = flags or 0

        if cover_type == PatCoverType.WORD:
            pat = r"\b" + pat + r"\b"

        elif cover_type == PatCoverType.LINE:
            pat = r"^" + pat + r"$"

        self.TEXT = re.sub(pat, new, self.TEXT, flags=flags)
        return self.TEXT

    def sub__regexps(self, *rules: Union[tuple[str], tuple[str, str | None], tuple[str, str | None, re.RegexFlag]], flags: re.RegexFlag = 0, cover_type: PatCoverType = PatCoverType.DIRECT) -> str:
        """
        GOAL
        ----

        SPECIALLY CREATED FOR
        ---------------------
        cover_type - for prepare_for_json_parsing
        WORD means syntax word!
        """
        for rule in rules:
            self.sub__regexp(*rule, flags=flags, cover_type=cover_type)

        return self.TEXT

    # -----------------------------------------------------------------------------------------------------------------
    def sub__word(self, *rule, flags: re.RegexFlag = 0) -> str:
        """
        GOAL
        ----
        replace exact word(defined by pattern) in text.
        """
        return self.sub__regexp(*rule, flags=flags, cover_type=PatCoverType.WORD)

    def sub__words(self, *rules, flags: re.RegexFlag = 0) -> str:
        """
        GOAL
        ----
        replace exact word(defined by pattern) in text.
        """
        return self.sub__regexps(*rules, flags=flags, cover_type=PatCoverType.WORD)

    # -----------------------------------------------------------------------------------------------------------------
    def sub__line(self, *rule, flags: re.RegexFlag = 0) -> str:
        return self.sub__regexp(*rule, flags=flags | re.MULTILINE, cover_type=PatCoverType.LINE)

    def sub__lines(self, *rules, flags: re.RegexFlag = 0) -> str:
        return self.sub__regexps(*rules, flags=flags | re.MULTILINE, cover_type=PatCoverType.LINE)

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

    def clear__space_duplicates(self) -> str:
        """
        GOAL
        ----
        replace repetitive spaces by single one
        """
        return self.sub__regexps((r" {2,}", " "))

    def clear__lines(self, *pats: str) -> str:
        """
        NOTE
        ----
        clear! NOT DELETE!!! exact lines!
        if need - apply delete!
        """
        for pat in pats:
            self.sub__line(pat, "")
        return self.TEXT

    def delete__lines_blank(self) -> str:
        """
        GOAL
        ----
        exact deleting blank lines!
        """
        # return self.clear__lines(r"\s*", )

        # variant1
        # self.sub__regexp(r"^\s*\n+", "", re.MULTILINE)        # not enough!
        # self.sub__regexp(r"^\s*\n+", "", re.MULTILINE)        # not enough!

        # variant2
        self.sub__regexp(r"^\s*$", "", re.MULTILINE)        # not enough!
        self.sub__regexp(r"^\s*\n+", "", re.MULTILINE)      # startwith
        self.sub__regexp(r"\n+\s*$", "", re.MULTILINE)      # endswith
        self.sub__regexp(r"\n+\s*\n+", "\n", re.MULTILINE)  # middle double
        return self.TEXT

    def delete__cmts(self, cmt_type: CmtType = CmtType.SHARP) -> str:
        """
        GOAL
        ----
        exact DELETING cmts

        NOTE
        ----
        if one line cmt - full line would be deleted!
        """
        # recursion -----------------------------
        if cmt_type == CmtType.ALL:
            for cmt_type in [CmtType.SHARP, CmtType.DSLASH, CmtType.REM]:
                self.delete__cmts(cmt_type)

        elif cmt_type == CmtType.AUTO:
            raise NotImplementedError(CmtType.AUTO)

        # work ----------------------------------
        if cmt_type == CmtType.SHARP:
            self.sub__regexp(PatCmts.SHARP_LINE, "", re.MULTILINE)
            self.sub__regexp(PatCmts.SHARP_INLINE, "", re.MULTILINE)

        elif cmt_type == CmtType.DSLASH:
            self.sub__regexp(PatCmts.DSLASH_LINE, "", re.MULTILINE)
            self.sub__regexp(PatCmts.DSLASH_INLINE, "", re.MULTILINE)

        elif cmt_type == CmtType.REM:
            self.sub__regexp(PatCmts.REM_LINE, "", re.MULTILINE | re.IGNORECASE)    # dont use \s* after REM!!!
            self.sub__regexp(PatCmts.REM_INLINE, "", re.MULTILINE | re.IGNORECASE)

        return self.TEXT

    # -----------------------------------------------------------------------------------------------------------------
    def strip__lines(self) -> str:
        self.lstrip__lines()
        self.rstrip__lines()
        return self.TEXT

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
        lines_all = self.TEXT.splitlines()
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

        source = self.TEXT
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
            result_i = re.findall(pat, self.TEXT)
            for value in result_i:
                value: str
                if value == "":
                    continue
                value = value.strip()
                if value not in result:
                    result.append(value)
        return result

    # =================================================================================================================
    def parse__number_single(self, fpoint: TYPE__FPOINT_DRAFT = FPoint.AUTO, num_type: NumType = NumType.BOTH) -> int | float | None:
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
        match = re.fullmatch(pat, self.TEXT)
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

    def parse__int_single(self) -> int | None:
        return self.parse__number_single(num_type=NumType.INT)

    def parse__float_single(self, fpoint: TYPE__FPOINT_DRAFT = FPoint.AUTO) -> float | None:
        return self.parse__number_single(fpoint=fpoint, num_type=NumType.FLOAT)

    # -----------------------------------------------------------------------------------------------------------------
    def parse__requirements_lines(self) -> list[str]:
        """
        GOAL
        ----
        get list of required modules (actually full lines stripped and commentsCleared)

        SPECIALLY CREATED FOR
        ---------------------
        setup.py install_requires
        """
        self.delete__cmts(CmtType.SHARP)
        self.delete__lines_blank()
        self.strip__lines()
        result = self.split_lines()
        return result

    # -----------------------------------------------------------------------------------------------------------------
    def parse__json_dumped(self) -> TYPING.ELEMENTARY | str:     # NoValue ????
        """
        NOTE
        ----
        intended source is json dumped!

        GOAL
        ----
        create an elementary object from text.
        or return source - FIXME: decide to use

        by now it works correct only with single elementary values like INT/FLOAT/BOOL/NONE
        for collections it may work but may not work correctly!!! so use it by your own risk and conscious choice!!
        """
        try:
            result = json.loads(self.TEXT)
            return result
        except Exception as exx:
            print(f"{exx!r}")
            return self.TEXT

    def parse__object_stringed(self) -> TYPING.ELEMENTARY | str:
        # PREPARE -----------------------------------------------------------------
        # replace pytonic values (usually created by str(Any)) before attempting to apply json.loads to get original python aux_types
        # so it just same process as re.sub by one func for several values

        # QUOTES ------------
        self.sub__regexp("\'", "\"")

        # BOOL ------------
        self.sub__word(r"True", "true")
        self.sub__word(r"False", "false")
        self.sub__word(r"None", "null")

        self.sub__word(r"\s*:\s*\"null\"", ":null")
        self.sub__word(r"\s*:\s*\"true\"", ":true")
        self.sub__word(r"\s*:\s*\"false\"", ":false")

        # NUM KEYS ------------
        self.sub__regexp(r"\b(\d+\.?\d*)\b\s*:\s*", r'"\1":')

        # RESULT -----------------------------------------------------------------
        return self.parse__json_dumped()

    # =================================================================================================================
    def parse__dict_csv(self, dict_format: DictTextFormat) -> TYPING.DICT_STR_ELEM | None:
        pass

    def parse__dict_ini(self, dict_format: DictTextFormat) -> TYPING.DICT_STR_ELEM | None:
        pass


# =====================================================================================================================
