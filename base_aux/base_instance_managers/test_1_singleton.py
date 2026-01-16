from typing import *
import pytest
import time
import threading
import abc

from base_aux.base_instance_managers.m1_singleton import *


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="Victim",
    argvalues=[
        Singleton_CallMeta,
        Singleton_New
    ]
)
def test__no_args(Victim):
    class Victim1(Victim):
        attr = 1

    class Victim2(Victim):
        attr = 2

    Victim._drop_all()
    assert Victim._SINGLETONS == []

    assert Victim1().attr == 1
    Victim1().attr = 11
    assert Victim1().attr == 11
    assert Victim._SINGLETONS == [Victim1(), ]
    assert Victim1._SINGLETONS == [Victim1(), ]
    try:
        assert Victim1()._SINGLETONS == [Victim1(), ]
    except:
        assert Victim == Singleton_CallMeta
    else:
        assert Victim == Singleton_New

    assert Victim2().attr == 2
    Victim2().attr = 22
    assert Victim2().attr == 22
    assert Victim._SINGLETONS == [Victim1(), Victim2()]
    assert Victim2._SINGLETONS == [Victim1(), Victim2()]
    try:
        assert Victim2()._SINGLETONS == [Victim1(), Victim2()]
    except:
        assert Victim == Singleton_CallMeta
    else:
        assert Victim == Singleton_New

    assert Victim1().attr == 11


def test__META_with_args():
    Victim = Singleton_CallMeta
    Victim._drop_all()
    class Victim1(Victim):
        def __init__(self, attr):
            self.attr = attr

    assert Victim._SINGLETONS == []
    instance = Victim1(1)

    assert instance.attr == 1
    assert Victim1(111).attr == 1
    assert Victim._SINGLETONS == [instance, ]

    Victim1(111).attr = 11
    assert Victim1(1).attr == 11
    assert Victim._SINGLETONS == [instance, ]

    assert Victim1(1111).attr == 11
    assert Victim._SINGLETONS == [instance, ]


def test__NoMETA_with_args():
    Victim = Singleton_New
    Victim._drop_all()
    class Victim1(Victim):
        def __init__(self, attr):
            self.attr = attr

    assert Victim._SINGLETONS == []
    instance = Victim1(1)

    assert instance.attr == 1
    assert Victim1(111).attr == 111
    assert Victim._SINGLETONS == [instance, ]

    assert Victim1(1).attr == 1
    assert Victim._SINGLETONS == [instance, ]


def test__META_nesting_else_one_meta():
    # cant use else one metaclass in nesting!
    try:
        class Victim1(Singleton_CallMeta, abc.ABC):
            attr = 1
    except TypeError:
        msg = """
        TypeError: metaclass conflict: the metaclass of a derived class must be a (non-strict) subclass of the metaclasses of all its bases

        """
        pass
    else:
        assert False

    class Victim2(Singleton_New, abc.ABC):
        attr = 2
    assert Victim2().attr == 2
    Victim2().attr = 22
    assert Victim2().attr == 22


@pytest.mark.parametrize(argnames="Victim", argvalues=[Singleton_CallMeta, Singleton_New])
def test__threading_spawn(Victim):
    class Victim1(Victim):
        def __init__(self):
            time.sleep(1)

    threads = [
        threading.Thread(target=Victim1),
        threading.Thread(target=Victim1),
        threading.Thread(target=Victim1),
        threading.Thread(target=Victim1),
        threading.Thread(target=Victim1),
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()
        assert thread.is_alive() is False


@pytest.mark.parametrize(argnames="Victim", argvalues=[Singleton_CallMeta, Singleton_New])
def test__several_levels_at_ones__low(Victim):
    class VictimBase2(Victim):
        attr = 0
    class Victim1(VictimBase2):
        attr = 1
    class Victim2(VictimBase2):
        attr = 2

    assert VictimBase2().attr == 0
    try:
        assert Victim1().attr == 1
    except Exc__NestingLevels:
        pass
    else:
        assert False


@pytest.mark.parametrize(argnames="Victim", argvalues=[Singleton_CallMeta, Singleton_New])
def test__several_levels_at_ones__up(Victim):
    class VictimBase2(Victim):
        attr = 0

    class Victim1(VictimBase2):
        attr = 1

    class Victim2(VictimBase2):
        attr = 2

    assert Victim1().attr == 1
    assert Victim2().attr == 2
    try:
        assert VictimBase2().attr == 0
    except Exc__NestingLevels:
        pass
    else:
        assert False


# =====================================================================================================================
