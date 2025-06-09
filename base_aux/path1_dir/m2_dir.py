import datetime
import time

from base_aux.path1_dir.m1_dirpath import Resolve_DirPath
from base_aux.aux_argskwargs.m2_argskwargs_aux import *
from base_aux.aux_values.m5_enums import *


# =====================================================================================================================
# @final      # dont use final here! expect nesting for fileWork!???
class DirAux:   # NOTE: Init_SOURCE - dont nest!!!
    """
    GOAL
    ----
    collect all meths for directory include several files EXTERNAL work!
    single file work with FileAux class!
    """
    DIRPATH: TYPING.PATH_FINAL

    def __init__(self, dirpath: TYPING.PATH_DRAFT = None) -> None:
        self.DIRPATH = Resolve_DirPath(dirpath).resolve()

    # -----------------------------------------------------------------------------------------------------------------
    def check_exists(self, timeout: int = 0) -> bool:
        """
        NOTE
        ----
        any object - DIR/FILE!
        """
        for i in range(timeout):
            if self.DIRPATH.exists():
                return True
            time.sleep(1)

        return self.DIRPATH.exists()

    # -----------------------------------------------------------------------------------------------------------------
    def create_dirtree(self) -> bool:
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
            fsobj: Enum_PathType = Enum_PathType.ALL,
            str_names_only: bool = False,

            # time filter -----
            mtime: Union[None, datetime.datetime, datetime.timedelta] = None,   # acceptable for both FileAux/Dirs
            mtime_cmp: Enum_CmpType = Enum_CmpType.GE,
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
                        (fsobj == Enum_PathType.FILE and path_obj.is_file())
                        or
                        (fsobj == Enum_PathType.DIR and path_obj.is_dir())
                        or
                        fsobj == Enum_PathType.ALL
                ):
                    if mtime:
                        mtime_i = path_obj.stat().st_mtime
                        if USE_DELTA:
                            mtime_i = datetime.datetime.now().timestamp() - mtime_i

                        if (
                                mtime_cmp == Enum_CmpType.LE and not mtime_i <= mtime  # OLDER
                                or
                                mtime_cmp == Enum_CmpType.LT and not mtime_i < mtime
                                or
                                mtime_cmp == Enum_CmpType.GE and not mtime_i >= mtime  # NEWER
                                or
                                mtime_cmp == Enum_CmpType.GT and not mtime_i > mtime
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
        yield from self.iter(*wmask, fsobj=Enum_PathType.FILE, **kwargs)

    def iter_dirs(self, *wmask, **kwargs) -> Iterator[Union[pathlib.Path, str]]:
        yield from self.iter(*wmask, fsobj=Enum_PathType.DIR, **kwargs)

    # -----------------------------------------------------------------------------------------------------------------
    def delete_blank(self, raise_fails: bool = None) -> bool | NoReturn:
        """
        GOAL
        ----
        delete SELF directory if blank!
        """
        result = True
        try:
            self.DIRPATH.rmdir()
        except Exception as exx:  # TODO: separate AccessPermition/FilesExists
            result = False
            if raise_fails:
                raise exx
        return result

    def delete_blank_items_wmask(
            self,
            *wmask: str,
            nested: bool = None,
    ) -> bool | NoReturn:
        """
        GOAL
        ----
        delete INTERNAL dirs in SELF if blanks!
        """
        # TODO: NOT WORKING!!!!! FINISH!!!! cant delete by access reason!!!
        result = True
        for dirpath in self.iter_dirs(*wmask, nested=nested):
            result &= DirAux(dirpath).delete_blank()

        return result

    def delete_dirtree(self, raise_fails: bool = None) -> bool | NoReturn:
        return self.delete_items(self.DIRPATH, raise_fails=raise_fails)

    @classmethod
    def delete_items(cls, *paths: TYPING.PATH_FINAL, raise_fails: bool = None) -> bool | NoReturn:
        result = True
        for path in paths:

            if path.is_file():
                try:
                    path.unlink()
                except Exception as exx:
                    result = False
                    if raise_fails:
                        raise exx

            elif path.is_dir():
                result &= cls.delete_items(*cls(path).iter_files(), raise_fails=raise_fails)
                result &= cls.delete_items(*cls(path).iter_dirs(), raise_fails=raise_fails)
                result &= DirAux(path).delete_blank(raise_fails=raise_fails)

            # TODO: if link

        return result


# =====================================================================================================================
