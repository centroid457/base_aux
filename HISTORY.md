# RELEASE HISTORY

********************************************************************************
## TODO

********************************************************************************
## FIXME

********************************************************************************
## NEWS

0.3.1.2(2025.07.15 15.24.01)
------------------------------
- [Warn] create  

0.3.0.1(2025.07.15 15.04.14)
------------------------------
- [Warn] create  

0.3.0(2025.07.15 10.49.48)
------------------------------
- THE BIG REF 2:  
	- many renames/moves/regroups/deprecates  
- [GIT]:  
	- finish = add recursive rootFind + add check_installed  
	- add DIRTY  
	- add UNTRACKED_FILES + check__status  
- [TPS]:  
	- finish TpManager with TpItem  
	- GUI - add CBB zero  
	- GUI - add BTN_tm_update+apply switching tpItem without clearing results  
	- GUI - add TableModel_Devs  
	- GUI - TableModel_Devs show ADDRESS in table  
	- LEDS - add blink Yellow on test  
	- RESULTS save only for existed and presented - finish  
- [FileText]:  
	- add pretty__json  
- [TableLine/lines/Columns]:  
	- create+apply in Breeders/DevLines/TpItems...  
- [EqValid] big full ref!:  
	- 1/ use validator a simple func  
	- 2/ place IRESULT_CUMULATE into base  
	- 3/ separate other_final_calculate  
	- create EqRaise  
	- separate EqValidChain_All/Any  
- [Lambda]:  
	- move in all methods from CallableAux(deprecated)  
- [Enums]:  
	- separate to EnumAdj+Value  
- CREATE:  
	- [EqArgs]  
	- [DictDiff]  
	- [StrIc]  
- [Base_KwargsEqValid] deprecate old ReqCheckStr_Os  
- [RaiseIf] move into ArgsAux + separate to ArgsBoolIf*  
- [Version] combine VerChecker into Vertion!+add derivatives  
- [Base_Exx] add autoPrint msg on init!  
- [TYPING] collect many fro other places  

0.2.25(2025.03.27 13.31.43)
------------------------------
- [pytest]:  
	- add ini/settings file in root  
	- hide logs for caught Raises (like in Try sent)  
- [Annots] add AttrAux_AnnotsLast =separate last/all nesting parents annotations +add EnumAdj_AnnotsDepthAllOrLast  
- [DictAux] separate to Base/DictAuxInline/Copy +add walk in keys_rename__by_func  

0.2.24(2025.03.20 17.03.41)
------------------------------
- [TP.gui.tm] add YellowColor on Startup/Teardown Cls  
- [Nest] create Nest_EqCls and apply in TC instead of middleGroup!  

0.2.23(2025.03.19 13.49.54)
------------------------------
- [lambdas/Threads] move all into callables +some ref  

0.2.22(2025.03.18 18.51.30)
------------------------------
- [alerts] ref to use deque+fix tlgrm +add Qtimer  
- [mt] ref TimeSeries +move into nympyAux  
- [nest] add NestCall_MethodName  
- [lambda] ref to keep Result/Exx in object  
- [Lambda] add Lambdalist +nest in threadItem  
- [flake8] add exclude Deprecated+hidden dirs  
- [serial] ref addresses_dump__answers quick threading   

0.2.21(2025.03.14 16.12.23)
------------------------------
- [Enum_*] zero rename all  
- [Nest] separate NestBool_False/True  

0.2.20(2025.03.13 18.28.07)
------------------------------
- zero fix ver!  

0.2.19.1(2025.03.13 18.25.25)
------------------------------
- [gui.BTN_devs_detect__clicked] link to resolve_addresses__cls  

0.2.19(2025.03.13 17.59.09)
------------------------------
- [BreederObj] add LIST__ALL_GENERATED  

0.2.18(2025.03.13 17.05.02)
------------------------------
- [TP] zero add init_post  

0.2.17(2025.03.13 16.22.47)
------------------------------
- [TextFormated] ref  
- [Alerts] start ref  
- [serial] add addresses_dump__answers  

0.2.16(2025.03.11 13.04.35)
------------------------------
- [TextFormated] create  
- [ReAttempts] create  
- [Attrs+Annots]:  
	- combine two classes finally in one  
	- add annots_ensure +annots__append  
	- separate NestRepr__ClsName_SelfStr  
- [IterAux] add get_first_is_not_none  
- [DateTime] add UPDATE_ON_STR+DEF_STR_FORMAT  
- [Nest*]:  
	- add NestCall_Other  
	- add NestStR_AttrsPattern  

0.2.15(2025.03.06 14.57.16)
------------------------------
- [TESTS] move all near source code  
- [AttrAux_AnnotsAll] BIG REF:  
	- make nested Annots from Attrs +use same meth in both  
	- rename sai_*/gai_  
	- add values__reinit_mutable +NestInit_MutableClsValues  

0.2.14(2025.03.03 16.16.50)
------------------------------
- [ini] add ConfigParserMod  
- [AttrKit] add  
- [Text]:  
	- add parse__dict_ini  
	- fix__json/parse__json  
	- add delete__cmts_c  
	- add search__group - need fix  
- [TextFile] add DictTextFileLoader  
- [NestInit_AttrsLambdasResolve] use with Resolvers  
- [Nest*_Attrs]:  
	- separate all for Attrs Contains/Eq/Len/StR  
	- [NestSAI_AttrAnycase] deprecate all Setattrs* cause recursion exx  
- [EqValid]:  
	- add EqValid_AnnotsAllExists  
	- add EqValid_AttrsByObjNotPrivate*  
- [PV] deprecate old and add new PvLoaderIni/json/env  
- [Kwargs] ref to simple dict nesting  

0.2.13(2025.02.27 15.07.31)
------------------------------
- [serial] turn back ValueUnit  

0.2.12(2025.02.27 11.00.13)
------------------------------
- [Version] full ref  
- [DateTimeAux] full ref+finish+add cmp+parseStr  
- [type/Info] add check__module  
- [Text] add clear__noneprintable +fix quotes incorrect  
- [serial] del answer by ValueUnit  

0.2.11 (2025/02/24 18:32:33)
------------------------------
- [PRJBase] move into share +use Version  
- [AttrsAux] add Base_AttrKit/Callable  

0.2.10 (2025/02/19 16:33:46)
------------------------------
- [Inits] add NestInit_AnnotsAttrsByKwArgs  
- [EqValid] add EqValid_IsinstanceSameinstance +EqValid_AttrsByKwargs  

0.2.9 (2025/02/17 12:37:00)
------------------------------
- [tc] add INFO_STR__ADD_ATTRS  
- [enums] add NestEq_EnumAdj  
- [DateTimeAux] apply getattr from PatDateTimeFormat  

0.2.8 (2025/02/13 19:42:18)
------------------------------
- [Valid] some fix  
- [tp.gui] improve HL  

0.2.7 (2025/02/13 14:31:48)
------------------------------
- [ValidSleep] add skipLink  

0.2.6 (2025/02/13 13:36:45)
------------------------------
- [Valid] add ValidBreak  

0.2.5 (2025/02/12 14:56:31)
------------------------------
- [EqValid] add EqValid_SingleNumParced  
- [Nums] add NumParsedSingle  
- [baseStatics] collect/move all in one place enums/exx/types/primitives  
- [Init*/Nest*] apply naming Style for special classes  
- [File/Dir] at last add and finish  
- [File+Text] combine in one class  
- [FilePath] add suffix/prefix  
- [Text] fix all editors(sub_*/clear/del)  
- [Annots] add set_values__by_dict  
- [enums] add cmtType/...  
- [Patts] separate in one file + move into text  
- [TYPING] create class and collect all User typing types  

0.2.4 (2025/02/06 15:02:40)
------------------------------
- [text] add parse__single_num +all derivatives  
- [enum] add EnumAdj_NumFPoint/EnumAdj_NumType  
- [base_patterns] start separating +add singleNum  

0.2.3 (2025/02/04 16:12:37)
------------------------------
- [filepath] start creating  

0.2.2 (2025/01/29 19:55:28)
------------------------------
- [EqValid] add EqValid_Endswith +repr  

0.2.1 (2025/01/29 19:26:12)
------------------------------
- [EqValid] add EqValid_Startswith  

0.2.0 (2025/01/28 18:21:18)
------------------------------
- [all PRJ] BIG REF:  
	- many renames/resorts  
	- [CIRCULAR IMPORT] final fix - clear all __init__py and use direct imports  
	- [NestInit_Source] apply in most classes  
	- [ArgsKwargs] apply+add types like TYPE__ARGS_DRAFT  
	- [@final] apply to protect classes if NestInit_Source nested  
	- [xxxAux]rename objects  
	- [EqValid/Value] big creation  
	- [CallableAux] create  
- [AttrAux_Existed] ref/fix/add dump/loadfix iters  
- [Enums] extend  
- [TextAux] ref+finish  
- [game_nouns_5letters] start creating  

0.1.9 (2024/12/12 11:20:41)
------------------------------
- [ValidAux_Obj -> lambdas] move all get_result_or_raise/*  
- separate others  
- [tests] work  

0.1.8 (2024/12/11 11:41:19)
------------------------------
- start separating parts [exceptions/TypeAux/pytester/attrs]   

0.1.7 (2024/12/09 17:03:42)
------------------------------
- [files] add filepath  
- [TP.gui] add save results MsgBox+hide in extend mode skip/async settings  

0.1.6 (2024/12/05 18:48:36)
------------------------------
- [TP.gui.TV] zero del prints  

0.1.5 (2024/12/05 18:44:42)
------------------------------
- [TP.gui.TV] add summary results footprint  
- [TP.save_results] use short style  

0.1.4 (2024/12/04 18:35:29)
------------------------------
- [TP.gui] separate layoutCtrl +Dialogs  

0.1.3 (2024/12/04 13:48:12)
------------------------------
- [TP]fix finish last tc  

0.1.2 (2024/12/03 17:25:59)
------------------------------
- [datetimes] unsand with minimals  
- [dicts] separate  
- [tp] make save results  

0.1.1 (2024/12/02 18:42:10)
------------------------------
- [zero] just fix imports and errors  

0.1.0 (2024/12/02 18:25:39)
------------------------------
- [argsKwargs] separate all variants and apply in pytest+add derivatives  
- [enums] separate typical  
- [t8] add/separate some files  

0.0.29 (2024/11/29 16:43:16)
------------------------------
- [tp.gui] ero fix headers  

0.0.28 (2024/11/29 15:55:38)
------------------------------
- [tp.gui] add and apply on finish devsDetect+Tp  

0.0.27 (2024/11/29 14:29:22)
------------------------------
- [gui.tm] fix columns  

0.0.26 (2024/11/29 14:12:13)
------------------------------
- [classes] add AttrsInitKwargs+Translator  
- [AttrAux_Existed] add attrs__to_dict  
- [gui] apply Translator for headers[gui] fix columns resizeByContents  

0.0.25 (2024/11/27 15:19:07)
------------------------------
- [tp] fix not closing/teardown last tc  
- [tp] iterate only not skipped tcs  
- [tp.gui] on dut not show FAIL if in process  
- [tp.gui] add btn_reset_all  
- [tc] add finished_cls  
- [serialClient] add reset  

0.0.24 (2024/11/26 10:24:31)
------------------------------
- [Valid/Lambdas] separate and full ref args/kwargs  

0.0.23 (2024/11/20 18:07:29)
------------------------------
- [serial] fix bool_if__LINUX stack  

0.0.22 (2024/11/20 17:28:32)
------------------------------
- [Lambdas] add InitArgsKwargs  

0.0.21 (2024/11/20 13:49:46)
------------------------------
- [lambdas] add Lambda_SleepAfter  

0.0.20 (2024/11/19 17:28:27)
------------------------------
- [ValueUnit] fix cmp with ValueVariants  

0.0.19 (2024/11/19 14:12:58)
------------------------------
- zeor ref +add old modules PrjFiles  

0.0.18 (2024/11/18 16:55:44)
------------------------------
- [setup] gen install_requires  
- [Text] create+ref  

0.0.17 (2024/11/15 11:44:38)
------------------------------
- [tcs] apply last ver gui  

0.0.16 (2024/11/14 18:40:40)
------------------------------
- [gui] add SB+MENU +switch to MainWindow +add mods from t8 +add About  
- [primitives] add Sleep* +Lambda_Sleep  

0.0.15 (2024/11/12 18:04:29)
------------------------------
- [DictGaAnnotRequired] add  
- [_SAND] create and add first content  

0.0.14 (2024/11/08 17:51:33)
------------------------------
- [Valid] add/apply get_logstr_attr  

0.0.13 (2024/11/08 17:06:55)
------------------------------
- [valid] fix str  

0.0.11 (2024/11/08 15:01:59)
------------------------------
- [share*] try fix  

0.0.10 (2024/11/08 13:28:04)
------------------------------
- [_share*] separate in folder  
-   

0.0.9 (2024/11/07 16:35:46)
------------------------------
- [classes.Lambda] add LambdaTrySuccess/+Fail  
- [classes.ClsException] add Base_Exx  

0.0.8 (2024/11/06 19:01:54)
------------------------------
- [classes.Lambda] add Lambda_Bool/+Reversed  

0.0.7 (2024/11/06 17:05:21)
------------------------------
- [classes.Lambda] add check_raise/*noRaise/*getResultOrExx  

0.0.6 (2024/11/06 15:56:06)
------------------------------
- [classes] add Lambda+NestInit_AttrsLambdaResolve  
- [classes.Valid] change REVERSE_LINK from simple static  

0.0.5 (2024/11/05 10:33:43)
------------------------------
- [classes] add DictIcKeys+DictGa  
- [stock] move here  
- [all] fix almost, so tests works (need fix privates for alerts)  

0.0.4 (2024/11/02 15:58:43)
------------------------------
- [TESTPLANS] fix finish not started tc_active  

0.0.3 (2024/11/01 21:40:45)
------------------------------
- [classes.valueVariants] add getItem  
- [SerialClient.TestShorted] add skipIf not detected for all classes  

0.0.2 (2024/10/31 15:14:48)
------------------------------
- [testplans] fix HL rules  

0.0.1 (2024/10/31 13:08:44)
------------------------------
- [ALL_MODULES] collect in one pkg

********************************************************************************
