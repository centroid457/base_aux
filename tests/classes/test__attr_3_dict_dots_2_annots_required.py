# from typing import *
# import pytest
#
# from base_aux.classes.attr_3_dict_dots_1_simple import DictDotsAnnotRequired
# from base_aux.classes import *
# from base_aux.objects import LAMBDA_EXX
#
#
# # =====================================================================================================================
# dict_example = {
#     "lowercase": "lowercase",
#     # "nested": {"n1":1},
# }
#
#
# class Victim(DictDotsAnnotRequired):
#     lowercase: str
#
#
# # =====================================================================================================================
# def test__dict_only():
#     assert LambdaTrySuccess(DictDotsAnnotRequired) == True
#     assert LambdaTrySuccess(DictDotsAnnotRequired)
#
#     assert LambdaTryFail(DictDotsAnnotRequired) != True
#     assert not LambdaTryFail(DictDotsAnnotRequired)
#
#     assert LambdaTrySuccess(DictDotsAnnotRequired, **dict_example)
#     assert LambdaTrySuccess(DictDotsAnnotRequired, lowercase="lowercase")
#     assert LambdaTrySuccess(DictDotsAnnotRequired, LOWERCASE="lowercase")
#
#
# def test__with_annots():
#     assert LambdaTryFail(Victim)
#     assert not LambdaTrySuccess(Victim)
#
#     victim = Victim(lowercase="lowercase")
#     assert victim["lowercase"] == "lowercase"
#
#     assert LambdaTrySuccess(Victim, **dict_example)
#     assert LambdaTrySuccess(Victim, lowercase="lowercase")
#     assert LambdaTrySuccess(Victim, LOWERCASE="lowercase")
#
#     assert LambdaTrySuccess(Victim, hello="lowercase")
#
#     victim = Victim(lowercase="lowercase")
#     assert victim == {"lowercase": "lowercase"}
#     assert victim[1] == None
#     assert victim.lowercase == "lowercase"
#
#
# # =====================================================================================================================
