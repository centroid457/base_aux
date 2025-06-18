from base_aux.base_nest_dunders.m3_calls import *
from base_aux.aux_attr.m2_annot3_gacls_keys_as_values import *
from base_aux.path0_static.m1_file_extensions import FilesStdExtensions


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
