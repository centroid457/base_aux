# RELEASE HISTORY

********************************************************************************
## TODO
1. create class with autoInit params from ATTRS  
2. [Valid*/Value*] ref/make all nested from VALID!!!  
3. add TIMEOUT (use start in thread!) for print! use timeout for GETATTR!!!  
4. realise PRINT_DIFFS=CHANGE_state/COMPARE_objects (one from different states like thread before and after start)!:  
	- this is about to save object STATE!  
	- add parameter show only diffs or show all  
	- add TESTS after this step!  
5. apply asyncio.run for coroutine?  
6. merge items Property/Meth? - cause it does not matter callable or not (just add type info block)  
7. add check__instance_of_user_class  
8. add check_file  
9. add SERIAL execution as method wait_all_piped! paired up with wait_all_parallel()  
10. add meta cumulative funks  
11. add GROUP threads - in decorator+wait+...  
12. maybe AUTO CLEAR if decorator get new funcName?  
13. TIME item+group  
14. monitors:  
	- check requirement for python version!  
	- csv.reader(ofilepath, delimiter=self.CSV_DELIMITER)  
	- module 'privates.csv' has no attribute 'reader'  
15. TODO test multyStart by one object (QThread)  
16. FIX NEED SOLVE ABILITY to work without PV.FILE!!! as just a http client  

********************************************************************************
## FIXME

********************************************************************************
## NEWS

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
