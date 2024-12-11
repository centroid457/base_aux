from base_aux.singletons import *

class MySingleton(SingletonCallMeta):
    pass

class MySingleton2(SingletonCallMeta):
    pass

class MySingleton(metaclass=SingletonCallMetaType):
    pass


# ===============================
# 2. access to created instances
from base_aux.singletons import *

class Victim1(SingletonCallMeta):
    attr = 1

class Victim2(SingletonCallMeta):
    attr = 2

assert SingletonCallMeta._SINGLETONS == []
Victim1()
assert SingletonCallMeta._SINGLETONS == [Victim1(), ]
assert Victim1._SINGLETONS == [Victim1(), ]
assert Victim1()._SINGLETONS == [Victim1(), ]
Victim2()
assert SingletonCallMeta._SINGLETONS == [Victim1(), Victim2(), ]


# ===============================
# 3. NOTICE: all your Singletons must be only last classes!
# don't use nesting from any Your Singletons!
from base_aux.singletons import *

class MySingleton(SingletonCallMeta):  # OK
    pass

class MySingleton2(MySingleton):  # WRONG
    pass