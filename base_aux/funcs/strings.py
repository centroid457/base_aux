from typing import *
import json


# =====================================================================================================================
TYPES_ELEMENTARY_SINGLE: tuple = (
    type(None), bool,
    str, bytes,
    int, float,
)
TYPES_ELEMENTARY_COLLECTION: tuple = (
    tuple, list,
    set, dict,
)
TYPES_ELEMENTARY: tuple = (*TYPES_ELEMENTARY_SINGLE, *TYPES_ELEMENTARY_COLLECTION,)

TYPE_ELEMENTARY = Union[*TYPES_ELEMENTARY]


# =====================================================================================================================
class Strings:
    SOURCE: str

    def __init__(self, source: Optional[str] = None):
        self.SOURCE = source

    def try_convert_to__elementary(self, source: Optional[Any] = None) -> TYPE_ELEMENTARY:
        """
        by now it works correct only with single elementary values like INT/FLOAT/BOOL/NONE
        for collections it may work but may not work correctly!!! so use it by your own risk and conscious choice!!
        """
        # FIXME: this is not work FULL and CORRECT!!!! need FIX!!!

        # INIT source -------------
        if source is None:
            source = self.SOURCE

        # PREPARE SOURCE ----------
        source_original = source
        if isinstance(source, str):
            # convert to jason expected - VALUES FOR NULL/FALSE/TRUE
            source = source.replace("True", "true")
            source = source.replace("False", "false")
            source = source.replace("None", "null")

        # WORK --------------------
        try:
            source_elementary = json.loads(source)
            return source_elementary
        except Exception as exx:
            print(f"{exx!r}")
            return source_original


# =====================================================================================================================
