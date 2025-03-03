from base_aux.aux_values.m0_explicit import *


# =====================================================================================================================
def test__explicit_cmp():
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
