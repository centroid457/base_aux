# from typing import *
#
# from base_aux.aux_text.m5_re1_rexp import *
# from base_aux.aux_iter.m1_iter_aux import *
# from base_aux.aux_attr.m1_attr2_nest8_iter_name_value import *
# from base_aux.base_statics.m2_exceptions import *
# from base_aux.base_nest_dunders.m3_nest_init_annots_attrs_by_kwargs import *
# from base_aux.aux_datetime.m1_datetime import *
#
#
# # =====================================================================================================================
# class Base_MsgLinesNamed:
#     """
#     GOAL
#     ----
#     use structured object for msg
#     with simply replacing special blocks
#     instead of manually parsing
#
#     SPECIALLY CREATED FOR
#     ---------------------
#     Alerts Telegram
#     """
#     _sep = "-"*20
#
#     ALERT: str
#     _sep1: str = _sep
#     BODY: str
#     _sep2: str = _sep
#     TS: TimeStampRenewStr = TimeStampRenewStr()
#
#     def __init__(self, text: str):
#         pass
#
#     def __str__(self):
#         result = ""
#         for name, value in self.iter_exisded_name_value():
#             name: str
#             if name.startswith("_"):
#                 result += f"[{name}]{value}"
#             else:
#                 result += f"{value}"
#
#     def __repr__(self):
#         return str(self)
#
#     def iter_exisded_name_value(self) -> tuple[str, Any]:
#         for name in self.__annotations__:
#             try:
#                 yield name, getattr(self, name)
#             except:
#                 pass
#
#
# # =====================================================================================================================
