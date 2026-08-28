from base_aux.base_types.m0_static_typing import *
from base_aux.base_lambdas.m1_lambda import *


# =====================================================================================================================
class OtherResolved:
    DRAFT: Any | Self

    RESOLVED: bool | None = None
    RAISED: bool | None = None
    EXC: Exception | None = None
    RESULT: Any | None = None

    def __init__(self, draft: Any) -> None:
        """
        GOAL
        just make
        """
        if isinstance(draft, OtherResolved):
            self.RESOLVED = draft.RESOLVED
            self.RESULT = draft.RESULT
            self.RAISED = draft.RAISED
            self.EXC = draft.EXC

            self.DRAFT = draft.DRAFT
        else:
            self.DRAFT = draft

        self._resolve()

    def _resolve(self) -> None:
        if self.RESOLVED:
            return

        try:
            self.RESULT = Lambda(self.DRAFT).resolve__raise()
            self.RAISED = False
        except Exception as exc:
            self.RAISED = True
            self.EXC = exc

        self.RESOLVED = True


# =====================================================================================================================
