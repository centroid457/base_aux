# HELP_RULES

********************************************************************************
## NAME PREFIX schema

1. BASEs
   1. Mark_* - class used only to show she main parent as purpose (like Mark_Monkey)
        use only with no attrs/meth!
   2. Abc_* - interface! or where we have BLANK methods!
        where we have at least one method as abstract (not realised logic! - return raise NotImplementedError())
   3. Base_* - base class for realising final objects - where we have finished methods and it could be (or not) redefine!
        all methods have coded logic!
   4. Nest*_* - middle class for adding specific universal logic in any other class
      - NestMeth_*
      - NestInit_*
      - NestStr_*
   5. Meta*_* - class is metaCls!!!
   6. Template_* - somtimes you cant apply Class as universal baseClass! so in such case this class created only as template.  
and you should use it as template for creating your own class.  

2. SPECIFIC parent/statics  
   1. static - cant be switched into other BaseType 
      - Enum_* - Enum
   2. BaseType can be logically replaced in any type (so prefix need to be changed inconveniently!)  
      - Data_* - dataclasses/STRUCTURES separated(!) from execution logic
      - Nt_* - NamedTuple
   3. Monkey_* - special test objects


********************************************************************************
