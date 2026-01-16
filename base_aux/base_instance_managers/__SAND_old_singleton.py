# =====================================================================================================================
# STARICHENKO UNIVERSAL IMPORT
import sys
sys.path.append("..")  # Adds higher directory to python modules path.

import time
import pathlib
import copy
import threading


# SINGLETON ===========================================================================================================
# 1=NEW======= USE!
class Meta_Singleton(type):   # starichenko
    def __call__(cls, *args, **kwargs):
        if not hasattr(cls, '__INSTANCE'):
            # FIRST VARIANT -------------------- cant create independent singletones!
            # if not hasattr(cls, 'INSTANCE'):
            #     cls.INSTANCE = super().__call__(*args, **kwargs)
            # return cls.INSTANCE

            # SECOND VARIANT --------------------
            # you need create attribute otherwise sometimes (DWDM) infinity resursive!!!
            # cls.__INSTANCE = None   # this is dont work!!!
            setattr(cls, '__INSTANCE', None)    # NEED THIS!!!

            cls.__INSTANCE = super().__call__(*args, **kwargs)

        return cls.__INSTANCE


# 2=OLD======= DONT USE!!!!
class _Singleton:   # starichenko
    """
    Create singleton class by inheriting this one!
    DONT CRIATE OBJECT DIRECT from this class!!!

    IMPORTANT STEPS:
    1=inherit your class from this one!
    2=in inheritance order place this class to last place!!!
    3=dont forget decorating __INIT__ by decorator_singleton_for_class_method_init!!!
        otherwise init will be called and all instances (links) will be owerinited to init state!!!

    see tests for example!
    """
    # TODO in future you can create single CLASS_DECORATOR! (if possible)
    # _INSTANCE = None              # moved to child class!!!
    # _INSTANCE_INITED_FLAG = None  # moved to child class!!!

    def __new__(cls, *args, **kwargs):
        # print(f"{args=}{kwargs=}")
        child_class = cls.__mro__[0]

        # you need to use inheritance from this class! Not direct!
        if __class__ == cls:
            msg = f"""
                    this class must not run directly!!!
                    use at least simple sample (its necessary and enough!)
                    class MyNewClassSingleton({cls.__name__}):
                        pass
            """
            raise Exception(msg)

        if not hasattr(child_class, "_INSTANCE") or child_class._INSTANCE is None:
            child_class._INSTANCE = super().__new__(cls)
        return child_class._INSTANCE


def _decorator_singleton_for_class_method_init(_func_link):  # starichenko
    def _wrapper_for_class_method(self, *args, **kwargs):
        # print(f"decorating[{self.__class__.__name__}.{_func_link.__name__}()]")
        if not hasattr(self.__class__, "_INSTANCE_INITED_FLAG") or not self.__class__._INSTANCE_INITED_FLAG:
            self.__class__._INSTANCE_INITED_FLAG = True
            return _func_link(self, *args, **kwargs)
        else:
            for class_i in self.__class__.__mro__:
                # in case of reinicialization _DictDotAttrAccess2_Singleton with new params!
                if class_i.__name__ == "_DictDotAttrAccess2_Singleton":
                    return class_i.__init__(self, *args, **kwargs)
            return None
    return _wrapper_for_class_method


# =====================================================================================================================
class _DictDotAttrAccess2_Singleton(_Singleton):    # starichenko
    """
    ***i tried create nonSingleton! but get fail!

    IMPORTANT:
        HERE INSIDE:
            DONT TOUCH/CHANGE ANY LINES WITHOUT IMMEDIATE CHECK BY TESTING!!! very easy to break it!!!

    ------------------------------------
    singleton alternative complicated variant for standard dict!

    differences from simple DICT
    0. all standard methods are usefull! (if not dont forget to add with tests!!)
    1. Singleton
    1. exists some another custom usefull methods!
    2. dotted attribute access! (only for first level)
    3. work with json file (can autosave dict)

    4. safe for input source dict!!! no inline changes!

    ------------------------------------
    USAGE
    create SINGLETONS:
        1. inherit this class (even if you need only one DictSingleton)!
            class Cls1(_DictDotAttrAccess2_Singleton):
                pass
            class Cls2(_DictDotAttrAccess2_Singleton):
                pass

        2. DONT REINHERIT ELSE ONE new your classes!!!
            class Cls3(Cls2):   # cause incorrect work! use only as shown above!!!
                pass

    add new ATTRIBUTES
        3. ALL ATTRIBUTES MUST BE FIRST INITED AS CLASS ATTR!!! only after this step you can use it by SELF reference!!!
            class Cls1(_DictDotAttrAccess2_Singleton):
                hello = None
                def hello_set(self, val):
                    self.hello = val

    add INIT
        4. if need init - DONT FORGET START super().__init__(*args, **kwargs) DEFINITLY AT FIRTS LINE!!!
        BUT i think it is not recommended to use INIT!!! try not use!
        but maybe you need some some reload from file?

            class Cls1(_DictDotAttrAccess2_Singleton):
                hello = 1
                def __init__(self, *args, **kwargs):
                    super().__init__(*args, **kwargs)
                    self.hello = 111

        5. if you need singleton init use @_decorator_singleton_for_class_method_init
        if no (need create yours attr on init state - dont use it BUT IT IS) dont use! but dict data will stay singleton!

    add new METHODS
        6. add it as usual!

    -------------------------------------
    РАБОТА С АТТРИБУТАМИ обьекта/класса
    0. теперь можно обращаться как к классовым атрибутам так и к обьектовым!
    - все равно будет изменяться и выдаваться именно классовый!!!
    1. если класс имеет атрибут - то любое обращение идет по нему!
    2. если класс не имеет атрибут, то любое обращение к его имени подразумевает обращение к словарю _DICT!
    - тоесть если значения там нет - то читается None, а при записи создается там!

    fully created by starichenko
    """

    # TODO: create minimal or even stable keys list for DICT ??????
    # RECOMMENDED ALL CLASS ATTR NAMES KEEP UPPERCASE!
    # AND DONT HIDE TO [__*] - will not work on inheritance!
    # _DICT = {}                # moved to child class!!!
    # _FILEPATH = None          # moved to child class!!!
    # _AUTO_DUMP_FLAG = True    # moved to child class!!!

    # get = dict.get    # dont work! dont know why!

    # DONT DECORATE BY SINGLETON!!! useful to keep it opened!
    def __init__(self, data=None, filepath=None, auto_dump_flag=None):     # CAREFULL! apply _DICT only if you want to ovewrite all instances!
        """

        ANY PARAMS REPLACE IN SINGLETON ONLY IF PASSED IN INIT!
        if you want to clear some of them - use special methods! or pass any value except NONE!

        :param dict:
        :param filepath: if you have it - dict will be automatic dumped on any data changed!
        :param auto_dump_flag:
        """
        super().__init__()
        self.__init_if_not_singleton_child_class_base_attributes()

        if isinstance(data, dict):
            self.replace_dict(data)
        elif data is None:
            pass
        else:
            msg = f"incorrect input [{data=}]"
            print(msg)

        if filepath is not None:
            self.filepath_change(filepath)

        if auto_dump_flag is not None:
            self.auto_dump_flag_change(auto_dump_flag)

    # BASE SINGLETON PREPARE ==========================================================================================
    def __init_if_not_singleton_child_class_base_attributes(self):
        """
        create base attr in child class
        :return:
        """
        if not hasattr(self.__class__, "_DICT"):
            self.__class__._DICT = {}

        if not hasattr(self.__class__, "_FILEPATH"):
            self.__class__._FILEPATH = None

        if not hasattr(self.__class__, "_AUTO_DUMP_FLAG"):
            self.__class__._AUTO_DUMP_FLAG = True

    # ATTRIBUTES WORK ======================
    def get_dict(self, get_safe_copy=True):
        """
        recommended use exact get_safe_copy!!! else you will have direct access to base DICT!!!!
        :param get_safe_copy:
        :return:
        """
        if get_safe_copy:
            return copy.deepcopy(self._DICT)
        else:
            return self._DICT

    def __getattr__(self, item):
        if item in dir(self):
            return getattr(self.__class__, item)
        else:
            return self.__class__._DICT.get(item)

    def __setattr__(self, key, value):
        if key in dir(self):
            # print()
            # print(self.__class__)
            setattr(self.__class__, key, value)
        else:
            self.update({key: value})

    def __delattr__(self, item):
        if item in dir(self):
            delattr(self.__class__, item)
        else:
            self.delete(item)

    # MAGIC STAFF ======================
    def __bool__(self):
        return bool(self._DICT)

    def __str__(self):
        return str(self._DICT)

    def __repr__(self):
        return repr(self._DICT)

    def __len__(self):
        return len(self._DICT)

    def __getitem__(self, key):
        return self._DICT.get(key)

    def __setitem__(self, key, value):
        self.update({key: value})

    def __delitem__(self, key):
        self.delete(key)

    def __iter__(self):
        return iter(self._DICT)

    def __eq__(self, other):
        return self._DICT == other

    def __ne__(self, other):
        return self._DICT != other

    # have NOT IN MAGIC staff ======================
    def get(self, key, _default=None):      # DONT RENAME!!! it uses in dict!!!
        return self._DICT.get(key, _default)

    def items(self):
        return self._DICT.items()

    def keys(self):
        return self._DICT.keys()

    def values(self):
        return self._DICT.values()

    def clear(self):
        self.delete()

    def update(self, new_dict={}):          # LINK all CHANGES to here!!!!
        self._DICT.update(new_dict)
        self.file_dump_if_auto()

    # CUSTOM (have not in DICT) ======================
    def set(self, key, value=None):
        self.update({key: value})

    def delete(self, key=None):             # LINK all DELETES to here!!!!
        if key is None:
            self._DICT.clear()
        else:
            try:
                del self._DICT[key]
            except:
                pass
        self.file_dump_if_auto()

    def check_empty(self):
        return self._DICT == {}

    def replace_dict(self, new_dict={}):    # LINK all REPLACES to here!!!!
        """
        fully replace original dict!
        you can use simply reinit new instance with this dict!

        IMPORTANT: DONT CHANGE TO SIMPLY
                self._DICT = new_dict
        IT WILL BREAK ALL WORKING!!!

        :param new_dict:
        :return:
        """
        self.clear()
        self._DICT.update(new_dict)
        self.file_dump_if_auto()

    # filepath ------------------------------------------------------------------------------------------------------
    def auto_dump_flag_change(self, auto_dump_flag=None):
        self._AUTO_DUMP_FLAG = auto_dump_flag

    def filepath_change(self, filepath=None):
        if filepath:
            self._FILEPATH = pathlib.Path(filepath)
        else:
            self._FILEPATH = None

    def file_dump_if_auto(self):
        # print(111)
        if self._AUTO_DUMP_FLAG:
            self.file_bump()

    def file_bump(self, filepath=None):
        if filepath:
            filepath = pathlib.Path(filepath)
        else:
            filepath = self._FILEPATH

        if filepath:
            return ProcessorJsonDict().json_dump(filepath=filepath, json_dict=self.get_dict())

    def file_load(self, filepath=None):
        if filepath:
            filepath = pathlib.Path(filepath)
        else:
            filepath = self._FILEPATH

        if filepath:
            data = ProcessorJsonDict().json_read(filepath)
            self.replace_dict(data)
            return data


# TESTS ===============================================================================================================
def test__Singleton__decorator_singleton_for_class_method_init():
    test_obj_link1 = _Singleton
    test_obj_link2 = _decorator_singleton_for_class_method_init

    class Cls1(test_obj_link1):
        cls_atr = 1
        @test_obj_link2
        def __init__(self, hello):
            self.atr = hello

    class Cls2(test_obj_link1):
        cls_atr = 2
        @test_obj_link2
        def __init__(self, hello):
            self.atr = hello

    def start_in_thread():
        obj_thread = Cls1(1)
        for i in range(10):
            print(f"{obj_thread.atr=}")
            time.sleep(0.5)

    thread = threading.Thread(target=start_in_thread, daemon=1)
    thread.start()
    time.sleep(1)

    print()
    obj1 = Cls1(1)
    print(F"{obj1.atr=}")
    assert obj1.atr == 1

    obj1.atr = 2
    print(F"{obj1.atr=}")
    assert obj1.atr == 2

    # 2=check not initing new instances!
    print()
    time.sleep(1)
    obj2 = Cls1(1)
    print(F"{obj1.atr=}")
    print(F"{obj2.atr=}")
    assert obj1.atr == 2
    assert obj2.atr == 2
    print()

    time.sleep(2)

    # check TWO CLASSES inherited from one _Singleton!!!
    # 1=only self attr!
    obj3 = Cls2(3)
    print(F"{obj1.atr=}")
    print(F"{obj3.atr=}")
    assert obj1.atr == 2
    assert obj3.atr == 3

    # 2=class attr - ОТВЯЗАННЫЙ!!! тоесть неизменяемый внутри!!!
    print()
    print()
    print(F"{Cls1().cls_atr=}")
    assert Cls1().cls_atr == 1
    Cls1().cls_atr = 111
    print(F"{Cls1().cls_atr=}")
    assert Cls1().cls_atr == 111

    print()
    print(F"{Cls2().cls_atr=}")
    assert Cls2().cls_atr == 2
    Cls2().cls_atr = 222
    print(F"{Cls2().cls_atr=}")
    assert Cls2().cls_atr == 222

    print(F"{Cls1().cls_atr=}")
    assert Cls1().cls_atr == 111

    Cls1().atr = 1
    assert Cls1().atr == 1
    assert Cls2().atr == 3

    # 3=class attr - ИЗМЕНЯЕМЫЙ внутри!!!


def test__DictDotAttrAccess2_Singleton():  # starichenko
    # test_obj_link = UFU._DictDotAttrAccess2_Singleton
    class test_obj_link(_DictDotAttrAccess2_Singleton):
        pass

    # SINGLETON -----------------------------------------------------------------------
    test_obj_link({1: 1})
    assert len(test_obj_link()) == 1  # SINGLETON
    assert len(test_obj_link({})) == 0  # SINGLETON

    obj1 = test_obj_link({1: 1})
    obj2 = test_obj_link({2: 2})
    assert obj1 == {2: 2}
    obj2[2] = 222
    assert obj1 == {2: 222}

    # INHERIT --------------------------------------------------------------------------
    # class Cls1(copy.copy(UFU._DictDotAttrAccess2_Singleton)):      # не помогло!!!
    class Cls1(_DictDotAttrAccess2_Singleton):
        hello = None
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.hello = 1
    class Cls2(_DictDotAttrAccess2_Singleton):
        hello = None
        @_decorator_singleton_for_class_method_init
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.hello = 2

    # several indepandent classes -----------------------------------------------
    assert test_obj_link({1:1}) == {1:1}
    assert Cls1() == {}                     # indepandent cls 1
    Cls1().attr = 111
    assert Cls1() == {"attr": 111}
    assert Cls2() != {"attr": 111}          # indepandent cls 2

    assert Cls1({2: 2}) == Cls2({2: 2})
    assert Cls1({}) != Cls2({3:3})

    # INITs
    assert Cls1({1:1}).hello == 1
    Cls1().hello = 111
    assert Cls1().hello == 1  # no singleton init

    assert Cls2({2:2}).hello == 2
    Cls2().hello = 222
    assert Cls2().hello == 222     # singleton init

    # ATTRIBUTES -----------------------------------------------------------------------
    # attr DICT
    assert test_obj_link({"atr": 1}) == {"atr": 1}            # .atr
    assert test_obj_link().atr == 1
    test_obj_link().atr = 111
    assert test_obj_link().atr == 111
    del test_obj_link().atr                # del.attr
    assert test_obj_link().atr == None
    del test_obj_link().atr                # del.attr not exists

    # attr OBJECT
    assert Cls1({1:1}).hello == 1
    assert Cls2({}).hello == 222
    assert Cls1({}) == {}
    assert Cls2({}) == {}

    # attr CLASS
    assert test_obj_link({})._DICT == {}
    test_obj_link().atr = 111
    assert test_obj_link()._DICT == {"atr": 111}

    assert test_obj_link._AUTO_DUMP_FLAG == True
    assert test_obj_link()._AUTO_DUMP_FLAG == True
    test_obj_link()._AUTO_DUMP_FLAG = False
    assert test_obj_link._AUTO_DUMP_FLAG == False
    assert test_obj_link()._AUTO_DUMP_FLAG == False
    assert test_obj_link()._DICT == {"atr": 111}

    assert test_obj_link({1:1}, auto_dump_flag=False)._AUTO_DUMP_FLAG == False
    assert test_obj_link(auto_dump_flag=True)._AUTO_DUMP_FLAG == True
    assert test_obj_link()._AUTO_DUMP_FLAG == True
    assert test_obj_link()._DICT == {1: 1}

    # REPRESENTS -----------------------------------------------------------------------
    assert str(test_obj_link({})) == "{}"     # STR
    assert str(test_obj_link({1: 1})) == "{1: 1}"

    assert bool(test_obj_link({})) == False           # BOOL
    assert bool(test_obj_link({1:1})) == True

    # ITER ----------------------------------------------------------------------------
    assert len(test_obj_link({1: 1})) == 1                # LEN
    assert list(test_obj_link({1: 1})) == [1]             # LIST

    new_list = []
    for key in test_obj_link():  # ITER
        new_list.append(key)
    assert list(test_obj_link()) == new_list

    assert (1 in test_obj_link({1: 1})) == True   # IN
    assert (111 in test_obj_link({1: 1})) == False   # IN

    new_dict = {}
    for key, value in test_obj_link().items():                      # ITEMS
        new_dict.update({key: value})
    assert list(test_obj_link().keys()) == list({1:1}.keys())       # keys
    assert list(test_obj_link().values()) == list({1:1}.values())   # values

    assert (test_obj_link() == new_dict) == True    # EQ
    assert (test_obj_link() != new_dict) == False   # NE

    # GET/SET/DEL --------------------------------------------------------------------------
    test_obj_link({}).set(11, 11)
    assert test_obj_link() == {11: 11}              # set(key, value)

    assert test_obj_link({1: 1}).get(1) == 1              # get()
    assert test_obj_link().get(1, 999) == 1         # get() default
    assert test_obj_link().get(2, 999) == 999       # get() default

    assert test_obj_link()[1] == 1                  # get[]
    assert test_obj_link()[2] == None               # get[] default

    test_obj_link()[1] = 11
    assert test_obj_link()[1] == 11         # set[]

    del test_obj_link()[1]
    del test_obj_link()[1]                  # del[] not exists
    assert test_obj_link()[1] == None       # del[]

    # SAFE SOURCE DICT ACCESS ---------------------------------------------------------
    temp_dir = {1:1}
    test_obj_link(temp_dir)
    assert test_obj_link()[1] == 1      # SAFE SOURCE DICT
    del test_obj_link()[1]
    assert test_obj_link()[1] == None
    assert temp_dir == {1:1}

    temp_dir = test_obj_link({})._DICT
    assert temp_dir == {}
    assert test_obj_link() == {}
    test_obj_link()[1] = 1
    assert temp_dir == {1:1}
    temp_dir[1] = 111
    assert test_obj_link() == {1:111}        # NOT SAFE ACCESS!

    temp_dir = test_obj_link({}).get_dict(get_safe_copy=False)
    assert temp_dir == {}
    assert test_obj_link() == {}
    test_obj_link()[1] = 1
    assert temp_dir == {1:1}
    temp_dir[1] = 111
    assert test_obj_link() == {1:111}        # NOT SAFE ACCESS!

    temp_dir = test_obj_link({}).get_dict(get_safe_copy=True)
    assert temp_dir == {}
    assert test_obj_link() == {}
    test_obj_link()[1] = 1
    assert temp_dir == {}
    temp_dir[1] = 111
    assert test_obj_link() == {1:1}        # SAFE ACCESS!

    # FULL DICT ------------------------------------------------------------------------
    assert test_obj_link().get_dict() == {1:1}         # get_dict
    # assert dict(test_obj_link()) == {1:1}         # dict()  --------НЕ РАБОТАЕТ!!! и не особо важно!

    assert test_obj_link().check_empty() == False  # check_empty

    test_obj_link({1:1}).clear()
    assert test_obj_link().check_empty() == True    # clear

    test_obj_link().update({1:1, 2:2})
    assert test_obj_link() == {1:1, 2:2}    # UPDATE
    test_obj_link().update({1:111})
    assert test_obj_link() == {1:111, 2:2}

    test_obj_link({1:1}).replace_dict({11: 11})
    assert test_obj_link() == {11:11}         # replace_dict

    # FILE ------------------------------------------------------------------------
    assert test_obj_link({1:1}, auto_dump_flag=True) == {1:1}
    assert test_obj_link()._AUTO_DUMP_FLAG == True
    test_obj_link().auto_dump_flag_change(False)
    assert test_obj_link()._AUTO_DUMP_FLAG == False     # auto_dump_flag_change

    test_obj_link().filepath_change("hello.json")
    assert test_obj_link()._FILEPATH == pathlib.Path("hello.json")     # filepath_change

    test_obj_link({1:1}).file_bump("hello.json")


# =====================================================================================================================
