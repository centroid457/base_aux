from base_aux.base_types.m0_static_typing import *
from base_aux.base_lambdas.m1_lambda import *

from base_aux.base_types.m0_static_types import TYPES


# =====================================================================================================================
class OtherResolved:
    DRAFT: Any | Self

    _finished: bool | None = None
    RAISED: bool | None = None
    EXC: Exception | None = None
    RESULT: Any | None = None

    modifiers_try: TYPING.MODIFIERS_TRY__FINAL
    _modifier_results: list[Any | Exception]    # for debugging!

    def __init__(self, draft: Any | Self, modifiers_try: TYPING.MODIFIERS_TRY__FINAL | None = None) -> None:
        """
        GOAL
        just make object which separate draft/result/exc(if accuses) ONLY IF IT CALLABLE

        SPECIALLY CREATED FOR
        Base_EqValid
        to move all artefacts from Base_EqValid into separated special object
        """
        # 0=ALREADY OtherResolved ----------------------------
        if isinstance(draft, OtherResolved):
            # copy all attrs into new object --------
            self.DRAFT = draft.DRAFT

            self._finished = draft._finished
            self.RESULT = draft.RESULT
            self.RAISED = draft.RAISED
            self.EXC = draft.EXC

            self.modifiers_try = draft.modifiers_try
            self._modifier_results = draft._modifier_results
        else:
            self.DRAFT = draft

        # 1=modifiers -------------------------------
        if modifiers_try:
            self.modifiers_try = modifiers_try
        else:
            self.modifiers_try = []

        self._modifier_results = []

        self._validate_modifiers_or_raise(self.modifiers_try)

        # 2=WORK ------------------------------------
        self._resolve()

    @staticmethod
    def _validate_modifiers_or_raise(modifiers: list[Any]) -> None | NoReturn:
        """
        GOAL
        raise if validators not callable!!!
        # TODO: decide using any modifier with no raising???
        """
        for item in modifiers:
            if not callable(item):
                msg = f"Incorrect type usage {item=}/{modifiers=}"
                raise Exception(msg)

    def _resolve(self) -> None:
        if self._finished:
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
                self._modifier_results.append(self.RESULT)
            except Exception as exc:
                self._modifier_results.append(exc)

        self._finished = True


# =====================================================================================================================
