# TODO-100: DATACLASS?? access by dots??
# TODO: implement JSON_DUMP_DEFAULT__MERGE

# =====================================================================================================================
import sys
import time
import pathlib
import typing as tp
import copy
import json
from utilities.processor_file import File
from dataclasses import dataclass, asdict


# =====================================================================================================================
class ProcessorJsonDict(File):     # P*JsonDICT IS IMPORTANT IN NAME!!! because Json may parse LIST or even digit!
    """
    class for working with json data file!
    result is self.json_dict!
    for exact working within internal data (keys, values) create exact special class!

    IMPORTANT:
        1. class has name *JsonDict because json may work with list/tuple/int/float/... even in root level!
        and we can certainly use it for dumping lists in this project in nearest future, i do!
        so in this class base data will always DICT! and always at least blank dict!

        2. RECOMMENDED for all internal keys use property so to keep inline access for containers (list/dict) values!
            for other value types - use getter/setter ----NO!!! DONT USE PROPERTY!!! USE DIRECT GET!!!
            BUT NEWER RETURN NEW INSTANCE!!!
    """
    JSON_AUTODUMP: bool = None      # redefine but CAREFUL - DONT change to TRUE in here!!!!
    JSON_DUMP_DEFAULT__MERGE: bool = True
    JSON_DICT_DEFAULT: dict = dict()  # REDEFINE!  idea is to keep always this value (when clear)!

    _json_dict: dict = None  # was unhide specially for dataclass applying!!! ++never be None!!! always return over clear!!!
    # DONT REDEFINE DEFAULT NONE TO {}!!!!!! ITS NESESSORY!!!
    pass

    # JSON_DICT ENCAPSULATION =========================================================================================
    # NOT WORKING!!!!
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self._json_dict: dict = {}  # was unhide specially for dataclass applying!!! ++never be None!!! always return over clear!!!
    #
    # def __getattr__(self, item):
    #     print(f"{item=}")
    #     return self._json_dict.get(item)
    #
    # def __setattr__(self, key, value):
    #     self._json_dict[key] = value
    #     self.json_dump_try_autodump()

    # JSON_DICT =======================================================================================================
    @property
    def json_dict(self) -> dict:
        """IMPORTANT
        YOU CANT GET ANYTHING LESS THEN IN DEFAULT!!!
        SO PLACE IN THERE ONLY THAT STRUCTURE THAT YOU CANT DELETE!!! only update!!!

        The only one ability is change directly JSON_DICT_DEFAULT!!!
        """
        if self._json_dict is None:
            self.json_clear(autodump=False)     # DONT FORGET USE HERE FALSE!!! OTHEWISE FILE WILL BE CLEARED AS DEFAULT!!!
            if self.filepath:
                self.json_load()
        return self._json_dict

    def json_get_active(self, json_dict: tp.Optional[dict] = None) -> dict:
        """
        used always get final json_dict (from instanse or specified param)
        """
        if json_dict is None:
            result = self.json_dict
        else:
            result = json_dict
        return result

    def json_ensure_applyed(self) -> bool:
        """
        if you need to be sure that you have enough information to get json_dict, and get it!
        so if you already have DICT - ok! else try to load, if loaded - ok! otherwise False!

        spetially created for _ProtocolCreatorThread
        """
        return self.json_check_no_clear() or self.json_load()

    # SET -------------------------------------------------------------------------------------------------------------
    def json_set(self, new_dict: dict) -> bool:
        """
        structure will always keep as JSON_DICT_DEFAULT!
        :param new_dict:
        :return:
        """
        self.json_clear()
        if new_dict is None:
            #use clear!!!
            return False
        self.json_validate(json_dict=new_dict)
        return self.json_merge(new_dict)

    # CLEAR -----------------------------------------------------------------------------------------------------------
    def json_clear(self, autodump: tp.Optional[bool] = None) -> None:
        if self.json_check_no_clear():
            self._json_dict = copy.deepcopy(self.JSON_DICT_DEFAULT)
            self.json_dump_try_autodump(autodump)

    def json_check_clear(self) -> bool:
        if self._json_dict == self.JSON_DICT_DEFAULT:
            return True
        else:
            msg = f"data is NOT clear {self.json_dict=}"
            print(msg)

    def json_check_no_clear(self) -> bool:
        if self._json_dict != self.JSON_DICT_DEFAULT:
            return True
        else:
            msg = f"data is clear {self.json_dict=}"
            print(msg)

    # MERGE -----------------------------------------------------------------------------------------------------------
    def json_merge(self, new_dict: dict, validate: bool = False, autodump: tp.Optional[bool] = None) -> tp.Optional[bool]:   # dont use name *UPDATE! its incorrect!!!
        result_dict = UFU.dicts_merge(
            [
                # self.JSON_DICT_DEFAULT,     #NOT NEED!!!!
                self.json_dict,
                new_dict
            ])
        if validate and not self.json_validate(json_dict=result_dict):
            msg = f"ERROR merge {new_dict=}"
            print(msg)
            return

        self._json_dict = result_dict
        self.json_dump_try_autodump(autodump)
        return True

    def json_merge_into_filepath(self, filepath: tp.Union[str, pathlib.Path], json_dict: tp.Optional[dict] = None) -> tp.Optional[bool]:
        """
        merge json or some dict into some file!
        destination is a filepath so its unbelievable situation merging some dict into self.filepath!
        """
        # INPUT ------------------
        # dont get filepath as active!!!
        json_dict = self.json_get_active(json_dict)

        # WORK ------------------
        json_read = self.json_read(filepath)
        json_merged = UFU.dicts_merge([json_read, json_dict])
        if json_merged:
            return self.json_dump(filepath=filepath, json_dict=json_merged)

    # VALUES ----------------------------------------------------------------------------------------------------------
    def json_value_set(self, key: str, value: tp.Any, autodump: tp.Optional[bool] = None) -> bool:
        """RECOMMENDED USE IT instead direct standard access by brackets []
        use it if you really need JSON_AUTODUMP
        """
        if key not in self.json_dict:
            msg = f"no {key=} in {self.json_dict=}"
            print(msg)

        self.json_dict[key] = value
        self.json_dump_try_autodump(autodump)
        return True

    def json_value_merge(self, key: str, value: dict, autodump: tp.Optional[bool] = None) -> bool:
        """RECOMMENDED USE IT instead direct standard access by update
        use it if you really need JSON_AUTODUMP
        """
        if key not in self.json_dict:
            msg = f"no {key=} in {self.json_dict=}"
            print(msg)

        value_old = self.json_value_get(key)
        if isinstance(value_old, dict) and isinstance(value, dict):
            merged_dict = UFU.dicts_merge([value_old, value])
            return self.json_value_set(key, merged_dict, autodump=autodump)

        else:
            msg = f"cant merge {key=} with {value_old=}/{value=}"
            print(msg)
            return False

    def json_value_get(self, key: str, default: tp.Any = None) -> tp.Any:
        """RECOMMENDED USE IT instead direct standard access by GET()
        """
        return self.json_dict.get(key, default)

    def json_value_get_by_keypath(
            self,
            keypath: tp.Union[str, list],
            json_dict: tp.Optional[dict] = None
    ) -> tp.Optional[tp.Any]:
        # INPUT ------------------------------------------
        json_dict = self.json_get_active(json_dict)
        return UFU.dict_value_get_by_keypath(source=json_dict, keypath=keypath)

    def json_value_get_by_keypath_first_in_dirpath(
            self,
            keypath: tp.Union[str, list],
            dirpath: tp.Union[None, str, pathlib.Path] = None,
            wmask: tp.Union[None, str, list] = None,
            nested: bool = False
    ) -> tp.Any:
        """
        specially created for finding short_pid as key in testplan///*_settings.json

        usually dont need to get filepath! just get the result found value!
        """
        for filepath in self.files_find_in_dirpath(dirpath=dirpath, wmask=wmask, nested=nested):
            json_dict = self.json_read(filepath)
            value = self.json_value_get_by_keypath(keypath=keypath, json_dict=json_dict)
            if value is not None:
                return value

        msg = f"no {keypath=} in any files {wmask=} in {dirpath=}"
        print(msg)

    # OTHER -----------------------------------------------------------------------------------------------------------
    def json_get_serialisable(self, json_dict: tp.Optional[dict] = None) -> dict:
        json_dict = self.json_get_active(json_dict)
        return UFU.dict_make_string_of_values_if_object(json_dict)

    def json_validate(self, json_dict: tp.Optional[dict] = None, etalon: tp.Optional[dict] = None) -> bool:
        json_dict = self.json_get_active(json_dict)
        etalon = etalon if etalon is not None else self.JSON_DICT_DEFAULT
        return UFU.dict_validate_by_etalon(source=json_dict, etalon=etalon)

    # READ/WRITE ======================================================================================================
    def json_read(self, filepath: tp.Union[None, str, pathlib.Path] = None, validate: bool = False) -> tp.Optional[dict]:
        """only read file and return dict
        """
        filepath = self.filepath_get_active(filepath)

        try:
            file_text = filepath.read_text(encoding="utf-8")
        except Exception as exc:
            msg = f"ERROR loading {filepath=}/{exc!r}"
            print(msg)
            return

        try:
            json_dict = json.loads(file_text)
        except Exception as exc:
            msg = f'ERROR decoding Json {filepath=}/{exc!r}'
            print(msg)
            return

        if validate:
            self.json_validate(json_dict=json_dict)

        return json_dict

    def json_load(self, filepath: tp.Union[None, str, pathlib.Path] = None, validate: bool = True) -> tp.Optional[bool]:
        """
        read file and load result into internal attribute
        """
        # CLEAR ALWAYS ON EACH ATTEMPT! even if will not correct! so we cant read old data!
        self.json_clear(autodump=False)

        # DONT SET FILEPATH into INSTANCE!!!! maybe you dont want/need it!!!!

        json_dict = self.json_read(filepath, validate=validate)
        return self.json_set(json_dict)

    def json_load_by_name(self, name: str, dirpath: tp.Union[None, str, pathlib.Path] = None, validate: bool = True) -> tp.Optional[bool]:
        filepath = self.filepath_get_by_name(name=name, dirpath=dirpath, only_if_existed=True)
        if filepath:
            return self.json_load(filepath=filepath, validate=validate)

    def json_dump(
            self,
            filepath: tp.Union[None, str, pathlib.Path] = None,
            json_dict: tp.Optional[dict] = None,
            backup: tp.Optional[bool] = None
    ) -> tp.Optional[bool]:
        # INPUT -----------------------------------------
        filepath = self.filepath_get_active(filepath)
        if not filepath:
            return

        json_dict = self.json_get_active(json_dict)

        # PREPARE -----------------------------------------
        if not self.dirpath_ensure(dirpath=filepath.parent):
            return

        # BACKUP ----------------------------------------
        self.filepath_backup_make(filepath=filepath, backup=backup)

        # WORK -----------------------------------------
        try:
            data_serialisable = self.json_get_serialisable(json_dict)
            data_text = json.dumps(data_serialisable, indent=4, ensure_ascii=False)
        except Exception as exc:
            msg = f'ERROR encoding {json_dict=}/{exc!r}'
            print(msg)
            return

        if not data_text:
            msg = f'data for dump is empty [{data_text=}]'
            print(msg)

        try:
            result = filepath.write_text(data=data_text, encoding='utf-8')
            print(f"{filepath=} dump", result)
            if result:
                return True
        except Exception as exc:
            msg = f'ERROR dumping {filepath=}/{exc!r}'
            print(msg)
            return

    def json_dump_try_autodump(self, dump: tp.Optional[bool] = None) -> tp.Optional[bool]:
        """
        only resolve dump or JSON_AUTODUMP!
        flag Autodump used only if flag dump is None!
        """
        if dump or dump is None and self.JSON_AUTODUMP:
            return self.json_dump()
        else:
            return True


# USAGE EXAMPLES ======================================================================================================
def example__json():
    class Cls(ProcessorJsonDict):
        # ALL KEYS EXPECTED IN DICT!
        attr1: int
        attr2: str

        JSON_DICT_DEFAULT = {
            "attr1": 123,
            "attr2": "hello"
        }

    obj = Cls()
    print(obj.attr1)    # 123


# DATACLASS ===========================================================================================================
# TODO: IT IS NOT WORKING!!!!! NEED BIG TESTS!!!
# TODO: IT IS NOT WORKING!!!!! NEED BIG TESTS!!!
# TODO: IT IS NOT WORKING!!!!! NEED BIG TESTS!!!
# TODO: IT IS NOT WORKING!!!!! NEED BIG TESTS!!!
# TODO: IT IS NOT WORKING!!!!! NEED BIG TESTS!!!
# TODO: IT IS NOT WORKING!!!!! NEED BIG TESTS!!!
# TODO: IT IS NOT WORKING!!!!! NEED BIG TESTS!!!
# TODO: IT IS NOT WORKING!!!!! NEED BIG TESTS!!!
@dataclass
class ProcessorJsonDataclass(ProcessorJsonDict):
    """
    second step of ProcessorJsonDict!
    seems we will use it always!

    SEE EXAMPLES!!!
    """
    def __post_init__(self):
        if self.JSON_DICT_DEFAULT:
            self.__dict__ = copy.deepcopy(self.JSON_DICT_DEFAULT)
        super().__init__()      # used for inheritage

    @property
    def _json_dict(self) -> dict:
        return self.__dict__

    @_json_dict.setter
    def _json_dict(self, value):
        self.__dict__ = value

    def __str__(self):
        result = f"{self.__class__.__name__}"
        result += "("
        result += ", ".join(f"'{key}'={value}" for (key, value) in self.__dict__.items())
        result += ")"
        return result

    __repr__ = __str__


def _example_dataclass_usage_1__by_dict():
    """
    SIMPLE but not so recommended! - couse attr* will not resolve by IDE!!!
    """
    class Cls(ProcessorJsonDataclass):
        JSON_DICT_DEFAULT = {"attr1": 1, "attr2": 2}

        # PREFER NOT TO USE INIT!!!
        def __init__(self):
            super().__init__()
            pass

    test_obj = Cls()
    assert test_obj.attr1 == 1


def _example_dataclass_usage_2__by_attr():
    """
    RECOMMENDED USAGE!
    """
    @dataclass
    class Cls(ProcessorJsonDataclass):
        attr1: int = 1
        attr2: int = 2

        # def __init__(self):
        def __post_init__(self):
            super().__post_init__()
            pass

    test_obj = Cls()
    assert test_obj.attr1 == 1


# =====================================================================================================================
if __name__ == "__main__":
    filepath = CONSTANTS.FILEPATH_TESTPLANS_SETTINGS_DEFAULT
    data = ProcessorJsonDict().json_read(filepath)
    print(data)


# =====================================================================================================================
