from typing import *
import json
import re

from base_aux.base_enums.m0_enums import *
from base_aux.aux_argskwargs.m2_argskwargs_aux import *
from base_aux.base_source.m1_source import InitSource

from base_aux.funcs.m0_static import TYPE__ELEMENTARY


# =====================================================================================================================
@final
class TextAux(InitSource):
    SOURCE: str = None

    def init_post(self) -> None | NoReturn:
        self.SOURCE = self.SOURCE or ""
        self.SOURCE = str(self.SOURCE)

    # -----------------------------------------------------------------------------------------------------------------
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

    # -----------------------------------------------------------------------------------------------------------------
    def prepare__json_loads(self) -> str:
        """
        GOAL
        ----
        replace pytonic values (usually created by str(Any)) before attempting to apply json.loads to get original python base_objects
        so it just same process as re.sub by one func for several values

        SPECIALLY CREATED FOR
        ---------------------
        try_convert_to_object
        """
        result = self.sub__words(
            rules = [
                (r"True", "true"),
                (r"False", "false"),
                (r"None", "null"),
            ]
        )
        result = re.sub("\'", "\"", result)
        return result

    def prepare__requirements(self) -> str:
        """
        GOAL
        ----
        replace pytonic values (usually created by str(Any)) before attempting to apply json.loads to get original python base_objects
        so it just same process as re.sub by one func for several values

        SPECIALLY CREATED FOR
        ---------------------
        try_convert_to_object
        """
        result = self.SOURCE
        result = TextAux(result).clear__cmts()
        result = TextAux(result).clear__blank_lines()
        return result

    # -----------------------------------------------------------------------------------------------------------------
    def sub__word(self, word_pat: str, new: str = "") -> str:
        """
        GOAL
        ----
        replace exact word(defined by pattern) in text.
        WORD means syntax word!

        SPECIALLY CREATED FOR
        ---------------------
        prepare_for_json_parsing
        """
        word_pat = r"\b" + word_pat + r"\b"
        result = re.sub(word_pat, new, self.SOURCE)
        return result

    def sub__words(self, rules: list[tuple[str, str]]) -> str:
        result = self.SOURCE
        for work_pat, new in rules:
            result = TextAux(result).sub__word(work_pat, new)
        return result

    # =================================================================================================================
    def clear__blank_lines(self) -> str:
        result = re.sub(pattern=r"^\s*$", repl="", string=self.SOURCE, flags=re.MULTILINE)
        return result

    def clear__cmts(self) -> str:
        result = re.sub(pattern=r"\s*\#.*$", repl="", string=self.SOURCE, flags=re.MULTILINE)
        return result

    def clear__spaces_all(self) -> str:
        result = re.sub(pattern=r" +", repl="", string=self.SOURCE)
        return result

    def clear__spaces_double(self) -> str:
        result = re.sub(pattern=r" {2,}", repl=" ", string=self.SOURCE)
        return result

    def strip__lines(self) -> str:
        result = self.SOURCE
        result = re.sub(pattern=r"^\s*", repl="", string=result, flags=re.MULTILINE)
        result = re.sub(pattern=r"\s*$", repl="", string=result, flags=re.MULTILINE)
        return result

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
                source = sub + source[-(maxlen - sub_len):]
            elif where == Where3.LAST:
                source = source[0:maxlen - sub_len] + sub
            elif where == Where3.MIDDLE:
                len_start = maxlen // 2 - sub_len // 2
                len_finish = maxlen - len_start - sub_len
                source = source[0:len_start] + sub + source[-len_finish:]

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
    def try_convert_to_object(self) -> TYPE__ELEMENTARY | str:
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
        source = self.prepare__json_loads()

        # WORK --------------------
        try:
            source_elementary = json.loads(source)
            return source_elementary
        except Exception as exx:
            print(f"{exx!r}")
            return source_original

    # -----------------------------------------------------------------------------------------------------------------
    def find_by_pats(self, patterns: list[str] | str) -> list[str]:
        """
        GOAL
        ----
        find all pattern values in text

        NOTE
        ----
        if pattern have group - return group value (as usual)
        """
        result = []
        patterns = ArgsKwargsAux(patterns).resolve_args()

        for pat in patterns:
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
        result = self.prepare__requirements()
        result = TextAux(result).strip__lines()
        result = TextAux(result).clear__blank_lines()
        result = TextAux(result).split_lines()
        return result


# =====================================================================================================================
