# from typing import *
#
# from base_aux.aux_attr.m1_annot_attr1_aux import *
# from base_aux.base_nest_dunders.m1_init2_annots1_attrs_by_args_kwargs import *
# from base_aux.base_nest_dunders.m2_str2_attrs import *
# from base_aux.base_nest_dunders.m4_gsai_ic__annots import *
# from base_aux.base_nest_dunders.m6_eq1_attrs import *
# from base_aux.base_nest_dunders.m8_contains_attrs import *
# from base_aux.base_nest_dunders.m8_len_attrs import *
#
#
# # =====================================================================================================================
# @final
# class AttrKit_LockedKeys(       # DEPRECATED! - use DictIc_LockedKeys
#     NestInit_AnnotsAttr_ByKwargs,
#
#     NestGAI_AnnotAttrIC,
#
#     NestEq_AttrsNotHidden,
#     NestStR_AttrsNotHidden,
#     NestLen_AttrNotHidden,
#     NestContains_AttrIcNotHidden,
# ):
#     """
#     GOAL
#     ----
#     create attrs by init.
#     then try to update values.
#
#     SAME AS - 1=Base_AttrKit
#     ------------------------
#     BUT attrs create by stable names only on INIT by kwargs! online!
#
#     SPECIALLY CREATED FOR
#     ---------------------
#     Base_Indicator to use as inline params setup - like an objectDict! with exact attrSet!
#     """
#     def __init__(self, **kwargs: Any) -> None:
#         super().__init__(**kwargs)
#
#         AttrAux_AnnotsLast(self).annots__append_with_values(**kwargs)
#
#     def __call__(self, *args, **kwargs) -> Self | NoReturn:
#         """
#         GOAL
#         ----
#         set values only for existed keys
#         so it used as try to update def values!
#         """
#         AttrAux_AnnotsLast(self).sai__by_args(*args)
#
#         for name in kwargs:
#             if AttrAux_AnnotsLast(self).name_ic__get_original(name) is None:
#                 msg = f"{name=} not in {self=}"
#                 raise Exx__NotExistsNotFoundNotCreated(msg)
#         AttrAux_AnnotsLast(self).sai__by_kwargs(**kwargs)
#
#         return self
#
#
# # =====================================================================================================================
# if __name__ == '__main__':
#     pass
#
#
# # =====================================================================================================================
