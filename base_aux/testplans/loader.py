from pathlib import Path
from base_aux.breeders.m2_breeder_objects import BreederObjectList
from base_aux.testplans.tc import Base_TestCase


# =====================================================================================================================
class Loader:
    DIR_TPS: Path = "TESTPLANS"
    DIR_TCS: Path = None
    LOADER: Path = None

    def load__devices(self) -> BreederObjectList:
        pass

    def load__tcs(self) -> list[type[Base_TestCase]]:
        pass


# =====================================================================================================================
