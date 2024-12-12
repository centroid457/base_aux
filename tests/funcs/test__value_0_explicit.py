from base_aux.funcs import *
from base_aux.classes import *
from base_aux.base_objects import *


# =====================================================================================================================
class Test__Explicit:
    # @classmethod
    # def setup_class(cls):
    #     # cls.Victim = ResultFunc
    #     pass
    #
    # @classmethod
    # def teardown_class(cls):
    #     pass
    #
    # def setup_method(self, method):
    #     pass
    #
    # def teardown_method(self, method):
    #     pass

    # -----------------------------------------------------------------------------------------------------------------
    def test__cmp(self):
        # NONE ---------------------------
        assert Explicit(None) == None
        assert Explicit(None) is not None
        assert Explicit(None)() == None
        assert Explicit(None)() is None

        # SINGLE -------------------------
        assert Explicit(111) == 111

        # COLLECTIONS -------------------------
        assert Explicit(()) == ()
        assert Explicit([]) == []
        assert Explicit({}) == {}

        assert Explicit(111) == 111
        assert Explicit([111]) == [111]
        assert Explicit({111}) == {111}
        assert Explicit({111: 222}) == {111: 222}


# =====================================================================================================================
