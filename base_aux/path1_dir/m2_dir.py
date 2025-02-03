from typing import *
import pathlib
import datetime
import shutil

from base_aux.aux_types.m0_types import *
from base_aux.aux_types.m2_info import *
from base_aux.path1_dir.m1_dirpath import Resolve_DirPath
from base_aux.aux_argskwargs.m2_argskwargs_aux import *
from base_aux.base_enums.m0_enums import *


# =====================================================================================================================
# @final      # dont use final here! expect nesting for fileWork!???
class Dir:
    """
    GOAL
    ----
    collect all meths for directory include several files work
    single file work with File class!
    """
    DIRPATH: TYPE__PATH_FINAL

    def __init__(self, dirpath: TYPE__PATH_DRAFT = None) -> None:
        self.set_dirpath(dirpath or self.DIRPATH)

    def set_dirpath(self, dirpath: TYPE__PATH_DRAFT) -> None:
        self.DIRPATH = Resolve_DirPath(dirpath).resolve()

    def dirtree_create(self) -> bool:
        try:
            self.DIRPATH.mkdir(parents=True, exist_ok=True)
        except:
            pass

        if self.DIRPATH.exists():
            return True
        else:
            msg = f"[ERROR] CANT create {self.DIRPATH=}"
            print(msg)
            return False

    # -----------------------------------------------------------------------------------------------------------------
    def iter(
            self,
            *wmask: str,
            nested: bool = None,
            fsobj: FsObject = FsObject.FILE,
            str_names_only: bool = False,
            dtime = None,
            dtime_cmp: CmpType = CmpType.GE,
    ) -> Iterator[Union[pathlib.Path, str]]:
        """
        GOAL
        ----
        list exact objects/names.
        """
        wmask = wmask or ["*", ]
        # result = []

        for mask in wmask:
            mask = mask if not nested else f"**/{mask}"
            for path_obj in self.DIRPATH.glob(mask):
                if (
                        (fsobj == FsObject.FILE and path_obj.is_file())
                        or
                        (fsobj == FsObject.DIR and path_obj.is_dir())
                        or
                        fsobj == FsObject.ALL
                ):
                    if dtime:
                        pass
                        # TODO: FINISH
                        # TODO: FINISH
                        # TODO: FINISH
                        # TODO: FINISH
                        # TODO: FINISH


                    if str_names_only:
                        yield path_obj.name
                    else:
                        yield path_obj

        # print(f"{result=}")
        # return result

    def iter_files(self, *wmask, **kwargs) -> Iterator[Union[pathlib.Path, str]]:
        yield from self.iter(*wmask, fsobj=FsObject.FILE, **kwargs)

    def iter_dirs(self, *wmask, **kwargs) -> Iterator[Union[pathlib.Path, str]]:
        yield from self.iter(*wmask, fsobj=FsObject.DIR, **kwargs)

    # -----------------------------------------------------------------------------------------------------------------
    def dirs_delete_blank(
            self,
            *wmask: str,
            nested: bool = False
    ) -> None:
        # TODO: NOT WORKING!!!!! FINISH!!!! cant delete by access reason!!!
        for dirpath in self.iter_dirs(*wmask, nested=nested):
            try:
                dirpath.rmdir()
            except:     # TODO: separate AccessPermition/FilesExists
                pass

    def delete(self, obj: TYPE__PATH_FINAL):
        pass
        # if dir/// recurtion


# =====================================================================================================================
