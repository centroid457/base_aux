from base_aux.base_values.m4_primitives import *
from base_aux.base_types.m2_info import *


# =====================================================================================================================
class ClsMain(ClsFullTypes):
    attrUpper = "ATTRUPPER"
    attrLower = "attrlower"
    attrSkipFullName = "attrSkipFullName"
    attrSkipPartName = "SkipPartName"


ObjectInfo(
    ClsMain(),
    log_iter=True,
    names__use_only_parts=[],
    names__skip_full=["attrSkipFullName", ],
    names__skip_parts=["SkipPartName", ],
    hide_build_in=None,
).print()
"""
==========================================================================================
----------OBJECTINFO.PRINT--------------------------------------------------------------------------
str(SOURCE)=<__main__.ClsMain object at 0x000001C739A83E00>
repr(SOURCE)=<__main__.ClsMain object at 0x000001C739A83E00>
type(SOURCE)=<class '__main__.ClsMain'>
mro(SOURCE)=['ClsMain', 'ClsFullTypes', 'object']
----------SETTINGS----------------------------------------------------------------------------------
self.NAMES__USE_ONLY_PARTS=[]
self.NAMES__SKIP_FULL=['attrSkipFullName']
self.NAMES__SKIP_PARTS=['init', 'new', 'create', 'enter', 'install', 'set', 'clone', 'copy', 'move', 'next', 'clear', 'reduce', 'close', 'del', 'exit', 'kill', 'exec', 'exec_', 'pyqtConfigure', 'checkout', 'detach', 'run', 'start', 'wait', 'join', 'terminate', 'quit', 'disconnect', 'pop', 'popleft', 'append', 'appendleft', 'extend', 'extendleft', 'add', 'insert', 'reverse', 'rotate', 'sort', 'SkipPartName']
self.HIDE_BUILD_IN=None
self.LOG_ITER=True
self.MAX_LINE_LEN=100
self.MAX_ITER_ITEMS=5
----------log_iter(wait last touched)---------------------------------------------------------------
1:	__class__
2:	__delattr__
3:	__dict__
4:	__dir__
5:	__doc__
6:	__eq__
7:	__format__
8:	__ge__
9:	__getattribute__
10:	__getstate__
11:	__gt__
12:	__hash__
13:	__init__
14:	__init_subclass__
15:	__le__
16:	__lt__
17:	__module__
18:	__ne__
19:	__new__
20:	__reduce__
21:	__reduce_ex__
22:	__repr__
23:	__setattr__
24:	__sizeof__
25:	__str__
26:	__subclasshook__
27:	__weakref__
28:	attrBytes
29:	attrCls
30:	attrClsBoolExx
31:	attrClsBoolFalse
32:	attrClsBoolTrue
33:	attrClsCall
34:	attrClsCallExx
35:	attrClsCallTrue
36:	attrClsGen
37:	attrClsIterYield
38:	attrDict
39:	attrFalse
40:	attrFloat
41:	attrFunc
42:	attrFuncDict
43:	attrFuncExx
44:	attrFuncGen
45:	attrFuncList
46:	attrFuncTrue
47:	attrGenCompr
48:	attrInst
49:	attrInstBooExx
50:	attrInstBoolFalse
51:	attrInstBoolTrue
52:	attrInstCall
53:	attrInstCallExx
54:	attrInstCallTrue
55:	attrInstGen
56:	attrInstIterYield
57:	attrInstMeth
58:	attrInt
59:	attrList
60:	attrListInst
61:	attrLower
62:	attrNone
63:	attrSet
64:	attrSkipFullName
65:	attrSkipPartName
66:	attrStr
67:	attrTrue
68:	attrTuple
69:	attrUpper
70:	attrZero
71:	classmethodNone
72:	methExx
73:	methFunc
74:	methInt
75:	methNone
76:	propertyClassmethodNone
77:	propertyExx
78:	propertyFunc
79:	propertyInt
80:	propertyNone
81:	staticmethodNone
----------SKIPPED_FULLNAMES-------------------------------------------------------------------------
1:	attrSkipFullName
----------SKIPPED_PARTNAMES-------------------------------------------------------------------------
1:	__delattr__
2:	__init__
3:	__init_subclass__
4:	__new__
5:	__reduce__
6:	__reduce_ex__
7:	__setattr__
8:	attrSkipPartName
----------PROPERTIES__ELEMENTARY_SINGLE-------------------------------------------------------------
__doc__             	NoneType    :None
__module__          	str         :__main__
__weakref__         	NoneType    :None
attrBytes           	bytes       :b'bytes'
attrFalse           	bool        :False
attrFloat           	float       :1.1
attrInt             	int         :1
attrLower           	str         :attrlower
attrNone            	NoneType    :None
attrStr             	str         :str
attrTrue            	bool        :True
attrUpper           	str         :ATTRUPPER
attrZero            	int         :0
propertyClassmethodNone	NoneType    :None
propertyInt         	int         :1
propertyNone        	NoneType    :None
----------PROPERTIES__ELEMENTARY_COLLECTION---------------------------------------------------------
__dict__            	dict        :{}
attrDict            	dict        :{1: 1}
attrList            	list        :[1, 2, 3]
attrListInst        	list        :[<pytest_aux.primitives.Cls object at 0x000001C74ACE37D0>, <...
                    	Cls         :	<pytest_aux.primitives.Cls object at 0x000001C74ACE37D0>
                    	Cls         :	<pytest_aux.primitives.Cls object at 0x000001C74ACE37D0>
                    	Cls         :	<pytest_aux.primitives.Cls object at 0x000001C74ACE37D0>
                    	int         :	1
attrSet             	set         :{1, 2, 3}
attrTuple           	tuple       :(1, 2, 3)
----------PROPERTIES__OBJECTS-----------------------------------------------------------------------
attrGenCompr        	generator   :<generator object <genexpr> at 0x000001C74A47D780>
attrInst            	ClsEmpty    :<pytest_aux.primitives.ClsEmpty object at 0x000001C74ACE35F0>
attrInstBooExx      	ClsBoolRaise  :<pytest_aux.primitives.ClsBoolRaise object at 0x000001C74ACE37A0>
attrInstBoolFalse   	ClsBoolFalse:<pytest_aux.primitives.ClsBoolFalse object at 0x000001C74ACE3770>
attrInstBoolTrue    	ClsBoolTrue :<pytest_aux.primitives.ClsBoolTrue object at 0x000001C74ACE3740>
attrInstGen         	ClsGen      :<pytest_aux.primitives.ClsGen object at 0x000001C74ACE3710>
attrInstIterYield   	ClsIterYield:<pytest_aux.primitives.ClsIterYield object at 0x000001C74ACE36E0>
----------PROPERTIES__EXX---------------------------------------------------------------------------
propertyExx         	Exception   :Exception('exxMsg')
----------METHODS__ELEMENTARY_SINGLE----------------------------------------------------------------
__getstate__        	NoneType    :None
__hash__            	int         :122198590432
__repr__            	str         :<__main__.ClsMain object at 0x000001C739A83E00>
__sizeof__          	int         :16
__str__             	str         :<__main__.ClsMain object at 0x000001C739A83E00>
attrFunc            	NoneType    :None
attrFuncTrue        	bool        :True
attrInstCall        	NoneType    :None
attrInstCallTrue    	bool        :True
attrInstMeth        	NoneType    :None
classmethodNone     	NoneType    :None
methInt             	int         :1
methNone            	NoneType    :None
propertyFunc        	NoneType    :None
staticmethodNone    	NoneType    :None
----------METHODS__ELEMENTARY_COLLECTION------------------------------------------------------------
__dir__             	list        :['__module__', 'attrUpper', 'attrLower', 'attrSkipFullName',...
                    	str         :	__module__
                    	str         :	attrUpper
                    	str         :	attrLower
                    	str         :	attrSkipFullName
                    	str         :	attrSkipPartName
                    	            :	...
attrFuncDict        	dict        :{<__main__.ClsMain object at 0x000001C739A83E00>: None}
attrFuncList        	list        :[<__main__.ClsMain object at 0x000001C739A83E00>]
----------METHODS__OBJECTS--------------------------------------------------------------------------
__class__           	ClsMain     :<__main__.ClsMain object at 0x000001C739C51A60>
__subclasshook__    	NotImplementedType:NotImplemented
attrCls             	ClsEmpty    :<pytest_aux.primitives.ClsEmpty object at 0x000001C739E91EB0>
attrClsBoolExx      	ClsBoolRaise  :<pytest_aux.primitives.ClsBoolRaise object at 0x000001C74ACE2690>
attrClsBoolFalse    	ClsBoolFalse:<pytest_aux.primitives.ClsBoolFalse object at 0x000001C74ACE27E0>
attrClsBoolTrue     	ClsBoolTrue :<pytest_aux.primitives.ClsBoolTrue object at 0x000001C74ACE28D0>
attrClsCall         	ClsCall     :<pytest_aux.primitives.ClsCall object at 0x000001C74ACE2990>
attrClsCallExx      	ClsCallExx  :<pytest_aux.primitives.ClsCallExx object at 0x000001C74ACE2A50>
attrClsCallTrue     	ClsCallTrue :<pytest_aux.primitives.ClsCallTrue object at 0x000001C74ACE2AE0>
attrClsGen          	ClsGen      :<pytest_aux.primitives.ClsGen object at 0x000001C74ACE2B40>
attrClsIterYield    	ClsIterYield:<pytest_aux.primitives.ClsIterYield object at 0x000001C74ACE2BA0>
attrFuncGen         	generator   :<generator object FUNC_GEN at 0x000001C74ACCE740>
methFunc            	function    :<function FUNC at 0x000001C74ACEA2A0>
----------METHODS__EXX------------------------------------------------------------------------------
__eq__              	TypeError   :TypeError('expected 1 argument, got 0')
__format__          	TypeError   :TypeError('ClsMain.__format__() takes exactly one argument (...
__ge__              	TypeError   :TypeError('expected 1 argument, got 0')
__getattribute__    	TypeError   :TypeError('expected 1 argument, got 0')
__gt__              	TypeError   :TypeError('expected 1 argument, got 0')
__le__              	TypeError   :TypeError('expected 1 argument, got 0')
__lt__              	TypeError   :TypeError('expected 1 argument, got 0')
__ne__              	TypeError   :TypeError('expected 1 argument, got 0')
attrFuncExx         	Exception   :Exception('CALLABLE_EXX')
attrInstCallExx     	Exception   :Exception()
methExx             	Exception   :Exception('exxMsg')
==========================================================================================
"""

ObjectInfo(
    ClsMain(),
    # log_iter=False,
    names__use_only_parts="attr",
    # names__skip_full=["attrSkipFullName", ],
    # names__skip_parts=["SkipPartName", ],
    # hide_build_in=None,
    # max_line_len=0,
    # max_iter_items=0,
).print()
"""
==========================================================================================
----------OBJECTINFO.PRINT--------------------------------------------------------------------------
str(SOURCE)=<__main__.ClsMain object at 0x000001C748B236B0>
repr(SOURCE)=<__main__.ClsMain object at 0x000001C748B236B0>
type(SOURCE)=<class '__main__.ClsMain'>
mro(SOURCE)=['ClsMain', 'ClsFullTypes', 'object']
----------SETTINGS----------------------------------------------------------------------------------
self.NAMES__USE_ONLY_PARTS=['attr']
self.NAMES__SKIP_FULL=['attrSkipFullName']
self.NAMES__SKIP_PARTS=['init', 'new', 'create', 'enter', 'install', 'set', 'clone', 'copy', 'move', 'next', 'clear', 'reduce', 'close', 'del', 'exit', 'kill', 'exec', 'exec_', 'pyqtConfigure', 'checkout', 'detach', 'run', 'start', 'wait', 'join', 'terminate', 'quit', 'disconnect', 'pop', 'popleft', 'append', 'appendleft', 'extend', 'extendleft', 'add', 'insert', 'reverse', 'rotate', 'sort', 'SkipPartName']
self.HIDE_BUILD_IN=None
self.LOG_ITER=None
self.MAX_LINE_LEN=100
self.MAX_ITER_ITEMS=5
----------log_iter(wait last touched)---------------------------------------------------------------
----------SKIPPED_FULLNAMES-------------------------------------------------------------------------
1:	attrSkipFullName
----------SKIPPED_PARTNAMES-------------------------------------------------------------------------
1:	__delattr__
2:	__setattr__
3:	attrSkipPartName
----------PROPERTIES__ELEMENTARY_SINGLE-------------------------------------------------------------
attrBytes           	bytes       :b'bytes'
attrFalse           	bool        :False
attrFloat           	float       :1.1
attrInt             	int         :1
attrLower           	str         :attrlower
attrNone            	NoneType    :None
attrStr             	str         :str
attrTrue            	bool        :True
attrUpper           	str         :ATTRUPPER
attrZero            	int         :0
----------PROPERTIES__ELEMENTARY_COLLECTION---------------------------------------------------------
attrDict            	dict        :{1: 1}
attrList            	list        :[1, 2, 3]
attrListInst        	list        :[<pytest_aux.primitives.Cls object at 0x000001C74ACE37D0>, <...
                    	Cls         :	<pytest_aux.primitives.Cls object at 0x000001C74ACE37D0>
                    	Cls         :	<pytest_aux.primitives.Cls object at 0x000001C74ACE37D0>
                    	Cls         :	<pytest_aux.primitives.Cls object at 0x000001C74ACE37D0>
                    	int         :	1
attrSet             	set         :{1, 2, 3}
attrTuple           	tuple       :(1, 2, 3)
----------PROPERTIES__OBJECTS-----------------------------------------------------------------------
attrGenCompr        	generator   :<generator object <genexpr> at 0x000001C74A47D780>
attrInst            	ClsEmpty    :<pytest_aux.primitives.ClsEmpty object at 0x000001C74ACE35F0>
attrInstBooExx      	ClsBoolRaise  :<pytest_aux.primitives.ClsBoolRaise object at 0x000001C74ACE37A0>
attrInstBoolFalse   	ClsBoolFalse:<pytest_aux.primitives.ClsBoolFalse object at 0x000001C74ACE3770>
attrInstBoolTrue    	ClsBoolTrue :<pytest_aux.primitives.ClsBoolTrue object at 0x000001C74ACE3740>
attrInstGen         	ClsGen      :<pytest_aux.primitives.ClsGen object at 0x000001C74ACE3710>
attrInstIterYield   	ClsIterYield:<pytest_aux.primitives.ClsIterYield object at 0x000001C74ACE36E0>
----------PROPERTIES__EXX---------------------------------------------------------------------------
----------METHODS__ELEMENTARY_SINGLE----------------------------------------------------------------
attrFunc            	NoneType    :None
attrFuncTrue        	bool        :True
attrInstCall        	NoneType    :None
attrInstCallTrue    	bool        :True
attrInstMeth        	NoneType    :None
----------METHODS__ELEMENTARY_COLLECTION------------------------------------------------------------
attrFuncDict        	dict        :{<__main__.ClsMain object at 0x000001C748B236B0>: None}
attrFuncList        	list        :[<__main__.ClsMain object at 0x000001C748B236B0>]
----------METHODS__OBJECTS--------------------------------------------------------------------------
attrCls             	ClsEmpty    :<pytest_aux.primitives.ClsEmpty object at 0x000001C74ACE39E0>
attrClsBoolExx      	ClsBoolRaise  :<pytest_aux.primitives.ClsBoolRaise object at 0x000001C74ACE3A10>
attrClsBoolFalse    	ClsBoolFalse:<pytest_aux.primitives.ClsBoolFalse object at 0x000001C74ACE3A70>
attrClsBoolTrue     	ClsBoolTrue :<pytest_aux.primitives.ClsBoolTrue object at 0x000001C74ACE3AA0>
attrClsCall         	ClsCall     :<pytest_aux.primitives.ClsCall object at 0x000001C74ACE3AD0>
attrClsCallExx      	ClsCallExx  :<pytest_aux.primitives.ClsCallExx object at 0x000001C74ACE3B00>
attrClsCallTrue     	ClsCallTrue :<pytest_aux.primitives.ClsCallTrue object at 0x000001C74ACE3B30>
attrClsGen          	ClsGen      :<pytest_aux.primitives.ClsGen object at 0x000001C74ACE3B60>
attrClsIterYield    	ClsIterYield:<pytest_aux.primitives.ClsIterYield object at 0x000001C74ACE3B90>
attrFuncGen         	generator   :<generator object FUNC_GEN at 0x000001C74ACCE8E0>
----------METHODS__EXX------------------------------------------------------------------------------
__getattribute__    	TypeError   :TypeError('expected 1 argument, got 0')
attrFuncExx         	Exception   :Exception('CALLABLE_EXX')
attrInstCallExx     	Exception   :Exception()
==========================================================================================
"""
