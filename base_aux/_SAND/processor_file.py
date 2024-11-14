# TODO-1=add logdata_load_by_name_wo_extention with extention param!
# TODO-1=add extention default? maybe NO!
# TODO-1=add delete blank dirs in dicrpath
# TODO-1=add delete dirtree

# =====================================================================================================================
# STARICHENKO UNIVERSAL IMPORT
import sys
sys.path.append("..")  # Adds higher directory to python modules path.

import time
import pathlib
from typing import *

import utilities.func_universal as UFU

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

# from users.user_profile import UserProfile_Singleton
# from stands.stand import Stand_Singleton
# from results.results_testplan import TestplanResults_Singleton
# =====================================================================================================================
import datetime
import shutil


# =====================================================================================================================
class ProcessorFileSelector:     # starichenko
    """
    BASE CLASS FOR WORKING WITH FILES! and selecting only one!
    if you need work only with path objects in FileSystem (list_dir for example) without exactly opening files
    use it directly or create special class.
    In other cases with special file types use other special classes inherited from this - Json/Log

    ATTENTION:
        1. DONT USE FILES READ/WRITE WITHOUT SELECTING!!!
            if you creating instance for working with exact file - dont read/write another file without selecting new one!!!
            all methods who get filepath-like parameter - will and must use selecting it!!!
    """
    FILEPATH_BACKUP: bool = None     # used right before dump

    FILEPATH_DEFAULT: Optional[pathlib.Path] = None  # REDEFINE!
    __filepath: Optional[pathlib.Path] = None

    DIRPATH_DEFAULT: Optional[pathlib.Path] = None  # REDEFINE! BUT IMPORTANT! use it only for perpose if you need to find filepath in exact dirpath

    # FILEPATH ========================================================================================================
    @property
    def filepath(self) -> Optional[pathlib.Path]:
        return self.__filepath or self.FILEPATH_DEFAULT

    def filepath_check_exists(self, filepath: Optional[pathlib.Path] = None) -> Optional[bool]:
        filepath = self.filepath_get_active(filepath)
        if filepath:
            return filepath.exists()

    def filepath_get_active(
            self,
            filepath: Union[None, str, pathlib.Path] = None,
    ) -> Optional[pathlib.Path]:
        """
        used always get final pathlib (from instanse or specified param)
        """
        if filepath is None:
            filepath = self.filepath
        else:
            filepath = pathlib.Path(filepath)

        if filepath is None:
            msg = f"blank {filepath=}"
            print(msg)
        return filepath

    def filepath_get_by_name(
            self,
            name: str,
            dirpath: Union[None, str, pathlib.Path] = None,
            only_if_existed: bool = False
    ) -> Optional[pathlib.Path]:  # never add wildcard or short name WoExt!!!
        if not name:
            msg = f"no {name=}"
            print(msg)
            return

        dirpath = self.dirpath_get_active(dirpath)
        filepath = dirpath.joinpath(name)
        if not only_if_existed or (only_if_existed and filepath.exists()):
            return filepath

    def filepath_clear(self) -> None:
        self.__filepath = self.FILEPATH_DEFAULT

    def filepath_set(self, filepath: Union[str, pathlib.Path], only_if_existed: bool = False) -> Optional[bool]:
        self.filepath_clear()
        if not filepath:
            msg = f"blank {filepath=}"
            print(msg)
            return

        filepath = pathlib.Path(filepath)

        if only_if_existed and not filepath.exists():
            msg = f"file not exists {self.filepath=}"
            print(msg)
            return

        self.__filepath = filepath
        return True

    def filepath_set_by_name(
            self,
            name: str,
            dirpath: Union[None, str, pathlib.Path] = None,
            only_if_existed: bool = False
    ) -> Optional[bool]:    # never add wildcard or short name WoExt!!!
        filepath = self.filepath_get_by_name(name=name, dirpath=dirpath, only_if_existed=only_if_existed)
        if filepath:
            return self.filepath_set(filepath=filepath, only_if_existed=only_if_existed)

    # BACKUPS ---------------------------------------------------------------------------------------------------------
    def filepath_get_with_new_stem(
            self,
            filepath: Union[None, str, pathlib.Path] = None,
            start_suffix: Optional[str] = None,
            preend_suffix: Optional[str] = None,
            end_suffix: Optional[str] = None
    ) -> Optional[pathlib.Path]:
        """
        for backup actually!
        """
        filepath = self.filepath_get_active(filepath)
        if not filepath:
            msg = f"not exists {filepath=}"
            print(msg)
            return

        start_suffix = start_suffix or ""
        preend_suffix = preend_suffix or ""
        end_suffix = end_suffix or ""

        filepath = filepath.parent.joinpath(f"{start_suffix}{filepath.stem}{preend_suffix}{end_suffix}{filepath.suffix}")
        return filepath

    def filepath_backup_make(
            self,
            filepath: Union[None, str, pathlib.Path] = None,
            dirpath: Union[None, str, pathlib.Path] = None,
            backup: Optional[bool] = None,
    ) -> Optional[bool]:
        # DECIDE --------------------------------
        backup = backup if backup is not None else self.FILEPATH_BACKUP
        if not backup:
            return True

        # SOURCE --------------------------------
        source = self.filepath_get_active(filepath)
        if not source.exists():
            msg = f"not exists {source=}"
            print(msg)
            return

        # DESTINATION --------------------------------
        # be careful to change this code!
        if filepath is not None and dirpath is None:
            destination = source.parent
        else:
            destination = self.dirpath_get_active(dirpath)
        destination = destination.joinpath(source.name)

        # suffix --------------------------------
        end_suffix = UFU.datetime_get_datetime_str()
        backup_filepath = self.filepath_get_with_new_stem(destination, start_suffix="-", preend_suffix="_", end_suffix=end_suffix)
        try:
            shutil.copy(source, backup_filepath)
            return True
        except:
            pass

    def file_backups_get_wildmask(self, filepath: Union[None, str, pathlib.Path] = None) -> str:
        filepath = self.filepath_get_active(filepath)
        wmask = f"*{filepath.stem}*{filepath.suffix}"
        return wmask

    def filepath_backups_get(
            self,
            filepath: Optional[pathlib.Path] = None,
            dirpath: Optional[pathlib.Path] = None,
            nested: bool = True
    ) -> list[pathlib.Path]:
        """
        find all backup files nearby
        """
        wmask = self.file_backups_get_wildmask(filepath)
        result = self.files_find_in_dirpath(dirpath=dirpath, wmask=[wmask], nested=nested)
        result = sorted(result, key=lambda obj: obj.stat().st_mtime, reverse=True)

        # exclude original data file
        if self.filepath in result:
            result.remove(self.filepath)

        return result

    def file_backups_delete__except_last_count(self, count: int = 15, filepath: Optional[pathlib.Path] = None, dirpath: Optional[pathlib.Path] = None) -> None:
        """
        delete old backups
        """
        filepath_to_delete_list = self.filepath_backups_get(filepath=filepath, dirpath=dirpath)
        if count:
            filepath_to_delete_list = filepath_to_delete_list[count:]

        for filepath in filepath_to_delete_list:
            filepath.unlink()

    def file_backups_delete__older(
            self,
            point: Union[int, float, datetime.datetime],
            filepath: Optional[pathlib.Path] = None,
            dirpath: Optional[pathlib.Path] = None) -> None:
        """
        delete old backups
        """
        filepath_to_delete_list = self.filepath_backups_get(filepath=filepath, dirpath=dirpath)
        return self.files_delete_older(point=point, files=filepath_to_delete_list)

    # DIRPATH =========================================================================================================
    @property
    def dirpath(self) -> pathlib.Path:  # dirpath never set!!! used only in some methods!!!
        """
        created only for resolving CWD or self.__filepath.parent

        CAREFUL:
            1. use it only forgetting parent from setted self.__filepath!!!!
            if you need resolve it by passing new filepath without saving in __filepath use dirpath_get_active!!!!
        :return:
        """
        if self.filepath:
            return self.filepath.parent

        return self.DIRPATH_DEFAULT or pathlib.Path.cwd()   # TODO: maybe delete cwd!!!!

    def dirpath_get_active(self, dirpath: Union[None, str, pathlib.Path] = None) -> pathlib.Path:
        """
        UNDER QUESTION!
            Дефолт дирпас - актуален только если вы не знаете какой будет файл но заранее известно в какой папке!
            После установки файла дирпас идет строго по нему!!!! А после очистки файла возвращается к дефолтному!!!
            Если дефолтных не установлен то свд ???
        """
        # NOT INPUTED -------------------------------
        if dirpath is None:
            return self.dirpath

        # INPUTED -------------------------------
        return pathlib.Path(dirpath)

    def dirpath_ensure(self, dirpath: Union[None, str, pathlib.Path] = None) -> bool:
        dirpath = self.dirpath_get_active(dirpath=dirpath)

        try:
            dirpath.mkdir(parents=True, exist_ok=True)
        except:
            pass

        if dirpath.exists():
            return True
        else:
            msg = f"CANT create {dirpath=}"
            print(msg)

    # FIND ------------------------------------------------------------------------------------------------------------
    def __find_in_dirpath(
            self,
            type_0files_1dirs: int,
            dirpath: Union[str, pathlib.Path] = None,
            return_0obj_1name: int = 0,               # TRY NOT TO USE STEMS!!!!
            wmask: Union[None, str, list] = None,
            nested: bool = False,
    ) -> list[Union[str, pathlib.Path]]:
        """
        list all variants. Repeated items not shown! order is preserved!
        """
        wmask = wmask or "*"
        wmask = UFU.sequence_make_ensured_if_not(wmask)

        dirpath = self.dirpath_get_active(dirpath)
        result = []

        for mask in wmask:
            mask = mask if not nested else f"**/{mask}"
            for path_obj in dirpath.glob(mask):
                if (type_0files_1dirs == 0 and path_obj.is_file()) or (type_0files_1dirs == 1 and path_obj.is_dir()):
                    if path_obj not in result:
                        result.append(path_obj)

        # FINISH
        if return_0obj_1name == 1:
            result = [path_obj.name for path_obj in result]

        print(f"{result=}")
        return result

    def files_find_in_dirpath(self, **kwargs):
        return self.__find_in_dirpath(type_0files_1dirs=0, **kwargs)

    def dirs_find_in_dirpath(self, **kwargs):
        return self.__find_in_dirpath(type_0files_1dirs=1, **kwargs)

    # DELETE ----------------------------------------------------------------------------------------------------------
    def files_find_and_delete_older(
            self,
            point: Union[None, int, float, datetime.datetime] = None,
            **kwargs
    ) -> None:
        files = self.files_find_in_dirpath(**kwargs)
        return self.files_delete_older(files=files, point=point)

    def files_delete_older(
            self,
            files: list[Union[str, pathlib.Path]],
            point: Union[None, int, float, datetime.datetime] = None
    ) -> None:
        # INPUT
        if isinstance(point, (datetime.datetime)):
            point = point.timestamp()
        if not isinstance(point, (type(None), int, float)):
            raise Exception

        # WORK
        for filepath in files:
            filepath = pathlib.Path(filepath)
            if not filepath.is_file():
                continue
            if not point or filepath.stat().st_mtime < point:
                filepath.unlink()

    # TODO: NOT WORKING!!!!! FINISH!!!! cant delete by access reason!!!
    def dirs_delete_if_blank(
            self,
            dirpath: Union[str, pathlib.Path],
            nested: bool = False
    ):
        dirs = self.dirs_find_in_dirpath(dirpath=dirpath, nested=nested)
        for dirpath in dirs:
            try:
                dirpath.rmdir()
            except:
                pass

    # READ/WRITE ======================================================================================================
    # READ ---------------------------------
    def filepath_read_text(self, filepath=None) -> Optional[str]:
        filepath = self.filepath_get_active(filepath)
        if filepath.exists() and filepath.is_file():
            return filepath.read_text(encoding="utf-8")

    def filepath_read_bytes(self, filepath=None) -> Optional[bytes]:
        filepath = self.filepath_get_active(filepath)
        if filepath.exists() and filepath.is_file():
            return filepath.read_bytes()

    # WRITE ---------------------------------
    def filepath_write_text(self, text: str, filepath=None) -> Optional[int]:
        filepath = self.filepath_get_active(filepath)
        if filepath:
            self.dirpath_ensure(self.filepath.parent)
            return filepath.write_text(data=text, encoding="utf-8")

    def filepath_write_bytes(self, data: bytes, filepath=None) -> Optional[int]:
        filepath = self.filepath_get_active(filepath)
        if filepath:
            self.dirpath_ensure(self.filepath.parent)
            return filepath.write_bytes(data=data)


# =====================================================================================================================
