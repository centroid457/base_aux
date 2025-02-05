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

    # -----------------------------------------------------------------------------------------------------------------
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
            *wmask: str,        # dont
            nested: bool = None,
            fsobj: PathType = PathType.ALL,
            str_names_only: bool = False,

            # time filter -----
            mtime: Union[None, datetime.datetime, datetime.timedelta] = None,   # acceptable for both File/Dirs
            mtime_cmp: CmpType = CmpType.GE,
    ) -> Iterator[Union[pathlib.Path, str]] | NoReturn:
        """
        GOAL
        ----
        iter masked objects/names.
        """
        USE_DELTA = None
        if mtime is None:
            pass
        elif isinstance(mtime, datetime.datetime):
            mtime = mtime.timestamp()
        elif isinstance(mtime, datetime.timedelta):
            USE_DELTA = True
            pass
        elif not isinstance(mtime, (type(None), int, float)):
            raise TypeError(f"{mtime=}")

        wmask = wmask or ["*", ]
        # result = []

        for mask in wmask:
            mask = mask if not nested else f"**/{mask}"
            for path_obj in self.DIRPATH.glob(mask):
                if (
                        (fsobj == PathType.FILE and path_obj.is_file())
                        or
                        (fsobj == PathType.DIR and path_obj.is_dir())
                        or
                        fsobj == PathType.ALL
                ):
                    if mtime:
                        mtime_i = path_obj.stat().st_mtime
                        if USE_DELTA:
                            mtime_i = datetime.datetime.now().timestamp() - mtime_i

                        if (
                                mtime_cmp == CmpType.LE and not mtime_i <= mtime  # OLDER
                                or
                                mtime_cmp == CmpType.LT and not mtime_i < mtime
                                or
                                mtime_cmp == CmpType.GE and not mtime_i >= mtime  # NEWER
                                or
                                mtime_cmp == CmpType.GT and not mtime_i > mtime
                        ):
                            continue

                    if str_names_only:
                        result_i = path_obj.name
                    else:
                        result_i = path_obj

                    yield result_i

        # print(f"{result=}")
        # return result

    def iter_files(self, *wmask, **kwargs) -> Iterator[Union[pathlib.Path, str]]:
        yield from self.iter(*wmask, fsobj=PathType.FILE, **kwargs)

    def iter_dirs(self, *wmask, **kwargs) -> Iterator[Union[pathlib.Path, str]]:
        yield from self.iter(*wmask, fsobj=PathType.DIR, **kwargs)

    # -----------------------------------------------------------------------------------------------------------------
    def delete_blank(self) -> None:
        """
        GOAL
        ----
        delete SELF directory if blank!
        """
        try:
            self.DIRPATH.rmdir()
        except:  # TODO: separate AccessPermition/FilesExists
            pass

    def delete_blank_wm(
            self,
            *wmask: str,
            nested: bool = None,
    ) -> None:
        """
        GOAL
        ----
        delete INTERNAL dirs in SELF if blanks!
        """
        # TODO: NOT WORKING!!!!! FINISH!!!! cant delete by access reason!!!
        for dirpath in self.iter_dirs(*wmask, nested=nested):
            Dir(dirpath).delete_blank()

    def delete(self, *paths: TYPE__PATH_FINAL, raise_fails: bool = None) -> bool | NoReturn:
        for path in paths:

            if path.is_file():
                try:
                    path.unlink()
                except Exception as exx:
                    if raise_fails:
                        raise exx

            if path.is_dir():
                self.delete(*Dir(path).iter_files(), raise_fails=raise_fails)
                self.delete(*Dir(path).iter_dirs(), raise_fails=raise_fails)
                Dir(path).delete_blank()


# =====================================================================================================================
