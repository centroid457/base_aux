import json
import re
import string

from base_aux.aux_text.m0_patterns import *
from base_aux.aux_text.m4_ini import ConfigParserMod
from base_aux.base_types.m0_static_typing import TYPING


# =====================================================================================================================
# @final      # dont use final here! expect nesting for fileWork! or FIXME: nest FileAux here!????
class TextAux:
    TEXT: TYPING.STR_FINAL = ""

    def __init__(self, text: TYPING.STR_DRAFT = NoValue, *args, **kwargs) -> None | NoReturn:
        if text is not NoValue:
            self.TEXT = str(text)
        super().__init__(*args, **kwargs)

    # =================================================================================================================
    def sub__regexp(self, pat: str, new: str | None = None, flags: re.RegexFlag = 0, *, cover_type: EnumAdj_PatCoverStyle = EnumAdj_PatCoverStyle.NONE) -> str:
        if new is None:
            new = ""

        flags = flags or 0

        if cover_type == EnumAdj_PatCoverStyle.WORD:
            pat = r"\b" + pat + r"\b"

        elif cover_type == EnumAdj_PatCoverStyle.LINE:
            pat = r"^" + pat + r"$"

        self.TEXT = re.sub(pat, new, self.TEXT, flags=flags)
        return self.TEXT

    def sub__regexps(self, *rules: Union[tuple[str], tuple[str, str | None], tuple[str, str | None, re.RegexFlag]], flags: re.RegexFlag = 0, cover_type: EnumAdj_PatCoverStyle = EnumAdj_PatCoverStyle.NONE) -> str:
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
        return self.sub__regexp(*rule, flags=flags, cover_type=EnumAdj_PatCoverStyle.WORD)

    def sub__words(self, *rules, flags: re.RegexFlag = 0) -> str:
        """
        GOAL
        ----
        replace exact word(defined by pattern) in text.
        """
        return self.sub__regexps(*rules, flags=flags, cover_type=EnumAdj_PatCoverStyle.WORD)

    # -----------------------------------------------------------------------------------------------------------------
    def sub__line(self, *rule, flags: re.RegexFlag = 0) -> str:
        return self.sub__regexp(*rule, flags=flags | re.MULTILINE, cover_type=EnumAdj_PatCoverStyle.LINE)

    def sub__lines(self, *rules, flags: re.RegexFlag = 0) -> str:
        return self.sub__regexps(*rules, flags=flags | re.MULTILINE, cover_type=EnumAdj_PatCoverStyle.LINE)

    # =================================================================================================================
    def fix__incorrect(self) -> str:
        self.fix__incorrect_quotes()
        self.fix__incorrect_spaces()
        return self.TEXT

    def fix__incorrect_quotes(self) -> str:
        self.TEXT = self.TEXT.replace('”', '"')
        self.TEXT = self.TEXT.replace('“', '"')
        return self.TEXT

    def fix__incorrect_spaces(self) -> str:
        # self.TEXT = self.TEXT.replace('“', ' ')
        return self.TEXT

    def fix__json(self) -> str:
        # PREPARE -----------------------------------------------------------------
        # replace pytonic values (usually created by str(Any)) before attempting to apply json.loads to get original python base_types
        # so it just same process as re.sub by one func for several values

        # JSON-cmts my special ------------
        self.delete__cmts_c()

        # JSON-COMMAS ------------
        self.clear__regexps(r',\s*(?=\})')

        # JSON-QUOTES ------------
        self.sub__regexp("\'", "\"")

        # JSON-BOOL ------------
        self.sub__word(r"True", "true")
        self.sub__word(r"False", "false")
        self.sub__word(r"None", "null")

        # JSON-dict VALUES ------------
        self.sub__word(r"\s*:\s*\"null\"", ":null")
        self.sub__word(r"\s*:\s*\"true\"", ":true")
        self.sub__word(r"\s*:\s*\"false\"", ":false")

        # NUM KEYS ------------
        self.sub__regexp(r"(?<=[{,])\s*(\d+(?:\.\d+)?)\s*:\s*", r'"\1":')

        return self.TEXT

    # EDIT ============================================================================================================
    def clear__regexps(self, *pats: str, **kwargs) -> str:
        for pat in pats:
            self.sub__regexp(pat=pat, new="", **kwargs)
        return self.TEXT

    def clear__noneprintable(self) -> str:
        return self.clear__regexps(f"[^{string.printable}а-яА-ЯёЁ]")

    def clear__punctuation(self) -> str:
        return self.clear__regexps(f"[^{string.punctuation}]")

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

    # =================================================================================================================
    def delete__cmts(self, cmt_type: EnumAdj_CmtStyle = EnumAdj_CmtStyle.SHARP) -> str:
        """
        GOAL
        ----
        exact DELETING cmts

        NOTE
        ----
        if one line cmt - full line would be deleted!
        """
        # recursion -----------------------------
        if cmt_type == EnumAdj_CmtStyle.ALL:
            for cmt_type in [EnumAdj_CmtStyle.SHARP, EnumAdj_CmtStyle.DSLASH, EnumAdj_CmtStyle.REM, EnumAdj_CmtStyle.C]:
                self.delete__cmts(cmt_type)

        elif cmt_type == EnumAdj_CmtStyle.AUTO:
            raise NotImplementedError(EnumAdj_CmtStyle.AUTO)

        # work ----------------------------------
        if cmt_type == EnumAdj_CmtStyle.SHARP:
            self.clear__regexps(Pat_Cmts.SHARP_LINE, flags=re.MULTILINE)
            self.clear__regexps(Pat_Cmts.SHARP_INLINE, flags=re.MULTILINE)

        elif cmt_type == EnumAdj_CmtStyle.DSLASH:
            self.clear__regexps(Pat_Cmts.DSLASH_LINE, flags=re.MULTILINE)
            self.clear__regexps(Pat_Cmts.DSLASH_INLINE, flags=re.MULTILINE)

        elif cmt_type == EnumAdj_CmtStyle.REM:
            self.clear__regexps(Pat_Cmts.REM_LINE, flags=re.MULTILINE | re.IGNORECASE)    # dont use \s* after REM!!!
            self.clear__regexps(Pat_Cmts.REM_INLINE, flags=re.MULTILINE | re.IGNORECASE)

        elif cmt_type == EnumAdj_CmtStyle.C:
            self.clear__regexps(Pat_Cmts.C_MLINE)

        return self.TEXT

    def delete__cmts_sharp(self) -> str:
        return self.delete__cmts(EnumAdj_CmtStyle.SHARP)

    def delete__cmts_dslash(self) -> str:
        return self.delete__cmts(EnumAdj_CmtStyle.DSLASH)

    def delete__cmts_rem(self) -> str:
        return self.delete__cmts(EnumAdj_CmtStyle.REM)

    def delete__cmts_c(self) -> str:
        return self.delete__cmts(EnumAdj_CmtStyle.C)

    # =================================================================================================================
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
        return self.sub__regexp(r"\s+$", "", re.MULTILINE)

    def lstrip__lines(self) -> str:
        """
        NOTE
        ----
        less usefull as lstrip__lines
        but for the company)
        """
        return self.sub__regexp(r"^\s+", "", re.MULTILINE)

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
            where: EnumAdj_Where3 = EnumAdj_Where3.LAST,
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

            if where is EnumAdj_Where3.FIRST:
                result = sub + source[-(maxlen - sub_len):]
            elif where is EnumAdj_Where3.LAST:
                result = source[0:maxlen - sub_len] + sub
            elif where is EnumAdj_Where3.MIDDLE:
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
            where: EnumAdj_Where3 = EnumAdj_Where3.LAST,
    ) -> str:
        """
        GOAL
        ----
        derivative-link for shortcut but no using subs!
        so it same as common slice
        """
        return self.shortcut(maxlen=maxlen, where=where, sub=None)

    # =================================================================================================================
    def findall(self, *pats: str, flags: int = 0) -> list[str]:
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
            result_i = re.findall(pat, self.TEXT, flags=flags)
            for value in result_i:
                value: str
                if value == "":
                    continue
                value = value.strip()
                result.append(value)
        return result

    def search__group(self, *pats: str, flags: int = 0) -> str | None:
        """
        GOAL
        ----
        get first found group 1
        if pat without group - just return found value
        None - not found!
        """
        for pat in pats:
            match = re.search(pat, self.TEXT, flags=flags)
            if match:
                try:
                    return match[1]     # group defined in pat
                except:
                    return match[0]     # group NOT defined in pat

        return

    # =================================================================================================================
    def parse__number_single(self, fpoint: TYPING__FPOINT_DRAFT = EnumAdj_NumFPoint.AUTO, num_type: EnumAdj_NumType = EnumAdj_NumType.BOTH) -> int | float | None:
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
            fpoint = EnumAdj_NumFPoint(fpoint)
        num_type = EnumAdj_NumType(num_type)

        # get PAT ---------
        if num_type == EnumAdj_NumType.INT:
            pat = Pat_NumberSingle(fpoint).INT_COVERED
        elif num_type == EnumAdj_NumType.FLOAT:
            pat = Pat_NumberSingle(fpoint).FLOAT_COVERED
        elif num_type == EnumAdj_NumType.BOTH:
            pat = Pat_NumberSingle(fpoint).BOTH_COVERED
        else:
            raise TypeError(f"{num_type=}")

        # FIND STR --------
        match = re.fullmatch(pat, self.TEXT)
        value: str | None = match and match[1]

        # get num ---------
        if value:
            value: str = value.replace(",", ".")

            if num_type == EnumAdj_NumType.INT:
                result = int(value)
            elif num_type == EnumAdj_NumType.FLOAT:
                result = float(value)
            elif num_type == EnumAdj_NumType.BOTH:
                if "." in value:
                    result = float(value)
                else:
                    result = int(value)
        # FINISH ----------
        return result

    def parse__int_single(self) -> int | None:
        return self.parse__number_single(num_type=EnumAdj_NumType.INT)

    def parse__float_single(self, fpoint: TYPING__FPOINT_DRAFT = EnumAdj_NumFPoint.AUTO) -> float | None:
        return self.parse__number_single(fpoint=fpoint, num_type=EnumAdj_NumType.FLOAT)

    # =================================================================================================================
    def parse__requirements_lines(self) -> list[str]:
        """
        GOAL
        ----
        get list of required modules (actually full lines stripped and commentsCleared)

        SPECIALLY CREATED FOR
        ---------------------
        setup.py install_requires
        """
        self.delete__cmts(EnumAdj_CmtStyle.SHARP)
        self.delete__lines_blank()
        self.strip__lines()
        result = self.split_lines()
        return result

    # -----------------------------------------------------------------------------------------------------------------
    def parse__json(self) -> TYPING.DICT_STR_ELEM | TYPING.ELEMENTARY | NoValue:  # NoValue ???? yes to separate from None as parsed object
        """
        NOTE
        ----
        intended source is json dumped! or stringed!

        GOAL
        ----
        create an elementary object from text.
        or return source - FIXME: decide to use - think NO!!!

        by now it works correct only with single elementary values like INT/FLOAT/BOOL/NONE
        for collections it may work but may not work correctly!!! so use it by your own risk and conscious choice!!
        """
        self.fix__json()
        try:
            result = json.loads(self.TEXT)
            return result
        except Exception as exx:
            print(f"{exx!r}")
            return NoValue

    def parse__object_stringed(self) -> TYPING.JSON_ANY | NoValue:
        return self.parse__json()

    # =================================================================================================================
    def parse__dict(self, style: EnumAdj_DictTextFormat = EnumAdj_DictTextFormat.AUTO) -> TYPING.DICT_STR_ELEM | None:
        if style == EnumAdj_DictTextFormat.AUTO:
            return self.parse__dict_auto()

        elif style == EnumAdj_DictTextFormat.JSON:
            return self.parse__dict_json()

        elif style == EnumAdj_DictTextFormat.INI:
            return self.parse__dict_ini()

        elif style == EnumAdj_DictTextFormat.CSV:
            return self.parse__dict_csv()

        else:
            raise NotImplementedError(f"{style=}")

    # -----------------------------------------------------------------------------------------------------------------
    def parse__dict_auto(self) -> TYPING.DICT_STR_ELEM | TYPING.DICT_STR_STR | None:
        for style in [EnumAdj_DictTextFormat.JSON, EnumAdj_DictTextFormat.INI, EnumAdj_DictTextFormat.CSV]:     # order is important!
            result = self.parse__dict(style)
            if result:
                return result

    # -----------------------------------------------------------------------------------------------------------------
    def parse__dict_json(self) -> TYPING.DICT_STR_ELEM | None:     # NoValue ????
        """
        SAME AS parse__json BUT
        -----------------------
        if result is not dict - return None!
        """
        result = self.parse__json()
        if isinstance(result, dict):
            return result

    def parse__dict_ini(self) -> TYPING.DICT_STR_STR | None:
        ini = ConfigParserMod()

        try:
            ini.read_string(self.TEXT)
            return ini.to_dict()
        except Exception as exx:
            msg = f"[CRITICAL] incorrect file!{exx!r}"
            print(msg)
            return

    def parse__dict_csv(self) -> TYPING.DICT_STR_STR | None:
        return
        # raise NotImplemented

    # =================================================================================================================
    def pretty__json(self) -> str | None:
        """
        GOAL
        ----
        make json-text pretty
        """
        data_dict = self.parse__dict_json()
        if data_dict:
            self.TEXT = json.dumps(data_dict, indent=4, ensure_ascii=False)
            return self.TEXT


# =====================================================================================================================
