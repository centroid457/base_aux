from base_aux.base_types.m0_static_typing import *
from base_aux.base_lambdas.m1_lambda import *

from base_aux.base_types.m0_static_types import TYPES


# =====================================================================================================================
class OtherResolved:
    DRAFT: Any | Self

    __finished: bool | None = None
    RAISED: bool | None = None
    EXC: Exception | None = None
    RESULT: Any | None = None

    modifiers_try: TYPING.MODIFIERS_TRY__FINAL

    def __init__(self, draft: Any | Self, modifiers_try: TYPING.MODIFIERS_TRY__FINAL | None = None) -> None:
        """
        GOAL
        just make object which separate draft/result/exc(if accuses) ONLY IF IT CALLABLE

        SPECIALLY CREATED FOR
        Base_EqValid
        to move all artefacts from Base_EqValid into separated special object
        """
        if isinstance(draft, OtherResolved):
            self.__finished = draft.__finished
            self.RESULT = draft.RESULT
            self.RAISED = draft.RAISED
            self.EXC = draft.EXC

            self.DRAFT = draft.DRAFT
        else:
            self.DRAFT = draft

        if modifiers_try:
            self.modifiers_try = modifiers_try
        else:
            self.modifiers_try = []
        self._resolve()

    def _resolve(self) -> None:
        if self.__finished:
            return

        try:
            self.RESULT = Lambda(self.DRAFT).resolve__raise()
            self.RAISED = False
        except Exception as exc:
            self.RAISED = True
            self.EXC = exc

        for modifier in self.modifiers_try:
            try:
                self.RESULT = modifier(self.RESULT)
            except:
                pass

        self.__finished = True


# =====================================================================================================================
