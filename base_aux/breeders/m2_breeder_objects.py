from typing import *
from enum import Enum, auto

from base_aux.base_exceptions.m1_exceptions import *


# =====================================================================================================================
TYPE__BREED_RESULT__ITEM = Union[Any, Exception]
TYPE__BREED_RESULT__GROUP = Union[
    TYPE__BREED_RESULT__ITEM,        # SINGLE variant
    list[TYPE__BREED_RESULT__ITEM]   # LIST variant
]
TYPE__BREED_RESULT__GROUPS = dict[str, TYPE__BREED_RESULT__GROUP]


# =====================================================================================================================
class BreederObjectList_GroupType(Enum):
    SINGLE = auto()
    LIST = auto()
    NOT_EXISTS = auto()


# =====================================================================================================================
class BreederObjectList:
    """
    class which keep all aux_types in one place!
    useful for multyObject systems.

    If you need just one object_instance for all duts - use direct attribute,
    else use LIST__*NAME* and dont forget to create annotation for direct Indexed item access!

    so you could
    - pass just one instance into all other classes!
    - check all devices for PRESENT (or else) in one place!
    - init all and check correctness for all

    AFTER GENERATING OBJECTS - ACCESS TO OBJECTS LIST USED OVER THE CLASS!!!
        OBJS_CLS = BreederObjectList
        OBJS = OBJS_CLS()
        devs = OBJS_CLS.LIST__DEV
    """
    # SETTINGS ----------------------
    COUNT: int = 1

    # usage EXAMPLES ------------------------------------------------------
    # CLS_LIST__DUT: type[DutBase] = DutBase
    # LIST__DUT: list[DutBase]
    # DUT: DutBase

    # CLS_SINGLE__ATC: Callable[..., DeviceBase]
    # ATC: DeviceBase

    # AUX ----------------------------------------------------------
    # definitions -----
    _STARTSWITH__DEFINE__CLS_LIST: str = "CLS_LIST__"
    _STARTSWITH__DEFINE__CLS_SINGLE: str = "CLS_SINGLE__"

    # access ----------
    _STARTSWITH__ACCESS__OBJECT_LIST__IN_BREEDER: str = "LIST__"
    _STARTSWITH__ACCESS__OBJECT_LIST__IN_SOURCE: str = "INSTS"
    _STARTSWITH__ACCESS__BREEDER_IN__SOURCE: str = "BREEDER"    # SINGLE:type[Breeder] // LIST:Breeder

    # AUX --------
    __groups__are_generated: bool = False

    # instance ---
    INDEX: int | None = None    # index used only in OBJECT INSTANCE

    def __init__(self, index: int, *args, **kwargs):
        """
        init only when you need to do access to exact items!
        """
        self.INDEX = index      # need first!
        super().__init__(*args, **kwargs)
        # self.generate__objects()

    @classmethod
    def groups_check__generated(cls) -> bool | None:
        return cls.__groups__are_generated

    # -----------------------------------------------------------------------------------------------------------------
    @classmethod
    def generate__objects(cls, force: bool | None = None) -> None:
        """exact and only one method to Gen all aux_types - dont forget to call it!
        """
        if force:
            cls.__groups__are_generated = False

        if cls.__groups__are_generated:
            return

        # WORK --------------------------------------
        for attr_name in dir(cls):
            # LIST --------------------------------------
            if attr_name.startswith(cls._STARTSWITH__DEFINE__CLS_LIST):
                group_name = attr_name.removeprefix(cls._STARTSWITH__DEFINE__CLS_LIST)
                obj_cls = getattr(cls, attr_name)

                obj_list__name = f"{cls._STARTSWITH__ACCESS__OBJECT_LIST__IN_BREEDER}{group_name}"
                obj_list__value = []
                for index in range(cls.COUNT):
                    try:
                        obj_instance = obj_cls(index)
                        setattr(obj_instance, cls._STARTSWITH__ACCESS__BREEDER_IN__SOURCE, cls(index=index))
                    except Exception as exx:
                        obj_instance = exx
                    obj_list__value.append(obj_instance)


                # apply GROUP to class -------
                setattr(cls, obj_list__name, obj_list__value)
                setattr(obj_cls, cls._STARTSWITH__ACCESS__OBJECT_LIST__IN_SOURCE, obj_list__value)

            # SINGLE --------------------------------------
            if attr_name.startswith(cls._STARTSWITH__DEFINE__CLS_SINGLE):
                group_name = attr_name.removeprefix(cls._STARTSWITH__DEFINE__CLS_SINGLE)
                obj_cls = getattr(cls, attr_name)
                try:
                    obj_instance = obj_cls()
                except Exception as exx:
                    obj_instance = exx
                # apply -------
                setattr(cls, group_name, obj_instance)
                setattr(obj_cls, cls._STARTSWITH__ACCESS__OBJECT_LIST__IN_SOURCE, obj_instance)
                setattr(obj_cls, cls._STARTSWITH__ACCESS__BREEDER_IN__SOURCE, cls)

        cls.__groups__are_generated = True

    # -----------------------------------------------------------------------------------------------------------------
    @classmethod
    def groups__get_names(cls) -> set[str]:
        result = set()
        for attr_name in dir(cls):
            if attr_name.startswith(cls._STARTSWITH__DEFINE__CLS_LIST):
                group_name = attr_name.removeprefix(cls._STARTSWITH__DEFINE__CLS_LIST)
                result.update([group_name, ])
            if attr_name.startswith(cls._STARTSWITH__DEFINE__CLS_SINGLE):
                group_name = attr_name.removeprefix(cls._STARTSWITH__DEFINE__CLS_SINGLE)
                result.update([group_name, ])

        return result

    # -----------------------------------------------------------------------------------------------------------------
    @classmethod
    def groups_count__generated(cls) -> int | None:
        """
        work only after called generate__objects(),
        so if you wasnot call generate__objects it will return None!
        """
        if cls.__groups__are_generated:
            return len(cls.groups__get_names())

    # GROUP -----------------------------------------------------------------------------------------------------------
    @classmethod
    def group_get__type(cls, name: str) -> BreederObjectList_GroupType:
        if f"{cls._STARTSWITH__DEFINE__CLS_SINGLE}{name}" in dir(cls):
            return BreederObjectList_GroupType.SINGLE

        if f"{cls._STARTSWITH__DEFINE__CLS_LIST}{name}" in dir(cls):
            return BreederObjectList_GroupType.LIST

        return BreederObjectList_GroupType.NOT_EXISTS

    @classmethod
    def group_check__exists(cls, name: str) -> bool:
        return cls.group_get__type(name) != BreederObjectList_GroupType.NOT_EXISTS

    @classmethod
    def group_get__cls(cls, name: str) -> Any | None:
        group_type = cls.group_get__type(name)

        if group_type == BreederObjectList_GroupType.SINGLE:
            attr = f"{cls._STARTSWITH__DEFINE__CLS_SINGLE}{name}"
            return getattr(cls, attr)

        if group_type == BreederObjectList_GroupType.LIST:
            attr = f"{cls._STARTSWITH__DEFINE__CLS_LIST}{name}"
            return getattr(cls, attr)

    @classmethod
    def group_get__insts(cls, name: str) -> Union[None, Any, list[Any]]:
        if cls.group_check__exists(name) and cls.__groups__are_generated:
            group_cls = cls.group_get__cls(name)
            result = getattr(group_cls, cls._STARTSWITH__ACCESS__OBJECT_LIST__IN_SOURCE)
            return result

    @classmethod
    def group_call__(cls, meth: str, group: str | None = None, args: list | None = None, kwargs: dict | None = None) -> Union[NoReturn, TYPE__BREED_RESULT__GROUP, TYPE__BREED_RESULT__GROUPS]:
        """
        call one method on exact group (every object in group) or all groups (every object in all groups).
        created specially for call connect/disconnect for devices in TP.

        :param meth:
        :param group:

        :param args:
        :param kwargs:
        :return:
            RAISE only if passed group and group is not exists! or groups are not generated
        """
        if not cls.__groups__are_generated:
            raise Exx__BreederObjectList_GroupsNotGenerated()

        args = args or ()
        kwargs = kwargs or {}

        # CALL ON ALL GROUPS -------------------------------------------------
        if group is None:
            results = {}
            for group_name in cls.groups__get_names():
                results.update({group_name: cls.group_call__(meth, group_name, args, kwargs)})
            return results

        # if group is not exists ---------------------------------------------
        if not cls.group_check__exists(group):
            raise Exx__BreederObjectList_GroupNotExists(group)

        # EXACT ONE GROUP ----------------------------------------------------
        group_objs = cls.group_get__insts(group)

        if isinstance(group_objs, list):
            results = []
            for obj in group_objs:
                try:
                    obj_meth = getattr(obj, meth)
                    obj_result = obj_meth(*args, **kwargs)
                except Exception as exx:
                    obj_result = exx
                results.append(obj_result)
        else:
            obj = group_objs
            try:
                obj_meth = getattr(obj, meth)
                obj_result = obj_meth(*args, **kwargs)
            except Exception as exx:
                obj_result = exx
            results = obj_result

        return results

    # -----------------------------------------------------------------------------------------------------------------
    def __getattr__(self, item: str) -> Union[None, Any, NoReturn]:
        """
        :param item:
        :return: existed OBJECT from LIST or SINGLE!!!
        """
        if self.INDEX is None:
            return

        # ACCESS TO OBJECT ----------------------------
        group_insts = self.group_get__insts(item)
        if group_insts is not None:
            if isinstance(group_insts, list):
                inst = group_insts[self.INDEX]
            else:
                inst = group_insts
            return inst

        # FINAL not found -----------------------------
        msg = f"{item=}/{self.INDEX=}"
        print(msg)
        raise Exx__BreederObjectList_GroupNotExists(msg)


# =====================================================================================================================
