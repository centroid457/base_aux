![Ver/TestedPython](https://img.shields.io/pypi/pyversions/base_aux)
![Ver/Os](https://img.shields.io/badge/os_development-Windows-blue)  
![repo/Created](https://img.shields.io/github/created-at/centroid457/base_aux)
![Commit/Last](https://img.shields.io/github/last-commit/centroid457/base_aux)
![Tests/GitHubWorkflowStatus](https://github.com/centroid457/base_aux/actions/workflows/test_linux.yml/badge.svg)
![Tests/GitHubWorkflowStatus](https://github.com/centroid457/base_aux/actions/workflows/test_windows.yml/badge.svg)  
![repo/Size](https://img.shields.io/github/repo-size/centroid457/base_aux)
![Commit/Count/t](https://img.shields.io/github/commit-activity/t/centroid457/base_aux)
![Commit/Count/y](https://img.shields.io/github/commit-activity/y/centroid457/base_aux)
![Commit/Count/m](https://img.shields.io/github/commit-activity/m/centroid457/base_aux)

# base_aux (current v0.0.18/![Ver/Pypi Latest](https://img.shields.io/pypi/v/base_aux?label=pypi%20latest))

## DESCRIPTION_SHORT
collect all my previous modules in one package

## DESCRIPTION_LONG



## Features
1. cmp - apply for cmp object with others  
2. getattr prefix  
3. getattr echo  
4. middle group  
5. Number+NumberArithm - use class as number  
6. Annotations - work with annotations +use special abilities+use nested classes  
7. perfect singleton (maybe thread safe!)  
8. collect all instances  
9. check correct instantiating singletons in tree project  
10. check requirements (systemOs), raise/bool if no match  
11. create fuck(?)/source and is it for check for settings  
12. [python PACKAGES/MODULES]:  
	- upgrade  
	- delete  
	- version_get_installed  
	- check_installed)  
	- upgrade pip  
13. [VERSION]:  
	- parse  
	- check  
	- compare  
14. send commands into OS terminal  
15. check if cli commands are accessible (special utilities is installed)  
16. access to standard parts of result in a simple ready-to-use form (stdout/stderr/retcode/full state)  
17. use batch timeout for list  
18. till_first_true  
19. counter/counter_in_list  
20. designed for common work with bitfields-like objects  
21. Flags  
22. Bits  
23. 
        Designed to use private data like username/pwd kept secure in OsEnvironment or Ini/Json-File for your several home projects at ones.  
        And not open it in public.  
    
        **CAUTION:**  
        in requirements for other projects use fixed version! because it might be refactored so you would get exception soon.
          
24. load values to instance attrs from:  
	- Environment  
	- IniFile  
	- JsonFile  
	- CsvFile  
	- direct text instead of file  
	- direct dict instead of file  
25. attr access:  
	- via any lettercase  
	- by instance attr  
	- like dict key on instance  
26. work with dict:  
	- apply  
	- update  
	- preupdate  
27. update_dict as cumulative result - useful in case of settings result  
28. use different managers for different funcs/methods if needed  
29. use just one decorator to spawn threads from func / methods  
30. keep all spawned threads in list by ThreadItem objects  
31. ThreadItem keeps result/exx/is_alive attributes!  
32. use wait_all/terminate_all()  
33. [SERVERS]:  
	- [aiohttp] (try not to use, as old)  
	- [FastApi] (preferred)  
34. client_requests item+stack  
35. [SerialClient]:  
	- keep all found ports in base class!  
36. Serial:  
	- Client+Server  
	- connect with Type__AddressAutoAcceptVariant FIRST_FREE/FIRST_FREE__ANSWER_VALID  
	- set/get params by SlashOrSpacePath addressing  
	- handle BackSpace send manually from terminal  
37. SerialServer values:  
	- as Callable  
	- ValueUnit  
	- ValueVariants  
	- list_results  
38. SerialServer cmd:  
	- NONE is equivalent for SUCCESS  
	- no need params (like line_parsed as before)  
	- help - for show all variants (Units/Variants/Callables)!  
39. Threading each monitor  
40. monitor:  
	- website data changes (tag text/attribute)  
	- email received with subject (by regexp) in exact folder  
41. Email/Telegram alert if:  
	- monitored data changed (from last state)  
	- html structure was changed so parsing can't be finished  
	- url became unreachable  
42. send alert msgs:  
	- emails  
	- telegram  
43. threading  
44. pyqt help examples and some other useful objects (overloaded pyqt classes)  
45. good template for TableView/Model/Signals  
46. add Events for TM/TV/PTE/...  


********************************************************************************
## License
See the [LICENSE](LICENSE) file for license rights and limitations (MIT).  
See the [LICENSE_bundled.md](LICENSE_bundled.md) file for parent licenses.  


## Release history
See the [HISTORY.md](HISTORY.md) file for release history.  


## Installation
```commandline
pip install base-aux
```


## Import
```python
from base_aux import *
```


********************************************************************************
## USAGE EXAMPLES
See tests, sourcecode and docstrings for other examples.  

********************************************************************************
