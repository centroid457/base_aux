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
# from results.results_testplan import ResultsTestplan_Singleton
# =====================================================================================================================

import string
from win32com.client import Dispatch
import pythoncom
from gui.wgt_logger import LogProgressBarValue, LogProgressBarTimeout, LogProgressBarCounter
from utilities.processor_file import ProcessorFileSelector


# funcs ===============================================================================================================
def excel_sheets_remove_all_except(sheet_index, wb_obj):
    """ In 'excel_book', removes all sheets except sheet_index.
        Return False if there is no such sheet
    """
    if sheet_index < wb_obj.Sheets.Count:
        UFU.logging_and_print_error(f'Ошибка: нет листа с индексом {sheet_index} в Excel-файле')
        return

    for sheet_i in range(wb_obj.Sheets.Count):
        if sheet_i == sheet_index:
            continue
        wb_obj.Sheets[sheet_i].Delete()
    return True


# EXCEL CELL ==========================================================================================================
class _ExcelCell:
    def __init__(self, row, column, sheet_obj):
        self.row = row          # номер строки
        self.column = column    # номер столбца
        self.sheet = sheet_obj      # объект листа .xlsx-файла

    @property
    def value(self):
        pass

    @value.setter
    def value(self, value):
        pass


class Win32comExcelCell(_ExcelCell):
    @property
    def value(self):
        return self.sheet.Cells(self.row, self.column).Value

    @value.setter
    def value(self, value):
        self.sheet.Cells(self.row, self.column).Value = value


# EXCEL HANDLER =======================================================================================================
class _ExcelProcessor:
    CLASS_CELL = None

    def __init__(self):
        self.app = None
        self.workbook = None
        self.sheet = None       # starichenko - before nobody use it!
        self.filepath = None  # Путь к файлу Excel для записи данных

    def initialize(self, file_path):
        """ Initializing Excel app, workbook, etc...
        return True  - successful
        return False - not successful
        """
        raise NotImplementedError

    def cell(self, row, column, sheet_index=0):
        """ Returns instance of interface-class for working with cells
        """
        sheet_obj = self.sheet_obj_get(sheet_index)
        if sheet_obj:
            return self.CLASS_CELL(row, column, sheet_obj)

        msg = f"Cannot create cell {row=}/{column=}/{sheet_index=}"
        UFU.logging_and_print_error(msg)

    @staticmethod
    def column_get_name_by_number(number):    # starichenko
        """ For given number returns its corresponding uppercase letter.
        Used for Excel column int-to-name transformation!

        Example:
            0 -> "", 1 -> 'A', 2 -> 'B', ..., 26 -> 'Z',
            27 -> "AA", 28 -> "AB", etc...
        """
        # letter_list = []
        # alphabet = list(string.ascii_uppercase)
        # alphabet_length = len(alphabet)
        # while number > 0:
        #     last_digit = alphabet_length if (number % alphabet_length == 0) else (number % alphabet_length)
        #     if alphabet[(last_digit - 1): last_digit]:
        #         letter = alphabet[last_digit - 1]
        #         letter_list.insert(0, letter)
        #     number = (number - last_digit) // alphabet_length
        # return ''.join(letter_list)

        base_list = list(string.ascii_uppercase)
        result_list_reverted = UFU.number_convert_to_list_by_baselist(source=base_list, number=number, zero_is_first=False)
        result_str = UFU.sequence_join_to_string_simple(source=result_list_reverted, revert_order=True)
        return result_str


class Win32comExcelProcessor(_ExcelProcessor):
    CLASS_CELL = Win32comExcelCell

    def importing(self):
        try:
            import win32com.client
            import pythoncom
            self.pythoncom = pythoncom
            return win32com.client

        except Exception as exx:
            UFU.logging_and_print_warning(f"{exx!r}")
            UFU.logging_and_print_warning('Cannot import Excel library')

    def initialize(self, file_path):
        # =================================================
        file_path = pathlib.Path(file_path)
        if not file_path.exists():
            UFU.logging_and_print_warning(f"Файл отчета не создан, не существует: {file_path}.")
            return False
        if not file_path.is_file():
            UFU.logging_and_print_warning(f"Файл отчета не создан, путь не указывает на файл: {file_path}.")
            return False
        self.file_path = file_path

        # =================================================
        self.importing()
        try:
            pythoncom.CoInitialize()    # я не знаю почему и зачем НО без этого не работает Dispatch!!!
            self.app = Dispatch("Excel.Application")
            # msg = f"created {self.app=}"
            # UFU.logging_and_print_warning(msg)
        except Exception as exx:
            msg = f"[Exception] Cannot dispatch ExcelApp:{exx!r}"
            UFU.logging_and_print_warning(msg)
            return

        try:
            self.app.DisplayAlerts = False  # отображение ошибок
            self.app.Visible = False        # Отключаем визуализацию, чтобы пользователь не вмешивался в процесс
            # msg = f"settings applied {self.app=}"
            # UFU.logging_and_print_warning(msg)
        except:
            msg = f'Cannot apply settings DisplayAlerts/Visible'
            UFU.logging_and_print_warning(msg)

        # self.workbook = self.app.Workbooks.Open(file_path)
        try:
            if self.app.Workbooks.Count > 0:
                UFU.logging_and_print_warning("Закрываем принудительно все открытые предыдущие сеансы книг Excel")
                try:
                    self.app.Workbooks.Close()
                except Exception as exx:
                    UFU.logging_and_print_warning(f"Ошибка закрытия книг Excel. {exx!r}")
            UFU.logging_and_print_debug(f"Открываем книгу Excel: {file_path=}")
            self.workbook = self.app.Workbooks.Open(file_path)
            # msg = f"created {self.workbook.FullName=}{file_path=}"
            # UFU.logging_and_print_warning(msg)
            return True
        except Exception as exx:
            msg = f"[Exception] Cannot open Excel {file_path=}:{exx!r}"
            UFU.logging_and_print_error(msg)

            msg = f"maybe you have some inconvenient range Names in XLSX-file (ex. Print_Area, ...?) find and delete it in [{file_path=}]"
            UFU.logging_and_print_error(msg)
            
            try:
                self.app.DisplayAlerts = True
                self.app.Workbooks.Close()
                self.app.Quit()
            except Exception as exx:
                UFU.logging_and_print_warning(f"Ошибка при попытке корректного закрытия книги и приложения Excel. {exx!r}")

    def close(self):
        result = True
        try:
            self.workbook.Save()
            self.workbook.Close()
        except Exception as exx:
            result = False
            UFU.logging_and_print_warning(f"[EXCEPTION]Cannot close workbook:{exx!r}")

        try:
            self.app.DisplayAlerts = False
            self.app.Visible = False
            # self.app.Quit()  # Убрал закрытие всего приложения, т.к. тут должны работать с конкретной книгой.
            # self.app = None
        except Exception as exx:
            result = False
            UFU.logging_and_print_error(f"[EXCEPTION]Cannot quit Excel application:{exx!r}")

        return result

    # SHEET -----------------------------------------------------------------------------------------------------------
    pass

    def sheets_name_list_get(self) -> list:
        sheets_name_list = []
        self.workbook
        try:
            sheets = self.workbook.Sheets
            if sheets:
                for sheet in sheets:
                    # logging.debug(f"sheet (Name, index) = ({sheet.Name}, {sheet.index})")
                    sheets_name_list.append(sheet.Name)
        except Exception as exx:
            UFU.logging_and_print_warning(f'{exx!r}')
            raise exx
        return sheets_name_list
        
    # 1=sheets=DIRECT name/index --------------------------------------------------
    def sheet_index_exist_check(self, sheet_index):
        result = sheet_index in range(self.sheets_count())
        # if not result:
        #     msg = f"SHEET not exist [{sheet_index=}]"
        #     UFU.logging_and_print_warning(msg)
        return result

    def _sheet_index_get_by_name(self, name):
        """
        you dont need use it! work directly with name_or_index for specifying sheet in any method!!!
        """
        i = 0
        for sheet_obj in self.workbook.Sheets:
            if sheet_obj.Name == name:
                return i
            else:
                i += 1

    def _sheet_name_get_by_index(self, sheet_index=0):
        """
        you dont need use it! work directly with name_or_index for specifying sheet in any method!!!
        """
        sheet_obj = self.sheet_obj_get(sheet_index)
        if sheet_obj:
            return sheet_obj.Name

    # 2=sheets=ANY name/index --------------------------------------------------
    def _sheet_index_get_by_any(self, name_or_index=None):   # starichenko
        """return ensured index! from any data"""
        try:
            return name_or_index.Index
        except:
            pass

        if name_or_index is None:
            index = 0
        elif isinstance(name_or_index, int):
            index = name_or_index
        elif isinstance(name_or_index, str):
            index = self._sheet_index_get_by_name(name_or_index)

        if self.sheet_index_exist_check(index):
            # msg = f"SHEET found {name_or_index=}{index=}"
            # UFU.logging_and_print_warning(msg)
            return index

    def _sheet_index_get(self, name_or_index):
        # sheet indexing begin from 0!!! but cells row/count from 1!!!

        msg = f"PLEASE DONT USE self._sheet_index_get!!!  NOT NEED RESOLVE INDEx BY NAME!!! USE DIRECTLY ANY OF Index/Name!!!"
        UFU.logging_and_print_warning(msg)
        return self._sheet_index_get_by_any(name_or_index)

    def sheet_obj_get(self, name_or_index=None):
        try:
            name_or_index.Index
            name_or_index.Name
            return name_or_index
        except:
            pass

        sheet_index = self._sheet_index_get_by_any(name_or_index)
        if sheet_index is not None:     # DONT DELETE NONE COMPARE!!!
            return self.workbook.Sheets[sheet_index]

    def sheet_name_rename(self, new_name, name_or_index=0):
        sheet_obj = self.sheet_obj_get(name_or_index)
        if sheet_obj:
            sheet_obj.Name = new_name
            return True

    def sheet_header_get(self, name_or_index=0):
        sheet_obj = self.sheet_obj_get(name_or_index)
        if sheet_obj:
            return sheet_obj.PageSetup.CenterHeader

    def sheet_header_set(self, new_header, name_or_index=0):
        sheet_obj = self.sheet_obj_get(name_or_index)
        if sheet_obj:
            sheet_obj.PageSetup.CenterHeader = new_header
            return True

    def sheet_footer_get(self, name_or_index=0):
        sheet_obj = self.sheet_obj_get(name_or_index)
        if sheet_obj:
            return sheet_obj.PageSetup.CenterFooter

    def sheet_footer_set(self, new_footer, name_or_index=0):
        sheet_obj = self.sheet_obj_get(name_or_index)
        if sheet_obj:
            sheet_obj.PageSetup.CenterFooter = new_footer
            return True

    def sheets_count(self):
        if self.workbook:
            # return len(self.workbook.Sheets)
            return self.workbook.Sheets.Count
        UFU.logging_and_print_error(f'Cannot get number of sheets {self.workbook.FullName=}')

    # @UFU.decorator_try__return_none_and_log_explanation
    def sheet_remove(self, name_or_index=None):
        sheet_obj = self.sheet_obj_get(name_or_index)
        if sheet_obj:
            sheet_obj.Delete()
            return True

    def sheets_remove_all_except_and_start_from(self, safe_sheet, start_sheet=0):
        safe_sheet_index = self._sheet_index_get_by_any(safe_sheet)
        start_sheet_index = self._sheet_index_get_by_any(start_sheet)
        sheet_obj = self.sheet_obj_get(safe_sheet_index)
        if not sheet_obj:
            return

        for sheet_i in range(start_sheet_index, self.sheets_count()):
            if sheet_i == safe_sheet_index:
                continue

            try:
                self.sheet_remove(sheet_i)
            except Exception as exx:
                UFU.logging_and_print_error(f"{exx!r}")

        return True

    def sheet_hide(self, sheet_name_or_index=None):    # starichenko
        sheet_obj = self.sheet_obj_get(sheet_name_or_index)
        if sheet_obj:
            sheet_obj.visible = False
            return True

    # row -------------------------------------------------------------------------------------------------------------
    def row_hide(self, index, sheet_name_or_index=None):
        sheet_obj = self.sheet_obj_get(sheet_name_or_index)
        if sheet_obj:
            sheet_obj.Rows(index).hidden = True
            return True

    # @UFU.decorator_try__return_none_and_log_explanation
    def row_copy_and_insert(self, copy_from_row, insert_to_row, sheet_name_or_index=None, first_column=1, last_column=100):
        sheet_obj = self.sheet_obj_get(sheet_name_or_index)
        if sheet_obj:
            first_cell_string_name = self.column_get_name_by_number(first_column) + str(copy_from_row)  # like 'A13'
            last_cell_string_name = self.column_get_name_by_number(last_column) + str(copy_from_row)    # like 'K13'
            sheet_obj.Range(first_cell_string_name + ':' + last_cell_string_name).Copy()
            first_cell_string_name = self.column_get_name_by_number(first_column) + str(insert_to_row)  # like 'A14'
            sheet_obj.Range(first_cell_string_name).Insert()
            sheet_obj.Rows(insert_to_row).RowHeight = sheet_obj.Rows(copy_from_row).RowHeight
            return True

    # column ----------------------------------------------------------------------------------------------------------
    def column_width_get(self, column_num, sheet_name_or_index=None):
        sheet_obj = self.sheet_obj_get(sheet_name_or_index)
        if sheet_obj:
            column_letter = self.column_get_name_by_number(column_num)
            column_width = sheet_obj.Columns(column_letter).ColumnWidth
            return column_width

    # @UFU.decorator_try__return_none_and_log_explanation
    def column_width_set(self, column_num, width, sheet_name_or_index=None):
        sheet_obj = self.sheet_obj_get(sheet_name_or_index)
        if sheet_obj:
            column_letter = self.column_get_name_by_number(column_num)
            sheet_obj.Columns(column_letter).ColumnWidth = width
            return True

    # @UFU.decorator_try__return_none_and_log_explanation
    def column_hide(self, letter_or_num, sheet_name_or_index=None):  # starichenko
        sheet_obj = self.sheet_obj_get(sheet_name_or_index)
        if sheet_obj:
            sheet_obj.Columns(letter_or_num).hidden = True
            return True

    # cell ------------------------------------------------------------------------------------------------------------
    def cell_value_get(self, row=None, column=None, sheet_name_or_index=None):  # starichenko
        row = row or 1
        column = column or 1

        sheet_obj = self.sheet_obj_get(sheet_name_or_index)
        if not sheet_obj:
            return

        return sheet_obj.Cells(row, column).Value

    def cell_value_set(self, value, row=None, column=None, sheet_name_or_index=None) -> bool:  # starichenko
        print(f"{value=}/{row=}/{column=}/{sheet_name_or_index=}")
        row = row or 1
        column = column or 1

        sheet_obj = self.sheet_obj_get(sheet_name_or_index)
        if not sheet_obj:
            return False

        if sheet_obj:
            sheet_obj.Cells(row, column).Value = value
            # time.sleep(0.05)
            # return sheet_obj.Cells(row, column).Value == value

    def excel_dump_dict(self, start_row=None, start_column=None, values_dict=None, sheet_name_or_index=None) -> tp.Optional[int]:    # return row_current
        """
        set values vertically by dict

        :param start_row:
        :param start_column:
        :param values_dict: = {column1_value: [column2_value, column3_value]}
        :param sheet_name_or_index:
        :return:
        """
        # INPUT -------------------------------------------------------------------------------------------------------
        start_row = start_row or 1
        start_column = start_column or 1

        sheet_obj = self.sheet_obj_get(sheet_name_or_index)
        if not sheet_obj:
            return

        # WORK --------------------------------------------------------------------------------------------------------
        progress_obj = LogProgressBarCounter(max_value=len(values_dict), title_prefix=f"заполнение данных в протокол [{sheet_obj.Name=}]")

        row_current = start_row
        for name, value in values_dict.items():
            progress_obj.update(title=f"{name}")

            # NAME ----------------------------------------------------------
            row_current += 1
            column_current = start_column
            self.cell_value_set(row=row_current, column=column_current, value=str(name), sheet_name_or_index=sheet_obj)

            # VALUE ---------------------------------------------------------
            if isinstance(value, (str, int, float, bytes, bool)):
                column_current += 1
                self.cell_value_set(row=row_current, column=column_current, value=str(value), sheet_name_or_index=sheet_obj)

            elif isinstance(value, (list, )):
                for value_i in value:
                    column_current += 1
                    if UFU.value_is_blanked(value_i, zero_as_blank=False):
                        value_i = ""
                    self.cell_value_set(row=row_current, column=column_current, value=str(value_i), sheet_name_or_index=sheet_obj)

            elif isinstance(value, (dict, )):
                row_current = 1 + self.excel_dump_dict(start_row=row_current + 1, start_column=start_column, values_dict=value, sheet_name_or_index=sheet_name_or_index)

        # finish -----------------------------------------------------------------------------------
        progress_obj.update_status(True)
        return row_current

    def cell_obj_find_by_text(self, string, sheet_name_or_index=None):   # starichenko
        sheet_obj = self.sheet_obj_get(sheet_name_or_index)
        if sheet_obj:
            return sheet_obj.Cells.Find(What=string)

    def cell_row_column_find_by_text(self, string, sheet_name_or_index=None, error_logging=True):
        cell_obj = self.cell_obj_find_by_text(string=string, sheet_name_or_index=sheet_name_or_index)
        if cell_obj:
            return (cell_obj.Row, cell_obj.Column)

    # @UFU.decorator_try__return_none_and_log_explanation
    def text_replace_on_sheet(self, replace_what, replace_by, sheet_name_or_index=None):
        """first or all???"""
        sheet_obj = self.sheet_obj_get(sheet_name_or_index)
        if sheet_obj:
            sheet_obj.Cells.Replace(What=replace_what, Replacement=replace_by)
            return True

    # areas -----------------------------------------------------------------------------------------------------------
    def areas_hide(self, sheets=[], sheet_rows={}, sheet_columns={}, rc_as_1names_2values=1):     # starichenko
        """
        :param sheet_rows/sheet_columns: type depends on rc_as_1names_2values
            {"sheet_name": [1, 2, ]                     # rc_as_1names_2values=1
            {"sheet_name": ["A", "B", ]                 # rc_as_1names_2values=1
            {"sheet_name": ["value10", "value11", ]     # rc_as_1names_2values=2

        :param rc_as_1names_2values: row/column as 1=name/index, 2values - need to find it!
        """
        result = True
        if sheets:
            for sheet in sheets:
                result &= self.sheet_hide(sheet)

        if sheet_rows:
            for sheet, row_list in sheet_rows.items():
                sheet_index = self._sheet_index_get_by_any(sheet)
                for row in row_list:
                    if rc_as_1names_2values == 1:
                        row_index = row
                    elif rc_as_1names_2values == 2:
                        cell_found_tuple = self.cell_row_column_find_by_text(row, sheet_name_or_index=sheet_index)
                        if cell_found_tuple:
                            row_index = cell_found_tuple[0]
                        else:
                            msg = f"cant find value=[{row}] in sheet=[{sheet}/{sheet_index}]"
                            UFU.logging_and_print_warning(msg)
                            result = False
                            continue

                    result &= self.row_hide(index=row_index, sheet_name_or_index=sheet_index)

        if sheet_columns:
            for sheet, column_list in sheet_columns.items():
                sheet_index = self._sheet_index_get_by_any(sheet)
                for column in column_list:
                    if rc_as_1names_2values == 1:
                        column_index = column
                    elif rc_as_1names_2values == 2:
                        cell_found_tuple = self.cell_row_column_find_by_text(column, sheet_name_or_index=sheet_index)
                        if cell_found_tuple:
                            column_index = cell_found_tuple[1]
                        else:
                            msg = f"cant find value=[{column}] in sheet=[{sheet}/{sheet_index}]"
                            UFU.logging_and_print_warning(msg)
                            result = False
                            continue

                    result &= self.column_hide(letter_or_num=column_index, sheet_name_or_index=sheet_index)

        return result


# ====================================================================================================================
def _test_wb():
    protocol_fullpath = 'C:\\!_STARICHENKO-T8\\!!!_GD_additional\\_PROJECTS\\dwdm_test_system\\t10.xlsx'

    file_processor = Win32comExcelProcessor()
    file_processor.initialize(protocol_fullpath)
    try:
        cell_obj_find = file_processor.cell_obj_find_by_text("hello", 0)
        print(cell_obj_find.Value)
        cell_obj_paste = cell_obj_find.getOffsetRange(0, 1)
        print(True)
        cell_obj_paste.Value = 100
    except:
        print("EXCEPTION!")
    file_processor.close()


def _test__read_cell_value():
    protocol_fullpath = 'C:\\!_STARICHENKO-T8\\!!!_GD_additional\\_PROJECTS\\dwdm_test_system\\t10.xlsx'

    file_processor = Win32comExcelProcessor()
    file_processor.initialize(protocol_fullpath)
    try:
        print(file_processor.cell_value_get())
        print(file_processor.cell_value_set(value="hello"))
        print(file_processor.cell_value_get())
    except Exception as exx:
        print(f"EXCEPTION!{exx!r}")
    file_processor.close()


def _test__table_write_by_dict():
    protocol_fullpath = 'C:\\!_STARICHENKO-T8\\!!!_GD_additional\\_PROJECTS\\dwdm_test_system\\t10.xlsx'

    file_processor = Win32comExcelProcessor()
    file_processor.initialize(protocol_fullpath)
    try:
        print(file_processor.excel_dump_dict(values_dict={1:123}))
    except Exception as exx:
        print(f"EXCEPTION!{exx!r}")
    file_processor.close()


# ====================================================================================================================
if __name__ == '__main__':  # starichenko
    _test__table_write_by_dict()
