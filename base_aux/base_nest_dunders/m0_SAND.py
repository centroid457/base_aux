import pytest
import asyncio
from typing import *


# =====================================================================================================================
class RuleChar(NamedTuple):
    NAME: str
    VALUE: str
    SPACE_BEFORE: bool
    SPACE_AFTER: bool


# ---------------------------------------------------------------------------------------------------------------------
class StrChainCreation:
    """
    GOAL
    ----
    just a str creation! by GA!

    EXAMPLE
    -------
    assert StrChainCreation().Hello._COMMA.World._EXCLAMATION() == "Hello, World!"
    """
    _RESULT_: str = ""
    _RULES_TRANSLATE: set[RuleChar] = {
        RuleChar("_COMMA", ",", False, True),
        RuleChar("_SEMICOLON", ";", False, True),
        RuleChar("_COLON", ":", False, True),
        RuleChar("_ELLIPSIS", "...", False, True),
        RuleChar("_DASH", "-", False, False),
        RuleChar("_HYPHEN", "-", True, True),
        RuleChar("_SLASH", "/", False, False),
        RuleChar("_BSLASH", "\\", False, False),

        RuleChar("_SHARP", "#", True, False),
        RuleChar("_HASH", "#", True, False),
        RuleChar("_GRID", "#", True, False),

        RuleChar("_T", "\t", False, False),
        RuleChar("_TAB", "\t", False, False),
        RuleChar("_N", "\n", False, False),
        RuleChar("_NEWLINE", "\n", False, False),

        RuleChar("_D", ".", False, True),
        RuleChar("_DOT", ".", False, True),
        RuleChar("_Q", "?", False, True),
        RuleChar("_QUESTION", "?", False, True),
        RuleChar("_E", "!", False, True),
        RuleChar("_EXCLAMATION", "!", False, True),

        # TODO: finish!
        # TODO: add additional pattern into name item for SPACES! like
        #   assert victim.a._SHARP.b() == "a #b"    # default rule!!!
        #   assert victim.a._SHARP__TT.b() == "a # b"
        #   assert victim.a._SHARP__TF.b() == "a #b"
        #   assert victim.a._SHARP__FF.b() == "a#b"
    }

    def get_rule_char(self, item: str) -> RuleChar | None:
        # todo: item is NAME/VALUE!
        pass

    def __getattr__(self, item: str) -> Self:
        if item in self._RULES_TRANSLATE:
            item = self._RULES_TRANSLATE[item]

        if not self._RESULT_ or item in [rulechar.VALUE for rulechar in self._RULES_TRANSLATE]:
            additional = f"{item}"
        else:
            additional = f" {item}"

        self._RESULT_ += additional

        return self

    def __call__(self) -> str:
        return self._RESULT_


# =====================================================================================================================
