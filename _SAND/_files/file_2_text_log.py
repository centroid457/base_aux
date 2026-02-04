# TODO-1=finish refact to generic structure!
# TODO-2=finish NotImplementedError
# TODO-2=add deleting older then date!
# TODO-2=add wolking with recurtion while finding list of backups
# TODO-2=add clearly finding backups like pattern not BACKUP!

# =====================================================================================================================
# STARICHENKO UNIVERSAL IMPORT
import sys
sys.path.append("..")  # Adds higher directory to python modules path.
import CONSTANTS

import time
import pathlib
import typing as tp

import utilities.func_universal as UFU
from gui.pyqt_import_all_by_star import *

# from users.user_profile import UserProfile_Singleton
# from stands.stand import Stand_Singleton
# from results.results_testplan import TestplanResults_Singleton
# =====================================================================================================================
import pytest
import re
from utilities.processor_file import File


# =====================================================================================================================
class ProcessorTextLog(File):     # starichenko
    """
    Simplify working with logFiles

    DEFINITIONS:
        LOGLINES - list of data strings/bytes(?)
        LogLINE - minimal unit of LogDATA (one line)
        LogBLOCK - unit of LogDATA created by separating it by any ligLine

    IMPORTANT RULES:
        1. all internal data
            - must be in list form!!!
            - end-lines not needed but its not wrong! RECOMMENDED NOT USE IT!!!
            - may be ANY data! and class not change IT! anless you save it and load!

        2. keep opened file object is obligated! every time you need reopen+close the fileObject!

        3. this class dont delete/miss blank lines or inputed LOGLINES! just ensure EOL on saving process!


    USAGE:
        1. if you need find pattern in data - use loglines_iter
    """
    __LOGLINES: list[tp.Union[str, bytes]] = []
    EOL = "\n"

    @property
    def LOGLINES(self):
        return self.__LOGLINES

    def loglines_set(self, data):
        self.__LOGLINES = self._loglines_get_from_any(data)

    def logdata_clear(self):
        self.__LOGLINES = []

    def loglines_get_active(self, logdata: tp.Optional[list[tp.Union[str, bytes]]] = None) -> list[tp.Union[str, bytes]]:
        """
        used always get final logdata (from instanse or specified param)
        """
        if logdata is None:
            logdata = self.LOGLINES
        else:
            logdata = self._loglines_get_from_any(logdata)

        if not logdata:
            msg = f"blank {logdata=}"
            UFU.logging_and_print_warning(msg)
        return logdata

    # converters ------------------------------------------------------------------------------------------------------
    def _logline_eol_ensure(self, source):
        source = f"{source}"
        if not source.endswith(self.EOL):
            source = source + self.EOL
        return source

    def _loglines_get_from_any(self, data_str):
        if isinstance(data_str, (str, bytes)):
            log_list = data_str.splitlines(keepends=True)
        elif UFU.type_is_iterable_but_not_str(data_str):
            log_list = list(data_str)
        else:
            log_list = []
        return log_list

    def _loglines_to_str(self, data: tp.Optional[list] = None):
        logdata = self.loglines_get_active()
        if UFU.type_is_iterable_but_not_str(logdata):
            data = UFU.sequence_join_to_string_simple(source=logdata, sep="\n")
        return data

    # READ/WRITE FULL -------------------------------------------------------------------------------------------------
    def loglines_read(self, filepath=None):
        raise NotImplementedError()






    def loglines_load(self, filepath=None) -> tp.Optional[bool]:
        self.logdata_clear()

        filepath = self.filepath_get_active(filepath)

        if not filepath:
            return

        if not filepath.exists():
            msg = f"файла не существует [{filepath=}]"
            UFU.logging_and_print_warning(msg)
            return

        try:
            with open(filepath, 'r', encoding='utf-8') as fo:
                data = fo.read()
                self.loglines_set(data.splitlines(keepends=False))
        except Exception as exc:
            msg = f"{exc!r}]"
            UFU.logging_and_print_warning(msg)
            return []

        return True

    def logdata_load_by_name_wo_extention(self, name, extension="log", dirpath=None):
        dirpath = dirpath or (self.filepath.parent if self.filepath else pathlib.Path.cwd())
        dirpath = pathlib.Path(dirpath)

        filepath = dirpath.joinpath(f"{name}.{extension}")
        return self.loglines_load(filepath)

    def loglines_dump(self, filepath=None, data=None, append=False):
        # filepath
        filepath = self.filepath_get_active(filepath)
        if filepath:
            filepath = pathlib.Path(filepath)
            dirpath = filepath.parent
            dirpath.mkdir(parents=True, exist_ok=True)
        else:
            msg = f"не выбран путь [{filepath=}]"
            UFU.logging_and_print_warning(msg)
            return []

        # LOGLINES
        data_list = self._loglines_get_from_any(data) if data is not None else self.LOGLINES

        try:
            with open(filepath, "a" if append else "w", encoding='utf-8') as fo:
                fo.writelines(map(self._logline_eol_ensure, data_list))
                return True
        except Exception as exc:
            UFU.logging_and_print_warning(f'{exc!r}')

    # READ/WRITE PART -------------------------------------------------------------------------------------------------
    def loglines_tail(self):  # starichenko
        raise NotImplementedError()

    # DATA ============================================================================================================
    pass

    def logline_validate(self, line, pattern=[".*", ], antipattern=[]):    # starichenko
        if not pattern:
            return

        if UFU.type_is_iterable_but_not_str(pattern):
            pattern_list = pattern
        else:
            pattern_list = [pattern, ]

        if any((re.search(pattern=str(pattern_i), string=str(line)) for pattern_i in pattern_list)):
            return not self.logline_validate(line=line, pattern=antipattern)

    def loglines_iter(self, pattern=[".*", ], antipattern=[], data=None, reverse=False):
        # INPUT -------------------------------------------------------------------------------------------------------
        if data is not None:
            data_list = self._loglines_get_from_any(data)
        else:
            data_list = self.LOGLINES

        if not data_list:
            msg = f"нет данных для обработки [{data_list=}]"
            UFU.logging_and_print_warning(msg)
            return []

        # WORK --------------------------------------------------------------------------------------------------------
        func_for_validate = lambda _line: self.logline_validate(line=_line, pattern=pattern, antipattern=antipattern)
        return filter(func_for_validate, data_list[::-1 if reverse else 1])

    # BLOCKS ----------------------------------------------------------------------------------------------------------
    def logblocks_iter__split_by_same_startswith(self, count_chars, data=None, reverse=False):
        raise NotImplementedError()

    def logblocks_iter__split_by_pattern(self, pattern, data=None, reverse=False, include_pattern_line=True):
        """
        return block data (lines ALWAYS IN DIRECT ORDER)!!!

        TIPS;
            1. typically you need last or prelast block (last finished if device still online).
            2. if you need get appended data from file - use full last row as pattern!

        :param pattern: you can use iven INT! but for your responsibility!
        :param data:
        :param skip_first_found_blocks_count:
        :param reverse:
        :return:
        """
        # INPUT -------------------------------------------------------------------------------------------------------
        pattern = str(pattern)

        if data:
            data_list = self._loglines_get_from_any(data)
        else:
            data_list = self.LOGLINES

        if not data_list:
            msg = f"нет данных для обработки [{data_list=}]"
            UFU.logging_and_print_warning(msg)
            return

        # WORK --------------------------------------------------------------------------------------------------------
        _block_id = 0   # just for debug
        block_data_list = []

        for line_str in data_list[::-1 if reverse else 1]:
            line_str = f"{line_str}"

            found_flag = re.search(pattern=pattern, string=line_str)
            if found_flag:
                if not reverse:
                    # DIRECT order
                    if not block_data_list:
                        # INIT! not yield - its first line in file from start!
                        pass
                    else:
                        yield block_data_list
                    block_data_list = [line_str, ] if include_pattern_line else []
                else:
                    # REVERSE order
                    if include_pattern_line:
                        block_data_list.insert(0, line_str)
                    yield block_data_list
                    block_data_list = []

                _block_id += 1

            else:
                if reverse:
                    block_data_list.insert(0, line_str)
                else:
                    block_data_list.append(line_str)

        # IF FINISH ALL ITERATIONS or BLANK!
        if not block_data_list:
            return
        else:
            yield block_data_list

    def logblock_get_index_from_splited_by_pattern(self, pattern, block_index=0, data=None, include_pattern_line=True):
        block_data_gen = self.logblocks_iter__split_by_pattern(
            pattern=pattern,
            data=data,
            reverse=block_index < 0,
            include_pattern_line=include_pattern_line)

        block_index = block_index if block_index >= 0 else (- block_index - 1)

        try:
            for index in range(block_index):
                block_data_list = next(block_data_gen)
                if not block_data_list:
                    return []

            result = next(block_data_gen)
            print(f"{result=}")
            return result
        except:
            return []


# TESTS ===============================================================================================================
def _test__ProcessorTextLog__save_load():
    test_obj_link = ProcessorTextLog

    data = [1,2,1, "", "\n", "3\n",4]
    filepath = "-hello.txt"
    test_obj = test_obj_link(filepath=filepath, data=data)

    # save/load
    assert test_obj.loglines_dump() == True

    load_file = test_obj.loglines_load()
    print(load_file)
    assert load_file == ['1', '2', '1', "", "", '3', '4']


@pytest.mark.parametrize(
    argnames="p1,p2,p3,p4,_EXPECTED",
    argvalues=[

        (None, 1, None, False, []),
        ("", 1, None, False, []),
        ([], 1, None, False, []),
        ([1, ], 1, None, False, [1, ]),
        ([1, ], 2, None, False, []),

        ([1, 2, 11, 22], 11, None, False, [11]),
        ([1, 2, 11, 22], 11, 1, False, []),             # antipattern

        ([1, 2, 11, 22], 1, None, False, [1, 11]),
        ([1, 2, 11, 22], "1", None, True, [11, 1]),

        # pattern SEVERAL
        ([1, 2, 11, 22], [1], None, False, [1, 11]),
        ([1, 2, 11, 22], [1, 22], None, False, [1, 11, 22]),
        ([1, 2, 11, 22], [1, 22], 11, False, [1, 22]),
    ]

)
def test__ProcessorTextLog__loglines_iter_by_patterns(p1,p2,p3,p4,_EXPECTED):
    test_obj_link = ProcessorTextLog().loglines_iter
    result = [*test_obj_link(data=p1, pattern=p2, antipattern=p3, reverse=p4)]
    assert result == _EXPECTED


@pytest.mark.parametrize(
    argnames="p1,p2,p3,p4,_EXPECTED",
    argvalues=[

        (None, "1", 0, True, []),
        ("", "1", 0, True, []),
        ([], "1", 0, True, []),

        # typical
        ([11, 2, 1, "", "\n", "3\n", 4], "1", 0, True, ["11", "2"]),
        ([11, 2, 1, "", "\n", "3\n", 4], 1, 0, True, ["11", "2"]),     # INT pattern

        # index DIRECT ORDER
        ([1, 2, 1, "", "\n", "3\n", 4], "1", 0, True, ["1", "2"]),
        ([1, 2, 1, "", "\n", "3\n", 4], "1", 1, True, ["1", "", "\n", "3\n", "4"]),
        ([1, 2, 1, "", "\n", "3\n", 4], "1", 2, True, []),                           # out of range
        ([1, 2, 1, "", "\n", "3\n", 4], "1", 3, True, []),                           # out of range

        ([1, 2, 1, "", "\n", "3\n", 4], "1", 0, False, ["2"]),  # include_pattern_line

        # index REVERSE ORDER
        ([1, 2, 1, "", "\n", "3\n", 4], "1", -1, True, ["1", "", "\n", "3\n", "4"]),
        ([1, 2, 1, "", "\n", "3\n", 4], "1", -2, True, ["1", "2"]),
        ([1, 2, 1, "", "\n", "3\n", 4], "1", -3, True, []),  # out of range
        ([1, 2, 1, "", "\n", "3\n", 4], "1", -4, True, []),  # out of range

        ([1, 2, 1, "", "\n", "3\n", 4], "1", -2, False, ["2"]),  # include_pattern_line

        # pattern on first and last position
        ([1, 2, 1], "1", 0, True, ["1", "2"]),
        ([1, 2, 1], "1", 1, True, ["1", ]),

        ([1, 2, 1], "1", -1, True, ["1", ]),
        ([1, 2, 1], "1", -2, True, ["1", "2"]),

    ]

)
def test__ProcessorTextLog__logblock_get_index_from_splited_by_pattern(p1,p2,p3,p4,_EXPECTED):
    test_obj_link = ProcessorTextLog().logblock_get_index_from_splited_by_pattern
    result = test_obj_link(data=p1, pattern=p2, block_index=p3, include_pattern_line=p4)
    assert result == _EXPECTED


def _test__system_syslog():
    test_obj_link = ProcessorTextLog
    filepath = "-system__syslog.log"
    syslog_obj = test_obj_link(filepath=filepath)
    UFU.list_pretty_string(syslog_obj.logblock_get_index_from_splited_by_pattern(pattern="T8-Linux syslog.info syslogd started", block_index=0, reverse=True))
    UFU.list_pretty_string(syslog_obj.logblock_get_index_from_splited_by_pattern(pattern="T8-Linux syslog.info syslogd started", block_index=1, reverse=True))


# ================================================================================================================
if __name__ == '__main__':   # starichenko
    _test__ProcessorTextLog__save_load()


# =====================================================================================================================
