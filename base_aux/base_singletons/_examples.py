from base_aux.base_singletons.m1_singleton import *

class MySingleton(Singleton_CallMeta):
    pass

class MySingleton2(Singleton_CallMeta):
    pass

class MySingleton(metaclass=Meta_SingletonCall):
    pass


# ===============================
# 2. access to created instances
from base_aux.base_singletons.m1_singleton import *

class Victim1(Singleton_CallMeta):
    attr = 1

class Victim2(Singleton_CallMeta):
    attr = 2

assert Singleton_CallMeta._SINGLETONS == []
Victim1()
assert Singleton_CallMeta._SINGLETONS == [Victim1(), ]
assert Victim1._SINGLETONS == [Victim1(), ]
assert Victim1()._SINGLETONS == [Victim1(), ]
Victim2()
assert Singleton_CallMeta._SINGLETONS == [Victim1(), Victim2(), ]


# ===============================
# 3. NOTICE: all your Singletons must be only last classes!
# don't use nesting from any Your Singletons!
from base_aux.base_singletons import *

class MySingleton(Singleton_CallMeta):  # OK
    pass

class MySingleton2(MySingleton):  # WRONG
    pass