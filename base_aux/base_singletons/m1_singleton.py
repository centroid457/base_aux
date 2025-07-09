from typing import *
from threading import Lock

from base_aux.base_values.m3_exceptions import *


# =====================================================================================================================
class Base_SingletonManager:
    """Base (manager) for classes to create singletons.

    GOALS:
    1. threading mutex
    2. prevent and raise incorrect singleton usage

    :ivar _SINGLETONS: collection of created singletons instances.
        when you create several classes, you maybe need to keep access to all of them.
        Used in tests!
        Dont access via instance! recommended using via classname!
    :ivar _MUTEX_SINGLETON: mutex for safe creating items
    :ivar _CLS_BLOCKED: set of classes which can NOT be used as singleton! for correct singletons reason!
        if we instantiate one class and then instantiate one of other class nesting this one -
        before you did not understand your architecture mistake, but now it will rase!
    :ivar _CLS_USED: set of classes which already used as singleton!
    :ivar __INSTANCE: actual singleton instance for current class, here it is just for showing exact usage and correct visualising in IDE!

    Bytheway, you can directly access to all this collections from any your singleton instance or even class! its basic!
    """
    _SINGLETONS: list[Self] = []
    _CLS_BLOCKED: set[Any] = set()
    _CLS_USED: set[Any] = set()

    _MUTEX_SINGLETON: Lock = Lock()  # keep this special name! dont use just MUTEX! (need uniq! in case of exists in source!)
    __INSTANCE: Any     # just to define usage!

    @classmethod
    def _check_correct_instantiating_singletons(cls, cls_obj: Any) -> Optional[NoReturn]:
        """realise checking right instantiating singletons in project

        :param cls_obj: the original class object!
            (this is very important using it here! using access to direct CLS is incorrect for meta!)
        """
        # check blocked --------------------------------------------
        if cls_obj in cls._CLS_BLOCKED:
            msg = f"{cls_obj.__name__=} WAS BLOCKED before by creating singleton in upper nesting level"
            for cls_blocked in cls._CLS_BLOCKED:
                msg += f"\n\t{cls_blocked.__name__=}"
            raise Exx__NestingLevels(msg)

        cls._CLS_USED.add(cls_obj)

        for cls_mro in cls_obj.__mro__[1:]:
            if cls_mro in cls._CLS_USED:
                msg = f"{cls_obj.__name__=} WAS USED before by creating singleton in less nesting level"
                for cls_used in cls._CLS_USED:
                    msg += f"\n\t{cls_used.__name__=}"
                raise Exx__NestingLevels(msg)
            cls._CLS_BLOCKED.add(cls_mro)

    @classmethod
    def _drop_all(cls) -> None:
        """delete all singletons!

        created just for correct testing
        """
        while cls._SINGLETONS:
            try:
                delattr(cls._SINGLETONS.pop(), "__INSTANCE")
            except:
                pass

    @classmethod
    def instance__check_created_and_enshure_it(cls, cls_obj: Any) -> bool:
        """check if instance not created yet and create it

        :returns: result of checking was it exists or not
        """
        result = hasattr(cls_obj, '__INSTANCE')
        if not result:
            setattr(cls_obj, '__INSTANCE', None)
        return result

    @classmethod
    def instance__collect(cls, cls_obj: Any) -> None:
        """collect all singleton base_types from all classes

        dont know why but it is not working! both in meta and noMeta
        """
        if cls_obj.__INSTANCE not in cls_obj._SINGLETONS:
            cls_obj._SINGLETONS.append(cls_obj.__INSTANCE)

    # @classmethod
    # def _instance_del(cls) -> None:
    #     """Delete class instance!
    #
    #     expected using for tests!
    #     """
    #     try:
    #         delattr(cls, "__INSTANCE")
    #     except:
    #         pass


# =====================================================================================================================
class Meta_SingletonCall(Base_SingletonManager, type):
    """metaclass which create the singletons by Call method

    USAGE
    -----
        class MySingleton(metaclass=_SingletonMeta):
            pass
    """
    def __call__(cls, *args, **kwargs):
        cls._check_correct_instantiating_singletons(cls)     # dont place into mutex!

        # -----------------------------------------
        cls._MUTEX_SINGLETON.acquire()

        if not cls.instance__check_created_and_enshure_it(cls):
            cls.__INSTANCE = super().__call__(*args, **kwargs)

            # singleton_group_class = cls.__mro__[1]
            # if not hasattr(singleton_group_class, '_INSTANCES'):
            #     setattr(singleton_group_class, '_INSTANCES', [])
            #     singleton_group_class._INSTANCES = []
            # singleton_group_class._INSTANCES.append(cls.__INSTANCE)

        # ------------------------
        # cls.instance__collect(cls)    # here it is not working!
        if cls.__INSTANCE not in cls._SINGLETONS:
            cls._SINGLETONS.append(cls.__INSTANCE)
        # ------------------------

        cls._MUTEX_SINGLETON.release()
        # -----------------------------------------
        return cls.__INSTANCE


class Singleton_CallMeta(metaclass=Meta_SingletonCall):
    """same as original metaclass Meta_SingletonCall but just an another variant of using it by simple nesting
    (without direct using metaclass parameter).

    USAGE
    -----
    BEST PRACTICE
    Use only one level nesting!
        class Victim1(Singleton):
            pass
        class Victim2(Singleton):
            pass
        class VictimINCORRECT(Victim1):
            pass
    """


# =====================================================================================================================
class Singleton_New(Base_SingletonManager):
    """Singleton manager, creating them by using NEW method without metaclassing
    else one variant after SingletonWMetaCall, in case of metaclass is not acceptable.

    USEFUL CASES:
    1. you need to use some metaclass (cant set two metaclasses).
    2. (main difference) always reinit instance on instantiating! (would be called __init__(*args/kwargs)!
        if blank init - will be the same as SingletonWMetaCall
    """
    def __new__(cls, *args, **kwargs):
        cls._check_correct_instantiating_singletons(cls)     # dont place into mutex!

        # -----------------------------------------
        cls._MUTEX_SINGLETON.acquire()
        if not cls.instance__check_created_and_enshure_it(cls):
            cls.__INSTANCE = super().__new__(cls)

        # ------------------------
        # cls.instance__collect(cls)    # here it is not working!
        if cls.__INSTANCE not in cls._SINGLETONS:
            cls._SINGLETONS.append(cls.__INSTANCE)
        # ------------------------

        cls._MUTEX_SINGLETON.release()
        # -----------------------------------------
        return cls.__INSTANCE


# =====================================================================================================================
class Multiton:
    # todo: create!!!
    pass


# =====================================================================================================================
