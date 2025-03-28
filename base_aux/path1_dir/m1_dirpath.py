import pathlib

from base_aux.base_statics.m1_types import *
from base_aux.base_nest_dunders.m1_init1_source import *
from base_aux.base_nest_dunders.m3_calls import *
from base_aux.aux_attr.m2_annot3_cls_keys_as_values import *


# =====================================================================================================================
class FilesStdExtensions(NestGaCls_AnnotNamesAsValuesIc):
    """
    GOAL
    ----
    use as collection for standard extension

    SPECIALLY CREATED FOR
    ---------------------
    Resolve_DirPath for detecting files withing names which are not exist
    """

    # TEXT -------------
    TXT: str
    JSON: str
    CSV: str
    INI: str
    INF: str
    IML: str
    XML: str
    YML: str
    FLAKE8: str
    MD: str
    GITIGNORE: str
    LOG: str
    HTML: str
    REG: str

    # EXECUTIVE ---------
    PY: str
    PYC: str
    C: str
    CPP: str
    H: str
    BAT: str
    CMD: str
    SH: str
    EXE: str
    MSI: str

    # MEDIA -------------
    ACCDB: str

    # graf
    BMP: str
    JPG: str
    JPEG: str
    PNG: str
    GIF: str
    TIFF: str
    ICO: str
    RAW: str

    # sound
    MP3: str
    FLAC: str
    APE: str
    OGG: str
    WAW: str
    AC3: str
    WMA: str
    M4A: str
    AAC: str

    # video
    AVI: str
    WMW: str
    MKV: str
    # 3GP: str
    FLV: str
    MPEG: str
    MP4: str
    MOV: str
    VOB: str

    # EXTRA -------------
    LNK: str

    # arch
    BK: str
    ISO: str
    RAR: str
    ZIP: str
    # 7Z: str

    # app
    PDF: str
    DOC: str
    DOCX: str
    XLS: str
    XLSX: str
    PPT: str
    PPTX: str


# =====================================================================================================================
@final
class Resolve_DirPath(NestInit_Source, NestCall_Resolve):
    """
    GOAL
    ----
    resolve dirpath by draft
    if file and fileExist - return parent!

    SPECIALLY CREATED FOR
    ---------------------
    Resolve_FilePath init dirpath
    """
    SOURCE: TYPING.PATH_DRAFT

    def resolve(self) -> TYPING.PATH_FINAL:
        # ---------------------
        if self.SOURCE is None:
            return pathlib.Path().cwd()

        # ---------------------
        if self.SOURCE is not None:
            self.SOURCE = pathlib.Path(self.SOURCE)

        self.SOURCE: pathlib.Path

        # try detect files by existed ---------------------
        if self.SOURCE.exists() and self.SOURCE.is_file():
            return self.SOURCE.parent

        # try detect files by extensions ---------------------
        splited = self.SOURCE.name.rsplit(".")
        if len(splited) == 2:
            name, extlast = splited
            if extlast in FilesStdExtensions:
                return self.SOURCE.parent

        # FINAL ---------------------
        return self.SOURCE


# =====================================================================================================================
