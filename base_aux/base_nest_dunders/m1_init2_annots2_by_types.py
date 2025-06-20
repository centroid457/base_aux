from base_aux.aux_attr.m1_annot_attr1_aux import AttrAux_AnnotsAll


# =====================================================================================================================
class NestInit_AnnotsByTypes_All:
    """
    GOAL
    ----
    when create class with only annots
    and need to init instance with default attr values like dict/list/set/...

    SPECIALLY CREATED FOR
    ---------------------
    game1_noun5letters.CharMask
    """
    # -----------------------------------------------------------------------------------------------------------------
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        AttrAux_AnnotsAll(self).reinit__annots_by_types(not_existed=False)


# =====================================================================================================================
class NestInit_AnnotsByTypes_NotExisted:
    """
    GOAL
    ----
    same as NestInit_AnnotsByTypes_All but for only not existed values
    """
    # -----------------------------------------------------------------------------------------------------------------
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        AttrAux_AnnotsAll(self).reinit__annots_by_types(not_existed=True)


# =====================================================================================================================
