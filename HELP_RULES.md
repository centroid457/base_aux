# HELP_RULES

********************************************************************************
## NAME PREFIX schema

1. BASEs  
   - Abc_* - interface! or where we have BLANK methods!
   - Base_* - base class for realising final objects - where we have finished methods and it could be (or not) redefine!
   - Nest*_* - middle class for adding specific universal logic in any other class
     - NestMeth_*
     - NestInit_*
     - NestStr_*
   - Meta*_* - class is metaCls!!!
   - Template_* - somtimes you cant apply Class as universal baseClass! so in such case this class created only as template.  
and you should use it as template for creating your own class.  

2. SPECIFIC parent/statics  
   1. static - cant be switched into other BaseType 
      - Enum_* - Enum
   2. BaseType can be logically replaced in any type (so prefix need to be changed inconveniently!)  
      - Data_* - dataclasses/STRUCTURES separated(!) from execution logic
      - Nt_* - NamedTuple
   3. Monkey_* - special test objects


********************************************************************************
