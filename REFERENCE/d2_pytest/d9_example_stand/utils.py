import asyncio


# ======================================================================================================================
class Dc:
    detected: bool | None = None
    # -----------------------------------------
    async def _connect(self) -> bool: return True
    async def _disconnect(self) -> bool: return True
    async def _detect(self) -> bool:
        result = True
        self.detected = result
        return result
    # -----------------------------------------
    async def on(self) -> bool:
        if not self.detected:
            return False
        return True
    async def off(self) -> bool:
        if not self.detected:
            return False
        return True

    # -----------------------------------------
    async def set_u(self, value: float) -> bool:
        if not self.detected:
            return False
        return True
    async def mesure_i(self) -> float | None:
        if not self.detected:
            return None
        return


# ======================================================================================================================
class Dut:
    detected: bool | None = None
    def __init__(self, index: int):
        self.index = index

    # -----------------------------------------
    async def _connect(self) -> bool: return True
    async def _disconnect(self) -> bool: return True
    async def _detect(self) -> bool:
        result = True
        self.detected = result
        return result

    # -----------------------------------------
    async def on(self) -> bool:
        if not self.detected:
            return False
        return True
    async def off(self) -> bool:
        if not self.detected:
            return False
        return True

    # -----------------------------------------
    async def set_i(self, value: float) -> bool:
        if not self.detected:
            return False
        return True

    async def mesure_u(self) -> float | None:
        if not self.detected:
            return None
        return


# ======================================================================================================================
