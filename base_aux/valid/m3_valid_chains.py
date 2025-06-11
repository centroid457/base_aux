import datetime

from base_aux.valid.m2_valid_derivatives import *
from base_aux.aux_callable.m1_callable import *
from base_aux.aux_values.m5_enums import *


# =====================================================================================================================
TYPING__CHAINS = list[Union[Valid, 'ValidChains', Any]]      # all Any will be converted to Valid!


# =====================================================================================================================
class ValidChains(Valid):
    """
    GOAL
    ----

    CREATED SPECIALLY FOR
    ---------------------

    CONSTRAINTS
    -----------

    BEST USAGE
    ----------
    val_chains = ValidChains(
        chains=[
            True,
            1+1 == 2,
            Valid(2),
            Valid(3, chain_cum=False),
            ValidChains([Valid(21), Valid(22)], chain_cum=False),
        ]
    )

    result = val_chains.run()

    WHY NOT: 1?
    -----------

    WHY NOT: 2?
    -----------
    """
    _CHAINS: TYPING__CHAINS

    def __init__(self, chains: TYPING__CHAINS, **kwargs):
        super().__init__(value_link=None, **kwargs)
        self._CHAINS = chains

    def __len__(self) -> int:
        return len(self._CHAINS)

    def __iter__(self):
        return iter(self._CHAINS)

    def run(self) -> bool:
        self.clear()
        self.timestamp_last = datetime.datetime.now()

        # SKIP ---------------------
        self.skip_last = CallableAux(self.SKIP_LINK).resolve_bool()

        if not self.skip_last:
            # WORK =======================
            self.STATE_ACTIVE = Enum_ProcessStateActive.STARTED
            self.log_lines.append(f"(START) len={len(self)}/timestamp={self.timestamp_last}")

            # init self.validate_last if None -----------
            # if self.validate_last is None:
            #     self.validate_last = True

            # ITER -----------
            for index, step in enumerate(self):
                if not isinstance(step, (Valid, ValidChains)):
                    step = Valid(step)

                step_result = step.run()
                self.log_lines.append(str(step))

                if step.skip_last:
                    continue

                if step.CHAIN__CUM:
                    self.validate_last &= step_result
                    if step.CHAIN__FAIL_STOP and not step_result:
                        self.log_lines.append(f"(FAIL STOP) [result={bool(self)}]{index=}/len={len(self)}")
                        break

                if isinstance(step, ValidBreak) and step_result:
                    break

            # -----------------
            self.STATE_ACTIVE = Enum_ProcessStateActive.FINISHED
            self.log_lines.append(f"(FINISH) [result={bool(self)}]/len={len(self)}")    # need after finish! to keep correct result
            # ============================

        return bool(self)


# =====================================================================================================================
if __name__ == "__main__":
    victim = ValidChains([Valid(True), Valid(False)])
    print(victim)
    print()

    victim.run()
    print(victim)


# =====================================================================================================================
