# =====================================================================================================================
class NestMethCI_GetClsName:
    """
    GOAL
    ----
    get cls name both inside cls and instance levels

    NOTE
    ----
    method is more prefer then property!!!
    """
    @classmethod
    def get_cls_name(cls) -> str:
        return cls.__name__


# =====================================================================================================================
