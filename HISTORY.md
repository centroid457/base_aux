# RELEASE HISTORY

********************************************************************************
## TODO
1. [Valid*/Value*] ref/make all nested from VALID!!!  

********************************************************************************
## FIXME
1. ...  

********************************************************************************
## NEWS

0.4.38 (2024/10/25 12:32:44)
------------------------------
- [annotsMovedTOClassesAux] apply  

0.4.37 (2024/10/25 11:21:07)
------------------------------
- add static.py  

0.4.36 (2024/10/24 15:46:21)
------------------------------
- [valid.__str__] fixDel extra newLine  

0.4.35 (2024/10/24 12:40:53)
------------------------------
- [Valid]:  
	- fix __str__ (hide not used argsKwargs)  
	- del str_pattern,  
	- rename ValidReverse  

0.4.34 (2024/10/23 16:20:16)
------------------------------
- [ValidReverse] add new  

0.4.33 (2024/10/16 15:05:53)
------------------------------
- try fix  

0.4.32 (2024/10/16 12:41:52)
------------------------------
- fix errors  

0.4.31 (2024/10/16 12:38:22)
------------------------------
- try apply last vers for modules like AnnotAux, seems errors exists!  

0.4.30 (2024/10/14 15:22:54)
------------------------------
- [Valid] separate ValidAux/derivatives  
- [ValidAux] add get_result  

0.4.29 (2024/10/11 11:08:31)
------------------------------
- [Valid] add VALIDATE_RETRY +derivatives ValidRetry1/2  

0.4.28 (2024/09/30 13:15:20)
------------------------------
- [ValidRegExp] add new  
- [ValidAux] separate from Valid  

0.4.27 (2024/09/26 17:30:56)
------------------------------
- [ValueVariants] big ref +add ValueNotExist to use as validator  

0.4.26 (2024/09/26 11:18:39)
------------------------------
- [ValueUnit] add ValueNotExist for using object as pattern  

0.4.25 (2024/09/25 16:21:42)
------------------------------
- [ValidChains] fix FailStop incorrect breakOut  
- rename to ValueNotExist  

0.4.24 (2024/09/24 14:13:57)
------------------------------
- [Valid] ref EQ on ValueNotExist+add tests  

0.4.23 (2024/09/23 16:38:51)
------------------------------
- [Explicit] add ValueNotExist+Type*=need tests  

0.4.22 (2024/09/05 15:09:31)
------------------------------
- [Valid] add ValidSleep for pause in chains  

0.4.21 (2024/09/05 14:41:43)
------------------------------
- [ValueVariants] fix cmp direct objects (not only by str)  
- [Valid] add validateLink as ValueVariants  

0.4.20 (2024/09/05 12:55:43)
------------------------------
- [Valid] just zero add ValidNoCum  

0.4.19 (2024/09/02 18:31:31)
------------------------------
- [BreederStrStack] add _INDEX_START  

0.4.18 (2024/08/12 13:06:29)
------------------------------
- [ENSURE_tuple] add param none_as_empty  

0.4.17 (2024/08/12 10:23:23)
------------------------------
- [ENSURE] separate file + add ensure_class  

0.4.16 (2024/08/07 18:11:41)
------------------------------
- [Valid] zero add derivatives ValidFailStop/*ContinueE  

0.4.15 (2024/08/07 12:33:07)
------------------------------
- [Explicit] rename +separate +use as base! +add cmp EQ/NE  

0.4.14 (2024/08/06 17:57:46)
------------------------------
- [Valid] fix STR_PATTERN2  

0.4.13 (2024/08/06 17:49:28)
------------------------------
- [Valid] fix STR_PATTERN  

0.4.12 (2024/08/06 17:15:37)
------------------------------
- [Valid] fix exx for new vers  

0.4.11 (2024/08/05 16:25:11)
------------------------------
- [Valid] fix all errors on tests  

0.4.10 (2024/08/05 15:11:54)
------------------------------
- [ARGS] create separated file + add tests  

0.4.9 (2024/08/05 14:23:20)
------------------------------
- [ARGS] create and separate +NEED FIX TESTS!!!  

0.4.8 (2024/08/02 10:43:25)
------------------------------
- [Valid] zero idea  

0.4.7 (2024/07/31 10:40:59)
------------------------------
- [Valid] rename TITLE to NAME! for future access to Valid from Chains  

0.4.6 (2024/07/31 10:34:46)
------------------------------
- [Valid/Chains] add timestamp_last  

0.4.5 (2024/07/31 10:14:17)
------------------------------
- [Valid]:  
	- add args/kwargs into Value/Validate  
	- add ltgt/**  

0.4.4 (2024/07/29 16:40:49)
------------------------------
- [ValidChains] fix str() by adding START/STOP/FINISH, +fix default None for validate_last  

0.4.3 (2024/07/29 15:07:45)
------------------------------
- [Valid] fix str()  

0.4.2 (2024/07/29 14:03:05)
------------------------------
- [Valid] zero rename meth to run__if_not_finished  

0.4.1 (2024/07/29 12:28:24)
------------------------------
- [Valid] zero rename meth to run__if_not_finished  

0.4.0 (2024/07/26 15:24:48)
------------------------------
- [ResultExpect*] full deprecate  
- [ResultFunc] deprecate  
- [Valid/Chains] add by replacing ResultExpect  
- [ValueUnit/Variants] zero rename  

0.3.14 (2024/07/23 10:16:44)
------------------------------
- [ResultCum] fix str for LogLines  

0.3.13 (2024/07/22 18:00:51)
------------------------------
- [ResultFunc] add get_result_or_exx as cls meth universal  

0.3.12 (2024/07/22 17:03:22)
------------------------------
- [ValueValidate_Cum] some fix  

0.3.11 (2024/07/22 14:58:25)
------------------------------
- [Value_WithUnit] some fix  

0.3.10 (2024/07/19 17:26:59)
------------------------------
- [ResultCum] create  

0.3.9 (2024/07/18 17:41:27)
------------------------------
- [Valid] add new  

0.3.8 (2024/07/15 14:40:53)
------------------------------
- [Value_WithUnit] big ref:  
	- apply NumberArithm  
	- add UNIT_MULT__VARIANTS into class! so ou can extend it  
	- add RUS multipliers  
	- add UNIT_MULT__DISABLE  

0.3.7 (2024/07/09 16:25:22)
------------------------------
- [Value_WithUnit] big ref!:  
	- add parse(source)  
	- add work with negative/positive  
	- add multipliers  
	- add full cmp  

0.3.6 (2024/07/05 14:49:13)
------------------------------
- [ResultExpectStep] add VALUE_ACTUAL! with good MSG as keep logging/dump results  

0.3.5 (2024/06/27 10:53:36)
------------------------------
- [testPrimitives] zero move into pytest_aux  

0.3.4 (2024/06/26 18:19:36)
------------------------------
- [ResultChain] fix MSG  

0.3.3 (2024/06/26 17:17:53)
------------------------------
- [FUNCS_DEBUG] add like LAMBDA_EXX/*  

0.3.2 (2024/06/26 16:33:50)
------------------------------
- [RESULT_CHAIN]:  
	- add direct values  
	- add SKIP_IF param  
	- zero separate files  

0.3.1 (2024/06/24 11:03:30)
------------------------------
- [TESTS] move into separated folder  

0.3.0 (2024/06/21 15:59:40)
------------------------------
- [CICD] apply last  
- [BADGES] add last variant  

0.2.16 (2024/06/20 17:56:00)
------------------------------
- [CICD] apply tests  

0.2.15 (2024/06/20 16:41:20)
------------------------------
- [CMP] remove to separate class into classes-aux  

0.2.14 (2024/06/18 19:26:55)
------------------------------
- [CMP] remove to separate class into classes-aux  

0.2.13 (2024/06/18 13:13:30)
------------------------------
- [CMP] add CMP  

0.2.12 (2024/06/07 14:12:33)
------------------------------
- [results]apply TypeChecker.check__func_or_meth for callable value  

0.2.11 (2024/06/07 10:06:54)
------------------------------
- [RESULTS] fix correct work by recognition callables and classes on value, not just callable  

0.2.10 (2024/06/06 15:10:51)
------------------------------
- [RESULTS] fix exx on __bool__  

0.2.9 (2024/06/06 14:49:51)
------------------------------
- [RESULTS] add STEP__FINISHED + run__if_not_finished  

0.2.8 (2024/06/05 11:12:58)
------------------------------
- [HISTORY] fix mistakes encoding  
- [Value_FromVariants] add VALUE_DEFAULT + reset  

0.2.7 (2024/05/31 11:07:18)
------------------------------
- [Values] add TYPE__VALUE_NOT_PASSED  

0.2.6 (2024/05/31 11:01:37)
------------------------------
- [Values] move here from bus_user  

0.2.5 (2024/05/23 17:34:15)
------------------------------
- [breederObj]:  
	- add force param in generate__objects + FIX  

0.2.4 (2024/05/23 17:17:12)
------------------------------
- [breederObj]:  
	- add force param in generate__objects  

0.2.3 (2024/05/23 15:41:22)
------------------------------
- [breederObj]:  
	- add BREEDER class (for single) and instance (with index for listed) in every instance object!  
	- separate internal tests  
	- finish tests  

0.2.2 (2024/05/23 12:03:47)
------------------------------
- [breederObj] ref:  
	- del _GROUP  
	- add INSTS in classes - place all instances in source classes  

0.2.1 (2024/05/22 12:15:48)
------------------------------
- [breeder_str] move AnnotAux into separated module![__INIT__.py] fix import  
- apply last pypi template  

0.2.0 (2024/05/21 13:02:53)
------------------------------
- [breeder_str]  
- rename NamesIndexed_Templated -> BreederStrSeries  
- rename NamesIndexed_Base -> BreederStrStack  
- [Series] add START_OUTER=0 and _raise_if_start_outer_none  
- [STACK] resolve AUTO index!  
- [STACK] sort _DATA  

0.1.9 (2024/05/20 12:19:28)
------------------------------
- [breeders] move here BreederObjectList + add tests  

0.1.8 (2024/05/17 12:57:16)
------------------------------
- [RESULTS] deprecate value_as_func - used auto!  

0.1.7 (2024/05/16 18:11:46)
------------------------------
- [COLLECTS]:  
	- add Test__NamesIndexed_Templated  
	- add get_listed_index__by_outer/get_listed_index__by_value  

0.1.6 (2024/05/16 14:37:12)
------------------------------
- [RESULTS] add STEP__EXX into MSG  

0.1.5 (2024/05/16 12:08:23)
------------------------------
- [RESULTS]:  
	- add ResultExpect_Base into root import  

0.1.4 (2024/05/16 12:00:23)
------------------------------
- [RESULTS]:  
	- add __bool__ + unhide BASE  
	- add MSGS  
	- add __str__  

0.1.3 (2024/04/27 16:31:41)
------------------------------
- [RESULTS] zero exten ....msg + add index in stack msg  

0.1.1 (2024/03/28 17:44:47)
------------------------------
- [COLLECTS.NamesIndexed] add count  

0.1.0 (2024/03/28 13:32:28)
------------------------------
- [COLLECTS]:  
	- add COLLECTS  
	- add NamesIndexed_Base  
- [PYPI] apply last ver  

0.0.10 (2024/03/22 17:24:00)
------------------------------
- [RESULTS]:  
	- return back for Explicit attr VALUE  

0.0.9 (2024/03/22 16:15:33)
------------------------------
- [RESULTS]:  
	- rename Explicit  
	- add ResultFunc + tests  
	- add ResultExpect_Step/ResultExpect_Chain + some tests  

0.0.8 (2024/03/01 11:55:18)
------------------------------
- add Strings.try_convert_to__elementary (not finished - correct working with singles only)  
- separate Explicit into file + tests  
- add ResultFunc (not tested)  

0.0.7 (2024/02/29 16:03:50)
------------------------------
- ref/rename collects +make it all as class!  
- add Explicit  

0.0.6 (2024/02/28 19:11:14)
------------------------------
- add collection__path_create_original_names  

0.0.5 (2024/02/28 11:03:13)
------------------------------
- open new group COLLECTS! add collection__get_original_item__case_type_insensitive  

0.0.4 (2023-10-04)
-------------------
- array_2d_get_compact_str

********************************************************************************
