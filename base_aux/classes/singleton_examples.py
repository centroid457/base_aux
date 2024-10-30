from base_aux.classes.singleton import *

class MySingleton(SingletonByCallMeta):
    pass

class MySingleton2(SingletonByCallMeta):
    pass

class MySingleton(metaclass=SingletonMetaCallClass):
    pass


# ===============================
# 2. access to created instances
from base_aux.classes.singleton import *

class Victim1(SingletonByCallMeta):
    attr = 1

class Victim2(SingletonByCallMeta):
    attr = 2

assert SingletonByCallMeta._SINGLETONS == []
Victim1()
assert SingletonByCallMeta._SINGLETONS == [Victim1(), ]
assert Victim1._SINGLETONS == [Victim1(), ]
assert Victim1()._SINGLETONS == [Victim1(), ]
Victim2()
assert SingletonByCallMeta._SINGLETONS == [Victim1(), Victim2(), ]


# ===============================
# 3. NOTICE: all your Singletons must be only last classes!
# don't use nesting from any Your Singletons!
from base_aux.classes.singleton import *

class MySingleton(SingletonByCallMeta):  # OK
    pass

class MySingleton2(MySingleton):  # WRONG
    pass