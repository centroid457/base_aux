from base_aux.versions.m3_derivatives import Version_Python


# =====================================================================================================================
class Test__ReqCheckVersion_Python:
    # -----------------------------------------------------------------------------------------------------------------
    def test__cmp_str(self):
        assert Version_Python("1.2rc2.3").check_eq("1.02rc2.3") is True
        assert Version_Python("1.2rc2.3").check_eq("1.2rc2.33") is False

        assert Version_Python("1.2rc2.3").check_ne("1.02rc2.3") is False
        assert Version_Python("1.2rc2.3").check_ne("1.2rc2.33") is True

        assert Version_Python("1.2").check_le("1.2rc2.3") is True
        assert Version_Python("1.2").check_lt("1.2rc2.3") is True

        assert Version_Python("1.2").check_ge("1.2rc2.3") is False
        assert Version_Python("1.2").check_gt("1.2rc2.3") is False

    def test__py(self):
        assert Version_Python().check_eq("1.02rc2.3") is False
        assert Version_Python().check_gt("1.02rc2.3") is True

    def test__raise(self):
        # IF -----------------
        print("START"*100)
        try:
            Version_Python("1.2").raise_if__check_eq("1.02")
        except:
            pass
        else:
            assert False

        Version_Python("1.2").raise_if__check_eq("1.22")

        # IF NOT -----------------
        Version_Python("1.2").raise_if_not__check_eq("1.02")
        try:
            Version_Python("1.2").raise_if_not__check_eq("1.22")
        except:
            pass
        else:
            assert False

    # @pytest.mark.parametrize(
    #     argnames="args, _EXPECTED",
    #     argvalues=[
    #         (("1.2rc2.3", "1.2rc2.3"), True),
    #     ]
    # )
    # def test__inst__cmp__eq(self, args, _EXPECTED):
    #     func_link = lambda source1, source2: Version_Python().check_eq("1.02rc2.3")
    #     Lambda(func_link, args).assert_check(_EXPECTED)


# =====================================================================================================================
