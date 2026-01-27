# TODO-1=add logdata_load_by_name_wo_extention with extention param!
# TODO-1=add extention default? maybe NO!


# =====================================================================================================================
from typing import *
import pathlib
import shutil


# =====================================================================================================================
class File:
    """
    BASE CLASS FOR WORKING WITH FILES! and selecting only one!
    if you need work only with path base_types in FileSystem (list_dir for example) without exactly opening files
    use it directly or create special class.
    In other cases with special file types use other special classes inherited from this - Json/Log

    ATTENTION:
        1. DONT USE FILES READ/WRITE WITHOUT SELECTING!!!
            if you creating instance for working with exact file - dont read/write another file without selecting new one!!!
            all methods who get filepath-like parameter - will and must use selecting it!!!
    """
    FILEPATH_BACKUP: bool = None     # used right before dump

    # BACKUPS ---------------------------------------------------------------------------------------------------------
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
        source = self.get_active__filepath(filepath)
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
        filepath = self.get_active__filepath(filepath)
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
        if self.FILEPATH in result:
            result.remove(self.FILEPATH)

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


# =====================================================================================================================
# PATH ----------------------------------------------------------------------------------------------------------------
def path_cwd_check_run_correctly(filename, path_cwd, raise_if_false=True):
    """show if you correctly starting your project!

    используется только в корневом файле проекта, который запускает пользователь!
    причина появления функции - пользователь может открыть терминал CMD и закинуть в него корневой файл проекта
    проект может запуститься НО корневая директория будет считаться корневой директорией терминала а не директорией проекта!!
    от этого все внутренние ссылки в проекте на текущий каталог будут неверными и ниодного файла/каталога не будет видно!

    RECOMMENDED USAGE!!!!
        import pathlib
        path_cwd_check_run_correctly(__file__, pathlib.Path.cwd())    # PLACE ONLY IN ROOT(__MAIN__) FILE!!!

    :param filename: recommended __file__
    :param path_cwd: recommended pass pathlib.Path.cwd() but you can use str or else
    """
    # todo: in future you may can work with stack! use __name_/__main__ ets...

    dirpath = pathlib.Path(filename).parent
    path_cwd = pathlib.Path(path_cwd)
    result = dirpath == path_cwd
    if not result:
        msg = f"""
            НЕВЕРНЫЙ КОРНЕВОЙ ПУТЬ (CWD) ЗАПУСКА ПРОГРАММЫ\n
            ПОСЛЕДСТВИЯ - программа не увидит папки и файлы проекта\n
            скорее всего запуск прозошел в терминале CMD\n
            фактическое расположение файла=[{dirpath=}]
            определен текущий каталог программой=[{path_cwd=}]

            для корректного запуска - в используемом терминале перейдите из [path_cwd] в [path_file]
        """
        print(msg)
        if raise_if_false:
            raise Exception(msg)

    return result


# =====================================================================================================================
